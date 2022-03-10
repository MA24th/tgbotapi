# -*- coding: utf-8 -*-

"""
tgbotapi.utils.logger
~~~~~~~~~~~~~~~~~~~~~
This submodule provides logger utility functions that are consumed internally by tgbotapi
"""
import logging
import sys


logger = logging.getLogger('TgBotAPI')
formatter = logging.Formatter('[%(asctime)s][%(levelname)s]-> %(threadName)s: "%(message)s"')
console_output_handler = logging.StreamHandler(sys.stderr)
console_output_handler.setFormatter(formatter)
logger.addHandler(console_output_handler)
logger.setLevel(logging.ERROR)
