#!/bin/python3
import subprocess
import threading
from queue import Queue
import time

leela_binary = './bin/leela_0110_linux_x64'

stderr = ''

queue = Queue()

class PipeListenerThread(threading.Thread):
    def __init__(self, pipe, output):
        threading.Thread.__init__(self)
        self.pipe = pipe
        self.output_queue = queue
    def run(self):
        global stderr
        while True:
            line = self.pipe.readline()
            self.output_queue.put(line)


class LeelaInterface(object):
    def __init__(self):
        self._leela = subprocess.Popen([leela_binary, '-g'], stdout=subprocess.PIPE,
        stdin=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
        self.stderr = ''
        self._stderrListener = PipeListenerThread(self._leela.stderr, queue)
        self._stderrListener.start()
        print("Starting leela")
        print(queue.get().strip())
        print(queue.get().strip())

    def get_stderr(self):
        self.stderr = ''
        while not queue.empty():
            self.stderr += queue.get()

    def ask(self, cmd):
        self.stderr = ''
        self._leela.stdin.write(cmd + '\n')
        answer = self._leela.stdout.readline()
        self._leela.stdout.readline()
        self.get_stderr()

        return answer, self.stderr


leels = LeelaInterface()

while True:
    cmd = input("command for leela > ")
    leela_answer, leela_stderr = leels.ask(cmd)
    print("leela_answer = " + leela_answer)
    print("leela_stderr = " + leela_stderr)

