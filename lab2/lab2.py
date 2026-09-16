import tkinter as tk
from tkinter import messagebox

from point import Point2D
from line import Line2D
from rectangle import Rectangle2D
from elipse import Ellipse2D

N = 113

SHAPE_CLASSES = {
    "point": Point2D,
    "line": Line2D,
    "rectangle": Rectangle2D,
    "ellipse": Ellipse2D,
}
SHAPE_NAMES_UA = {
    "point": "Крапка",
    "line": "Лінія",
    "rectangle": "Прямокутник",
    "ellipse": "Еліпс",
}


class GraphicEditorApp:
    def __init__(self, root):
        self.root = root
        self.pcshape = [None] * N
        self.count = 0
        self.current_type = "rectangle"
        self.drawing = False
        self.current_shape = None

        self._build_menu()
        self._build_canvas()
        self._update_title()

    def _build_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Новий", command=self.on_new)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.root.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)

        objects_menu = tk.Menu(menubar, tearoff=0)
        self.type_var = tk.StringVar(value=self.current_type)
        for key in ("point", "line", "rectangle", "ellipse"):
            objects_menu.add_radiobutton(
                label=SHAPE_NAMES_UA[key],
                variable=self.type_var,
                value=key,
                command=self.on_type_change,
            )
        menubar.add_cascade(label="Об'єкти", menu=objects_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Про програму", command=self.on_about)
        menubar.add_cascade(label="Довідка", menu=help_menu)

        self.root.config(menu=menubar)

    def _build_canvas(self):
        self.canvas = tk.Canvas(self.root, width=700, height=500, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

    def _update_title(self):
        self.root.title(f"OOP_Lab2 (Варіант 13) - {SHAPE_NAMES_UA[self.current_type]}")

    def on_type_change(self):
        self.current_type = self.type_var.get()
        self._update_title()

    def on_new(self):
        self.canvas.delete("all")
        self.pcshape = [None] * N
        self.count = 0

    def on_about(self):
        messagebox.showinfo(
            "Про програму",
            "Лабораторна робота №2\nГрафічний редактор об'єктів\nВаріант 13",
        )

    def on_mouse_down(self, event):
        if self.count >= N:
            messagebox.showwarning("Увага", "Масив об'єктів переповнено")
            return
        cls = SHAPE_CLASSES[self.current_type]
        self.current_shape = cls()
        self.current_shape.set_start((event.x, event.y))
        self.drawing = True

    def on_mouse_move(self, event):
        if self.drawing and self.current_shape:
            self.current_shape.draw_rubber(self.canvas, (event.x, event.y))

    def on_mouse_up(self, event):
        if self.drawing and self.current_shape:
            self.canvas.delete("rubber")
            self.current_shape.set_end((event.x, event.y))
            self.current_shape.draw_final(self.canvas)
            self.pcshape[self.count] = self.current_shape
            self.count += 1
            self.current_shape = None
            self.drawing = False


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphicEditorApp(root)
    root.mainloop()