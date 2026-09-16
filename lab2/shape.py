from abc import ABC, abstractmethod


class Shape(ABC):
    RUBBER_COLOR = "red"

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
        canvas.delete(tag)
        if self.start:
            canvas.create_line(
                self.start[0], self.start[1],
                current_point[0], current_point[1],
                fill=self.RUBBER_COLOR, width=1, tags=tag
            )