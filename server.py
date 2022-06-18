from socketserver import DatagramRequestHandler as UDP, UDPServer, BaseServer
from typing import List


class MineServer(UDP):
    clients = {}

    @staticmethod
    def start() -> UDPServer:
        server = UDPServer(("", 12300), MineServer)
        server.clients = {}
        server.serve_forever()
        return server

    def handle(self):
        while True:
            data = self.rfile.readline().decode("utf-8")
            response = self.resolve(data)
            if response is not None:
                self.wfile.write(response.encode("utf-8"))

    def send(self, data, addr):
        self.socket.sendto(data.encode("utf-8"), addr)

    def radio(self, data, avoid: List[str] = []):
        for _hash in self.clients:
            if _hash not in avoid:
                print("send to %d %s" % (_hash, data))
                self.send(data, self.clients[_hash])

    def resolve(self, data):
        _hash, data = data[0:4], data[4:]
        if data.startswith("ping"):
            return self.ping(data)
        elif data.startswith("register"):
            self.register(_hash)

    def ping(self, msg):
        return "pong" + msg[4:]

    def register(self, _hash, addr):
        self.clients[_hash] = addr


if __name__ == "__main__":
    print("Miner server v0.1")
    server = MineServer.start()
