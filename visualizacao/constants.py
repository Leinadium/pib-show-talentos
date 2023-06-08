from os import path
from enum import Enum


class Mensagem(Enum):
    ELIMINACAO = 1
    RESET = 2
    EXIT = 3
    COUNTDOWN = 4
    JINGLE1 = 5
    JINGLE2 = 6
    JINGLE3 = 7
    JINGLE4 = 8
    JINGLE5 = 9
    JINGLE6 = 10
    


BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0

PORT = 4474
HOST = '0.0.0.0'

DIRETORIO_ASSETS = path.join(path.dirname(path.abspath(__file__)), 'assets')
