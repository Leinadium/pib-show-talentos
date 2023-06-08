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
    def __init__(self, quantidade_x: int, countdown_max: int):
        pygame.init()
        pygame.mixer.init()

        self.running = False

        self.tela = pygame.display.set_mode(
            # (0, 0), pygame.FULLSCREEN | pygame.RESIZABLE
            (800, 600), pygame.RESIZABLE
        )
        self.tela_cheia = False

        self.comprimento, self.altura = self.tela.get_size()
        self.marcacoes: List[Marcacao] = list()
        self.quantidade: int = quantidade_x

        self.imagem_original = pygame.image.load(path.join(DIRETORIO_ASSETS, 'x_3.png'))
        self.imagem = self.imagem_original  # vai ser sobreescrita

        self.fundo_original = pygame.image.load(path.join(DIRETORIO_ASSETS, 'fundo_final.png'))
        self.fundo = self.fundo_original

        self.som_erro = pygame.mixer.Sound(path.join(DIRETORIO_ASSETS, 'erro.wav'))
        self.som_erro.set_volume(0.7)

        self.som_eliminacao = pygame.mixer.Sound(path.join(DIRETORIO_ASSETS, 'eliminacao.wav'))
        self.som_eliminacao.set_volume(0.5)

        # self.som_jingle1 = pygame.mixer.Sound(path.join(DIRETORIO_ASSETS, 'jingle1.wav'))
        # self.som_jingle2 = pygame.mixer.Sound(path.join(DIRETORIO_ASSETS, 'jingle2.wav'))
        # enquanto nao tem os jingles, vai ser o erro
        self.som_jingle1 = pygame.mixer.Sound(path.join(DIRETORIO_ASSETS, 'risadas.wav'))
        self.som_jingle2 = pygame.mixer.Sound(path.join(DIRETORIO_ASSETS, 'ui.wav'))
        self.som_jingle3 = pygame.mixer.Sound(path.join(DIRETORIO_ASSETS, 'cavalo.wav'))
        self.som_jingle4 = pygame.mixer.Sound(path.join(DIRETORIO_ASSETS, 'ele-gosta.wav'))
        self.som_jingle5 = pygame.mixer.Sound(path.join(DIRETORIO_ASSETS, 'rapaz.wav'))
        self.som_jingle6 = pygame.mixer.Sound(path.join(DIRETORIO_ASSETS, 'dilicia.wav'))

        self.channel_jingle1: Optional[pygame.mixer.Channel] = None
        self.channel_jingle2: Optional[pygame.mixer.Channel] = None
        self.channel_jingle3: Optional[pygame.mixer.Channel] = None
        self.channel_jingle4: Optional[pygame.mixer.Channel] = None
        self.channel_jingle5: Optional[pygame.mixer.Channel] = None
        self.channel_jingle6: Optional[pygame.mixer.Channel] = None

        self.comprimento_marcacao = -1
        self.altura_marcacao = -1

        self._update_dimensions()

        self.countdown_enable = False    # para o timer
        self.countdown_timer: int = 0
        self.font = pygame.font.SysFont('arial', 80, True)
        self.evento_timer = pygame.USEREVENT + 1 + quantidade_x
        self.countdown_max = countdown_max

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

        self.fundo = pygame.transform.scale(
            self.fundo_original, (self.comprimento, self.altura)
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

    def draw_timer(self):
        if not self.countdown_enable:
            return

        t = abs(self.countdown_timer)
        tempo = f'{"-" if self.countdown_timer < 0 else ""}{t // 60:02d}:{t % 60:02d}'
        surface = self.font.render(tempo, False, WHITE if self.countdown_timer > 0 else RED)
        rect = surface.get_rect()
        rect.x = (self.comprimento - rect.w) // 2
        rect.y = self.altura // 10 * 8

        self.tela.blit(surface, rect)
    
    def check_busy(self):
        busies = [
            not (self.channel_jingle1 is not None and self.channel_jingle1.get_busy()),
            not (self.channel_jingle2 is not None and self.channel_jingle2.get_busy()),
            not (self.channel_jingle3 is not None and self.channel_jingle3.get_busy()),
            not (self.channel_jingle4 is not None and self.channel_jingle4.get_busy()),
            not (self.channel_jingle5 is not None and self.channel_jingle5.get_busy()),
            not (self.channel_jingle6 is not None and self.channel_jingle6.get_busy()),
        ]
        return any(busies)
        

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
            # parando timer
            self.countdown_enable = False
            pygame.time.set_timer(pygame.event.Event(self.evento_timer), millis=0)

        elif msg == Mensagem.JINGLE1:
            # if not (self.channel_jingle1 is not None and self.channel_jingle1.get_busy()):
            self.channel_jingle1 = self.som_jingle1.play(fade_ms=100)

        elif msg == Mensagem.JINGLE2:
            # if not (self.channel_jingle2 is not None and self.channel_jingle2.get_busy()):
            self.channel_jingle2 = self.som_jingle2.play(fade_ms=100)
        
        elif msg == Mensagem.JINGLE3:
            # if not (self.channel_jingle3 is not None and self.channel_jingle3.get_busy()):
            self.channel_jingle3 = self.som_jingle3.play(fade_ms=100)
        
        elif msg == Mensagem.JINGLE4:
            # if not (self.channel_jingle4 is not None and self.channel_jingle4.get_busy()):
            self.channel_jingle4 = self.som_jingle4.play(fade_ms=100)
        
        elif msg == Mensagem.JINGLE5:
            # if not (self.channel_jingle5 is not None and self.channel_jingle5.get_busy()):
            self.channel_jingle5 = self.som_jingle5.play(fade_ms=100)
        
        elif msg == Mensagem.JINGLE6:
            # if not (self.channel_jingle6 is not None and self.channel_jingle6.get_busy()):
            self.channel_jingle6 = self.som_jingle6.play(fade_ms=100)
                
        elif msg == Mensagem.COUNTDOWN:
            # zerando countdown
            self.countdown_timer = self.countdown_max
            pygame.time.set_timer(
                pygame.event.Event(
                    self.evento_timer
                ),
                millis=1000,
                loops=0     # pra sempre
            )

            self.countdown_enable = True

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

                if hasattr(event, 'key') and event.key == pygame.K_F11:
                    if self.tela_cheia:
                        self.tela = pygame.display.set_mode(
                            (self.comprimento, self.altura), pygame.RESIZABLE
                        )
                    else:
                        self.tela = pygame.display.set_mode(
                            (0, 0), pygame.FULLSCREEN | pygame.RESIZABLE
                        )
                    self.comprimento, self.altura = self.tela.get_size()
                    self._update_dimensions()
                    self.tela_cheia = not self.tela_cheia

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

            # countdown
            elif event.type == self.evento_timer and self.running:
                self.countdown_timer -= 1

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

        self.draw_timer()

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
