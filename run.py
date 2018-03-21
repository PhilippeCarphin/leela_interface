#!/usr/local/bin/python3
from src.gtpwrapper import GTPWrapper
import time
import signal
import os

gnugo_cmd = ['gnugo', '--mode', 'gtp']

leelaz_cmd = ['leelaz', '-g', '-w', './src/leelaz-model-5309030-128000.txt']

if __name__ == "__main__":

    leels = GTPWrapper(leelaz_cmd)
    def stop():
        leels.quit()
        quit(0)
    signal.signal(signal.SIGINT, lambda a,b: stop())

    time.sleep(.5)
    initial_msg = leels.get_stderr()
    # print(initial_msg)
    while True:
        cmd = input("command for leela > ")
        if cmd == 'quit':
            stop()
        leels.ask(cmd)
        leela_answer = leels.get_stdout()
        leela_stderr = leels.get_stderr()
        print("LeelaInterface : leela_answer : " + leela_answer)
        print("LeelaInterface : leela_stderr : " + leela_stderr)

