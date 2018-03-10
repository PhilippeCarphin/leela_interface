from src.leela import LeelaInterface


if __name__ == "__main__":

    opencl = input("use opencl ? [y/n] ")
    if opencl == 'y':
        leela_binary += '_opencl'


    leels = LeelaInterface('./bin/leela_0110_linux_x64')
    while True:
        cmd = input("command for leela > ")
        if cmd == 'quit':
            print('to quit just press CTRL-C a bunch of times')
            continue
        leela_answer, leela_stderr = leels.ask(cmd)
        print("LeelaInterface : leela_answer : " + leela_answer)
        print("LeelaInterface : leela_stderr : " + leela_stderr)

