import json, socket

class Connection:
    def __init__(self, sock):
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # no batching delay
        self.sock = sock
        self.f = sock.makefile("rw", encoding="utf-8", newline="\n")

    def send(self, msg: dict):
        self.f.write(json.dumps(msg) + "\n")
        self.f.flush()

    def recv(self) -> dict:
        line = self.f.readline()          # blocks until a full line arrives
        if not line:
            raise ConnectionError("peer disconnected")
        return json.loads(line)

def host(port=5000):
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", port))           # 0.0.0.0 = reachable from the LAN
    srv.listen(1)
    print("Waiting for opponent...")
    sock, addr = srv.accept()
    print("Connected:", addr)
    return Connection(sock)

def join(ip, port=5000):
    return Connection(socket.create_connection((ip, port)))

