import tkinter as tk
from tkinter import messagebox, ttk

from .core.config_file import write_values
from .ui.icons import load_photo
from .core.settings import CONFIG_PATH, OPTIMIZED_VALUES, RESTORE_VALUES
from .integrations.steam import SteamLaunchOptionError, add_dx11_launch_option, is_steam_running, remove_dx11_launch_option
from .ui.theme import *
from .ui.widgets import RoundedButton, RoundedCard
from .ui.graphics import GraphicsPanel


class OptimizerApp:
    def __init__(self, root):
        self.root = root
        self.graphics = None
        self.status_var = tk.StringVar(value="Prêt.")
        self.header_icon_image = None

        self.root.title("SauveLeSherif Optimizer")
        self.root.geometry("980x820")
        self.root.minsize(860, 700)
        self.root.configure(bg=BG)
        self.apply_window_icon()
        self.configure_style()
        self.build_ui()

    def apply_window_icon(self):
        if ICON_PATH.exists():
            try:
                self.root.iconbitmap(str(ICON_PATH))
            except tk.TclError:
                pass

    def configure_style(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("Surface.TFrame", background=SURFACE)
        style.configure("Vertical.TScrollbar", background="#d1d5db", troughcolor=SURFACE, arrowcolor=MUTED)

    def label(self, parent, text, size=10, weight="normal", fg=TEXT, bg=SURFACE):
        return tk.Label(parent, text=text, font=("Segoe UI", size, weight), fg=fg, bg=bg)

    def build_ui(self):
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True, padx=18, pady=16)
        self.build_header(main)
        self.build_actions(main)
        self.build_config_path(main)
        self.build_graphics(main)
        self.build_footer(main)

    def build_header(self, parent):
        card = RoundedCard(parent, fill=HERO, radius=28, padding=20, height=140)
        card.pack(fill="x", pady=(0, 14))
        content = card.content
        content.columnconfigure(1, weight=1)

        badge = tk.Canvas(content, width=88, height=88, bg=HERO, highlightthickness=0)
        badge.grid(row=0, column=0, rowspan=2, padx=(0, 20), sticky="w")
        self.header_icon_image = load_photo(ICON_PATH, 88)
        if self.header_icon_image:
            badge.create_image(44, 44, image=self.header_icon_image)
        else:
            badge.create_text(44, 44, text="DX", fill="white", font=("Segoe UI", 18, "bold"))

        self.label(content, "SauveLeSherif Optimizer", 21, "bold", "white", HERO).grid(row=0, column=1, sticky="sw")
        self.label(content, "Réglages graphiques, preset performance et options Steam.", 10, fg="#cbd5e1", bg=HERO).grid(row=1, column=1, sticky="nw", pady=(4, 0))
        tk.Label(
            content,
            text="Steam fermé requis\n(pour les réglages DirectX)",
            font=("Segoe UI", 9, "bold"),
            fg="#dbeafe",
            bg=HERO_SOFT,
            padx=12,
            pady=6,
            justify="center",
        ).grid(row=0, column=2, rowspan=2, sticky="e")

    def build_actions(self, parent):
        card = RoundedCard(parent, radius=24, padding=14, height=168)
        card.pack(fill="x", pady=(0, 12))
        self.label(card.content, "Actions rapides", 11, "bold").pack(anchor="w", pady=(0, 12))

        grid = tk.Frame(card.content, bg=SURFACE)
        grid.pack(fill="x")
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        actions = [
            (0, 0, "Optimiser", self.apply_optimized, ACCENT, "white", ACCENT_DARK),
            (0, 1, "Restaurer", self.restore_defaults, "#eef2ff", TEXT, "#e0e7ff"),
            (1, 0, "lancer avec DirectX11 (recommandé)", self.apply_steam_dx11, SUCCESS, "white", SUCCESS_DARK),
            (1, 1, "Retirer DirectX11", self.remove_steam_dx11, DANGER_SOFT, DANGER, "#fecaca"),
        ]
        for row, col, text, command, fill, fg, hover in actions:
            button = RoundedButton(grid, text, command, fill=fill, fg=fg, hover=hover, height=42)
            button.grid(row=row, column=col, sticky="ew", padx=(0 if col == 0 else 10, 0), pady=(0 if row == 0 else 10, 0))

    def build_config_path(self, parent):
        card = RoundedCard(parent, radius=22, padding=14, height=78)
        card.pack(fill="x", pady=(0, 12))
        self.label(card.content, "Fichier de configuration", 10, "bold").pack(anchor="w")
        self.label(card.content, str(CONFIG_PATH), 9, fg=MUTED).pack(anchor="w", pady=(6, 0))

    def build_graphics(self, parent):
        card = RoundedCard(parent, radius=24, padding=14)
        card.pack(fill="both", expand=True)
        self.graphics = GraphicsPanel(self, card.content)

    def build_footer(self, parent):
        footer = tk.Frame(parent, bg=BG)
        footer.pack(fill="x", pady=(12, 0))
        tk.Label(footer, textvariable=self.status_var, font=("Segoe UI", 9), fg=MUTED, bg=BG).pack(side="left", fill="x", expand=True)
        button = RoundedButton(footer, "Appliquer les curseurs", self.apply_sliders, fill=TEXT, fg="white", hover="#374151", height=38)
        button.pack(side="right", fill="x")
        button.configure(width=190)

    def bind_mousewheel(self, canvas):
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-event.delta // 120, "units"))
        canvas.bind_all("<Button-4>", lambda _event: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda _event: canvas.yview_scroll(1, "units"))

    def unbind_mousewheel(self):
        self.root.unbind_all("<MouseWheel>")
        self.root.unbind_all("<Button-4>")
        self.root.unbind_all("<Button-5>")

    def apply_sliders(self):
        if write_values(self.graphics.values()):
            self.status_var.set("Curseurs appliqués. Relance le jeu si besoin.")
            messagebox.showinfo("Terminé", "Paramètres appliqués avec succès.\n\nRelance le jeu si besoin.")

    def apply_optimized(self):
        self.graphics.set_values(OPTIMIZED_VALUES)
        if write_values(OPTIMIZED_VALUES):
            self.status_var.set("Preset optimisé appliqué.")
            messagebox.showinfo("Optimisé", "Paramètres optimisés avec succès.\n\nRelance le jeu si besoin.")

    def restore_defaults(self):
        self.graphics.set_values(RESTORE_VALUES)
        if write_values(RESTORE_VALUES):
            self.status_var.set("Paramètres restaurés.")
            messagebox.showinfo("Restauré", "Paramètres restaurés avec succès.")

    def ensure_steam_closed(self):
        if not is_steam_running():
            return True
        self.status_var.set("Steam est ouvert : action annulée.")
        messagebox.showwarning("Steam ouvert", "Ferme Steam avant d'ajouter ou retirer DirectX11.\n\nAucune modification n'a été faite.")
        return False

    def apply_steam_dx11(self):
        self.mutate_steam(add_dx11_launch_option, "already_present", "DirectX11 ajouté aux options de lancement Steam.")

    def remove_steam_dx11(self):
        self.mutate_steam(remove_dx11_launch_option, "already_absent", "DirectX11 retiré des options de lancement Steam.")

    def mutate_steam(self, action, no_change_key, success_status):
        if not self.ensure_steam_closed():
            return
        try:
            result = action()
        except SteamLaunchOptionError as error:
            self.status_var.set("Steam : action impossible.")
            messagebox.showerror("Steam", str(error))
            return
        except PermissionError as error:
            self.status_var.set("Steam : accès refusé au fichier de configuration.")
            messagebox.showerror("Steam", f"Impossible d'écrire dans la configuration Steam. Ferme Steam puis réessaie.\n\nDétail : {error}")
            return

        if result[no_change_key]:
            self.status_var.set("Aucun changement Steam nécessaire.")
            messagebox.showinfo("Steam", f"{result['flag']} est déjà dans l'état demandé pour l'AppID {result['app_id']}.")
            return

        backups = "\n".join(str(path) for path in result["backups"] if path)
        self.status_var.set(success_status)
        messagebox.showinfo("Steam", f"{success_status}\n\nAppID {result['app_id']}\nBackup créé :\n{backups}")


def main():
    root = tk.Tk()
    OptimizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
