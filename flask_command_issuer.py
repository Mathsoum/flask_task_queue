from flask import Flask
import queue
import threading
import time

app = Flask(__name__)
tasks = queue.Queue()
task_count = 0


class Runner(threading.Thread):
    def __init__(self, local_queue):
        threading.Thread.__init__(self)
        self.queue = local_queue

    def run(self):
        while True:
            msg = self.queue.get()

            for sec in range(10, 0, -1):
                print('%s : %ds' % (msg, sec))
                time.sleep(1)

            self.queue.task_done()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/add')
def add_task():
    global task_count
    tasks.put('Task #%d' % task_count)
    task_count += 1
    return "New task added"


if __name__ == '__main__':
    t = Runner(tasks)
    t.setDaemon(True)
    t.start()

    app.run()
