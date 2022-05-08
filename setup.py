#!/usr/bin/env python3
from io import open

from setuptools import setup, find_packages

from tgbotapi.__version__ import __title__, __version__, __description__, __author__, __author_email__, __license__


def read(filename):
    with open(filename, encoding='utf-8') as file:
        return file.read()


setup(name=__title__,
      version=__version__,
      description=__description__,
      long_description=read('README.md'),
      long_description_content_type="text/markdown",
      author=__author__,
      author_email=__author_email__,
      url='https://github.com/MA24th/tgbotapi',
      packages=find_packages(),
      classifiers=[
          'Framework :: tgbotapi',
          'Topic :: Software Development',
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: English'],
      license=__license__,
      keywords='telegram-bot-api, tgbotapi, framework, telegram bot api, bot api',
      install_requires=['requests', 'six'],

      )
