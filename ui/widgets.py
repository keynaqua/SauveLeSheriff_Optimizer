import tkinter as tk

from .theme import BG, SURFACE


def rounded_rect(canvas, x1, y1, x2, y2, radius, **kwargs):
    points = [
        x1 + radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius,
        x2, y2 - radius, x2, y2, x2 - radius, y2, x1 + radius, y2,
        x1, y2, x1, y2 - radius, x1, y1 + radius, x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


class RoundedCard(tk.Frame):
    def __init__(self, parent, bg=BG, fill=SURFACE, radius=24, padding=16, height=None):
        super().__init__(parent, bg=bg)
        self.fill = fill
        self.radius = radius
        self.padding = padding
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.content = tk.Frame(self.canvas, bg=fill)
        self.window = self.canvas.create_window(padding, padding, window=self.content, anchor="nw")
        if height is not None:
            self.configure(height=height)
            self.pack_propagate(False)
        self.canvas.bind("<Configure>", self.draw)

    def draw(self, event):
        self.canvas.delete("shape")
        width, height = max(event.width, 2), max(event.height, 2)
        rounded_rect(self.canvas, 1, 1, width - 1, height - 1, self.radius, fill=self.fill, outline="", tags="shape")
        self.canvas.tag_lower("shape")
        self.canvas.itemconfigure(self.window, width=max(width - self.padding * 2, 1), height=max(height - self.padding * 2, 1))


class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, fill, fg="white", hover=None, radius=18, height=40):
        super().__init__(parent, height=height, bg=parent.cget("bg"), highlightthickness=0, bd=0, cursor="hand2")
        self.text, self.command = text, command
        self.fill, self.hover, self.fg = fill, hover or fill, fg
        self.radius, self.height, self.current_fill = radius, height, fill
        for event, handler in (("<Configure>", self.draw), ("<Enter>", self.enter), ("<Leave>", self.leave)):
            self.bind(event, handler)
        self.bind("<Button-1>", lambda _event: self.command())

    def draw(self, _event=None):
        self.delete("all")
        width = max(self.winfo_width(), 2)
        rounded_rect(self, 1, 1, width - 1, self.height - 1, self.radius, fill=self.current_fill, outline="")
        self.create_text(width // 2, self.height // 2, text=self.text, fill=self.fg, font=("Segoe UI", 10, "bold"))

    def enter(self, _event):
        self.current_fill = self.hover
        self.draw()

    def leave(self, _event):
        self.current_fill = self.fill
        self.draw()
