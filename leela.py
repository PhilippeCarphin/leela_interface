#!/bin/python3
import subprocess
from queue import Queue
from pipelistener import PipeListener
import time

leela_binary = './bin/leela_0110_linux_x64'

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
    def __init__(self):
        print("===Python : LeelaInterface : Starting leela ===")
        self._leela = subprocess.Popen(
                [leela_binary, '-g'],
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1,
                universal_newlines=True
            )
        self.stderr_queue = Queue()
        self._stderr_listener = PipeListener(
                input_pipe=self._leela.stderr,
                output_queue=self.stderr_queue
            )
        self._stderr_listener.start()
        print(self.stderr_queue.get().strip())
        print(self.stderr_queue.get().strip())

    def get_stderr(self):
        return self._stderr_listener.get_content()
    def get_stdout(self):
        stdout = ''
        stdout += self._leela.stdout.readline()
        self._leela.stdout.readline()
        return stdout

    def ask(self, cmd):
        self._leela.stdin.write(cmd + '\n')

        answer = self.get_stdout()

        # Sometimes I do showboard and leela outputs two lines faster then it
        # outputs the board.  So the function ask finishes before anything has
        # time to make it into the queue.  The output of showboard will be seen
        # after the next command.  That is why there is a .1 second delay here.
        time.sleep(0.1)
        return answer, self.get_stderr()


if __name__ == "__main__":

    opencl = input("use opencl ? [y/n] ")
    if opencl == 'y':
        leela_binary += '_opencl'


    leels = LeelaInterface()
    while True:
        cmd = input("command for leela > ")
        if cmd == 'quit':
            print('to quit just press CTRL-C a bunch of times')
            continue
        leela_answer, leela_stderr = leels.ask(cmd)
        print("LeelaInterface : leela_answer : " + leela_answer)
        print("LeelaInterface : leela_stderr : " + leela_stderr)

