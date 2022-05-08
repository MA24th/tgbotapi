# -*- coding: utf-8 -*-

"""
tgbotapi.utils.api_exception
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module contains the exceptions that are thrown by the Telegram API.
"""


class APIException(Exception):
    """
    This class represents an Exception thrown when a call to the Telegram API fails.
    """

    def __init__(self, message):
        super(APIException, self).__init__(f"{message}")


class TelegramAPIError(Exception):
    """
    This class represents an Exception thrown when a call to the Telegram API fails.
    """
    def __init__(self, message, result=None):
        super(TelegramAPIError, self).__init__(f"{message}")
        self.result = result
