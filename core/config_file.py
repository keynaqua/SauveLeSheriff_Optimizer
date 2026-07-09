from tkinter import messagebox
import stat

from .settings import CONFIG_PATH, ENGINE_CONFIG_PATH


def read_ini():
    if not CONFIG_PATH.exists():
        messagebox.showerror("Fichier introuvable", f"Impossible de trouver :\n\n{CONFIG_PATH}")
        return None
    return CONFIG_PATH.read_text(encoding="utf-8", errors="ignore").splitlines()


def write_values(values):
    lines = read_ini()
    if lines is None:
        return False

    found, output = set(), []
    for line in lines:
        stripped = line.strip()
        for key, value in values.items():
            if stripped.startswith(key + "="):
                output.append(f"{key}={value}")
                found.add(key)
                break
        else:
            output.append(line)

    output.extend(f"{key}={value}" for key, value in values.items() if key not in found)
    CONFIG_PATH.write_text("\n".join(output) + "\n", encoding="utf-8")
    return True


def make_writable(path):
    if path.exists():
        path.chmod(path.stat().st_mode | stat.S_IWRITE | stat.S_IREAD)


def make_read_only(path):
    path.chmod(stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH)


def read_text_if_exists(path):
    if not path.exists():
        return []
    return path.read_text(encoding="utf-8", errors="ignore").splitlines()


def write_engine_values(values):
    ENGINE_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    make_writable(ENGINE_CONFIG_PATH)

    lines = read_text_if_exists(ENGINE_CONFIG_PATH)
    if not lines:
        lines = ["[SystemSettings]"]

    section_start = None
    section_end = len(lines)
    for index, line in enumerate(lines):
        if line.strip().lower() == "[systemsettings]":
            section_start = index
            break

    if section_start is None:
        lines.extend(["", "[SystemSettings]"])
        section_start = len(lines) - 1
        section_end = len(lines)
    else:
        for index in range(section_start + 1, len(lines)):
            stripped = lines[index].strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                section_end = index
                break

    found = set()
    updated = []
    section_lines_removed = 0
    for index, line in enumerate(lines):
        if section_start < index < section_end:
            stripped = line.strip()
            key = stripped.split("=", 1)[0] if "=" in stripped else None
            if key in values:
                if key not in found:
                    updated.append(f"{key}={values[key]}")
                    found.add(key)
                else:
                    section_lines_removed += 1
                continue
        updated.append(line)

    insertion_index = section_end - section_lines_removed
    missing = [f"{key}={value}" for key, value in values.items() if key not in found]
    if missing:
        if insertion_index > 0 and updated[insertion_index - 1].strip():
            missing.insert(0, "")
        updated[insertion_index:insertion_index] = missing

    ENGINE_CONFIG_PATH.write_text("\n".join(updated).rstrip() + "\n", encoding="utf-8")
    make_read_only(ENGINE_CONFIG_PATH)
    return True


def delete_engine_config():
    if not ENGINE_CONFIG_PATH.exists():
        return False
    make_writable(ENGINE_CONFIG_PATH)
    ENGINE_CONFIG_PATH.unlink()
    return True
