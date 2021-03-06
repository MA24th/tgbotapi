## Getting started.

This framework is tested with:

* Python 3.6
* Python 3.7
* Python 3.8

[![GPLv2 license](https://img.shields.io/badge/LICENSE-GPLv2-red)](https://github.com/ma24th/tgbotapi/blob/master/LICENSE)
[![Build Status](https://travis-ci.com/ma24th/tgbotapi.svg?branch=master)](https://travis-ci.com/ma24th/tgbotapi)
[![PyPI](https://img.shields.io/badge/PyPI-v4.7.0-yellow.svg)](https://pypi.org/project/tgbotapi/)
[![Telegram Group](https://img.shields.io/badge/Telegram-Group-blue.svg)](https://telegram.me/@grid9x)


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

*Note: all handlers are tested in the order in which they were declared*

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

## General API Documentation

### Types

All types are defined in types. They are all completely in line with the [Telegram API's definition of the types](https://core.telegram.org/bots/api#available-types), except for the Message's `from` field, which is renamed to `from_user` (because `from` is a Python reserved token). Thus, attributes such as `message_id` can be accessed directly with `message.message_id`. Note that `message.chat` can be either an instance of `User` or `GroupChat`.

The Message object also has a `content_type`attribute, which defines the type of the Message. `content_type` can be one of the following strings:
`text`, `audio`, `document`, `photo`, `sticker`, `video`, `video_note`, `voice`, `location`, `contact`, `new_chat_members`, `left_chat_member`, `new_chat_title`, `new_chat_photo`, `delete_chat_photo`, `group_chat_created`, `supergroup_chat_created`, `channel_chat_created`, `migrate_to_chat_id`, `migrate_from_chat_id`, `pinned_message`.

You can use some types in one function. Example:

```content_types=["text", "sticker", "pinned_message", "photo", "audio"]```

### Methods

All [API methods](https://core.telegram.org/bots/api#available-methods) are located in the TBot class. They are renamed to follow common Python naming conventions. E.g. `getMe` is renamed to `get_me` and `sendMessage` to `send_message`.

### General use of the API

Outlined below are some general use cases of the API.

#### Message handlers
A message handler is a function that is decorated with the `message_handler` decorator of a TBot instance. Message handlers consist of one or multiple filters.
Each filter much return True for a certain message in order for a message handler to become eligible to handle that message. A message handler is declared in the following way (provided `bot` is an instance of TBot):
```python
@bot.message_handler(filters)
def function_name(message):
	bot.reply_to(message, "This is a message handler")
```
`function_name` is not bound to any restrictions. Any function name is permitted with message handlers. The function must accept at most one argument, which will be the message that the function must handle.
`filters` is a list of keyword arguments.
A filter is declared in the following manner: `name=argument`. One handler may have multiple filters.
TBot supports the following filters:

|name|argument(s)|Condition|
|:---:|---| ---|
|content_types|list of strings (default `['text']`)|`True` if message.content_type is in the list of strings.|
|regexp|a regular expression as a string|`True` if `re.search(regexp_arg)` returns `True` and `message.content_type == 'text'` (See [Python Regular Expressions](https://docs.python.org/2/library/re.html)|
|commands|list of strings|`True` if `message.content_type == 'text'` and `message.text` starts with a command that is in the list of strings.|
|func|a function (lambda or function reference)|`True` if the lambda or function reference returns `True`

Here are some examples of using the filters and message handlers:

```python
import tgbotapi
bot = tgbotapi.TBot("TOKEN")

# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
	pass

# Handles all sent documents and audio files
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
	pass

# Handles all text messages that match the regular expression
@bot.message_handler(regexp="SOME_REGEXP")
def handle_message(message):
	pass

#Handles all messages for which the lambda returns True
@bot.message_handler(func=lambda message: message.document.mime_type == 'text/plain', content_types=['document'])
def handle_text_doc(message):
	pass

#Which could also be defined as:
def test_message(message):
	return message.document.mime_type == 'text/plain'

@bot.message_handler(func=test_message, content_types=['document'])
def handle_text_doc(message)
	pass

# Handlers can be stacked to create a function which will be called if either message_handler is eligible
# This handler will be called if the message starts with '/hello' OR is some emoji
@bot.message_handler(commands=['hello'])
@bot.message_handler(func=lambda msg: msg.text.encode("utf-8") == SOME_FANCY_EMOJI)
def send_something(message):
    pass
```
**Important: all handlers are tested in the order in which they were declared**

#### Edited Message handlers

Same as Message handlers

#### channel_post_handler

Same as Message handlers

#### edited_channel_post_handler

Same as Message handlers

#### Callback Query Handler

You can get `callback_query` in update object. In tgbotapi use `callback_query_handler` to process callback_querys.

```python
@bot.callback_query_handler(func=lambda call: True)
def  test_callback(call):
    logger.info(call)
```

#### TBot
```python
import tgbotapi

TOKEN = '<token_string>'
tb = tgbotapi.TBot(TOKEN)	#create a new Telegram Bot object

# Upon calling this function, TBot starts polling the Telegram servers for new messages.
# - none_stop: True/False (default False) - Don't stop polling when receiving an error from the Telegram servers
# - interval: True/False (default False) - The interval between polling requests
#           Note: Editing this parameter harms the bot's response time
# - timeout: integer (default 20) - Timeout in seconds for long polling.
tb.polling(none_stop=False, interval=0, timeout=20)

# getMe
user = tb.get_me()

# setWebhook
tb.set_webhook(url="http://example.com", certificate=open('mycert.pem'))
# unset webhook
tb.remove_webhook()

# getUpdates
updates = tb.get_updates()
updates = tb.get_updates(1234,100,20) #get_Updates(offset, limit, timeout):

# sendMessage
tb.send_message(chatid, text)

# forwardMessage
tb.forward_message(to_chat_id, from_chat_id, message_id)

# All send_xyz functions which can take a file as an argument, can also take a file_id instead of a file.
# sendPhoto
photo = open('/tmp/photo.png', 'rb')
tb.send_photo(chat_id, photo)
tb.send_photo(chat_id, "FILEID")

# sendAudio
audio = open('/tmp/audio.mp3', 'rb')
tb.send_audio(chat_id, audio)
tb.send_audio(chat_id, "FILEID")

## sendAudio with duration, performer and title.
tb.send_audio(CHAT_ID, file_data, 1, 'Mustafa', 'GruadBot')

# sendVoice
voice = open('/tmp/voice.ogg', 'rb')
tb.send_voice(chat_id, voice)
tb.send_voice(chat_id, "FILEID")

# sendDocument
doc = open('/tmp/file.txt', 'rb')
tb.send_document(chat_id, doc)
tb.send_document(chat_id, "FILEID")

# sendSticker
sti = open('/tmp/sti.webp', 'rb')
tb.send_sticker(chat_id, sti)
tb.send_sticker(chat_id, "FILEID")

# sendVideo
video = open('/tmp/video.mp4', 'rb')
tb.send_video(chat_id, video)
tb.send_video(chat_id, "FILEID")

# sendVideoNote
videonote = open('/tmp/videonote.mp4', 'rb')
tb.send_video_note(chat_id, videonote)
tb.send_video_note(chat_id, "FILEID")

# sendLocation
tb.send_location(chat_id, lat, lon)

# sendChatAction
# action_string can be one of the following strings: 'typing', 'upload_photo', 'record_video', 'upload_video',
# 'record_audio', 'upload_audio', 'upload_document' or 'find_location'.
tb.send_chat_action(chat_id, action_string)

# getFile
# Downloading a file is straightforward
# Returns a File object
import requests
file_info = tb.get_file(file_id)

file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path))


```
#### Reply markup
All `send_xyz` functions of TBot take an optional `reply_markup` argument. This argument must be an instance of `ReplyKeyboardMarkup`, `ReplyKeyboardRemove` or `ForceReply`, which are defined in types.

```python
from tgbotapi import types

# Using the ReplyKeyboardMarkup class
# It's constructor can take the following optional arguments:
# - resize_keyboard: True/False (default False)
# - one_time_keyboard: True/False (default False)
# - selective: True/False (default False)
# - row_width: integer (default 3)
# row_width is used in combination with the add() function.
# It defines how many buttons are fit on each row before continuing on the next row.
markup = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('a')
itembtn2 = types.KeyboardButton('v')
itembtn3 = types.KeyboardButton('d')
markup.add(itembtn1, itembtn2, itembtn3)
tb.send_message(chat_id, "Choose one letter:", reply_markup=markup)

# or add KeyboardButton one row at a time:
markup = types.ReplyKeyboardMarkup()
itembtna = types.KeyboardButton('a')
itembtnv = types.KeyboardButton('v')
itembtnc = types.KeyboardButton('c')
itembtnd = types.KeyboardButton('d')
itembtne = types.KeyboardButton('e')
markup.row(itembtna, itembtnv)
markup.row(itembtnc, itembtnd, itembtne)
tb.send_message(chat_id, "Choose one letter:", reply_markup=markup)
```
The last example yields this result:

[ReplyKeyboardMarkup](https://farm3.staticflickr.com/2933/32418726704_9ef76093cf_o_d.jpg "ReplyKeyboardMarkup")

```python
# ReplyKeyboardRemove: hides a previously sent ReplyKeyboardMarkup
# Takes an optional selective argument (True/False, default False)
markup = types.ReplyKeyboardRemove(selective=False)
tb.send_message(chat_id, message, reply_markup=markup)
```

```python
# ForceReply: forces a user to reply to a message
# Takes an optional selective argument (True/False, default False)
markup = types.ForceReply(selective=False)
tb.send_message(chat_id, "Send me another word:", reply_markup=markup)
```
ForceReply:

[ForceReply](https://farm4.staticflickr.com/3809/32418726814_d1baec0fc2_o_d.jpg "ForceReply")

### Inline Mode

More information about [Inline mode](https://core.telegram.org/bots/inline).

#### inline_handler

Now, you can use inline_handler to get inline_query in tgbotapi.

```python

@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    # Query message is text
```


#### chosen_inline_handler

Use chosen_inline_handler to get chosen_inline_result in tgbotapi. Don't forgot add the /setinlinefeedback
command for @Botfather.

More information : [collecting-feedback](https://core.telegram.org/bots/inline#collecting-feedback)

```python
@bot.chosen_inline_handler(func=lambda chosen_inline_result: True)
def test_chosen(chosen_inline_result):
    # Process all chosen_inline_result.
```

#### answer_inline_query

```python
@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'Result', types.InputTextMessageContent('Result message.'))
        r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Result message2.'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)

```
### Working with entities:
This object represents one special entity in a text message. For example, hashtags, usernames, URLs, etc.
Attributes:
* `type`
* `url`
* `offset`
* `length`
* `user`


**Here's an Example:**`message.entities[num].<attribute>`<br>
Here `num` is the entity number or order of entity in a reply, for if incase there are multiple entities in the reply/message.<br>
`message.entities` returns a list of entities object. <br>
`message.entities[0].type` would give the type of the first entity<br>
Refer [Bot Api](https://core.telegram.org/bots/api#messageentity) for extra details

## Advanced use of the API

### Asynchronous delivery of messages
There exists an implementation of TBot which executes all `send_xyz` and the `get_me` functions asynchronously. This can speed up you bot __significantly__, but it has unwanted side effects if used without caution.
To enable this behaviour, create an instance of AsyncTBot instead of TBot.
```python
tb = tgbotapi.AsyncTBot("TOKEN")
```
Now, every function that calls the Telegram API is executed in a separate Thread. The functions are modified to return an AsyncTask instance (defined in util.py). Using AsyncTBot allows you to do the following:
```python
import tgbotapi

tb = tgbotapi.AsyncTBot("TOKEN")
task = tb.get_me() # Execute an API call
# Do some other operations...
a = 0
for a in range(100):
	a += 10

result = task.wait() # Get the result of the execution
```
*Note: if you execute send_xyz functions after eachother without calling wait(), the order in which messages are delivered might be wrong.*

### Sending large text messages
Sometimes you must send messages that exceed 5000 characters. The Telegram API can not handle that many characters in one request, so we need to split the message in multiples. Here is how to do that using the API:
```python
from tgbotapi import util
large_text = open("large_text.txt", "rb").read()

# Split the text each 3000 characters.
# split_string returns a list with the splitted text.
splitted_text = util.split_string(large_text, 3000)
for text in splitted_text:
	tb.send_message(chat_id, text)
```
### Controlling the amount of Threads used by TBot
The TBot constructor takes the following optional arguments:

 - threaded: True/False (default True). A flag to indicate whether
   TBot should execute message handlers on it's polling Thread.

### The listener mechanism
As an alternative to the message handlers, one can also register a function as a listener to TBot. Example:
```python
def handle_messages(messages):
	for message in messages:
		# Do something with the message
		bot.reply_to(message, 'Hi')

bot.set_update_listener(handle_messages)
bot.polling()
```

### Using web hooks
When using webhooks telegram sends one Update per call, for processing it you should call process_new_messages([update.message]) when you recieve it.

There are some examples using webhooks in the *examples/webhook_examples* directory.

### Logging

You can use the tgbotapi module logger to log debug info about TBot. Use `tgbotapi.logger` to get the logger of the TBot module.
It is possible to add custom logging Handlers to the logger. Refer to the [Python logging module page](https://docs.python.org/2/library/logging.html) for more info.

```python
import logging
import tgbotapi as tbot

logger = tbot.logger
tbot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.
```

### Proxy

You can use proxy for request. `apihelper.proxy` object will use by call `requests` proxies argument.

```python
from tgbotapi import apihendler

apihendler.proxy = {'http':'http://10.10.1.10:3128'}
```

If you want to use socket5 proxy you need install dependency `pip install requests[socks]` and make sure, that you have the latest version of `gunicorn`, `PySocks`, `tgbotapi`, `requests` and `urllib3`.

```python
apihendler.proxy = {'https':'socks5://userproxy:password@proxy_address:port'}
```


### How can I distinguish a User and a GroupChat in message.chat?
Telegram Bot API support new type Chat for message.chat.

- Check the ```type``` attribute in ```Chat``` object:

```python
if message.chat.type == "private":
	# private chat message

if message.chat.type == "group":
	# group chat message

if message.chat.type == "supergroup":
	# supergroup chat message

if message.chat.type == "channel":
	# channel message
```

## Support
We now have a Telegram Chat Group as well! Keep yourself up to date with API changes, and [join it](https://t.me/grid9x).
