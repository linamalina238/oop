from shape import Shape


class Line2D(Shape):
    def draw_final(self, canvas):
        canvas.create_line(
            self.start[0], self.start[1],
            self.end[0], self.end[1],
            fill="black", width=1
        )