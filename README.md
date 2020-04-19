# tgbotapi

The Ultimate [Telegram Bot API](https://core.telegram.org/bots/api) Client Framework

[![GPLv2 license](https://img.shields.io/badge/LICENSE-GPLv2-red)](https://github.com/ma24th/tgbotapi/blob/master/LICENSE)
[![Build Status](https://travis-ci.com/ma24th/tgbotapi.svg?branch=master)](https://travis-ci.com/ma24th/tgbotapi)
[![PyPI](https://img.shields.io/badge/PyPI-v4.7.0-yellow.svg)](https://pypi.org/project/tgbotapi/)
[![Telegram Group](https://img.shields.io/badge/Telegram-Group-blue.svg)](https://telegram.me/@grid9x)

## Getting Started

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

*While the API is production-ready, it is still under development and it has regular updates, do not forget to update it regularly by calling `pip install tgbotapi --upgrade`*

## ChangeLog
**_version 4.7.0_**
- Added the method sendDice for sending a dice message, which will have a random value from 1 to 6. (Yes, we're aware of the “proper” singular of die. But it's awkward, and we decided to help it change. One dice at a time!)
- Added the field dice to the Message object.
- Added the method getMyCommands for getting the current list of the bot's commands.
- Added the method setMyCommands for changing the list of the bot's commands through the Bot API instead of @BotFather.
- Added the ability to create animated sticker sets by specifying the parameter tgs_sticker instead of png_sticker in the method createNewStickerSet.
- Added the ability to add animated stickers to sets created by the bot by specifying the parameter tgs_sticker instead of png_sticker in the method addStickerToSet.
- Added the field thumb to the StickerSet object.
- Added the ability to change thumbnails of sticker sets created by the bot using the method setStickerSetThumb.

**_Fixes_**

there is no fixes for now.

## WiKi
Goto the [wiki tab](https://github.com/MA24th/tgbotapi/wiki).

## Support

We now have a Telegram Channel and Chat Group as well!,
Keep yourself up to date with API changes,
[join it](https://t.me/grid9x).
