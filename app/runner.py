import threading

import time

from app import full_task_list


class Task:
    next_task_id = 0

    def __init__(self, msg):
        self.msg = msg
        self.status = 'Waiting'
        self.id = Task.next_task_id + 1
        Task.next_task_id += 1
        full_task_list.append(self)

    def start(self):
        for sec in range(10, 0, -1):
            print('Task #%d -- %s : %ds' % (self.id, self.msg, sec))
            time.sleep(1)


class Runner(threading.Thread):
    def __init__(self, local_queue):
        threading.Thread.__init__(self)
        self.queue = local_queue

    def run(self):
        while True:
            task = self.queue.get()
            task.status = 'Running'
            task.start()
            self.queue.task_done()
            task.status = 'Done !'
