from line import Line2D
from rectangle import Rectangle2D


class Cube2D(Line2D, Rectangle2D):
    def _draw_parts(self, canvas, start, end, tag=None):
        x1, y1 = start
        x2, y2 = end
        k = min(abs(x2 - x1), abs(y2 - y1)) // 2 

        self.draw_part(Rectangle2D, canvas, (x1, y1), (x2, y2), tag)
        self.draw_part(Rectangle2D, canvas, (x1 + k, y1 - k), (x2 + k, y2 - k), tag)
        for x, y in ((x1, y1), (x2, y1), (x2, y2), (x1, y2)):
            self.draw_part(Line2D, canvas, (x, y), (x + k, y - k), tag)

    def draw_final(self, canvas):
        self._draw_parts(canvas, self.start, self.end)

    def draw_rubber(self, canvas, current_point, tag="rubber"):
        if self.start:
            self._draw_parts(canvas, self.start, current_point, tag)