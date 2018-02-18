import os
import random
import threading
import subprocess

import time

from app import full_task_list
from config import COMMAND_OUTPUT_DIR


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
        cmd_stdout_path = os.path.join(COMMAND_OUTPUT_DIR, 'cmd_%d_out.txt' % self.id)
        cmd_stderr_path = os.path.join(COMMAND_OUTPUT_DIR, 'cmd_%d_err.txt' % self.id)
        with open(cmd_stdout_path, 'w') as stdout_fd:
            with open(cmd_stderr_path, 'w') as stderr_fd:
                try:
                    process = subprocess.run([self.command], stdout=stdout_fd, stderr=stderr_fd, shell=True)
                    exit_code = process.returncode
                except subprocess.SubprocessError as ex:
                    stderr_fd.write('Exception occurred during the execution of the command [%s]\n' % self.command)
                    stderr_fd.write(str(ex))
                    exit_code = 1

            self.terminate(exit_code == 0)
            print('Exit code : %d' % exit_code)
            print('Command output available here : %s' % cmd_stdout_path)


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
