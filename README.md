# tgbotapi

The Ultimate [Telegram Bot API](https://core.telegram.org/bots/api) Framework

[![GPLv2 license](https://img.shields.io/badge/LICENSE-GPLv2-red)](https://github.com/ma24th/tgbotapi/blob/master/LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-v6.0.0-yellow.svg)](https://pypi.org/project/tgbotapi/)
[![Python package](https://github.com/MA24th/tgbotapi/actions/workflows/python-package.yml/badge.svg)](https://github.com/MA24th/tgbotapi/actions/workflows/python-package.yml)
[![Telegram Group](https://img.shields.io/badge/Telegram-Group-blue.svg)](https://t.me/GuardBotc)


> Based On [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)

## How to Use

### Prerequisites

> Presumed you have obtained a bot token with [@BotFather](https://core.telegram.org/bots#botfather)

### A Simple Bot

The Bot class encapsulates all API calls in a single class, It provides functions such as `send_xyz` (`send_message`
, `send_document` etc.)
and several ways to listen for incoming messages.

Create a file called `echo_bot.py`. Then, open the file and create an instance of the Bot class.

```python
import tgbotapi

# Note: Make sure to actually replace TOKEN with your own API token
bot = tgbotapi.Bot(access_token="TOKEN")


# After that declaration, we need to register some so-called update handler.
# update_type define filters which can be a message, If a message passes the filter, 
# the decorated function is called and the incoming message is passed as an argument.

# Let's define an update handler which handles incoming `/start` and `/help` bot_command.
@bot.update_handler(update_type='message', bot_command=['/start', '/help'])
# A function which is decorated by an update handler can have an arbitrary name, 
# however, it must have only one parameter (the msg)
def send_welcome(msg):
    bot.send_message(chat_id=msg.chat.uid, text="Howdy, how are you doing?", parse_mode=None, entities=None,
                     disable_web_page_preview=False, disable_notification=False, reply_to_message_id=msg.message_id,
                     allow_sending_without_reply=True, reply_markup=None)


# This one echoes all incoming text messages back to the sender. 
# It uses a lambda function to test a message. If the lambda returns True, 
# the message is handled by the decorated function. 
# Since we want all text messages to be handled by this function, 
# so it simply always return True.
@bot.update_handler(update_type='message', func=lambda message: message.text)
def echo_all(msg):
    bot.send_message(chat_id=msg.chat.uid, text=msg.text, parse_mode=None, entities=None,
                     disable_web_page_preview=False, disable_notification=False, reply_to_message_id=None,
                     allow_sending_without_reply=True, reply_markup=None)


# Finally, we call long polling function
bot.polling()
```

Alright, that's it! Our source file, To start the bot, simply open up a terminal and enter `python echo_bot.py` to run
the bot!
Test it by sending commands ('/start' and '/help') and arbitrary text messages.

### ChangeLog

**_version 5.7_**

- Added support for Video Stickers. Added the field is_video to the classes Sticker and StickerSet.
- Added the parameter webm_sticker to the methods createNewStickerSet and addStickerToSet.

**_Fixes_**

- No Issues until Now

### Framework Explanation

A `handler` is a function that is decorated with the `update_handler` decorator of a Bot instance, handlers consist of
one or multiple filters, Each filter match returns True for a certain message in order for an update handler to become
eligible.

Here are some examples of using the filters and handlers:

| update_type           | filters                                      | return types        | function argument |
|-----------------------|----------------------------------------------|---------------------|-------------------|
| `message`             | `chat_type`, `bot_command`, `regexp`, `func` | `Message`           | `message`         |
| `message_edited`      | `chat_type`, `bot_command`, `regexp`, `func` | `Message`           | `message`         |
| `channel_post`        | `chat_type`, `bot_command`, `regexp`, `func` | `Message`           | `message`         |
| `edited_channel_post` | `chat_type`, `bot_command`, `regexp`, `func` | `Message`           | `message`         |
| `inline_query`        | `regexp`, `func`                             | `InlineQuery`       | `query`           |
| `chosen_inline_query` | `regexp`, `func`                             | `ChosenInlineQuery` | `query`           |
| `callback_query`      | `regexp`, `func`                             | `CallbackQuery`     | `query`           |
| `shipping_query`      | `regexp`, `func`                             | `ShippingQuery`     | `query`           |
| `per_checkout_query`  | `regexp`, `func`                             | `PreCheckoutQuery`  | `query`           |
| `poll`                | `regexp`, `func`                             | `Poll`              | `poll`            |
| `poll_answer`         | `regexp`, `func`                             | `PollAnswer`        | `poll`            |
| `my_chat_member`      | `regexp`, `func`                             | `ChatMemberUpdated` | `member`          |
| `chat_member`         | `regexp`, `func`                             | `ChatMemberUpdated` | `member`          |
| `chat_join_request`   | `regexp`, `func`                             | `ChatJoinRequest`   | `member`          |

A message handler is declared in the following way:

```python
import tgbotapi

bot = tgbotapi.Bot(access_token="TOKEN")


@bot.update_handler(update_type='message')  # filters
def function_name(message):
    bot.send_message(chat_id=message.chat.uid, text="This is a message handler")
```

`function_name` is not bound to any restrictions. Any function name is permitted with update handlers. The function must
accept at most one argument, which will be the message that the function must handle.

`filters` is a list of keyword arguments. A filter is declared in the following manner: `name=argument`. One handler may
have multiple filters.

Bot supports the following filters:

|    name     | argument(s)                                                             | Condition                                                                            |
|:-----------:|-------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| update_type | list of strings or string (default `['message']`)                       | `True` if `update.message` is present.                                               |
|  chat_type  | list of strings or string (`private`, `channel`, `group`, `supergroup`) | `True` if `message.chat.ttype` in `chat_type`                                        |
| bot_command | list of strings or string (`/start`)                                    | `True` if `message.entities[0].bot_command` and `message.text` starts with a command |
|    regex    | a regular expression as a string                                        | `True` if `re.search(regexp_arg)` returns `True`                                     |
|    func     | a function (lambda or function reference)                               | `True` if the lambda or function reference returns `True`                            |



`Logging` You can use the tgbotapi module logger to log debug info about Bot.

It is possible to add custom logging Handlers to the logger,
Refer to the [Python logging](https://docs.python.org/3/library/logging.html) for more info.

```python
import logging
from tgbotapi import logger

logger.setLevel(logging.DEBUG) # Outputs debug messages to console.
```

## How to Contribute

- You must follow [Contributing](https://github.com/MA24th/MA24th/blob/main/OpenSource/Software/CONTRIBUTING.md)
  Guidelines.
- We are committed to providing a friendly community, for more experience
  read [Code Of Conduct](https://github.com/MA24th/MA24th/blob/main/OpenSource/Software/CODE_OF_CONDUCT.md).

## How to Communicate

You're welcome to drop in and ask questions, discuss bugs and such,
Check [Communication](https://github.com/MA24th/MA24th/blob/main/OpenSource/Software/COMMUNICATION.md) Methods.

## Frequently Asked Questions

- How can I distinguish a User and a GroupChat in Message Chat?

> Telegram Bot API supports type Chat for message Check the ```ttype``` attribute in ```Chat``` object

## Attribution

These Documents are adapted
for [MA24th Open Source Software](https://github.com/MA24th/MA24th/blob/main/OpenSource/Software/),

For more information [Contact](mailto:ma24th@yahoo.com) with any additional questions or comments.
