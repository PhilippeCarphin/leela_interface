#!/bin/python3
import subprocess
import time

class LeelaInterface(object):
    def __init__(self):
        self._leela = subprocess.Popen(['./bin/leela_0110_linux_x64', '-g'], stdout=subprocess.PIPE,
        stdin=subprocess.PIPE, bufsize=1, universal_newlines=True)

    def ask(self, cmd):
        self._leela.stdin.write(cmd + '\n')
        answer = self._leela.stdout.readline()
        #Have to read an extra line to consume an empty line
        self._leela.stdout.readline()

        return answer


leels = LeelaInterface()

while True:
    cmd = input("command for leela > ")
    leela_answer = leels.ask(cmd)
    print("leela_answer = " + leela_answer)

