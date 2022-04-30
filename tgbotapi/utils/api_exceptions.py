# -*- coding: utf-8 -*-

"""
tgbotapi.utils.api_exception
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This submodule provides api exception objects that are consumed internally by tgbotapi
"""


class ApiException(Exception):
    """
    This class represents an Exception thrown when a call to the Telegram API fails.
    """

    def __init__(self, text, result=None):
        super(ApiException, self).__init__(f"{text}")
        self.result = result
