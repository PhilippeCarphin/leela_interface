from multiprocessing import Process
import os

def f(name):
    os.execvp('sh', ['$0-here', './script.sh'])

def g(name):
    os.execvp('./bin/leela_0110_linux_x64', ['./script.sh hello ' + name])

if __name__ == '__main__':

    q = Process(target=f, args=('bob',))
    p = Process(target=g, args=('patate',))

    q.start()

    q.join()

    p.start()

    p.join()

