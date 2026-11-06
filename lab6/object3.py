import sys
import tkinter as tk
from fractions import Fraction
from tkinter import messagebox

from messenger import MessageServer


class Object3App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.title("Object3 - детермінант")
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.header = tk.Label(self.root, text="Очікування повідомлення від Lab6...",
                               font=("Arial", 11, "bold"), padx=16, pady=8)
        self.header.pack()
        self.result = tk.Label(self.root, text="", font=("Arial", 16, "bold"),
                               fg="darkblue", padx=16, pady=10)
        self.result.pack()
        self.status = tk.Label(self.root, text="", fg="gray30", padx=16, pady=6)
        self.status.pack()

        try:
            self.server = MessageServer(self.root, "Object3", self.on_message)
        except OSError:
            messagebox.showerror("Object3", "Програма Object3 вже запущена")
            self.root.destroy()
            sys.exit(1)

    def run(self):
        self.root.mainloop()

    def on_message(self, text):
        parts = text.split()
        if not parts:
            return "ERROR empty"
        command = parts[0]
        if command == "PING":
            return "PONG Object3"
        if command == "DET":
            x, y = map(int, parts[1:3])
            # Object3 про Object2 нічого не знає, дані бере тільки з Clipboard
            matrix = self.read_clipboard()
            det = self.determinant(matrix)
            self.show_result(len(matrix), det)
            self.place_window(x, y)
            return f"OK {det}"
        if command == "EXIT":
            self.root.after(100, self.on_exit)
            return "OK"
        return f"ERROR unknown command {command}"

    def read_clipboard(self):
        text = self.root.clipboard_get()
        matrix = [[int(v) for v in line.split()] for line in text.strip().splitlines() if line.strip()]
        n = len(matrix)
        if n == 0 or any(len(row) != n for row in matrix):
            raise ValueError("у Clipboard немає квадратної матриці")
        return matrix

    @staticmethod
    def determinant(matrix):
        # метод Гауса: зводимо матрицю до трикутного вигляду,
        # det = добуток діагоналі, кожна перестановка рядків міняє знак.
        # Fraction, щоб не було похибки округлення
        a = [[Fraction(v) for v in row] for row in matrix]
        n = len(a)
        det = Fraction(1)
        for col in range(n):
            pivot = next((r for r in range(col, n) if a[r][col] != 0), None)
            if pivot is None:
                return 0
            if pivot != col:
                a[col], a[pivot] = a[pivot], a[col]
                det = -det
            det *= a[col][col]
            for r in range(col + 1, n):
                k = a[r][col] / a[col][col]
                for c in range(col, n):
                    a[r][c] -= k * a[col][c]
        return int(det)

    def show_result(self, n, det):
        self.header.config(text=f"Матриця {n}×{n} зчитана з Clipboard")
        self.result.config(text=f"det = {det}")
        self.status.config(text="Детермінант обчислено методом Гауса")

    def place_window(self, x, y):
        self.root.update_idletasks()
        self.root.geometry(f"+{x}+{y}")
        self.root.deiconify()
        self.root.lift()
        self.root.update_idletasks()

    def on_exit(self):
        self.server.close()
        self.root.destroy()


if __name__ == "__main__":
    app = Object3App()
    app.run()