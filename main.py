from visualizacao.view import View
from web.app import app, Contador
# from web.conexao import Conexao as ConexaoWeb

from threading import Thread
import requests

if __name__ == "__main__":
    host_servidor = '0.0.0.0'
    host_client = 'localhost'
    port = 4474
    flask_port = 5000

    # preparando pygame
    view = View(4, 60 * 3)
    view.server_start()

    # iniciando flask
    Contador.start(host_client, port)
    thread_flask = Thread(
        target=app.run,
        kwargs={
            'host': '0.0.0.0',
            'port': flask_port,
            'debug': False
        }
    )
    thread_flask.start()

    # loop pygame
    view.loop()
    print("fechando tudo!")

    # fechando
    # para matar o site, precisa enviar um /end
    _r = requests.get(f'http://127.0.0.1:{flask_port}/end')

    thread_flask.join()
