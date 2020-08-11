import socket


class BaseLine:
    def __init__(self, server_ip: str):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_ip = server_ip