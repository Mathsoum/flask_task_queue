import datetime
import locale
import os
import threading
import subprocess

from app import full_task_list
from config import Config


class Task:
    next_task_id = 0

    CMD_OUTPUT_HEADER = """\
==================================================
===
=== Command           : {command}
=== Date of execution : {date}
=== Status            : {status}
===
==================================================

"""
    CMD_OUTPUT_FOOTER = """

==================================================
===
=== EOF
===
=================================================="""

    CMD_STDOUT_FILE_NAME = 'cmd_%d_out.txt'

    def __init__(self, command):
        self.command = command
        self.status = 'Waiting'
        self.done = False
        self.id = Task.next_task_id + 1
        self.pid = 0
        self.log_file = ''
        self.success = False
        self.stdout_file_name = Task.CMD_STDOUT_FILE_NAME % self.id
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
        file = os.path.join(Config.COMMAND_OUTPUT_DIR, self.stdout_file_name)
        with open(file, 'w', encoding="utf-8") as stdout_fd:
            process = None
            exception_output = ''
            try:
                process = subprocess.run([self.command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                exit_code = process.returncode
            except subprocess.SubprocessError as ex:
                exception_output = 'Exception occurred during the execution of the command [%s]\n%s' % (self.command,
                                                                                                        str(ex))
                exit_code = 1

            self.terminate(exit_code == 0)

            header_dict = {'command': self.command, 'date': str(datetime.datetime.now()), 'status': self.status}
            stdout_fd.write(Task.CMD_OUTPUT_HEADER.format(**header_dict))
            if process is not None:
                stdout_fd.write(str(process.stdout, encoding=locale.getpreferredencoding()))
            else:
                stdout_fd.write(exception_output)

            stdout_fd.write(Task.CMD_OUTPUT_FOOTER)


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
