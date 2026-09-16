import tkinter as tk

import module1
import module2
import module3
from utils import center_window


class MainApp:
    def __init__(self, root):
        self._root = root
        self._root.title("Лабораторна робота №2")

        self._result_label = tk.Label(self._root, text="Результат: -", font=("Arial", 12))
        self._result_label.pack(padx=20, pady=20)

        self._build_menu()
        center_window(self._root, 400, 150)

    def _build_menu(self):
        menu_bar = tk.Menu(self._root)
        menu_bar.add_command(label="Робота1", command=self._open_robota1)
        menu_bar.add_command(label="Робота2", command=self._open_robota2)
        self._root.config(menu=menu_bar)

    def _open_robota1(self):
        module1.open_dialog(self._root, self._on_robota1_result)

    def _on_robota1_result(self, value):
        self._result_label.config(text=f"Робота1: вибрано число {value}")

    def _open_robota2(self):
        module2.open_dialog(self._root, self._open_robota2_step2)

    def _open_robota2_step2(self):
        module3.open_dialog(self._root, self._open_robota2)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()