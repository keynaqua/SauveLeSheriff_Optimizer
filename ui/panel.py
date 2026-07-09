import tkinter as tk
from tkinter import ttk

from ..core.settings import RESTORE_VALUES, SLIDER_KEYS
from .theme import ACCENT, ACCENT_DARK, DISPLAY_NAMES, MUTED, QUALITY_LABELS, SURFACE, TEXT
from .widgets import ImageTextLabel, rounded_rect, text_font


class ModernScrollbar(tk.Canvas):
    def __init__(self, parent, command, width=12):
        super().__init__(parent, width=width, bg=SURFACE, highlightthickness=0, bd=0, cursor="hand2")
        self.command = command
        self.first = 0.0
        self.last = 1.0
        self.drag_offset = 0
        self.hover = False
        self.bind("<Configure>", self.draw)
        self.bind("<Enter>", self.enter)
        self.bind("<Leave>", self.leave)
        self.bind("<Button-1>", self.jump)
        self.bind("<B1-Motion>", self.drag)

    def set(self, first, last):
        self.first = float(first)
        self.last = float(last)
        self.draw()

    def enter(self, _event):
        self.hover = True
        self.draw()

    def leave(self, _event):
        self.hover = False
        self.draw()

    def thumb_geometry(self):
        height = max(self.winfo_height(), 2)
        visible = min(max(self.last - self.first, 0.05), 1.0)
        max_first = max(1.0 - visible, 0.0001)
        thumb_height = max(int(height * visible), 42)
        travel = max(height - thumb_height, 1)
        top = int(travel * min(self.first / max_first, 1.0))
        return top, top + thumb_height, travel, thumb_height, max_first

    def draw(self, _event=None):
        self.delete("all")
        width = max(self.winfo_width(), 2)
        height = max(self.winfo_height(), 2)
        if self.first <= 0 and self.last >= 1:
            return
        track_x1 = width // 2 - 3
        track_x2 = width // 2 + 3
        rounded_rect(self, track_x1, 4, track_x2, height - 4, 6, fill="#e0e7ff", outline="")
        top, bottom, _travel, _thumb_height, _max_first = self.thumb_geometry()
        fill = "#2563eb" if self.hover else "#93c5fd"
        rounded_rect(self, 1, top + 2, width - 1, bottom - 2, 8, fill=fill, outline="")

    def jump(self, event):
        top, bottom, _travel, _thumb_height, _max_first = self.thumb_geometry()
        self.drag_offset = event.y - top if top <= event.y <= bottom else _thumb_height // 2
        self.drag(event)

    def drag(self, event):
        top, bottom, travel, thumb_height, max_first = self.thumb_geometry()
        ratio = (event.y - self.drag_offset) / max(travel, 1)
        ratio = min(max(ratio, 0.0), 1.0)
        self.command("moveto", ratio * max_first)


class ChoiceButton(tk.Canvas):
    def __init__(self, parent, text, command, height=32):
        super().__init__(parent, height=height, bg="#f8fafc", highlightthickness=0, bd=0, cursor="hand2")
        self.text = text
        self.command = command
        self.height = height
        self.selected = False
        self.hover = False
        self.bind("<Configure>", self.draw)
        self.bind("<Button-1>", lambda _event: self.command())
        self.bind("<Enter>", self.enter)
        self.bind("<Leave>", self.leave)

    def set_selected(self, selected):
        self.selected = selected
        self.draw()

    def enter(self, _event):
        self.hover = True
        self.draw()

    def leave(self, _event):
        self.hover = False
        self.draw()

    def draw(self, _event=None):
        self.delete("all")
        width = max(self.winfo_width(), 2)
        fill = ACCENT if self.selected else ("#dbeafe" if self.hover else "#ffffff")
        outline = ACCENT if self.selected else "#bfdbfe"
        fg = "white" if self.selected else TEXT
        rounded_rect(self, 1, 1, width - 1, self.height - 1, 10, fill=fill, outline=outline)
        self.create_text(width // 2, self.height // 2, text=self.text, fill=fg, font=text_font(self.text, 9, "bold"))


class QualitySelector(tk.Frame):
    def __init__(self, parent, variable, command):
        super().__init__(parent, bg="#f8fafc", padx=4, pady=4)
        self.variable = variable
        self.command = command
        self.buttons = {}
        for column, (value, label) in enumerate(QUALITY_LABELS.items()):
            self.columnconfigure(column, weight=1, uniform="quality")
            button = ChoiceButton(self, label, lambda v=value: self.set(v))
            button.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 4, 0))
            self.buttons[value] = button
        self.refresh()

    def set(self, value):
        self.variable.set(value)
        self.refresh()
        self.command()

    def refresh(self):
        selected = round(self.variable.get())
        for value, button in self.buttons.items():
            button.set_selected(value == selected)


