from tkinter import messagebox

from .settings import CONFIG_PATH


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
