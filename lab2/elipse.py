from shape import Shape


class Ellipse2D(Shape):
    FILL_COLOR = "yellow"

    def draw_rubber(self, canvas, current_point, tag="rubber"):
        canvas.delete(tag)
        if self.start:
            canvas.create_rectangle(
                self.start[0], self.start[1],
                current_point[0], current_point[1],
                outline=self.RUBBER_COLOR, tags=tag
            )

    def draw_final(self, canvas):
        x1, y1 = self.start
        x2, y2 = self.end
        canvas.create_oval(x1, y1, x2, y2, outline="black", fill=self.FILL_COLOR)