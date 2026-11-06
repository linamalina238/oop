import random
import sys
import tkinter as tk
from tkinter import messagebox

from messenger import MessageServer


class Object2App:
    def __init__(self):
        self.root = tk.Tk()
        
        self.root.withdraw()
        self.root.title("Object2 - матриця")
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.matrix = []

        self.header = tk.Label(self.root, text="Очікування повідомлення від Lab6...",
                               font=("Arial", 11, "bold"), padx=10, pady=8)
        self.header.pack()
        self.grid_frame = tk.Frame(self.root, padx=10, pady=4)
        self.grid_frame.pack()
        self.status = tk.Label(self.root, text="", fg="gray30", padx=10, pady=6)
        self.status.pack()

        try:
            self.server = MessageServer(self.root, "Object2", self.on_message)
        except OSError:
            messagebox.showerror("Object2", "Програма Object2 вже запущена")
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
            return "PONG Object2"
        if command == "MATRIX":
            n, min_value, max_value, x, y = map(int, parts[1:6])
            self.create_matrix(n, min_value, max_value)
            self.show_matrix(min_value, max_value)
            self.write_clipboard()
            return self.place_window(x, y)
        if command == "EXIT":
            self.root.after(100, self.on_exit)
            return "OK"
        return f"ERROR unknown command {command}"

    def create_matrix(self, n, min_value, max_value):
        self.matrix = [[random.randint(min_value, max_value) for _ in range(n)] for _ in range(n)]

    def show_matrix(self, min_value, max_value):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        n = len(self.matrix)
        self.header.config(text=f"Матриця {n}×{n}, значення від {min_value} до {max_value}")
        for i, row in enumerate(self.matrix):
            for j, value in enumerate(row):
                tk.Label(self.grid_frame, text=str(value), width=6, relief=tk.GROOVE,
                         bg="white", padx=2, pady=3).grid(row=i, column=j)
        self.status.config(text="Матрицю записано в Clipboard у текстовому форматі")

    
    def matrix_to_text(self):
        return "\n".join("\t".join(str(v) for v in row) for row in self.matrix)

    def write_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.matrix_to_text())
        self.root.update()

    def place_window(self, x, y):
        self.root.update_idletasks()
        self.root.geometry(f"+{x}+{y}")
        self.root.deiconify()
        self.root.lift()
        self.root.update_idletasks()
       
        return f"OK {self.root.winfo_reqwidth()} {self.root.winfo_reqheight()}"

    def on_exit(self):
        self.server.close()
        self.root.destroy()


if __name__ == "__main__":
    app = Object2App()
    app.run()