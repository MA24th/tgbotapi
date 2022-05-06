# -*- coding: utf-8 -*-

"""
tgbotapi.utils.api_exception
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module contains the exceptions that are thrown by the Telegram API.
"""


class ApiException(Exception):
    """
    This class represents an Exception thrown when a call to the Telegram API fails.
    """

    def __init__(self, message, result=None):
        super(ApiException, self).__init__(f"{message}")
        self.result = result
