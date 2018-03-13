#!/usr/local/bin/python3
from src.leela import LeelaInterface


if __name__ == "__main__":

    leels = LeelaInterface()
    while True:
        cmd = input("command for leela > ")
        if cmd == 'quit':
            print('to quit just press CTRL-C a bunch of times')
            continue
        leela_answer, leela_stderr = leels.ask(cmd)
        print("LeelaInterface : leela_answer : " + leela_answer)
        print("LeelaInterface : leela_stderr : " + leela_stderr)

