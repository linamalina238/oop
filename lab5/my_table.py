import tkinter as tk
from tkinter import ttk


class ObjectTable:
    COLUMNS = ("№", "Тип", "x1", "y1", "x2", "y2")
    WIDTHS = (40, 150, 55, 55, 55, 55)

    def __init__(self, master):
        self.master = master
        self.window = None
        self.tree = None

        # Колбеки.Таблиця нічого не знає про того, хто її використовує,
        # вона просто викликає ці функції, якщо їх підставили зовні
        self.on_select = None   
        self.on_delete = None   
        self.on_close = None   

    def is_open(self):
        return self.window is not None

    def open(self, x=None, y=None):
        if self.window:
            return
        self.window = tk.Toplevel(self.master)
        self.window.title("Таблиця об'єктів")
        self.window.transient(self.master)
        if x is not None and y is not None:
            self.window.geometry(f"+{x}+{y}")
        self.window.protocol("WM_DELETE_WINDOW", self._on_x)

        frame = tk.Frame(self.window)
        frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(frame, columns=self.COLUMNS, show="headings",
                                 selectmode="browse", height=14)
        for name, width in zip(self.COLUMNS, self.WIDTHS):
            self.tree.heading(name, text=name)
            self.tree.column(name, width=width, anchor=tk.CENTER)
        scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        btn = tk.Button(self.window, text="Видалити виділений", command=self._on_delete_click)
        btn.pack(fill=tk.X)

        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        self.tree.bind("<Delete>", lambda e: self._on_delete_click())

    def close(self):
        if self.window:
            self.window.destroy()
            self.window = None
            self.tree = None

    def set_rows(self, rows):
        if not self.tree:
            return
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def add_row(self, row):
        if not self.tree:
            return
        item = self.tree.insert("", tk.END, values=row)
        self.tree.see(item)

    def selected_index(self):
        if not self.tree:
            return None
        sel = self.tree.selection()
        if not sel:
            return None
        return self.tree.index(sel[0])

    def _on_tree_select(self, event):
        if self.on_select:
            self.on_select(self.selected_index())

    def _on_delete_click(self):
        index = self.selected_index()
        if index is not None and self.on_delete:
            self.on_delete(index)

    def _on_x(self):
        self.close()
        if self.on_close:
            self.on_close()