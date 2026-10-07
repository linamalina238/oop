from abc import ABC, abstractmethod


class Shape(ABC):
    RUBBER_COLOR = "blue"
    RUBBER_DASH = (4, 4)

    def __init__(self):
        self.start = None
        self.end = None

    def set_start(self, point):
        self.start = point

    def set_end(self, point):
        self.end = point

    @abstractmethod
    def draw_final(self, canvas):
        raise NotImplementedError

    def draw_rubber(self, canvas, current_point, tag="rubber"):
        if self.start:
            canvas.create_line(
                self.start[0], self.start[1],
                current_point[0], current_point[1],
                fill=self.RUBBER_COLOR, width=1, dash=self.RUBBER_DASH, tags=tag
            )

    def draw_part(self, parent, canvas, start, end, tag=None):
        old_start, old_end = self.start, self.end
        self.start, self.end = start, end
        if tag:
            parent.draw_rubber(self, canvas, end, tag)
        else:
            parent.draw_final(self, canvas)
        self.start, self.end = old_start, old_end