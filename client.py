import random
from socket import *
class MineClient:
    def __init__(self):
        self.server_addr = ("127.0.0.1",12300)
        self.bufsize = 1024
        self.client = socket(AF_INET,SOCK_DGRAM)
        self.hash = "".join(random.sample("1234567890abcdef",4))
        self.send("register")

    def send(self,data):
        self.client.sendto(data.encode("utf-8"), self.server_addr)
        data, saddr = self.client.recvfrom(self.bufsize)
        print(data.decode("utf-8"))
        return data.decode("utf-8")

    def preprocess(self,data):
        return self.hash+","+data


if __name__ == "__main__":
    client = MineClient()
    client.send("ping")