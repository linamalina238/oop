import tkinter as tk

SIZE = 24
INK = "#000000"
GREEN = "#90ee90"

class _Bitmap:
    def __init__(self, size=SIZE):
        self.size = size
        self.pixels = {}

    def dot(self, x, y, color=INK):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.pixels[(x, y)] = color

    def line(self, x0, y0, x1, y1, color=INK, thick=2):
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            for ox in range(thick):
                for oy in range(thick):
                    self.dot(x0 + ox, y0 + oy, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def rect(self, x0, y0, x1, y1, color=INK, fill=None):
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                on_border = x in (x0, x1) or y in (y0, y1)
                if on_border:
                    self.dot(x, y, color)
                elif fill:
                    self.dot(x, y, fill)

    def ellipse(self, cx, cy, rx, ry, color=INK, fill=None):
        for x in range(self.size):
            for y in range(self.size):
                px, py = x + 0.5 - cx, y + 0.5 - cy
                outer = (px / rx) ** 2 + (py / ry) ** 2
                inner = (px / (rx - 1)) ** 2 + (py / (ry - 1)) ** 2 if rx > 1 and ry > 1 else 0
                if outer <= 1 and inner > 1:
                    self.dot(x, y, color)
                elif inner <= 1 and fill:
                    self.dot(x, y, fill)

    def to_photo(self):
        photo = tk.PhotoImage(width=self.size, height=self.size)
        for (x, y), color in self.pixels.items():
            photo.put(color, to=(x, y))
        return photo


def _point():
    b = _Bitmap()
    b.ellipse(12, 12, 4, 4, INK, fill=INK)
    return b


def _line():
    b = _Bitmap()
    b.line(4, 19, 19, 4)
    return b


def _rectangle():
    b = _Bitmap()
    b.rect(3, 6, 20, 17)
    return b


def _ellipse():
    b = _Bitmap()
    b.ellipse(12, 12, 10, 7, INK, fill=GREEN)
    return b


def _line_oo():
    b = _Bitmap()
    b.line(6, 17, 17, 6)
    b.ellipse(6.5, 17.5, 3.6, 3.6, INK, fill=GREEN)
    b.ellipse(17.5, 6.5, 3.6, 3.6, INK, fill=GREEN)
    return b


def _cube():
    b = _Bitmap()
    b.rect(3, 9, 16, 21)
    b.rect(8, 4, 21, 16)
    for x, y in ((3, 9), (16, 9), (16, 21), (3, 21)):
        b.line(x, y, x + 5, y - 5, thick=1)
    return b


_BUILDERS = {
    "point": _point,
    "line": _line,
    "rectangle": _rectangle,
    "ellipse": _ellipse,
    "line_oo": _line_oo,
    "cube": _cube,
}


def make_icon(key):
    return _BUILDERS[key]().to_photo()