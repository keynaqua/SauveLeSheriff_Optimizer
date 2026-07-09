import base64
import struct
import tkinter as tk


def load_ico_photo(path):
    data = path.read_bytes()
    if len(data) < 6:
        return None

    reserved, icon_type, count = struct.unpack_from("<HHH", data, 0)
    if reserved != 0 or icon_type != 1 or count < 1:
        return None

    entries = []
    for index in range(count):
        offset = 6 + index * 16
        if offset + 16 > len(data):
            continue
        width, height, _colors, _reserved, _planes, bit_count, size, image_offset = struct.unpack_from(
            "<BBBBHHII", data, offset
        )
        entries.append((bit_count, 256 if width == 0 else width, 256 if height == 0 else height, size, image_offset))

    for _bit_count, _width, _height, size, offset in sorted(entries, reverse=True):
        photo = load_icon_entry(data[offset:offset + size])
        if photo is not None:
            return photo
    return None


def load_icon_entry(image_data):
    if image_data.startswith(b"\x89PNG\r\n\x1a\n"):
        try:
            return tk.PhotoImage(data=base64.b64encode(image_data).decode("ascii"))
        except tk.TclError:
            return None
    return load_bitmap_icon(image_data)


def load_bitmap_icon(image_data):
    if len(image_data) < 40:
        return None

    header_size = struct.unpack_from("<I", image_data, 0)[0]
    if header_size < 40 or len(image_data) < header_size:
        return None

    width = struct.unpack_from("<i", image_data, 4)[0]
    height = struct.unpack_from("<i", image_data, 8)[0] // 2
    bit_count = struct.unpack_from("<H", image_data, 14)[0]
    if width <= 0 or height <= 0 or bit_count not in (24, 32):
        return None

    bpp = bit_count // 8
    stride = ((width * bpp + 3) // 4) * 4
    if len(image_data) < header_size + stride * height:
        return None

    photo = tk.PhotoImage(width=width, height=height)
    transparent = []
    for y in range(height):
        source_y = height - 1 - y
        row = header_size + source_y * stride
        colors = []
        for x in range(width):
            pixel = row + x * bpp
            blue, green, red = image_data[pixel], image_data[pixel + 1], image_data[pixel + 2]
            alpha = image_data[pixel + 3] if bpp == 4 else 255
            colors.append(f"#{red:02x}{green:02x}{blue:02x}")
            if alpha < 24:
                transparent.append((x, y))
        photo.put("{" + " ".join(colors) + "}", to=(0, y))

    for x, y in transparent:
        try:
            photo.transparency_set(x, y, True)
        except tk.TclError:
            break
    return photo


def round_photo_corners(photo, radius):
    width, height = photo.width(), photo.height()
    if radius <= 0:
        return photo

    for y in range(height):
        for x in range(width):
            dx = max(radius - x, 0, x - (width - radius - 1))
            dy = max(radius - y, 0, y - (height - radius - 1))
            if dx * dx + dy * dy > radius * radius:
                try:
                    photo.transparency_set(x, y, True)
                except tk.TclError:
                    return photo
    return photo


def resize_photo(photo, size):
    source_width, source_height = photo.width(), photo.height()
    if source_width == size and source_height == size:
        return photo

    resized = tk.PhotoImage(width=size, height=size)
    for y in range(size):
        source_y = min(source_height - 1, int(y * source_height / size))
        colors = []
        transparent = []
        for x in range(size):
            source_x = min(source_width - 1, int(x * source_width / size))
            color = photo.get(source_x, source_y)
            if isinstance(color, tuple):
                color = "#{:02x}{:02x}{:02x}".format(*color[:3])
            colors.append(color)
            try:
                if photo.transparency_get(source_x, source_y):
                    transparent.append(x)
            except tk.TclError:
                pass
        resized.put("{" + " ".join(colors) + "}", to=(0, y))
        for x in transparent:
            try:
                resized.transparency_set(x, y, True)
            except tk.TclError:
                break
    return resized


def load_photo(path, max_size, radius=0):
    if not path.exists():
        return None

    try:
        photo = tk.PhotoImage(file=str(path))
    except tk.TclError:
        photo = load_ico_photo(path)
    if photo is None:
        return None

    photo = resize_photo(photo, max_size)
    return round_photo_corners(photo, radius)
