import tkinter as tk
from tkinter import messagebox, ttk

from .core.config_file import delete_engine_config, write_engine_values, write_values
from .ui.icons import load_photo
from .core.settings import CONFIG_PATH, ENGINE_CONFIG_PATH, ENGINE_OPTIMIZATION_PRESETS, OPTIMIZED_VALUES, RESTORE_VALUES
from .ui.theme import *
from .ui.widgets import ImageTextLabel, RoundedButton, RoundedCard, RoundedLabel, text_font
from .ui.panel import GraphicsPanel


class OptimizerApp:
    def __init__(self, root):
        self.root = root
        self.graphics = None
        self.status_var = tk.StringVar(value="Prêt.")
        self.engine_preset_buttons = []
        self.header_icon_image = None

        self.root.title("SauveLeSherif Optimizer")
        self.root.geometry("980x820")
        self.root.minsize(900, 800)
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
        return tk.Label(parent, text=text, font=text_font(text, size, weight), fg=fg, bg=bg)

    def build_ui(self):
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True, padx=18, pady=16)
        self.build_header(main)
        self.build_actions(main)
        self.build_graphics(main)
        self.build_footer(main)

    def build_header(self, parent):
        card = RoundedCard(parent, fill=HERO, radius=28, padding=20, height=140)
        card.pack(fill="x", pady=(0, 14))
        content = card.content
        content.columnconfigure(1, weight=1)

        badge = tk.Canvas(content, width=92, height=92, bg=HERO, highlightthickness=0)
        badge.grid(row=0, column=0, rowspan=2, padx=(0, 20), sticky="w")
        self.header_icon_image = load_photo(ICON_PATH, 92, radius=16)
        if self.header_icon_image:
            badge.create_image(46, 46, image=self.header_icon_image)
        else:
            badge.create_text(46, 46, text="SLS", fill=HERO, font=("Segoe UI", 18, "bold"))

        self.label(content, "Sauve Le Sherif Optimizer", 21, "bold", "white", HERO).grid(row=0, column=1, sticky="sw")
        self.label(content, "Réglages graphiques, preset performance et optimisation.", 10, fg="#cbd5e1", bg=HERO).grid(row=1, column=1, sticky="nw", pady=(4, 0))
        author = RoundedLabel(
            content,
            "Made by Keyn (@aquakeyn)",
            fill=HERO_SOFT,
            fg="#dbeafe",
            radius=18,
            height=42,
            icon_name="made_by",
            fallback_icon="⛩️",
        )
        author.grid(row=0, column=2, rowspan=2, sticky="e")

    def build_actions(self, parent):
        card = RoundedCard(parent, radius=24, padding=14, height=238)
        card.pack(fill="x", pady=(0, 12))
        ImageTextLabel(
            card.content,
            "Actions rapides",
            icon_name="actions",
            fallback_icon="⚡️",
            size=11,
            fg=TEXT,
            bg=SURFACE,
        ).pack(anchor="w", pady=(0, 12))

        grid = tk.Frame(card.content, bg=SURFACE)
        grid.pack(fill="x")
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        actions = [
            (0, 0, "Optimiser", self.apply_optimized, "#2563eb", "white", "#1d4ed8", "optimize", "🚀"),
            (0, 1, "Restaurer", self.restore_defaults, "#eeeeee", TEXT, "#dadada", "restore", "↩️"),
        ]
        for row, col, text, command, fill, fg, hover, icon_name, fallback_icon in actions:
            button = RoundedButton(
                grid,
                text,
                command,
                fill=fill,
                fg=fg,
                hover=hover,
                height=42,
                icon_name=icon_name,
                fallback_icon=fallback_icon,
            )
            button.grid(row=row, column=col, sticky="ew", padx=(0 if col == 0 else 10, 0), pady=0)

        extra = tk.Frame(card.content, bg=SURFACE)
        extra.pack(fill="x", pady=(16, 0))
        ImageTextLabel(
            extra,
            "Optimisation plus avancée. Peut réduire la qualité visuelle",
            icon_name="advanced",
            fallback_icon="⛲️",
            size=10,
            fg=TEXT,
            bg=SURFACE,
        ).pack(anchor="w")

        buttons = tk.Frame(extra, bg=SURFACE)
        buttons.pack(fill="x", pady=(10, 0))
        self.engine_preset_buttons = []
        for column, preset in enumerate(ENGINE_OPTIMIZATION_PRESETS):
            buttons.columnconfigure(column, weight=1, uniform="engine_preset")
            item = tk.Frame(buttons, bg=SURFACE)
            item.grid(row=0, column=column, sticky="nsew", padx=(0 if column == 0 else 8, 0))
            palette = [
                ("#ecfeff", "#0e7490", "#cffafe"),
                ("#f0fdf4", "#15803d", "#dcfce7"),
                ("#fff7ed", "#c2410c", "#ffedd5"),
                ("#fef2f2", "#b91c1c", "#fee2e2"),
            ][column]
            button = RoundedButton(
                item,
                preset.get("button", preset["name"]),
                lambda selected=preset: self.apply_engine_preset(selected),
                fill=palette[0],
                fg=palette[1],
                hover=palette[2],
                height=38,
            )
            button.pack(fill="x")
            self.engine_preset_buttons.append(button)
            tk.Label(
                item,
                text=preset["description"],
                font=("Segoe UI", 8),
                fg=MUTED,
                bg=SURFACE,
                justify="left",
                wraplength=190,
            ).pack(anchor="w", pady=(6, 0))

    def build_graphics(self, parent):
        card = RoundedCard(parent, radius=24, padding=14)
        card.pack(fill="both", expand=True)
        self.graphics = GraphicsPanel(self, card.content)

    def build_footer(self, parent):
        footer = tk.Frame(parent, bg=BG)
        footer.pack(fill="x", pady=(12, 0))
        tk.Label(footer, textvariable=self.status_var, font=text_font("status", 9, "normal"), fg=MUTED, bg=BG).pack(side="left", fill="x", expand=True)
        button = RoundedButton(
            footer,
            "Appliquer",
            self.apply_sliders,
            fill="#172554",
            fg="white",
            hover="#1d4ed8",
            height=38,
            icon_name="apply",
            fallback_icon="✅",
        )
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
            removed = delete_engine_config()
            suffix = " Engine.ini supprimé." if removed else " Aucun Engine.ini à supprimer."
            self.status_var.set("Paramètres restaurés." + suffix)
            messagebox.showinfo("Restauré", "Paramètres restaurés avec succès.\n\n" + suffix.strip())

    def apply_engine_preset(self, preset):
        try:
            write_engine_values(preset["values"])
        except PermissionError as error:
            self.status_var.set("Engine.ini : acces refuse.")
            messagebox.showerror("Engine.ini", f"Impossible d'ecrire dans Engine.ini.\n\nDetail : {error}")
            return
        self.status_var.set(f"{preset['name']} applique. Engine.ini est en lecture seule.")
        messagebox.showinfo(
            "Optimisation supplementaire",
            f"{preset['name']} applique.\n\nFichier cree ou mis a jour :\n{ENGINE_CONFIG_PATH}\n\nLe fichier est maintenant en lecture seule.",
        )


def main():
    root = tk.Tk()
    OptimizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
