#!/usr/bin/env python3
from io import open
from setuptools import setup, find_packages


def read(filename):
    with open(filename, encoding='utf-8') as file:
        return file.read()


setup(name='tgbotapi',
      version='5.2',
      description='The Ultimate Telegram Bot API Client Framework',
      long_description=read('README.rst'),
      long_description_content_type="text/x-rst",
      author='Mustafa Asaad',
      author_email='ma24th@yahoo.com',
      url='https://github.com/MA24th/tgbotapi',
      packages=find_packages(),
      license='GNU GPLv2',
      keywords='telegram-bot-api, tgbotapi, framework, telegram bot api, bot api',
      install_requires=['requests', 'six'],
      extras_require={'json': 'json'},
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3.9',
                   'Environment :: Console',
                   'License :: OSI Approved :: GNU General Public License v2 (GPLv2)']
      )
