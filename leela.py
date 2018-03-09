#!/bin/python3
import subprocess
import time

p = subprocess.Popen(['./bin/leela_0110_linux_x64'], stdout=subprocess.PIPE,
        stdin=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=69, universal_newlines=True)

while True:
    cmd = input("command for leela > ")
    p.stdin.write(cmd + '\n')
    leela_answer = p.stdout.readline()

    #Have to read an extra line to consume an empty line
    garbage = p.stdout.readline()

    print("leela_answer = " + leela_answer)

