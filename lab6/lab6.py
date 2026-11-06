import os
import socket
import subprocess
import sys
import time
import tkinter as tk
from tkinter import messagebox

HOST = "127.0.0.1"
# у кожної програми свій постійний порт
PORTS = {"Object2": 50002, "Object3": 50003}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROGRAMS = {
    "Object2": os.path.join(BASE_DIR, "object2.py"),
    "Object3": os.path.join(BASE_DIR, "object3.py"),
}
START_TIMEOUT = 10.0
GAP = 20


def send_message(name, text, timeout=5.0):
    with socket.create_connection((HOST, PORTS[name]), timeout=timeout) as sock:
        sock.sendall((text + "\n").encode("utf-8"))
        return sock.recv(4096).decode("utf-8").strip()


def is_running(name):
    try:
        return send_message(name, "PING", timeout=1.0) == "PONG " + name
    except OSError:
        return False


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


class Lab6App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OOP_Lab6 (Варіант 13)")
        self.root.geometry("460x320+40+60")
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Варіант 13 (13 mod 4 = 1): матриця n×n і її детермінант
        self.params = (4, -10, 10)
        self.busy = False

        self._build_menu()
        self._build_body()
        self.set_state("Готово. Оберіть «Файл → Виконати...»")

    def run(self):
        self.root.mainloop()

    def _build_menu(self):
        menubar = tk.Menu(self.root)

        self.file_menu = tk.Menu(menubar, tearoff=0)
        self.file_menu.add_command(label="Виконати...", command=self.on_execute)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Вихід", command=self.on_exit)
        menubar.add_cascade(label="Файл", menu=self.file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Про програму", command=self.on_about)
        menubar.add_cascade(label="Довідка", menu=help_menu)

        self.root.config(menu=menubar)

    def _build_body(self):
        self.state_label = tk.Label(self.root, anchor="w", font=("Arial", 10, "bold"), padx=8, pady=6)
        self.state_label.pack(fill=tk.X)

        frame = tk.Frame(self.root, padx=8)
        frame.pack(fill=tk.BOTH, expand=True)
        self.log = tk.Listbox(frame, font=("Consolas", 9))
        scroll = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.log.yview)
        self.log.configure(yscrollcommand=scroll.set)
        self.log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.result_label = tk.Label(self.root, anchor="w", padx=8, pady=6)
        self.result_label.pack(fill=tk.X)

    def set_state(self, text):
        self.state_label.config(text=text)

    def add_log(self, text):
        self.log.insert(tk.END, time.strftime("%H:%M:%S  ") + text)
        self.log.see(tk.END)
        self.root.update_idletasks()

    def on_execute(self):
        if self.busy:
            return
        dialog = ParamsDialog(self.root, *self.params)
        params = dialog.show()
        if params is None:
            return
        self.params = params
        n, min_value, max_value = params

        self.busy = True
        self.file_menu.entryconfig("Виконати...", state=tk.DISABLED)
        self.log.delete(0, tk.END)
        self.result_label.config(text="")
        self.set_state("Виконується обмін повідомленнями...")
        self.root.state("normal")
        self.root.geometry("460x320+40+60")
        self.root.update_idletasks()

        x2 = self.root.winfo_x() + self.root.winfo_width() + GAP
        y = self.root.winfo_y()

        try:
            self.start_program("Object2")
            self.add_log(f"Lab6 -> Object2: MATRIX {n} {min_value} {max_value}")
            answer = self.request("Object2", f"MATRIX {n} {min_value} {max_value} {x2} {y}")
            self.add_log(f"Object2 -> Lab6: {answer}")

            width = int(answer.split()[1])
            height = int(answer.split()[2])

            self.start_program("Object3")
            x3 = x2 + width + GAP
            y3 = y
            if x3 + 350 > self.root.winfo_screenwidth():
                x3 = x2
                y3 = y + height + GAP + 40
            self.add_log("Lab6 -> Object3: DET")
            answer = self.request("Object3", f"DET {x3} {y3}")
            self.add_log(f"Object3 -> Lab6: {answer}")

            self.add_log("Роботу завершено")
            self.result_label.config(text=f"Детермінант матриці: {answer.split()[1]}")
            self.finish("Готово. Можна виконати роботу повторно")
        except Exception as e:
            self.add_log("Помилка: " + str(e))
            self.finish("Помилка під час обміну повідомленнями")
            messagebox.showerror("Помилка", str(e))

    def start_program(self, name):
        # якщо програма вже запущена, повторно її не стартуємо
        if is_running(name):
            self.add_log(f"{name} вже запущено")
            return
        self.add_log(f"Запуск {name}...")
        subprocess.Popen([sys.executable, PROGRAMS[name]], cwd=BASE_DIR)
        deadline = time.time() + START_TIMEOUT
        while time.time() < deadline:
            if is_running(name):
                self.add_log(f"{name} запущено і готове до роботи")
                return
            self.root.update()  # щоб вікно Lab6 не зависало
            time.sleep(0.2)
        raise RuntimeError(f"Не вдалося запустити {name}")

    @staticmethod
    def request(name, text):
        answer = send_message(name, text)
        if not answer.startswith("OK"):
            raise RuntimeError(f"{name}: {answer or 'немає відповіді'}")
        return answer

    def finish(self, state):
        self.busy = False
        self.file_menu.entryconfig("Виконати...", state=tk.NORMAL)
        self.set_state(state)
        self.root.lift()
        self.root.focus_force()

    def on_about(self):
        messagebox.showinfo(
            "Про програму",
            "Лабораторна робота №6\nПрограмна система з множини об'єктів,\n"
            "керованих повідомленнями\nВаріант 13 (13 mod 4 = 1)",
        )

    def on_exit(self):
        if self.busy:
            return

        for name in PROGRAMS:
            try:
                send_message(name, "EXIT", timeout=1.0)
            except OSError:
                pass
        self.root.destroy()


if __name__ == "__main__":
    app = Lab6App()
    app.run()