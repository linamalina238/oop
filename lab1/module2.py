import tkinter as tk
from utils import center_window


class _Step1:
    def __init__(self, parent, on_next):
        self._on_next = on_next

        self._win = tk.Toplevel(parent)
        self._win.title("Робота 2 - Крок 1")
        self._win.resizable(False, False)
        self._win.grab_set()

        tk.Label(self._win, text="Перше вікно діалогу.").pack(padx=20, pady=20)

        btn_frame = tk.Frame(self._win)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Далі >", width=10, command=self._on_go_next).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Відміна", width=10, command=self._on_cancel).pack(side="left", padx=5)

        center_window(self._win, 300, 130)
        self._win.protocol("WM_DELETE_WINDOW", self._on_cancel)

    def _on_go_next(self):
        self._win.destroy()
        self._on_next()

    def _on_cancel(self):
        self._win.destroy()


def open_dialog(parent, on_next):
    _Step1(parent, on_next)