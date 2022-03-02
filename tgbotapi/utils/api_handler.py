from .logger import logger
from .api_exceptions import ApiException
import queue as q
import threading
import traceback
import requests
import sys
import six

thread_local = threading.local()


class WorkerThread(threading.Thread):
    count = 0

    def __init__(self, exception_callback=None, queue=None, name=None):
        if not name:
            name = f"WorkerThread{self.__class__.count + 1}"
            self.__class__.count += 1
        if not queue:
            queue = q.Queue()

        threading.Thread.__init__(self, name=name)
        self.queue = queue
        self.daemon = True

        self.received_task_event = threading.Event()
        self.done_event = threading.Event()
        self.exception_event = threading.Event()
        self.continue_event = threading.Event()

        self.exception_callback = exception_callback
        self.exc_info = None
        self._running = True
        self.start()

    def run(self):
        while self._running:
            try:
                task, args, kwargs = self.queue.get(block=True, timeout=.5)
                self.continue_event.clear()
                self.received_task_event.clear()
                self.done_event.clear()
                self.exception_event.clear()

                logger.info("TASK RECEIVED")
                self.received_task_event.set()
                task(*args, **kwargs)
                self.done_event.set()
                logger.info("TASK COMPLETE")
            except q.Empty:
                pass
            except Exception as e:
                logger.error(type(e).__name__ + " OCCURRED, ARGS=" +
                             str(e.args) + "\n" + traceback.format_exc())
                self.exc_info = sys.exc_info()
                self.exception_event.set()

                if self.exception_callback:
                    self.exception_callback(self, self.exc_info)
                self.continue_event.wait()

    def put(self, task, *args, **kwargs):
        self.queue.put((task, args, kwargs))

    def raise_exceptions(self):
        if self.exception_event.is_set():
            six.reraise(self.exc_info[0], self.exc_info[1], self.exc_info[2])

    def clear_exceptions(self):
        self.exception_event.clear()
        self.continue_event.set()

    def stop(self):
        self._running = False


class ThreadPool:

    def __init__(self, num_threads=2):
        self.tasks = q.Queue()
        self.workers = [WorkerThread(self.on_exception, self.tasks)
                        for _ in range(num_threads)]
        self.num_threads = num_threads

        self.exception_event = threading.Event()
        self.exc_info = None

    def put(self, func, *args, **kwargs):
        self.tasks.put((func, args, kwargs))

    def on_exception(self, worker_thread, exc_info):
        self.exc_info = exc_info
        self.exception_event.set()
        worker_thread.continue_event.set()

    def raise_exceptions(self):
        if self.exception_event.is_set():
            six.reraise(self.exc_info[0], self.exc_info[1], self.exc_info[2])

    def clear_exceptions(self):
        self.exception_event.clear()

    def close(self):
        for worker in self.workers:
            worker.stop()
        for worker in self.workers:
            worker.join()


class AsyncTask:
    def __init__(self, target, *args, **kwargs):
        self.target = target
        self.args = args
        self.kwargs = kwargs

        self.done = False
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def _run(self):
        try:
            self.result = self.target(*self.args, **self.kwargs)
        except:
            self.result = sys.exc_info()
        self.done = True

    def wait(self):
        if not self.done:
            self.thread.join()
        if isinstance(self.result, BaseException):
            six.reraise(self.result[0], self.result[1], self.result[2])
        else:
            return self.result


def async_dec():
    def decorator(fn):
        def wrapper(*args, **kwargs):
            return AsyncTask(fn, *args, **kwargs)

        return wrapper

    return decorator


def or_set(self):
    self._set()
    self.changed()


def or_clear(self):
    self._clear()
    self.changed()


def orify(e, changed_callback):
    e._set = e.set
    e._clear = e.clear
    e.changed = changed_callback
    e.set = lambda: or_set(e)
    e.clear = lambda: or_clear(e)


def events_handler(*events):
    event = threading.Event()

    def changed():
        bools = [e.is_set() for e in events]
        if any(bools):
            event.set()
        else:
            event.clear()

    def busy_wait():
        while not event.is_set():
            event._wait(3)

    for e in events:
        orify(e, changed)
    event._wait = event.wait
    event.wait = busy_wait
    changed()
    return event


def per_thread(key, construct_value, reset=True):
    if reset or not hasattr(thread_local, key):
        value = construct_value()
        setattr(thread_local, key, value)

    return getattr(thread_local, key)


def get_req_session(reset=True):
    return per_thread('req_session', lambda: requests.session(), reset)


def make_request(method, api_url, api_method, files, params, proxies):
    """
    Makes a request to the Telegram API.
    """
    """
    :param str method: HTTP method ['get', 'post'].
    :param str api_url: telegram api url for api_method.
    :param str api_method: Name of the API method to be called. (E.g. 'getUpdates').
    :param any files: files content's a data.
    :param dict or None params: Should be a dictionary with key-value pairs.
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :return: JSON DICT FORMAT
    :rtype: dict
    """
    logger.info(f"{api_method}")
    logger.debug(f"{method.upper()} -> {api_url} {params} files={files}")
    timeout = 2.99
    if params:
        if 'timeout' in params:
            timeout = params['timeout'] + 10

    resp = get_req_session().request(method, api_url, params, data=None, headers=None, cookies=None, files=files,
                                     auth=None, timeout=timeout, allow_redirects=True, proxies=proxies, verify=None,
                                     stream=None, cert=None)
    logger.debug(f"The Server Returned: '{resp.text.encode('utf8')}'")
    if resp.status_code != 200:
        msg = f"The Server Returned HTTP {resp.status_code} {resp.reason}"
        raise ApiException(msg, api_method, resp)

    try:
        resp_json = resp.json()
    except Exception:
        msg = f"The Server Returned an invalid JSON response. Response body:\n[{resp.text.encode('utf8')}]"
        raise ApiException(msg, api_method, resp)

    if not resp_json['ok']:
        msg = f"Error code: {resp_json['error_code']} Description: {resp_json['description']}"
        raise ApiException(msg, api_method, resp)
    return resp_json['result']
