import os
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from ..core.settings import STEAM_APP_ID, STEAM_LAUNCH_FLAG


class SteamLaunchOptionError(Exception):
    pass


def is_steam_running():
    try:
        if os.name == "nt":
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq steam.exe"],
                capture_output=True,
                text=True,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                check=False,
            )
            return "steam.exe" in result.stdout.lower()

        return subprocess.run(["pgrep", "-x", "steam"], capture_output=True, check=False).returncode == 0
    except OSError:
        return False


def steam_roots():
    roots = []
    for name in ("STEAM_PATH", "SteamPath"):
        if os.environ.get(name):
            roots.append(Path(os.environ[name]))
    for name in ("PROGRAMFILES(X86)", "PROGRAMFILES"):
        if os.environ.get(name):
            roots.append(Path(os.environ[name]) / "Steam")
    if os.environ.get("LOCALAPPDATA"):
        roots.append(Path(os.environ["LOCALAPPDATA"]) / "Steam")
    if os.environ.get("USERPROFILE"):
        roots.append(Path(os.environ["USERPROFILE"]) / "AppData" / "Local" / "Steam")
    roots += [Path("C:/Program Files (x86)/Steam"), Path("C:/Program Files/Steam")]

    seen = set()
    for root in roots:
        key = str(root).lower()
        if key not in seen:
            seen.add(key)
            yield root


def find_steam_root():
    for root in steam_roots():
        if (root / "steamapps").exists() or (root / "userdata").exists():
            return root
    raise SteamLaunchOptionError("Steam est introuvable sur les chemins habituels.")


def app_id():
    if not STEAM_APP_ID:
        raise SteamLaunchOptionError("STEAM_APP_ID n'est pas configuré dans settings.py.")
    return str(STEAM_APP_ID)


def localconfig_files(steam_root):
    userdata = steam_root / "userdata"
    return sorted(userdata.glob("*/config/localconfig.vdf")) if userdata.exists() else []


def is_section_line(line, key):
    return re.match(rf'^\s*"{re.escape(key)}"\s*$', line) is not None


def find_section(lines, key, start=0, end=None):
    end = len(lines) if end is None else end
    for index in range(start, end):
        if not is_section_line(lines[index], key):
            continue
        open_index = index + 1
        while open_index < end and not lines[open_index].strip():
            open_index += 1
        if open_index >= end or lines[open_index].strip() != "{":
            continue

        depth = 0
        for close_index in range(open_index, end):
            stripped = lines[close_index].strip()
            if stripped == "{":
                depth += 1
            elif stripped == "}":
                depth -= 1
                if depth == 0:
                    return index, open_index, close_index
    return None


def find_launch_options(lines, start, end):
    pattern = re.compile(r'^(\s*)"LaunchOptions"\s+"([^"]*)"\s*$')
    for index in range(start, end):
        match = pattern.match(lines[index])
        if match:
            return index, match.group(1), match.group(2)
    return None


def write_backup(path):
    backup = path.with_suffix(path.suffix + ".backup-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    shutil.copy2(path, backup)
    return backup


def update_options(options, flag, remove=False):
    parts = options.split()
    has_flag = flag in parts
    if remove:
        return " ".join(part for part in parts if part != flag), has_flag
    if has_flag:
        return options, False
    return f"{options.strip()} {flag}".strip(), True


def mutate_localconfig(path, game_app_id, flag, remove=False):
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    apps_section = find_section(lines, "apps")

    if apps_section is None:
        if remove:
            return False, None
        root_section = find_section(lines, "UserLocalConfigStore")
        insert_at = root_section[2] if root_section else len(lines)
        lines[insert_at:insert_at] = [
            '\t"apps"',
            '\t{',
            f'\t\t"{game_app_id}"',
            '\t\t{',
            f'\t\t\t"LaunchOptions" "{flag}"',
            '\t\t}',
            '\t}',
        ]
    else:
        app_section = find_section(lines, game_app_id, apps_section[1] + 1, apps_section[2])
        if app_section is None:
            if remove:
                return False, None
            lines[apps_section[2]:apps_section[2]] = [
                f'\t\t"{game_app_id}"',
                '\t\t{',
                f'\t\t\t"LaunchOptions" "{flag}"',
                '\t\t}',
            ]
        else:
            launch_options = find_launch_options(lines, app_section[1] + 1, app_section[2])
            if launch_options is None:
                if remove:
                    return False, None
                lines[app_section[2]:app_section[2]] = [f'\t\t\t"LaunchOptions" "{flag}"']
            else:
                index, indent, options = launch_options
                new_options, changed = update_options(options, flag, remove=remove)
                if not changed:
                    return False, None
                lines[index] = f'{indent}"LaunchOptions" "{new_options}"'

    backup = write_backup(path)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True, backup


def mutate_dx11(remove=False):
    steam_root = find_steam_root()
    configs = localconfig_files(steam_root)
    if not configs:
        raise SteamLaunchOptionError("Aucun fichier localconfig.vdf Steam trouvé.")

    changed_files, backups = [], []
    for config in configs:
        changed, backup = mutate_localconfig(config, app_id(), STEAM_LAUNCH_FLAG, remove=remove)
        if changed:
            changed_files.append(config)
            backups.append(backup)

    return {
        "app_id": app_id(),
        "flag": STEAM_LAUNCH_FLAG,
        "changed_files": changed_files,
        "backups": backups,
        "already_absent" if remove else "already_present": not changed_files,
    }


def add_dx11_launch_option():
    return mutate_dx11(remove=False)


def remove_dx11_launch_option():
    return mutate_dx11(remove=True)
