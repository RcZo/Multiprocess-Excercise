import random
import time
from multiprocessing import Manager, Process
import logging

def get_stream_logger(level=logging.DEBUG):
    """Return logger with configured StreamHandler."""
    stream_logger = logging.getLogger('stream_logger')
    stream_logger.handlers = []
    stream_logger.setLevel(level)
    sh = logging.StreamHandler()
    sh.setLevel(level)
    fmt = '[%(asctime)s %(processName)s] --- %(message)s'
    formatter = logging.Formatter(fmt)
    sh.setFormatter(formatter)
    stream_logger.addHandler(sh)

    return stream_logger


def calculate_pi():
    k = 1
    s = 0
    for i in range(100000000):
        if i % 2 == 0:
            s += 4 / k
        else:
            s -= 4 / k
        k += 2
    return


def save_data(save_que, file_):
    stream_logger = get_stream_logger()
    for data in iter(save_que.get, 'STOP'):
        stream_logger.debug(f"saving: {data}...")  # DEBUG
        # If you want to monitor your cpu cores...
        # calculate_pi()
        time.sleep(random.randint(3, 4))  # random delay
        stream_logger.debug(f"saving: {data} completed.")  # DEBUG
    stream_logger.debug("Queue is empty.")  # DEBUG
    return


def produce_data(save_que, n_workers):
    stream_logger = get_stream_logger()
    for _ in range(10):
        time.sleep(random.randint(0, 1))
        data = random.randint(100, 200)
        stream_logger.debug(f"producing: {data}")  # DEBUG
        save_que.put(data)

    for _ in range(n_workers):
        save_que.put("STOP")


if __name__ == '__main__':

    file_ = "file"
    n_processes = 3 

    manager = Manager()
    save_que = manager.Queue()

    processes = []
    for _ in range(n_processes):
        processes.append(Process(target=save_data, args=(save_que, file_)))

    for p in processes:
        p.start()

    produce_data(save_que, n_workers=n_processes)

    for p in processes:
        p.join()
