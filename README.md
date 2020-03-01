# tgbotapi

The Ultimate [Telegram Bot API](https://core.telegram.org/bots/api) Client Framework

[![GPLv2 license](https://img.shields.io/badge/LICENSE-GPLv2-red)](https://github.com/ma24th/tgbotapi/blob/master/LICENSE)
[![Build Status](https://travis-ci.com/ma24th/tgbotapi.svg?branch=master)](https://travis-ci.com/ma24th/tgbotapi)
[![PyPI](https://img.shields.io/badge/PyPI-v4.0.0-yellow.svg)](https://pypi.org/project/tgbotapi/)
[![Telegram Group](https://img.shields.io/badge/Telegram-Group-blue.svg)](https://telegram.me/@grid9x)

## Getting started

This API is tested with:

* Python 3.6
* Python 3.7
* Python 3.8

There are two ways to install the framework:

* Installation using pip (a Python package manager):

```bash
pip install tgbotapi
```

* Installation from source (requires git):

```bash
git clone https://github.com/ma24th/tgbotapi.git
cd tgbotapi
python setup.py install
```

It is generally recommended to use the first option.

**While the API is production-ready, it is still under development and it has regular updates, do not forget to update it regularly by calling `pip install tgbotapi --upgrade`*

## Writing your first bot

### Prerequisites

It is presumed that you [have obtained an API token with @BotFather](https://core.telegram.org/bots#botfather). We will call this token `TOKEN`.
Furthermore, you have basic knowledge of the Python programming language and more importantly [the Telegram Bot API](https://core.telegram.org/bots/api).

### A simple echo bot

The TBot class (defined in \__init__.py) encapsulates all API calls in a single class. It provides functions such as `send_xyz` (`send_message`, `send_document` etc.) and several ways to listen for incoming messages.

Create a file called `echo_bot.py`.
Then, open the file and create an instance of the TBot class.

```python
import tgbotapi

bot = tgbotapi.TBot("TOKEN")
```

*Note: Make sure to actually replace TOKEN with your own API token.*

After that declaration, we need to register some so-called message handlers. Message handlers define filters which a message must pass. If a message passes the filter, the decorated function is called and the incoming message is passed as an argument.

Let's define a message handler which handles incoming `/start` and `/help` commands.

```python
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
 bot.reply_to(message, "how are you doing?")
```

A function which is decorated by a message handler __can have an arbitrary name, however, it must have only one parameter (the message)__.

Let's add another handler:

```python
@bot.message_handler(func=lambda m: True)
def echo_all(message):
 bot.reply_to(message, message.text)
```

This one echoes all incoming text messages back to the sender. It uses a lambda function to test a message. If the lambda returns True, the message is handled by the decorated function. Since we want all messages to be handled by this function, we simply always return True.

_Note_: all handlers are tested in the order in which they were declared*

We now have a basic bot which replies a static message to "/start" and "/help" commands and which echoes the rest of the sent messages. To start the bot, add the following to our source file:

```python
bot.polling()
```

Alright, that's it! Our source file now looks like this:

```python
import tgbotapi

bot = tgbotapi.TBot("TOKEN")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
 bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
 bot.reply_to(message, message.text)

bot.polling()
```

To start the bot, simply open up a terminal and enter `python echo_bot.py` to run the bot! Test it by sending commands ('/start' and '/help') and arbitrary text messages.

## Documentation

See at <https://ma24th.github.io/tgbotapi/>

## Support

We now have a Telegram Chat Group as well! Keep yourself up to date with API changes, and [join it](https://t.me/grid9x).
