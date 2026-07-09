import tkinter as tk
from tkinter import font as tkfont

from .icons import load_photo
from .theme import BG, EMOJI_DIR, SURFACE


def has_emoji(text):
    return any(
        0x203C <= ord(char) <= 0x3299
        or 0x1F000 <= ord(char) <= 0x1FAFF
        for char in text
    )


def text_font(text, size=10, weight="bold"):
    if has_emoji(text):
        return ("Segoe UI Emoji", size, weight)
    return ("Segoe UI", size, weight)


def rounded_rect(canvas, x1, y1, x2, y2, radius, **kwargs):
    points = [
        x1 + radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius,
        x2, y2 - radius, x2, y2, x2 - radius, y2, x1 + radius, y2,
        x1, y2, x1, y2 - radius, x1, y1 + radius, x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


def load_emoji_png(name, size):
    if not name:
        return None
    return load_photo(EMOJI_DIR / f"{name}.png", size)


class ImageTextLabel(tk.Frame):
    def __init__(self, parent, text, icon_name, fallback_icon="", size=10, weight="bold", fg="#111827", bg=SURFACE, icon_size=24):
        super().__init__(parent, bg=bg)
        self.icon_image = load_emoji_png(icon_name, icon_size)
        if self.icon_image:
            tk.Label(self, image=self.icon_image, bg=bg, bd=0).pack(side="left", padx=(0, 6))
            label_text = text
        else:
            label_text = f"{fallback_icon} {text}" if fallback_icon else text
        tk.Label(self, text=label_text, font=text_font(label_text, size, weight), fg=fg, bg=bg).pack(side="left")


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
    def __init__(
        self,
        parent,
        text,
        command,
        fill,
        fg="white",
        hover=None,
        radius=18,
        height=40,
        icon_name=None,
        fallback_icon="",
        icon_size=24,
    ):
        super().__init__(parent, height=height, bg=parent.cget("bg"), highlightthickness=0, bd=0, cursor="hand2")
        self.text, self.command = text, command
        self.fill, self.hover, self.fg = fill, hover or fill, fg
        self.radius, self.height, self.current_fill = radius, height, fill
        self.fallback_icon = fallback_icon
        self.icon_image = load_emoji_png(icon_name, icon_size)
        self.icon_size = icon_size
        for event, handler in (("<Configure>", self.draw), ("<Enter>", self.enter), ("<Leave>", self.leave)):
            self.bind(event, handler)
        self.bind("<Button-1>", lambda _event: self.command())

    def draw(self, _event=None):
        self.delete("all")
        width = max(self.winfo_width(), 2)
        rounded_rect(self, 1, 1, width - 1, self.height - 1, self.radius, fill=self.current_fill, outline="")
        text = self.text if self.icon_image else (f"{self.fallback_icon} {self.text}" if self.fallback_icon else self.text)
        font = text_font(text, 10, "bold")
        if self.icon_image:
            text_width = tkfont.Font(font=font).measure(text)
            icon_x = width // 2 - (self.icon_size + 6 + text_width) // 2
            self.create_image(icon_x, self.height // 2, image=self.icon_image, anchor="w")
            self.create_text(icon_x + self.icon_size + 6, self.height // 2, text=text, fill=self.fg, font=font, anchor="w")
        else:
            self.create_text(width // 2, self.height // 2, text=text, fill=self.fg, font=font)

    def enter(self, _event):
        self.current_fill = self.hover
        self.draw()

    def leave(self, _event):
        self.current_fill = self.fill
        self.draw()


class RoundedLabel(tk.Canvas):
    def __init__(
        self,
        parent,
        text,
        fill,
        fg="white",
        radius=18,
        height=38,
        padx=16,
        icon_name=None,
        fallback_icon="",
        icon_size=24,
    ):
        super().__init__(parent, height=height, bg=parent.cget("bg"), highlightthickness=0, bd=0)
        self.text = text
        self.fill = fill
        self.fg = fg
        self.radius = radius
        self.height = height
        self.padx = padx
        self.icon_image = load_emoji_png(icon_name, icon_size)
        self.fallback_icon = fallback_icon
        self.icon_size = icon_size
        measured_text = text if self.icon_image else (f"{fallback_icon} {text}" if fallback_icon else text)
        self.font = text_font(measured_text, 9, "bold")
        image_width = icon_size + 6 if self.icon_image else 0
        self.configure(width=tkfont.Font(font=self.font).measure(measured_text) + image_width + padx * 2)
        self.bind("<Configure>", self.draw)

    def draw(self, _event=None):
        self.delete("all")
        width = max(self.winfo_width(), 2)
        rounded_rect(self, 1, 1, width - 1, self.height - 1, self.radius, fill=self.fill, outline="")
        if self.icon_image:
            text_width = tkfont.Font(font=self.font).measure(self.text)
            icon_x = width // 2 - (self.icon_size + 6 + text_width) // 2
            self.create_image(icon_x, self.height // 2, image=self.icon_image, anchor="w")
            self.create_text(icon_x + self.icon_size + 6, self.height // 2, text=self.text, fill=self.fg, font=self.font, anchor="w")
        else:
            text = f"{self.fallback_icon} {self.text}" if self.fallback_icon else self.text
            self.create_text(width // 2, self.height // 2, text=text, fill=self.fg, font=self.font)
