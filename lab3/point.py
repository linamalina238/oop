from shape import Shape


class Point2D(Shape):
    RADIUS = 3

    def draw_rubber(self, canvas, current_point, tag="rubber"):
        canvas.delete(tag)

    def draw_final(self, canvas):
        x, y = self.end if self.end else self.start
        canvas.create_oval(
            x - self.RADIUS, y - self.RADIUS,
            x + self.RADIUS, y + self.RADIUS,
            outline="black", fill="black"
        )