class GraphicsPanel:
    def __init__(self, app, parent):
        self.app = app
        self.vars = {}
        self.selectors = {}
        self.value_labels = {}
        self.build(parent)

    def build(self, parent):
        header = tk.Frame(parent, bg=SURFACE)
        header.pack(fill="x", pady=(0, 10))
        ImageTextLabel(
            header,
            "Qualité graphique",
            icon_name="graphics",
            fallback_icon="🗻",
            size=11,
            fg=TEXT,
            bg=SURFACE,
        ).pack(side="left")
        self.app.label(header, "Bas / Moyen / Haut / Epic", 9, fg=MUTED).pack(side="right")

        canvas = tk.Canvas(parent, bg=SURFACE, highlightthickness=0)
        scrollbar = ModernScrollbar(parent, command=canvas.yview)
        rows = ttk.Frame(canvas, style="Surface.TFrame")
        rows.bind("<Configure>", lambda _event: canvas.configure(scrollregion=canvas.bbox("all")))
        window = canvas.create_window((0, 0), window=rows, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y", padx=(10, 0))
        canvas.bind("<Configure>", lambda event: canvas.itemconfigure(window, width=event.width))
        canvas.bind("<Enter>", lambda _event: self.app.bind_mousewheel(canvas))
        canvas.bind("<Leave>", lambda _event: self.app.unbind_mousewheel())
        self.build_rows(rows)

    def build_rows(self, parent):
        parent.columnconfigure(1, weight=1)
        for row, key in enumerate(SLIDER_KEYS):
            var = tk.IntVar(value=RESTORE_VALUES[key])
            self.vars[key] = var

            label_frame = tk.Frame(parent, bg=SURFACE)
            label_frame.grid(row=row, column=0, padx=(6, 20), pady=9, sticky="w")
            self.app.label(label_frame, DISPLAY_NAMES.get(key, key), 10).pack(anchor="w")
            self.app.label(label_frame, key, 8, fg="#9ca3af").pack(anchor="w")

            selector = QualitySelector(parent, var, lambda setting=key: self.update(setting))
            selector.grid(row=row, column=1, padx=8, pady=9, sticky="ew")
            self.selectors[key] = selector

            value = tk.Label(parent, text=self.value_text(var.get()), bg="#f8fafc", fg=ACCENT_DARK, font=("Segoe UI", 9, "bold"), padx=12, pady=5)
            value.grid(row=row, column=2, padx=(12, 8), pady=9, sticky="e")
            self.value_labels[key] = value

    def value_text(self, value):
        value = round(value)
        return f"{value} {QUALITY_LABELS[value]}"

    def update(self, key):
        value = round(self.vars[key].get())
        self.vars[key].set(value)
        self.value_labels[key].configure(text=self.value_text(value))
        self.selectors[key].refresh()

    def values(self):
        return {key: round(var.get()) for key, var in self.vars.items()}

    def set_values(self, values):
        for key, value in values.items():
            if key in self.vars:
                self.vars[key].set(value)
                self.update(key)
