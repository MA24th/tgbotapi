# -*- coding: utf-8 -*-

"""
tgbotapi.utils.api_handler
~~~~~~~~~~~~~~~~~~~~~~~~~~
This submodule provides api handler functions that are consumed internally by methods.py
"""

import threading
import requests
from .logger import logger
from .api_exceptions import ApiException

thread_local = threading.local()


def per_thread(key, value):
    logger.debug(f'{thread_local.__class__.__name__}: {key} -> {value.status_code}')
    if thread_local:
        setattr(thread_local, key, value)

    return getattr(thread_local, key)


def make_request(method, api_url, api_method, files, params, proxies):
    """
    Makes a request to the Telegram API
    :param str method: HTTP method ['get', 'post']
    :param str api_url: telegram api url for api_method
    :param str api_method: Name of the API method to be called. (E.g. 'getUpdates')
    :param any files: files content's a data to be uploaded with request
    :param dict or None params: Should be a dictionary with key-value pairs
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy
    :return: JSON DICT FORMAT
    :rtype: dict
    """
    logger.info(f"{api_method} -> params={params} files={files}")
    headers = {
        'Accept': 'application/json',
        'Accept-Charset': 'utf-8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'close',
        'Content-Encoding': 'gzip',
        'User-Agent': 'tgbotapi v5.7.0'
    }
    reqs = requests.session().request(method, url=api_url, params=params, headers=headers, files=files, proxies=proxies)
    response = per_thread(key=api_method, value=reqs)

    if response.status_code != 200:
        raise ApiException(f"The Server Returns {response.text}", response.text)
    else:
        try:
            resp_json = response.json()
        except AssertionError:
            raise ApiException(f"Invalid JSON, Response body:\n {response.text}", response.text)

    logger.info(f"Response <- {resp_json}")
    return resp_json.get('result')
