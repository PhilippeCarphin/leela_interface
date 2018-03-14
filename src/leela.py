#!/bin/python3
import subprocess
from queue import Queue
import time
import os

from .pipelistener import PipeListener

leela_cmd = [os.path.join(os.getcwd(),'bin', 'leela_0110_linux_x64'), '-g']

gnugo_cmd = ['gnugo', '--mode', 'gtp']

leelaz_cmd = ['leelaz', '-g', '-w', './src/leelaz-model-5309030-128000.txt']

'''
Interface LeelaInterface:  une instance de LeelaInterface encapsule
une instance réelle du programme de go Leela avec des pipe Unix pour
écrire à son stdin et lire de son stdout et son stderr.

La classe a la méthode ask(cmd) qui permet d'envoyer une commande à
leela via son stdin, et récupère le output principal de son stdout
le output secondaire via son stderr.

La fonction retourne un tuple (contenu de stdout, contenu de stderr)

NOTE: <pipe>.readline() est un appel bloquant il faut donc utiliser
un thread séparé pour lire un nombre inconnu de lignes de stderr.

Leela output 2 lignes exactement sur STDOUT pour chaque commande.
on peut donc faire deux readline() par commande on sait qu'après ces
deux getline, le coup est fini.  C'est ce que la fonction ask() fait.

Pour le output sur STDERR, c'est plus compliqué parce qu'on ne sait
pas combien de readline() faire.  C'est la raison pour stderr_queue
et PipeListenerThread.  De façon asynchrone, les lignes lues de stderr
sont mises dans stderr_queue.

Le main thread peut donc "vider stderr" de façon non-bloquante.
'''

class LeelaInterface(object):
    def __init__(self, engine_cmd=leelaz_cmd, stdout_queue=None,
            stderr_queue=None):
        print("===Python : LeelaInterface : Starting leela ===")
        self._leela = subprocess.Popen(
                engine_cmd,
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1,
                universal_newlines=True
            )
        self.stdout_queue = stdout_queue if stdout_queue is not None else Queue()
        self._stdout_listener = PipeListener(
                input_pipe=self._leela.stdout,
                output_queue=self.stdout_queue
            )
        self._stdout_listener.start()

        self.stderr_queue = stderr_queue if stderr_queue is not None else Queue()
        self._stderr_listener = PipeListener(
                input_pipe=self._leela.stderr,
                output_queue=self.stderr_queue
            )
        self._stderr_listener.start()

    def get_stderr(self):
        return self._stderr_listener.get_content()
    def get_stdout(self):
        stdout = ''
        stdout += self.stdout_queue.get()
        self.stdout_queue.get()
        return stdout

    def ask(self, cmd):
        self._leela.stdin.write(cmd + '\n')

    def quit(self):
        self.ask('quit')
        self._stderr_listener.stop()
        self._stdout_listener.stop()
        outs, errs = self._leela.communicate()
