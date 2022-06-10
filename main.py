from visualizacao.view import View
from web.app import app
from web.conexao import Conexao as ConexaoWeb

from threading import Thread

if __name__ == "__main__":

    host = '0.0.0.0'
    port = 4474

    # preparando pygame
    view = View(3)
    thread_pygame = Thread(target=view.loop)

    # configurando conexao do flask
    ConexaoWeb.config(host, port)
    thread_flask = Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000, 'debug': True})

    # iniciando tudo
    thread_pygame.start()
    thread_flask.start()