from os import path
from enum import Enum


class Mensagem(Enum):
    ELIMINACAO = 1
    RESET = 2
    EXIT = 3


BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0

PORT = 4474
HOST = '0.0.0.0'


DIRETORIO_IMAGEMS = path.join(path.abspath(__file__), '..', 'imagem')

