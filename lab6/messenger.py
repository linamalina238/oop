import socket

HOST = "127.0.0.1"
# у кожної програми свій постійний порт
PORTS = {"Object2": 50002, "Object3": 50003}


def send_message(name, text, timeout=5.0):
   
    with socket.create_connection((HOST, PORTS[name]), timeout=timeout) as sock:
        sock.sendall((text + "\n").encode("utf-8"))
        return sock.recv(4096).decode("utf-8").strip()


def is_running(name):
    try:
        return send_message(name, "PING", timeout=1.0) == "PONG " + name
    except OSError:
        return False


class MessageServer:
    def __init__(self, root, name, handler):
        self.root = root
        self.handler = handler
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      
        self.sock.bind((HOST, PORTS[name]))
        self.sock.listen()
        self.sock.setblocking(False)
        self.root.after(50, self.check)

    def check(self):
      
        try:
            conn, _ = self.sock.accept()
        except BlockingIOError:
            conn = None
        if conn:
            conn.settimeout(2.0)
            text = conn.recv(4096).decode("utf-8").strip()
            try:
                answer = self.handler(text)
            except Exception as e:
                answer = f"ERROR {e}"
            conn.sendall((answer + "\n").encode("utf-8"))
            conn.close()
        self.root.after(50, self.check)

    def close(self):
        self.sock.close()