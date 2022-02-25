import os
import logging
from tgbotapi import logger
from tgbotapi import Bot as Bt

logger.setLevel(logging.DEBUG)
bot = Bt(token=os.getenv("BOT_TOKEN"), threaded=True, skip_pending=False, num_threads=2, proxies=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(msg):
    bot.send_message(chat_id=msg.chat.uid, text="Howdy, how are you doing?", parse_mode=None, entities=None,
                     disable_web_page_preview=False, disable_notification=False, reply_to_message_id=msg.message_id,
                     allow_sending_without_reply=True, reply_markup=None)


@bot.message_handler(func=lambda message: True)
def echo_all(msg):
    bot.send_message(chat_id=msg.chat.id, text=msg.text, parse_mode=None, entities=None,
                     disable_web_page_preview=False, disable_notification=False, reply_to_message_id=None,
                     allow_sending_without_reply=True, reply_markup=None)


bot.polling()
