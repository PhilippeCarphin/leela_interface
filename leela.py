from subprocess import Popen, PIPE

engine = Popen(['./leela_0110_linux_x64', '-g'], stdout=PIPE, stderr=PIPE, stdin=PIPE)


stdout, stderr = engine.communicate(b'play black C4')
stdout, stderr = engine.communicate(b'play white C5')

print(stdout)
print(stderr)
engine.wait()

