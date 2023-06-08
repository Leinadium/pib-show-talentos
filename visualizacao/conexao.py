import socket

from .constants import Mensagem
from typing import Callable


class Conexao:
    def __init__(self, host, port, callback):
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.callback: Callable[[Mensagem], None] = callback

    def client_handler(self, conn: socket.socket):
        data: bytes = conn.recv(1024)
        while len(data) != 0:
            print("recebi: ", data)
            try:
                data_str: str = data.decode('utf-8')
            except UnicodeError:
                print("invalid data: ", data)
                return

            if data_str.startswith('r'):
                self.callback(Mensagem.RESET)

            elif data_str.startswith('x'):
                self.callback(Mensagem.ELIMINACAO)

            elif data_str.startswith('k'):
                self.callback(Mensagem.EXIT)
                conn.shutdown(socket.SHUT_RDWR)
                return

            elif data_str.startswith('j'):
                x = data_str[1]
                if x == '1':
                    self.callback(Mensagem.JINGLE1)
                elif x == '2':
                    self.callback(Mensagem.JINGLE2)
                elif x == '3':
                    self.callback(Mensagem.JINGLE3)
                elif x == '4':
                    self.callback(Mensagem.JINGLE4)
                elif x == '5':
                    self.callback(Mensagem.JINGLE5)
                elif x == '6':
                    self.callback(Mensagem.JINGLE6)

            elif data_str.startswith('c'):
                self.callback(Mensagem.COUNTDOWN)

            data: bytes = conn.recv(1024)

        self.callback(Mensagem.EXIT)

    def loop(self):
        self.socket.listen()
        print(self.socket.getsockname())

        # while True:
        #     conn, addr = self.socket.accept()
        #     print("Recebi conexao", conn, addr)
        #     self.client_handler(conn)

        conn, addr = self.socket.accept()
        print("Recebi conexao", conn, addr)
        self.client_handler(conn)
