#!/bin/python3
import subprocess
from queue import Queue
import time

from .pipelistener import PipeListener


'''
Interface EngineInterface:  une instance de EngineInterface encapsule
une instance réelle du programme de go Engine avec des pipe Unix pour
écrire à son stdin et lire de son stdout et son stderr.

La classe a la méthode ask(cmd) qui permet d'envoyer une commande au
engine via son stdin, et récupère le output principal de son stdout
le output secondaire via son stderr.

La fonction retourne un tuple (contenu de stdout, contenu de stderr)

NOTE: <pipe>.readline() est un appel bloquant il faut donc utiliser
un thread séparé pour lire un nombre inconnu de lignes de stderr.

Engine output 2 lignes exactement sur STDOUT pour chaque commande.
on peut donc faire deux readline() par commande on sait qu'après ces
deux getline, le coup est fini.  C'est ce que la fonction ask() fait.

Pour le output sur STDERR, c'est plus compliqué parce qu'on ne sait
pas combien de readline() faire.  C'est la raison pour stderr_queue
et PipeListenerThread.  De façon asynchrone, les lignes lues de stderr
sont mises dans stderr_queue.

Le main thread peut donc "vider stderr" de façon non-bloquante.
'''

class EngineInterface(object):
    def __init__(self, engine_cmd, stdout_queue=None, stderr_queue=None):
        print("===Python : EngineInterface : Starting {} ===".format(engine_cmd[0]))
        self._engine = subprocess.Popen(
                engine_cmd,
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1,
                universal_newlines=True
            )
        self.stdout_queue = stdout_queue if stdout_queue is not None else Queue()
        self._stdout_listener = PipeListener(
                input_pipe=self._engine.stdout,
                output_queue=self.stdout_queue
            )
        self._stdout_listener.start()

        self.stderr_queue = stderr_queue if stderr_queue is not None else Queue()
        self._stderr_listener = PipeListener(
                input_pipe=self._engine.stderr,
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
        self._engine.stdin.write(cmd + '\n')

    def quit(self):
        self.ask('quit')
        self._stderr_listener.stop()
        self._stdout_listener.stop()
        outs, errs = self._engine.communicate()

    def kill(self):
        self._engine.kill()
        self._stderr_listener.stop()
        self._stdout_listener.stop()
        outs, errs = self._engine.communicate()
