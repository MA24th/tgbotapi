# tgbotapi

The Ultimate [Telegram Bot API](https://core.telegram.org/bots/api) Client Framework

[![GPLv2 license](https://img.shields.io/badge/LICENSE-GPLv2-red)](https://github.com/ma24th/tgbotapi/blob/master/LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-v5.1-yellow.svg)](https://pypi.org/project/tgbotapi/)
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

After that declaration, we need to register some so-called message handlers.
Message handlers define filters which a message must pass. If a message passes the filter, 
the decorated function is called and the incoming message is passed as an argument.

Let's define a message handler which handles incoming `/start` and `/help` bot_command.
```python
@bot.update_handler(update_type='message', bot_command=['start', 'help'])
def send_welcome(msg):
	bot.send_message(chat_id=msg.chat.uid, text="Howdy, how are you doing?", parse_mode=None, entities=None,
                     disable_web_page_preview=False, disable_notification=False, reply_to_message_id=msg.message_id,
                     allow_sending_without_reply=True, reply_markup=None)
```
A function which is decorated by a message handler __can have an arbitrary name, however, it must have only one parameter (the message)__.

Let's add another handler:
```python
@bot.update_handler(update_type='message', func=lambda message: message.text)
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

@bot.update_handler(update_type='message', bot_command=['start', 'help'])
def send_welcome(msg):
    bot.send_message(chat_id=msg.chat.uid, text="Howdy, how are you doing?", parse_mode=None, entities=None,
                     disable_web_page_preview=False, disable_notification=False, reply_to_message_id=msg.message_id,
                     allow_sending_without_reply=True, reply_markup=None)


@bot.update_handler(update_type='message', func=lambda message: message.text)
def echo_all(msg):
    bot.send_message(chat_id=msg.chat.uid, text=msg.text, parse_mode=None, entities=None,
                     disable_web_page_preview=False, disable_notification=False, reply_to_message_id=None,
                     allow_sending_without_reply=True, reply_markup=None)


bot.polling()
```
To start the bot, simply open up a terminal and enter `python echo_bot.py` to run the bot! Test it by sending commands ('/start' and '/help') and arbitrary text messages.

### ChangeLog
**_version 5.1_**
#### Added two new update types
- Added updates about member status changes in chats, represented by the class ChatMemberUpdated and the fields 
my_chat_member and chat_member in the Update class. The bot must be an administrator in the chat to receive chat_member 
updates about other chat members. By default, only my_chat_member updates about the bot itself are received.

#### Improved Invite Links
- Added the class ChatInviteLink, representing an invite link to a chat.
- Added the method createChatInviteLink, which can be used to create new invite links in addition to the primary invite 
link.
- Added the method editChatInviteLink, which can be used to edit non-primary invite links created by the bot.
- Added the method revokeChatInviteLink, which can be used to revoke invite links created by the bot.

#### Voice Chat Info
- Added the type VoiceChatStarted and the field voice_chat_started to the class Message.
- Added the type VoiceChatEnded and the field voice_chat_ended to the class Message.
- Added the type VoiceChatParticipantsInvited and the field voice_chat_participants_invited to the class Message.
- Added the new administrator privilege can_manage_voice_chats to the class ChatMember and parameter 
can_manage_voice_chats to the method promoteChatMember. For now, bots can use this privilege only for passing to other 
administrators.

#### And More
- Added the type MessageAutoDeleteTimerChanged and the field message_auto_delete_timer_changed to the class Message.
- Added the parameter revoke_messages to the method kickChatMember, allowing to delete all messages from a group for the 
user who is being removed.
- Added the new administrator privilege can_manage_chat to the class ChatMember and parameter can_manage_chat to the 
method promoteChatMember. This administrator right is implied by any other administrator privilege.
- Supported the new bowling animation for the random dice. Choose between different animations (dice, darts, basketball, 
football, bowling, slot machine) by specifying the emoji parameter in the method sendDice.

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
