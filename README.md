# tgbotapi

The Ultimate [Telegram Bot API](https://core.telegram.org/bots/api) Client Framework

[![GPLv2 license](https://img.shields.io/badge/LICENSE-GPLv2-red)](https://github.com/ma24th/tgbotapi/blob/master/LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-v4.9.0-yellow.svg)](https://pypi.org/project/tgbotapi/)
![Python package](https://github.com/MA24th/tgbotapi/workflows/Python%20package/badge.svg)
![Upload Python Package](https://github.com/MA24th/tgbotapi/workflows/Upload%20Python%20Package/badge.svg)

> Based On [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
## How to Use
### Installation
There are two ways to install the framework:
* Installation using pip (a Python package manager)*:
```bash
$ pip install tgbotapi
```
* Installation from source (requires git):

```bash
$ git clone https://github.com/ma24th/tgbotapi.git
$ cd tgbotapi
$ python setup.py install
```

It is generally recommended to use the first option.

*While the API is production-ready, it is still under development and it has regular updates, do not forget to update it regularly by calling `pip install tgbotapi --upgrade`*

## Writing your first bot

### Prerequisites

It is presumed that you [have obtained an API token with @BotFather](https://core.telegram.org/bots#botfather). We will call this token `TOKEN`.
Furthermore, you have basic knowledge of the Python programming language and more importantly [the Telegram Bot API](https://core.telegram.org/bots/api).

### A simple echo bot

The Bot class (defined in \__init__.py) encapsulates all API calls in a single class. It provides functions such as `send_xyz` (`send_message`, `send_document` etc.) and several ways to listen for incoming messages.

Create a file called `echo_bot.py`.
Then, open the file and create an instance of the TBot class.
```python
import tgbotapi

bot = tgbotapi.Bot(based_url="https://api.telegram.org/bot"+ "BOT_TOKEN")
```
*Note: Make sure to actually replace TOKEN with your own API token.*

After that declaration, we need to register some so-called message handlers. Message handlers define filters which a message must pass. If a message passes the filter, the decorated function is called and the incoming message is passed as an argument.

Let's define a message handler which handles incoming `/start` and `/help` commands.
```python
@bot.message_handler(commands=['start', 'help'])
def send_welcome(msg):
	bot.send_message(chat_id=msg.chat.uid, text="Howdy, how are you doing?", parse_mode=None, entities=None,
                     disable_web_page_preview=False, disable_notification=False, reply_to_message_id=msg.message_id,
                     allow_sending_without_reply=True, reply_markup=None)
```
A function which is decorated by a message handler __can have an arbitrary name, however, it must have only one parameter (the message)__.

Let's add another handler:
```python
@bot.message_handler(func=lambda message: True)
def echo_all(msg):
    bot.send_message(chat_id=msg.chat.uid, text=msg.text, parse_mode=None, entities=None,
                     disable_web_page_preview=False, disable_notification=False, reply_to_message_id=None,
                     allow_sending_without_reply=True, reply_markup=None)

```
This one echoes all incoming text messages back to the sender. It uses a lambda function to test a message. If the lambda returns True, the message is handled by the decorated function. Since we want all messages to be handled by this function, we simply always return True.

*Note: all handlers are tested in the order in which they were declared*

We now have a basic bot which replies a static message to "/start" and "/help" commands and which echoes the rest of the sent messages. To start the bot, add the following to our source file:
```python
bot.polling()
```
Alright, that's it! Our source file now looks like this:
```python
import tgbotapi

bot = tgbotapi.Bot(based_url="https://api.telegram.org/bot"+ "BOT_TOKEN")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(msg):
    bot.send_message(chat_id=msg.chat.uid, text="Howdy, how are you doing?", parse_mode=None, entities=None,
                     disable_web_page_preview=False, disable_notification=False, reply_to_message_id=msg.message_id,
                     allow_sending_without_reply=True, reply_markup=None)


@bot.message_handler(func=lambda message: True)
def echo_all(msg):
    bot.send_message(chat_id=msg.chat.uid, text=msg.text, parse_mode=None, entities=None,
                     disable_web_page_preview=False, disable_notification=False, reply_to_message_id=None,
                     allow_sending_without_reply=True, reply_markup=None)


bot.polling()
```
To start the bot, simply open up a terminal and enter `python echo_bot.py` to run the bot! Test it by sending commands ('/start' and '/help') and arbitrary text messages.

### ChangeLog
**_version 5.0_**
#### Run Your Own Bot API Server

- Bot API source code is now available at telegram-bot-api. You can now run your own Bot API server locally, boosting your bots' performance.
- Added the method logOut, which can be used to log out from the cloud Bot API server before launching your bot locally. You must log out the bot before running it locally, otherwise there is no guarantee that the bot will receive all updates.
- Added the method close, which can be used to close the bot instance before moving it from one local server to another.

#### Transfer Bot Ownership
- You can now use @BotFather to transfer your existing bots to another Telegram account.

#### Webhooks
- Added the parameter ip_address to the method setWebhook, allowing to bypass DNS resolving and use the specified fixed IP address to send webhook requests.
- Added the field ip_address to the class WebhookInfo, containing the current IP address used for webhook connections creation.
- Added the ability to drop all pending updates when changing webhook URL using the parameter drop_pending_updates in the methods setWebhook and deleteWebhook.

#### Working with Groups
- The getChat request now returns the user's bio for private chats if available.
- The getChat request now returns the identifier of the linked chat for supergroups and channels, i.e. the discussion group identifier for a channel and vice versa.
- The getChat request now returns the location to which the supergroup is connected (see Local Groups). Added the class ChatLocation to represent the location.
- Added the parameter only_if_banned to the method unbanChatMember to allow safe unban.

#### Working with Files
- Added the field file_name to the classes Audio and Video, containing the name of the original file.
- Added the ability to disable server-side file content type detection using the parameter disable_content_type_detection in the method sendDocument and the class inputMediaDocument.

#### Multiple Pinned Messages
- Added the ability to pin messages in private chats.
- Added the parameter message_id to the method unpinChatMessage to allow unpinning of the specific pinned message.
- Added the method unpinAllChatMessages, which can be used to unpin all pinned messages in a chat.

#### File Albums
- Added support for sending and receiving audio and document albums in the method sendMediaGroup.

#### Live Locations
- Added the field live_period to the class Location, representing a maximum period for which the live location can be updated.
- Added support for live location heading: added the field heading to the classes Location, InlineQueryResultLocation, InputLocationMessageContent and the parameter heading to the methods sendLocation and editMessageLiveLocation.
- Added support for proximity alerts in live locations: added the field proximity_alert_radius to the classes Location, InlineQueryResultLocation, InputLocationMessageContent and the parameter proximity_alert_radius to the methods sendLocation and editMessageLiveLocation.
- Added the type ProximityAlertTriggered and the field proximity_alert_triggered to the class Message.
- Added possibility to specify the horizontal accuracy of a location. Added the field horizontal_accuracy to the classes Location, InlineQueryResultLocation, InputLocationMessageContent and the parameter horizontal_accuracy to the methods sendLocation and editMessageLiveLocation.

#### Anonymous Admins
- Added the field sender_chat to the class Message, containing the sender of a message which is a chat (group or channel). For backward compatibility in non-channel chats, the field from in such messages will contain the user 777000 for messages automatically forwarded to the discussion group and the user 1087968824 (@GroupAnonymousBot) for messages from anonymous group administrators.
- Added the field is_anonymous to the class chatMember, which can be used to distinguish anonymous chat administrators.
- Added the parameter is_anonymous to the method promoteChatMember, which allows to promote anonymous chat administrators. The bot itself should have the is_anonymous right to do this. Despite the fact that bots can have the is_anonymous right, they will never appear as anonymous in the chat. Bots can use the right only for passing to other administrators.
- Added the custom title of an anonymous message sender to the class Message as author_signature.

#### And More
- Added the method copyMessage, which sends a copy of any message.
- Maximum poll question length increased to 300.
- Added the ability to manually specify text entities instead of specifying the parse_mode in the classes InputMediaPhoto, InputMediaVideo, InputMediaAnimation, InputMediaAudio, InputMediaDocument, InlineQueryResultPhoto, InlineQueryResultGif, InlineQueryResultMpeg4Gif, InlineQueryResultVideo, InlineQueryResultAudio, InlineQueryResultVoice, InlineQueryResultDocument, InlineQueryResultCachedPhoto, InlineQueryResultCachedGif, InlineQueryResultCachedMpeg4Gif, InlineQueryResultCachedVideo, InlineQueryResultCachedAudio, InlineQueryResultCachedVoice, InlineQueryResultCachedDocument, InputTextMessageContent and the methods sendMessage, sendPhoto, sendVideo, sendAnimation, sendAudio, sendDocument, sendVoice, sendPoll, editMessageText, editMessageCaption.
- Added the fields google_place_id and google_place_type to the classes Venue, InlineQueryResultVenue, InputVenueMessageContent and the optional parameters google_place_id and google_place_type to the method sendVenue to support Google Places as a venue API provider.
- Added the field allow_sending_without_reply to the methods sendMessage, sendPhoto, sendVideo, sendAnimation, sendAudio, sendDocument, sendSticker, sendVideoNote, sendVoice, sendLocation, sendVenue, sendContact, sendPoll, sendDice, sendInvoice, sendGame, sendMediaGroup to allow sending messages not a as reply if the replied-to message has already been deleted.

#### And Last but not Least
- Supported the new football and slot machine animations for the random dice. Choose between different animations (dice, darts, basketball, football, slot machine) by specifying the emoji parameter in the method sendDice.

**_Fixes_**

there is no fixes for now.

### Guide
For more explanation goto [Wiki Tab](https://github.com/MA24th/tgbotapi/wiki).


## How to Contribute
- You must follow [Contributing](https://github.com/MA24th/MA24th/blob/main/OpenSource/Software/CONTRIBUTING.md) Guidelines.
- We are committed to providing a friendly community, for more experience read [Code Of Conduct](https://github.com/MA24th/MA24th/blob/main/OpenSource/Software/CODE_OF_CONDUCT.md).


## How to Communicate
You're welcome to drop in and ask questions, 
discuss bugs and such, Check [Communication](https://github.com/MA24th/MA24th/blob/main/OpenSource/Software/COMMUNICATION.md) Methods.


## Frequently Asked Questions
- How can I distinguish a User and a GroupChat in message.chat?
>Telegram Bot API supports new type Chat for message.chat.
Check the ```ttype``` attribute in ```Chat``` object:
```python
if message.chat.ttype == "private":
	# private chat message

if message.chat.ttype == "group":
	# group chat message

if message.chat.ttype == "supergroup":
	# supergroup chat message
```
## Attribution
These Documents are adapted for [MA24th Open Source Software](https://github.com/MA24th/MA24th/blob/main/OpenSource/Software/),
For more information [contact me](mailto:ma24th@yahoo.com) with any additional questions or comments.

## Support
Join our channel on [![Telegram Group](https://img.shields.io/badge/Telegram-Group-blue.svg)](https://t.me/GuardBotc)
and [![Discord Server](https://img.shields.io/badge/Discord-Server-blue.svg)](https://discord.gg/g65AqbPK6g) .
