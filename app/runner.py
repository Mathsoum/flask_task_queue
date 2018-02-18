import datetime
import locale
import os
import threading
import subprocess

from app import full_task_list
from config import COMMAND_OUTPUT_DIR


class Task:
    next_task_id = 0

    CMD_OUTPUT_HEADER = """\
==================================================
===
=== Command           : {command}
=== Date of execution : {date}
=== File type         : {file_type}
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
    CMD_STDERR_FILE_NAME = 'cmd_%d_err.txt'

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
        cmd_stdout_path = os.path.join(COMMAND_OUTPUT_DIR, Task.CMD_STDOUT_FILE_NAME % self.id)
        cmd_stderr_path = os.path.join(COMMAND_OUTPUT_DIR, Task.CMD_STDERR_FILE_NAME % self.id)
        with open(cmd_stdout_path, 'w', encoding=locale.getpreferredencoding()) as stdout_fd:
            with open(cmd_stderr_path, 'w', encoding=locale.getpreferredencoding()) as stderr_fd:
                header_dict = {'command': self.command, 'date': str(datetime.datetime.now())}
                header_dict.update({'file_type': 'STDOUT'})
                stdout_fd.write(Task.CMD_OUTPUT_HEADER.format(**header_dict))
                header_dict.update({'file_type': 'STDERR'})
                stderr_fd.write(Task.CMD_OUTPUT_HEADER.format(**header_dict))

                try:
                    process = subprocess.run([self.command], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                             encoding=locale.getpreferredencoding(), shell=True)
                    stdout_fd.write(process.stdout)
                    stderr_fd.write(process.stderr)
                    exit_code = process.returncode
                except subprocess.SubprocessError as ex:
                    stderr_fd.write('Exception occurred during the execution of the command [%s]\n' % self.command)
                    stderr_fd.write(str(ex))
                    exit_code = 1

                stdout_fd.write(Task.CMD_OUTPUT_FOOTER)
                stderr_fd.write(Task.CMD_OUTPUT_FOOTER)

        self.terminate(exit_code == 0)


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
