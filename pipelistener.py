import threading

'''
Fills a queue with lines read from a pipe
'''

class PipeListener(threading.Thread):
    def __init__(self, input_pipe, output_queue):
        threading.Thread.__init__(self)
        self.input_pipe = input_pipe
        self.output_queue = output_queue

    def run(self):
        while True:
            line = self.input_pipe.readline()
            self.output_queue.put(line)

    def get_content(self):
        pipecontent = ''
        while not self.output_queue.empty():
            pipecontent += self.output_queue.get()
        return pipecontent


