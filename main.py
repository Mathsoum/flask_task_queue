from app import tasks, app
from app.runner import Runner

if __name__ == '__main__':
    t = Runner(tasks)
    t.setDaemon(True)
    t.start()

    app.run()
