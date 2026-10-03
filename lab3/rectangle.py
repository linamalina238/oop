from shape import Shape


class Rectangle2D(Shape):
    def draw_rubber(self, canvas, current_point, tag="rubber"):
        canvas.delete(tag)
        if self.start:
            canvas.create_rectangle(
                self.start[0], self.start[1],
                current_point[0], current_point[1],
                outline=self.RUBBER_COLOR, tags=tag
            )

    def draw_final(self, canvas):
        canvas.create_rectangle(
            self.start[0], self.start[1],
            self.end[0], self.end[1],
            outline="black", fill=""
        )