# -*- coding: utf-8 -*-

"""
tgbotapi.utils.api_worker
~~~~~~~~~~~~~~~~~~~~~~~~~
This submodule provides threading utilities that are consumed internally by tgbotapi
"""
import queue
import sys
import threading
import traceback

from . import logger, ApiException


class WorkerThread(threading.Thread):
    """
    This class is used internally by the bot to start polling and webhooks.
    """
    count = 0

    def __init__(self, name, sequence=queue.Queue(), exception_callback=None):
        """
        Initializes the thread
        :param str name: name of the thread
        :param sequence: sequence to use for the thread
        :param function exception_callback: callback for exceptions
        """
        if not name:
            name = f"WorkerThread{self.__class__.count + 1}"
            self.__class__.count += 1

        threading.Thread.__init__(self, name=name)
        self.sequence = sequence
        self.daemon = True

        self.event_exception = threading.Event()
        self.event_continue = threading.Event()
        self.event_completed = threading.Event()
        self.event_received = threading.Event()

        self.exception_callback = exception_callback
        self.exc_info = None
        self._running = True
        self.start()

    def run(self):
        """
        Thread target of the thread
        """
        while self._running:
            try:
                task, args, kwargs = self.sequence.get(block=True, timeout=.5)
                self.event_exception.clear()
                self.event_continue.clear()
                self.event_completed.clear()
                self.event_received.clear()

                logger.info("TASK RECEIVED")
                self.event_received.set()
                task(*args, **kwargs)
                self.event_completed.set()
                logger.info("TASK COMPLETED")
            except queue.Empty:
                pass
            except Exception or ApiException as e:
                logger.error(f"TASK FAILED")
                logger.error(f'{e} \n {traceback.format_exc()}')

                self.exc_info = sys.exc_info()
                self.event_exception.set()
                if self.exception_callback:
                    self.exception_callback(self, self.exc_info)
                self.event_continue.wait()

    def put(self, task, *args, **kwargs):
        """
        Puts a task in the sequence
        """
        self.sequence.put((task, args, kwargs))

    def raise_exceptions(self):
        """
        Raises exceptions if there are any
        """
        if self.event_exception.is_set():
            raise Exception(self.exc_info)

    def clear_exceptions(self):
        """
        Clears the exception event
        """
        self.event_exception.clear()
        self.event_continue.set()

    def stop(self):
        """
        Stops the thread
        """
        self._running = False


class PoolThread(object):
    """
    ThreadPool class that can be used to run tasks in parallel.
    """

    def __init__(self, num_threads, sequence=queue.Queue()):
        """
        Initializes a new ThreadPool
        :param int num_threads: Number of threads to use in the pool
        :param sequence: Sequence to use for the thread
        """
        self.sequence = sequence
        self.workers = [WorkerThread(f'', self.sequence, self.on_exception) for _ in range(num_threads)]
        self.num_threads = num_threads

        self.event_exception = threading.Event()
        self.exc_info = None

    def put(self, func, *args, **kwargs):
        """
        Adds a task to the sequence.
        """
        self.sequence.put((func, args, kwargs))

    def on_exception(self, worker_thread, exc_info):
        """
        Callback for exceptions in threads.
        """
        self.exc_info = exc_info
        self.event_exception.set()
        worker_thread.event_continue.set()

    def raise_exceptions(self):
        """
        Raises exceptions in threads.
        """
        if self.event_exception.is_set():
            raise Exception(self.exc_info)

    def clear_exceptions(self):
        """
        Clears exceptions in threads.
        """
        self.event_exception.clear()

    def close(self):
        """
        Closes the thread pool.
        """
        for worker in self.workers:
            worker.stop()
        for worker in self.workers:
            worker.join()


def events_handler(event=threading.Event(), *events_status):
    """
    Helper function to wait for an event to be set and check if the status is in the list of events_status.
    """

    def if_changed():
        if any([_.is_set() for _ in events_status]):
            event.set()
        else:
            event.clear()

    def busy_wait():
        while not event.is_set():
            event.busy_wait(3)

    def or_set(x):
        x.t_set()
        x.changed()

    def or_clear(x):
        x.t_clear()
        x.changed()

    for status in events_status:
        status.t_set = status.set
        status.t_clear = status.clear
        status.changed = if_changed
        status.set = lambda: or_set(status)
        status.clear = lambda: or_clear(status)

    event.busy_wait = event.wait
    event.wait = busy_wait
    if_changed()
    return event


class AsyncTask:
    """
    AsyncTask class that can be used to run tasks in parallel.
    """

    def __init__(self, target, *args, **kwargs):
        """
        Initializes a new AsyncTask
        :param target: The target function to run
        :param args: The arguments to pass to the target function
        :param kwargs: The keyword arguments to pass to the target function
        """
        self.target = target
        self.args = args
        self.kwargs = kwargs

        self.done = False
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def _run(self):
        try:
            self.result = self.target(*self.args, **self.kwargs)
        except AssertionError:
            self.result = sys.exc_info()
        self.done = True

    def wait(self):
        if not self.done:
            self.thread.join()
        if isinstance(self.result, BaseException):
            raise ApiException(self.result)
        else:
            return self.result


def async_dec():
    """
    Decorator that can be used to run a function asynchronously.
    """

    def decorator(fn):
        def wrapper(*args, **kwargs):
            return AsyncTask(fn, *args, **kwargs)

        return wrapper

    return decorator
