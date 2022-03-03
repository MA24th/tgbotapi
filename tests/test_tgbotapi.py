import os
import logging
from tgbotapi import logger
from tgbotapi import Bot as Bt

logger.setLevel(logging.DEBUG)
bot = Bt(based_url="https://api.telegram.org/bot" + os.getenv("BOT_TOKEN"), allowed_updates=['message'],
         threaded=True, skip_pending=False, num_threads=200, proxies=None)


@bot.update_handler(update_type='message', bot_command=['start', 'help'])
def send_welcome(msg):
    bot.send_message(chat_id=msg.chat.uid, text="Howdy, how are you doing?", parse_mode=None, entities=None,
                     disable_web_page_preview=False, disable_notification=False, reply_to_message_id=msg.message_id,
                     allow_sending_without_reply=True, reply_markup=None)


@bot.update_handler(update_type='message', regexp='hi')
def send_hi(msg):
    bot.send_message(chat_id=msg.chat.uid, text=f'Hi 👋, {msg.from_user.first_name}', parse_mode=None, entities=None,
                     disable_web_page_preview=False, disable_notification=False, reply_to_message_id=None,
                     allow_sending_without_reply=True, reply_markup=None)


@bot.update_handler(update_type='message', func=lambda message: message.text)
def echo_all(msg):
    bot.send_message(chat_id=msg.chat.uid, text=msg.text, parse_mode=None, entities=None,
                     disable_web_page_preview=False, disable_notification=False, reply_to_message_id=None,
                     allow_sending_without_reply=True, reply_markup=None)


bot.polling()
