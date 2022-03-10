# -*- coding: utf-8 -*-

"""
tgbotapi.utils.api_handler
~~~~~~~~~~~~~~~~~~~~~~~~~~
This submodule provides api handler functions that are consumed internally by tgbotapi
"""

import threading
import requests
from .logger import logger
from .api_exceptions import ApiException


thread_local = threading.local()


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
    logger.info(f"Request -> method={api_method} params={params} files={files}")
    timeout = 14.99
    if params:
        if 'timeout' in params:
            timeout = params['timeout'] + 10

    resp = get_req_session().request(method, api_url, params, data=None, headers=None, cookies=None, files=files,
                                     auth=None, timeout=timeout, allow_redirects=True, proxies=proxies, verify=None,
                                     stream=None, cert=None)

    if resp.status_code != 200:
        raise ApiException(f"The Server Returned {resp.text} ", api_method, resp)

    try:
        resp_json = resp.json()
    except AssertionError:
        msg = f"Invalid JSON, Response body:\n[{resp.text.encode('utf8')}]"
        raise ApiException(msg, api_method, resp)

    if resp_json['ok']:
        logger.info(f"Response -> '{resp_json}")
        return resp_json['result']
    else:
        msg = f"Error code: {resp_json['error_code']} Description: {resp_json['description']}"
        raise ApiException(msg, api_method, resp)
