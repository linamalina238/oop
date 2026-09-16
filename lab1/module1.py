import tkinter as tk
from utils import center_window


class _Dialog1:
    def __init__(self, parent, on_result):
        self._on_result = on_result
        self._value = 1

        self._win = tk.Toplevel(parent)
        self._win.title("Робота 1")
        self._win.resizable(False, False)
        self._win.grab_set()

        tk.Label(self._win, text="Виберіть число від 1 до 100:").pack(padx=20, pady=(15, 5))

        self._scale = tk.Scale(
            self._win, from_=1, to=100, orient="horizontal",
            length=250, command=self._on_scale_change
        )
        self._scale.set(1)
        self._scale.pack(padx=20, pady=5)

        btn_frame = tk.Frame(self._win)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Так", width=10, command=self._on_ok).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Відміна", width=10, command=self._on_cancel).pack(side="left", padx=5)

        center_window(self._win, 320, 160)
        self._win.protocol("WM_DELETE_WINDOW", self._on_cancel)

    def _on_scale_change(self, value):
        self._value = int(value)

    def _on_ok(self):
        self._on_result(self._value)
        self._win.destroy()

    def _on_cancel(self):
        self._win.destroy()


def open_dialog(parent, on_result):
    _Dialog1(parent, on_result)