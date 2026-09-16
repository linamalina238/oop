import tkinter as tk
from utils import center_window


class _Step2:
    def __init__(self, parent, on_back):
        self._on_back = on_back

        self._win = tk.Toplevel(parent)
        self._win.title("Робота 2 - Крок 2")
        self._win.resizable(False, False)
        self._win.grab_set()

        tk.Label(self._win, text="Друге вікно діалогу.").pack(padx=20, pady=20)

        btn_frame = tk.Frame(self._win)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="< Назад", width=10, command=self._on_go_back).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Так", width=10, command=self._on_finish).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Відміна", width=10, command=self._on_cancel).pack(side="left", padx=5)

        center_window(self._win, 340, 130)
        self._win.protocol("WM_DELETE_WINDOW", self._on_cancel)

    def _on_go_back(self):
        self._win.destroy()
        self._on_back()

    def _on_finish(self):
        self._win.destroy()

    def _on_cancel(self):
        self._win.destroy()


def open_dialog(parent, on_back):
    _Step2(parent, on_back)