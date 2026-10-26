import tkinter as tk
from tkinter import messagebox, filedialog

from point import Point2D
from line import Line2D
from rectangle import Rectangle2D
from elipse import Ellipse2D
from line_oo import LineOO2D
from cube import Cube2D
from my_table import ObjectTable
from tooltip import ToolTip
from icons import make_icon

N = 114  # Ж = 14 (як у Lab3 і Lab4), N = Ж + 100

# Щоб додати нову фігуру: зробити її модуль (клас-нащадок Shape з KEY і NAME)
# і дописати клас у цей список. Меню, кнопки Toolbar, таблиця і файл
# самі підхоплять її через KEY і NAME. Якщо для неї немає своєї іконки
# в icons.py, на кнопці буде стандартна іконка.
SHAPE_CLASSES = [Point2D, Line2D, Rectangle2D, Ellipse2D, LineOO2D, Cube2D]
SHAPES_BY_KEY = {cls.KEY: cls for cls in SHAPE_CLASSES}


class MyEditor:
    _allow_create = False

    def __init__(self):
        # напряму створити редактор не можна, тільки через get_instance()
        if not MyEditor._allow_create:
            raise RuntimeError("Використовуй MyEditor.get_instance()")

        self.root = tk.Tk()
        self.pcshape = [None] * N
        self.count = 0
        self.current_type = Rectangle2D.KEY
        self.drawing = False
        self.current_shape = None

        self.type_var = tk.StringVar(value=self.current_type)
        self.table_var = tk.BooleanVar(value=False)

        self.table = ObjectTable(self.root)
        self.table.on_select = self.on_table_select
        self.table.on_delete = self.on_table_delete
        self.table.on_close = self.on_table_closed

        self._build_menu()
        self._build_toolbar()
        self._build_canvas()
        self.root.title("OOP_Lab5 (Варіант 13)")
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

    @staticmethod
    def get_instance():
        # Singleton Меєрса: єдиний об'єкт живе як "статична локальна змінна"
        # функції. Він створюється при першому виклику, а далі повертається
        # той самий.
        if not hasattr(MyEditor.get_instance, "obj"):
            MyEditor._allow_create = True
            try:
                MyEditor.get_instance.obj = MyEditor()
            finally:
                MyEditor._allow_create = False
        return MyEditor.get_instance.obj

    def run(self):
        self.root.mainloop()

    def _build_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Новий", command=self.on_new)
        file_menu.add_command(label="Відкрити...", command=self.on_open)
        file_menu.add_command(label="Зберегти як...", command=self.on_save)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.on_exit)
        menubar.add_cascade(label="Файл", menu=file_menu)

        objects_menu = tk.Menu(menubar, tearoff=0, postcommand=self.on_init_menu_popup)
        for cls in SHAPE_CLASSES:
            objects_menu.add_radiobutton(
                label=cls.NAME,
                variable=self.type_var,
                value=cls.KEY,
                command=self.on_type_change,
            )
        menubar.add_cascade(label="Об'єкти", menu=objects_menu)

        # окремий пункт меню для відкриття/закриття вікна таблиці
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_checkbutton(
            label="Таблиця об'єктів",
            variable=self.table_var,
            command=self.on_toggle_table,
        )
        menubar.add_cascade(label="Вигляд", menu=view_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Про програму", command=self.on_about)
        menubar.add_cascade(label="Довідка", menu=help_menu)

        self.root.config(menu=menubar)

    def _build_toolbar(self):
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        # PhotoImage треба зберігати у полі класу, інакше Python їх видалить
        self.icons = {}
        for cls in SHAPE_CLASSES:
            self.icons[cls.KEY] = make_icon(cls.KEY)
            btn = tk.Radiobutton(
                toolbar,
                image=self.icons[cls.KEY],
                variable=self.type_var,
                value=cls.KEY,
                indicatoron=False,
                padx=4,
                pady=4,
                command=self.on_type_change,
            )
            btn.pack(side=tk.LEFT, padx=1, pady=1)
            ToolTip(btn, cls.NAME)

    def _build_canvas(self):
        self.canvas = tk.Canvas(self.root, width=700, height=500, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

    # відмітка поточного типу в меню (Ж mod 2 = 0)
    def on_init_menu_popup(self):
        self.type_var.set(self.current_type)

    def on_type_change(self):
        self.current_type = self.type_var.get()


    def draw_shape(self, shape):
        # запам'ятовуємо id елементів Canvas, з яких складається фігура,
        # щоб потім підсвітити її при виділенні рядка таблиці
        before = set(self.canvas.find_all())
        shape.draw_final(self.canvas)
        shape.items = list(set(self.canvas.find_all()) - before)

    def redraw(self):
        self.canvas.delete("all")
        for i in range(self.count):
            self.draw_shape(self.pcshape[i])

    def row_for(self, index):
        shape = self.pcshape[index]
        return (index + 1, shape.NAME) + shape.coords()

    def all_rows(self):
        return [self.row_for(i) for i in range(self.count)]


    def on_new(self):
        self.canvas.delete("all")
        self.pcshape = [None] * N
        self.count = 0
        self.table.set_rows([])

    def on_save(self):
        path = filedialog.asksaveasfilename(
            title="Зберегти об'єкти",
            defaultextension=".txt",
            filetypes=[("Текстові файли", "*.txt")],
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                for i in range(self.count):
                    f.write(self.pcshape[i].to_line() + "\n")
        except OSError as e:
            messagebox.showerror("Помилка", f"Не вдалося записати файл:\n{e}")

    def on_open(self):
        path = filedialog.askopenfilename(
            title="Відкрити файл з об'єктами",
            filetypes=[("Текстові файли", "*.txt")],
        )
        if not path:
            return
        shapes = []
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.split()
                    if not parts:
                        continue
                    cls = SHAPES_BY_KEY[parts[0]]
                    x1, y1, x2, y2 = map(int, parts[1:])
                    shape = cls()
                    shape.set_start((x1, y1))
                    shape.set_end((x2, y2))
                    shapes.append(shape)
        except (OSError, KeyError, ValueError):
            messagebox.showerror("Помилка", "Файл пошкоджений або має невірний формат")
            return
        if len(shapes) > N:
            messagebox.showerror("Помилка", f"У файлі більше {N} об'єктів")
            return

        self.pcshape = shapes + [None] * (N - len(shapes))
        self.count = len(shapes)
        self.redraw()
        self.table.set_rows(self.all_rows())

    def on_exit(self):
        self.table.close()
        self.root.destroy()

    def on_about(self):
        messagebox.showinfo(
            "Про програму",
            "Лабораторна робота №5\nГрафічний редактор об'єктів\nВаріант 13",
        )

    def on_toggle_table(self):
        if self.table_var.get():
            x = self.root.winfo_rootx() + self.root.winfo_width() + 10
            y = self.root.winfo_rooty()
            self.table.open(x, y)
            self.table.set_rows(self.all_rows())
        else:
            self.table.close()
            self.canvas.delete("select")

    # колбеки, які викликає таблиця (сама таблиця про MyEditor нічого не знає)
    def on_table_closed(self):
        self.table_var.set(False)
        self.canvas.delete("select")

    def on_table_select(self, index):
        self.canvas.delete("select")
        if index is None or index >= self.count:
            return
        box = self.canvas.bbox(*self.pcshape[index].items)
        if box:
            x1, y1, x2, y2 = box
            self.canvas.create_rectangle(
                x1 - 4, y1 - 4, x2 + 4, y2 + 4,
                outline="red", width=2, dash=(3, 3), tags="select",
            )

    def on_table_delete(self, index):
        if index >= self.count:
            return
        del self.pcshape[index]
        self.pcshape.append(None)  # розмір масиву лишається N
        self.count -= 1
        self.redraw()
        self.table.set_rows(self.all_rows())

    def on_mouse_down(self, event):
        if self.count >= N:
            messagebox.showwarning("Увага", "Масив об'єктів переповнено")
            return
        cls = SHAPES_BY_KEY[self.current_type]
        self.current_shape = cls()
        self.current_shape.set_start((event.x, event.y))
        self.drawing = True

    def on_mouse_move(self, event):
        if self.drawing and self.current_shape:
            self.canvas.delete("rubber")
            self.current_shape.draw_rubber(self.canvas, (event.x, event.y))

    def on_mouse_up(self, event):
        if self.drawing and self.current_shape:
            self.canvas.delete("rubber")
            self.current_shape.set_end((event.x, event.y))
            self.draw_shape(self.current_shape)
            self.pcshape[self.count] = self.current_shape
            self.count += 1
            self.table.add_row(self.row_for(self.count - 1))
            self.current_shape = None
            self.drawing = False


if __name__ == "__main__":
    editor = MyEditor.get_instance()
    editor.run()