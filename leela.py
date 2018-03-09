#!/bin/python3
import subprocess
import time

p = subprocess.Popen(['./bin/leela_0110_linux_x64'], stdout=subprocess.PIPE,
        stdin=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=69, universal_newlines=True)

p.stdin.write('play white g4\n')
p.stdin.write('genmove white\n')
p.stdin.write('genmove black\n')
p.stdin.write('genmove white\n')
p.stdin.write('genmove white\n')
out1 = p.stdout.readline()
print("out1 = " + out1)
p.stdin.write('genmove black\n')


out2 = p.stdout.readline()
out3 = p.stderr.readline()



print("out2 = " + out2)
print("out3 = " + out3)
