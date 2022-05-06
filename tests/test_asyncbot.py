# -*- coding: utf-8 -*-

import os
import logging
from tgbotapi import logger
from tgbotapi import AsyncBot

logger.setLevel(logging.INFO)

bot = AsyncBot(access_token=os.getenv("BOT_TOKEN"), max_workers=os.sysconf('SC_NPROCESSORS_ONLN') * 2)


@bot.update_handler(bot_command=['/start', '/help'])
def send_welcome(msg):
    bot.send_message(chat_id=msg.chat.uid, text="Howdy, how are you doing?", parse_mode=None, entities=None,
                     disable_web_page_preview=False, disable_notification=False,
                     reply_to_message_id=msg.message_id, allow_sending_without_reply=True, reply_markup=None)


@bot.update_handler(regexp='hi')
def send_hi(msg):
    bot.send_message(chat_id=msg.chat.uid, text=f'Hi 👋, {msg.from_user.first_name}', parse_mode=None, entities=None,
                     disable_web_page_preview=False, disable_notification=False, reply_to_message_id=None,
                     allow_sending_without_reply=True, reply_markup=None)


@bot.update_handler(func=lambda message: message.text)
def echo_all(msg):
    bot.send_message(chat_id=msg.chat.uid, text=msg.text, parse_mode=None, entities=None,
                     disable_web_page_preview=False, disable_notification=False, reply_to_message_id=None,
                     allow_sending_without_reply=True, reply_markup=None)


bot.polling()
