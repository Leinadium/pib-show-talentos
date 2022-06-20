import os
import signal
from flask import Flask, render_template, redirect
from threading import Lock

from .conexao import Conexao

from typing import Optional

app = Flask(__name__)


class Contador:
    q = 0
    lock = Lock()
    conexao: Optional[Conexao] = None

    @classmethod
    def start(cls, host, port):
        Conexao.config(host, port)
        cls.conexao = Conexao()

    @classmethod
    def increment(cls):
        with cls.lock:
            cls.q += 1
            cls.conexao.enviar_eliminacao()
        return

    @classmethod
    def reset(cls):
        with cls.lock:
            cls.q = 0
            cls.conexao.enviar_reset()
        return

    @classmethod
    def get(cls) -> int:
        return cls.q

    @classmethod
    def jingle(cls, x: int):
        # meio feio ficar aqui no Contador, mas é onde tem a conexao
        cls.conexao.enviar_jingle(x)
        return

    @classmethod
    def countdown(cls):
        # mesma coisa feia do metodo acima...
        cls.conexao.enviar_countdown()
        return


@app.route('/')
def index():
    return render_template('index.html', pressed=False)


@app.route('/x')
def press():
    Contador.increment()
    return render_template('index.html', pressed=True)


@app.route('/update')
def update():
    return {'contador': Contador.get()}


@app.route('/reset')
def reset():
    # sempre reseta, para tbm parar os sons caso estejam tocando
    Contador.reset()

    return redirect('/')


@app.route('/jingle/<int:x>')
def jingle(x: int):
    Contador.jingle(x)
    return ':D'


@app.route('/countdown')
def countdown():
    Contador.countdown()
    return ':DD'


@app.route('/end')
def end():
    os.kill(os.getpid(), signal.SIGINT)     # se fecha
    return 'shutting down'


if __name__ == "__main__":
    Contador.start('localhost', 4474)
    app.run(host='0.0.0.0', port=5000, debug=False)
