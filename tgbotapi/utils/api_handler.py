# -*- coding: utf-8 -*-

"""
tgbotapi.utils.api_handler
~~~~~~~~~~~~~~~~~~~~~~~~~~
This module contains the api handler functions that are consumed internally by methods.py
"""

import requests

from tgbotapi import __version__
from .api_exceptions import TelegramAPIError
from .json_helper import JsonDeserializable
from .logger import logger


class Response(JsonDeserializable):
    """
    This class represents a Telegram API response.
    """

    def __init__(self, ok, result, error_code, description):
        """
        This method initializes a Response instance
        :param bool ok: True if the request was successful
        :param str or list or dict result: The API result
        :param int error_code: The error code returned by the Telegram API
        :param str description: The API description
        """
        self.ok = ok
        self.result = result
        self.error_code = error_code
        self.description = description

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        ok = obj['ok']
        result = None
        if 'result' in obj:
            result = obj['result']
        error_code = None
        if 'error_code' in obj:
            error_code = obj['error_code']
        description = None
        if 'description' in obj:
            description = obj['description']
        return cls(ok, result, error_code, description)


def make_request(method, url, api_method, files, params, proxies):
    """
    This method makes a request to the Telegram API
    :param str method: HTTP method ['get', 'post']
    :param str url: The URL to send the request to
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
        'User-Agent': f'tgbotapi v{__version__}'
    }
    reqs = requests.request(method, url, params=params, headers=headers, files=files, proxies=proxies)
    logger.info(f"Response <- {reqs.json()}")

    response = Response.de_json(reqs.json())
    if response.ok:
        return response.result
    else:
        logger.debug(f"The Server Responded with an Error: {response.error_code} - {response.description}")
        if response.error_code == 400:
            raise TelegramAPIError(f'Bad Request: {response.description}')
        elif response.error_code == 401:
            raise TelegramAPIError(f'Unauthorized: {response.description}')
        elif response.error_code == 404:
            raise TelegramAPIError(f'Invalid Bot Token: {response.description}')
        elif response.error_code == 429:
            raise TelegramAPIError(f'Too Many Requests: {response.description}')
        else:
            raise TelegramAPIError(f'Unknown Error: {response.description}')
