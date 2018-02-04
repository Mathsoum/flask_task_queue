import random
import threading
import subprocess

import time

from app import full_task_list


class Task:
    next_task_id = 0

    def __init__(self, command):
        self.command = command
        self.status = 'Waiting'
        self.done = False
        self.id = Task.next_task_id + 1
        self.pid = 0
        self.log_file = ''
        self.success = False
        Task.next_task_id += 1
        full_task_list.append(self)

    def success(self):
        return self.status == 'Done !' and self.success

    def terminate(self, success):
        self.done = True
        self.success = success
        if success:
            self.status = 'OK'
        else:
            self.status = 'KO'

    def start(self):
        for sec in range(10, 0, -1):
            with open('cmd_output_%d.txt' % self.id, 'a') as output_fd:
                exit_code = subprocess.call(['dir'], stdout=output_fd, shell=True)
                print('Exit code : %d' % exit_code)
                print('Task #%d -- %s : %ds' % (self.id, self.command, sec))
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
            task.terminate(random.choice([True, False]))
