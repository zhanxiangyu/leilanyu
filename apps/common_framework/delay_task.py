import sched
import threading
import time


def new_task(function, delay_time, args):
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(delay_time, 10, function, args)
    thread = threading.Thread(target=scheduler.run)
    thread.start()

    return thread
