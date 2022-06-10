import socket


class Conexao:
    PORTA = 4474
    HOST = 'localhost'

    @classmethod
    def config(cls, host: str, port: int):
        cls.HOST = host
        cls.PORTA = port

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.HOST, self.PORTA))
        print(self.sock.getpeername())

    def _send(self, msg: str):
        q = self.sock.send(f'{msg}\n'.encode('utf-8'))
        print(f'enviado {q} bytes')
        return

    def enviar_eliminacao(self):
        print("Enviando eliminacao")
        self._send('x')
        return

    def enviar_reset(self):
        print("Enviando reset")
        self._send('r')
        return

    def fechar(self):
        self.sock.close()
