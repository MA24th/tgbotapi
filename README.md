# tgbotapi

The Ultimate [Telegram Bot API](https://core.telegram.org/bots/api) Client Framework

[![GPLv2 license](https://img.shields.io/badge/LICENSE-GPLv2-red)](https://github.com/ma24th/tgbotapi/blob/master/LICENSE)
![Python package](https://github.com/MA24th/tgbotapi/workflows/Python%20package/badge.svg)
![Upload Python Package](https://github.com/MA24th/tgbotapi/workflows/Upload%20Python%20Package/badge.svg)
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
pip install .
```

It is generally recommended to use the first option.

*While the API is production-ready, it is still under development and it has regular updates, do not forget to update it regularly by calling `pip install tgbotapi --upgrade`*

## ChangeLog
**_version 4.8.0_**
- Add explanations by specifying the parameters explanation and explanation_parse_mode in the method sendPoll.
- Added the fields explanation and explanation_entities to the Poll object.
- Supported timed polls that automatically close at a certain date and time. Set up by specifying the parameter open_period or close_date in the method sendPoll.
- Added the fields open_period and close_date to the Poll object.
- Supported the new darts animation for the dice mini-game. Choose between the default dice animation and darts animation by specifying the parameter emoji in the method sendDice.
- Added the field emoji to the Dice object.ed the ability to change thumbnails of sticker sets created by the bot using the method setStickerSetThumb.

**_Fixes_**

there is no fixes for now.

## WiKi
Goto the [wiki tab](https://github.com/MA24th/tgbotapi/wiki).

## Support

We now have a Telegram Channel and Chat Group as well!,
Keep yourself up to date with API changes,
[join it](https://t.me/grid9x).
