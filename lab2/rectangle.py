from shape import Shape


class Rectangle2D(Shape):
    def _corners(self, current_point):
        cx, cy = self.start
        dx = abs(current_point[0] - cx)
        dy = abs(current_point[1] - cy)
        return (cx - dx, cy - dy, cx + dx, cy + dy)

    def draw_rubber(self, canvas, current_point, tag="rubber"):
        canvas.delete(tag)
        if self.start:
            x1, y1, x2, y2 = self._corners(current_point)
            canvas.create_rectangle(x1, y1, x2, y2, outline=self.RUBBER_COLOR, tags=tag)

    def draw_final(self, canvas):
        x1, y1, x2, y2 = self._corners(self.end)
        canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="")