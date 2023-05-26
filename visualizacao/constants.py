from os import path
from enum import Enum


class Mensagem(Enum):
    ELIMINACAO = 1
    RESET = 2
    EXIT = 3
    JINGLE1 = 4
    JINGLE2 = 5
    COUNTDOWN = 6


BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0

PORT = 4474
HOST = '0.0.0.0'

DIRETORIO_ASSETS = path.join(path.dirname(path.abspath(__file__)), 'assets')
