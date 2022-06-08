import pygame
from sys import exit

from constants import *

from typing import List


class Marcacao:
    def __init__(self):  # , x, y, tamanho):
        # self.x = x
        # self.y = y
        # self.tamanho = tamanho

        self.aceso = True


class View:
    def __init__(self, quantidade_x: int):
        pygame.init()

        self.tela = pygame.display.set_mode(
            # (0, 0), pygame.FULLSCREEN | pygame.RESIZABLE
            (800, 600), pygame.RESIZABLE
        )
        self.comprimento, self.altura = self.tela.get_size()
        self.marcacoes: List[Marcacao] = list()
        self.quantidade: int = quantidade_x
        self.comprimento_marcacao = self.comprimento // (self.quantidade + 2)
        self.altura_marcacao = self.altura // (self.quantidade + 2)

        self.eventos: List[int] = [pygame.USEREVENT + 1 + i for i in range(quantidade_x)]

    def blink_mark(self, ident=False):
        marcas = [self.marcacoes[ident]] if ident > 0 else self.marcacoes
        for m in marcas:
            m.aceso = not m.aceso

    def update(self):   # noqa
        for event in pygame.event.get():
            # sair
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            # adicionar uma marca
            elif event.type == pygame.MOUSEBUTTONDOWN:
                tipo = self.eventos[len(self.marcacoes)]
                pygame.time.set_timer(
                    pygame.event.Event(
                        tipo,
                        ident=len(self.marcacoes)
                    ),
                    millis=250,
                    loops=6
                )
                self.marcacoes.append(Marcacao())

            # mudar tamanho da tela
            elif event.type == pygame.VIDEORESIZE:
                self.tela = pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE
                )
                self.comprimento, self.altura = event.w, event.h

            # apertou algum botao
            elif event.type in self.eventos:
                if hasattr(event, 'ident'):
                    self.blink_mark(ident=event.ident)

    def draw(self):
        self.tela.fill(BLACK)
        for i, m in enumerate(self.marcacoes):

            # self.tela.blit
            pygame.draw.rect(
                surface=self.tela,
                color=RED if m.aceso else WHITE,
                rect=(
                    self.comprimento_marcacao * (i + 1),
                    (self.altura - self.altura_marcacao) // 2,
                    self.comprimento_marcacao, self.altura_marcacao
                ),
            )

        pygame.display.flip()

    def loop(self):
        while True:
            self.update()
            self.draw()
