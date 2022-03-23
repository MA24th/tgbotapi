#!/usr/bin/env python3
from io import open
from setuptools import setup, find_packages


def read(filename):
    with open(filename, encoding='utf-8') as file:
        return file.read()


setup(name='tgbotapi',
      version='5.7',
      description='The Ultimate Telegram Bot API Framework',
      long_description=read('README.md'),
      long_description_content_type="text/markdown",
      author='Mustafa Asaad',
      author_email='ma24th@yahoo.com',
      url='https://github.com/MA24th/tgbotapi',
      packages=find_packages(),
      license='GNU GPLv2',
      keywords='telegram-bot-api, tgbotapi, framework, telegram bot api, bot api',
      install_requires=['requests', 'six'],
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Framework :: tgbotapi'
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3.9']
      )
