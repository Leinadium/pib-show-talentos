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
    if Contador.get() > 0:
        Contador.reset()

    return redirect('/')


@app.route('/end')
def end():
    os.kill(os.getpid(), signal.SIGINT)     # se fecha
    return 'shutting down'


if __name__ == "__main__":
    Contador.start('localhost', 4474)
    app.run(host='0.0.0.0', port=5000, debug=False)
