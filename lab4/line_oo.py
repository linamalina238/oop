from line import Line2D
from elipse import Ellipse2D


class LineOO2D(Line2D, Ellipse2D):
    R = 6  

    def _draw_parts(self, canvas, start, end, tag=None):
        self.draw_part(Line2D, canvas, start, end, tag)
        for x, y in (start, end):
            self.draw_part(Ellipse2D, canvas, (x, y), (x + self.R, y + self.R), tag)

    def draw_final(self, canvas):
        self._draw_parts(canvas, self.start, self.end)

    def draw_rubber(self, canvas, current_point, tag="rubber"):
        if self.start:
            self._draw_parts(canvas, self.start, current_point, tag)