import pygame
from threading import Thread

from .constants import *
from .conexao import Conexao

from typing import List


class Marcacao:
    def __init__(self):  # , x, y, tamanho):
        # self.x = x
        # self.y = y
        # self.tamanho = tamanho

        self.aceso = True

    def __repr__(self):
        return f'<Marcacao {"acesa" if self.aceso else "apagada"}>'


class View:
    def __init__(self, quantidade_x: int):
        pygame.init()

        self.running = False

        self.tela = pygame.display.set_mode(
            # (0, 0), pygame.FULLSCREEN | pygame.RESIZABLE
            (800, 600), pygame.RESIZABLE
        )
        self.comprimento, self.altura = self.tela.get_size()
        self.marcacoes: List[Marcacao] = list()
        self.quantidade: int = quantidade_x

        self.imagem = pygame.image.load(path.join(DIRETORIO_IMAGEMS, 'x.png'))

        self.comprimento_marcacao = -1
        self.altura_marcacao = -1

        self._update_dimensions()

        self.eventos: List[int] = [pygame.USEREVENT + 1 + i for i in range(quantidade_x)]

        self.conexao = Conexao(HOST, PORT, self.receive_message)
        self.conexao_thread = Thread(target=self.conexao.loop)
        self.clock = pygame.time.Clock()

    def _update_dimensions(self):
        self.comprimento_marcacao = self.comprimento // (self.quantidade + 1)
        # self.altura_marcacao = self.altura // (self.quantidade + 1)
        self.altura_marcacao = self.comprimento_marcacao    # para ficar quadrado

        self.imagem = pygame.transform.scale(
            self.imagem, (self.comprimento_marcacao, self.altura_marcacao)
        )

    def blink_mark(self, ident=-1):
        print("blink!", ident)
        try:
            marcas = [self.marcacoes[ident]] if ident != -1 else self.marcacoes
        except IndexError:
            return      # ignora erros
        for m in marcas:
            m.aceso = not m.aceso

        print(self.marcacoes)

    def receive_message(self, msg: Mensagem):
        if msg == Mensagem.ELIMINACAO:
            ident: int = len(self.marcacoes)
            if ident == self.quantidade:
                return
            tipo = self.eventos[ident]
            pygame.time.set_timer(
                pygame.event.Event(
                    tipo,
                    ident=ident
                ),
                millis=250,
                loops=6
            )
            self.marcacoes.append(Marcacao())

        elif msg == Mensagem.RESET:
            self.marcacoes.clear()

        elif msg == Mensagem.EXIT:
            self.exit()

    def exit(self):
        self.running = False

    def update(self):   # noqa
        for event in pygame.event.get():
            # sair
            if event.type == pygame.QUIT:
                self.exit()

            # ignora clique
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass

            # mudar tamanho da tela
            elif event.type == pygame.VIDEORESIZE:
                self.tela = pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE
                )
                self.comprimento, self.altura = event.w, event.h
                self._update_dimensions()

            # apertou algum botao
            elif event.type in self.eventos:
                print(event)
                if hasattr(event, 'ident'):
                    self.blink_mark(ident=event.ident)

    def draw(self):
        self.tela.fill(BLACK)
        for i, m in enumerate(self.marcacoes):

            if m.aceso:
                rect = self.imagem.get_rect()
                rect.x = self.comprimento_marcacao * (i + 0.5)
                rect.y = (self.altura - self.altura_marcacao) // 2

                self.tela.blit(self.imagem, rect)

            # self.tela.blit
            # pygame.draw.rect(
            #     surface=self.tela,
            #     color=RED if m.aceso else WHITE,
            #     rect=(
            #         self.comprimento_marcacao * (i + 0.5),
            #         (self.altura - self.altura_marcacao) // 2,
            #         self.comprimento_marcacao, self.altura_marcacao
            #     ),
            # )

        pygame.display.flip()

    def server_start(self):
        self.conexao_thread.start()

    def loop(self):
        self.clock.tick(30)

        self.running = True
        while self.running:
            self.update()
            self.draw()

        pygame.quit()
        # exit(0)
        return
