import os
from importlib import reload
from multiprocessing import Process
import time

from dispatcher import run_pooling

PATH = "."  # The path to watch
WAIT = 10  # How often we check the filesystem for changes (in seconds)


def write_mtimes(data):
    with open('mtimes.txt', 'a') as f:
        f.write(f"{data}\n")


def file_times(path):
    for top_level in filter(lambda name: (not name.startswith(".")), os.listdir(path)):
        for root, dirs, files in os.walk(top_level):
            for file in filter(lambda name: (not name.startswith(".")) and (name.endswith(".py")), files):
                print(file)
                if file == "dispatcher.py":
                    write_mtimes(str(os.stat(os.path.join(root, file)).st_mtime))
                yield os.stat(os.path.join(root, file)).st_mtime


def start_pooling():
    p = Process(target=run_pooling, daemon=True)
    p.start()
    return p


if __name__ == '__main__':
    # The process to autoreload
    process = start_pooling()

    # The current maximum file modified time under the watched directory
    last_mtime = max(file_times(PATH))

    while True:
        max_mtime = max(file_times(PATH))
        if max_mtime > last_mtime:
            last_mtime = max_mtime
            print("Changes discovered. Restarting process.")
            process.terminate()
            process.close()
            process = start_pooling()
        time.sleep(WAIT)
