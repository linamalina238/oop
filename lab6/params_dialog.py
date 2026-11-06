import tkinter as tk
from tkinter import messagebox


class ParamsDialog:
    N_MAX = 10

    def __init__(self, master, n=4, min_value=-10, max_value=10):
        self.master = master
        self.result = None
        self.window = tk.Toplevel(master)
        self.window.title("Параметри матриці")
        self.window.resizable(False, False)
        self.window.transient(master)
        self.window.protocol("WM_DELETE_WINDOW", self._on_cancel)

        frame = tk.Frame(self.window, padx=12, pady=10)
        frame.pack()

        self.n_var = tk.StringVar(value=str(n))
        self.min_var = tk.StringVar(value=str(min_value))
        self.max_var = tk.StringVar(value=str(max_value))

        rows = (
            (f"Розмір матриці n (1..{self.N_MAX}):", self.n_var),
            ("Мінімальне значення Min:", self.min_var),
            ("Максимальне значення Max:", self.max_var),
        )
        for i, (text, var) in enumerate(rows):
            tk.Label(frame, text=text, anchor="w").grid(row=i, column=0, sticky="w", pady=3)
            entry = tk.Entry(frame, textvariable=var, width=10)
            entry.grid(row=i, column=1, padx=(8, 0), pady=3)
            if i == 0:
                entry.focus_set()
                entry.select_range(0, tk.END)

        buttons = tk.Frame(self.window, pady=8)
        buttons.pack()
        tk.Button(buttons, text="Так", width=10, command=self._on_ok).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons, text="Відміна", width=10, command=self._on_cancel).pack(side=tk.LEFT, padx=5)

        self.window.bind("<Return>", lambda e: self._on_ok())
        self.window.bind("<Escape>", lambda e: self._on_cancel())

        self.window.update_idletasks()
        x = master.winfo_rootx() + 40
        y = master.winfo_rooty() + 40
        self.window.geometry(f"+{x}+{y}")
        self.window.grab_set()

    def show(self):
        self.master.wait_window(self.window)
        return self.result

    def _on_ok(self):
        try:
            n = int(self.n_var.get())
            min_value = int(self.min_var.get())
            max_value = int(self.max_var.get())
        except ValueError:
            messagebox.showerror("Помилка", "Усі значення мають бути цілими числами", parent=self.window)
            return
        if not 1 <= n <= self.N_MAX:
            messagebox.showerror("Помилка", f"n має бути від 1 до {self.N_MAX}", parent=self.window)
            return
        if min_value > max_value:
            messagebox.showerror("Помилка", "Min не може бути більшим за Max", parent=self.window)
            return
        self.result = (n, min_value, max_value)
        self.window.destroy()

    def _on_cancel(self):
        self.result = None
        self.window.destroy()