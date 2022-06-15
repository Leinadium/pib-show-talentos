import pygame
from threading import Thread

from .constants import *
from .conexao import Conexao

from typing import List, Optional


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
        pygame.mixer.init()

        self.running = False

        self.tela = pygame.display.set_mode(
            # (0, 0), pygame.FULLSCREEN | pygame.RESIZABLE
            (800, 600), pygame.RESIZABLE
        )
        self.comprimento, self.altura = self.tela.get_size()
        self.marcacoes: List[Marcacao] = list()
        self.quantidade: int = quantidade_x

        self.imagem_original = pygame.image.load(path.join(DIRETORIO_ASSETS, 'x_2.png'))
        self.imagem = self.imagem_original  # vai ser sobreescrita

        self.fundo_original = pygame.image.load(path.join(DIRETORIO_ASSETS, 'fundo_branco.jpg'))
        self.fundo = self.fundo_original

        self.som_erro = pygame.mixer.Sound(path.join(DIRETORIO_ASSETS, 'erro.wav'))
        self.som_erro.set_volume(0.7)

        self.som_eliminacao = pygame.mixer.Sound(path.join(DIRETORIO_ASSETS, 'eliminacao.wav'))
        self.som_eliminacao.set_volume(0.5)

        # self.som_jingle1 = pygame.mixer.Sound(path.join(DIRETORIO_ASSETS, 'jingle1.wav'))
        # self.som_jingle2 = pygame.mixer.Sound(path.join(DIRETORIO_ASSETS, 'jingle2.wav'))
        # enquanto nao tem os jingles, vai ser o erro
        self.som_jingle1 = pygame.mixer.Sound(path.join(DIRETORIO_ASSETS, 'erro.wav'))
        self.som_jingle2 = pygame.mixer.Sound(path.join(DIRETORIO_ASSETS, 'eliminacao.wav'))
        self.channel_jingle1: Optional[pygame.mixer.Channel] = None
        self.channel_jingle2: Optional[pygame.mixer.Channel] = None

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
            self.imagem_original, (self.comprimento_marcacao, self.altura_marcacao)
        )

        comp = int(self.comprimento * 0.6)
        alt = int(self.altura * 0.6)
        self.fundo = pygame.transform.scale(
            self.fundo_original, (comp, alt)
        )

    def blink_mark(self, ident=-1):
        # print("blink!", ident)
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
                    ident=ident,
                ),
                millis=250,
                loops=6
            )
            self.marcacoes.append(Marcacao())

            # tocando som
            if len(self.marcacoes) == self.quantidade:
                # eliminado
                self.som_eliminacao.play(fade_ms=500)
            else:
                self.som_erro.play(fade_ms=100)

        elif msg == Mensagem.RESET:
            self.marcacoes.clear()
            pygame.mixer.stop()

        elif msg == Mensagem.JINGLE1:
            if not (self.channel_jingle2 is not None and self.channel_jingle2.get_busy()):
                self.channel_jingle1 = self.som_jingle1.play(fade_ms=100)

        elif msg == Mensagem.JINGLE2:
            if not (self.channel_jingle1 is not None and self.channel_jingle1.get_busy()):
                self.channel_jingle2 = self.som_jingle2.play(fade_ms=100)

        elif msg == Mensagem.EXIT:
            self.exit()

    def exit(self):
        self.running = False

    def update(self):   # noqa
        for event in pygame.event.get():
            # sair
            if event.type == pygame.QUIT:
                self.exit()

            # ignora clique de mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass

            # botao de emergencia
            elif event.type == pygame.KEYDOWN:
                if hasattr(event, 'key') and event.key == pygame.K_SPACE:
                    pygame.mixer.stop()
                    self.marcacoes.clear()

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
        self.tela.fill(WHITE)

        # projetando o background
        fundo_rect = self.fundo.get_rect()
        self.tela.blit(
            self.fundo, (
                (self.comprimento - fundo_rect.w) // 2,
                (self.altura - fundo_rect.h) // 2
            )
        )

        # projetando os X
        for i, m in enumerate(self.marcacoes):

            if m.aceso:
                rect = self.imagem.get_rect()
                rect.x = self.comprimento_marcacao * (i + 0.5)
                rect.y = (self.altura - self.altura_marcacao) // 2

                self.tela.blit(self.imagem, rect)

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
