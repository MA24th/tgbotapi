# -*- coding: utf-8 -*-

"""
tgbotapi.bot - Synchronous Telegram Bot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module provides a bot client instance to implement all telegram bot api methods and types.
for example:
    >>> import tgbotapi
    >>> # Note: Make sure to actually replace TOKEN with your own API token
    >>> bot = tgbotapi.Bot(access_token="TOKEN")
    >>>
    >>>
    >>> # After that declaration, we need to register some so-called update handler.
    >>> # update_type define filters which can be a message, If a message passes the filter,
    >>> # the decorated function is called and the incoming message is passed as an argument.
    >>>
    >>> # Let's define an update handler which handles incoming `/start` and `/help` bot_command.
    >>> @bot.update_handler(update_type='message', bot_command=['/start', '/help'])
    >>> # A function which is decorated by an update handler can have an arbitrary name,
    >>> # however, it must have only one parameter (the msg)
    >>> def send_welcome(msg):
    >>>     bot.send_message(chat_id=msg.chat.uid, text="Howdy, how are you doing?")
    >>>
    >>>
    >>> # This one echoes all incoming text messages back to the sender.
    >>> # It uses a lambda function to test a message. If the lambda returns True,
    >>> # the message is handled by the decorated function.
    >>> # Since we want all text messages to be handled by this function,
    >>> # so it simply always return True.
    >>> @bot.update_handler(update_type='message', func=lambda message: message.text)
    >>> def echo_all(msg):
    >>>     bot.send_message(chat_id=msg.chat.uid, text=msg.text)
    >>>
    >>>
    >>> # Finally, we call long polling function
    >>> bot.polling()

:copyright: (c) 2022 by Mustafa Asaad.
:license: GPLv2, see LICENSE for more details.
"""

import re
import threading
import time

from . import methods
from . import types
from . import utils


class Bot:
    def __init__(self, access_token, max_workers=2, based_url=None, proxies=None):
        """
        Use this class to create bot instance
        :param str access_token: Telegram Bot Access Token
        :param int max_workers: Number of thread workers to process incoming tasks, default 2
        :param str based_url: Required, The API url with Bot token
        :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy
        """

        self.__based_url = "https://api.telegram.org/bot" if based_url is None else based_url
        self.__api_url = f'{self.__based_url}{access_token}'
        self.__proxies = proxies

        self.__worker_pool = utils.ThreadPool(max_workers)
        self.__skip_pending = False
        self.__stop_polling = threading.Event()
        self.__allowed_updates = None
        self.__last_update_id = 0

        self.__message_handlers = []
        self.__edited_message_handlers = []
        self.__channel_post_handlers = []
        self.__edited_channel_post_handlers = []
        self.__inline_query_handlers = []
        self.__chosen_inline_handlers = []
        self.__callback_query_handlers = []
        self.__shipping_query_handlers = []
        self.__pre_checkout_query_handlers = []
        self.__poll_handlers = []
        self.__poll_answer_handlers = []
        self.__my_chat_member_handlers = []
        self.__chat_member_handlers = []
        self.__chat_join_request_handlers = []

    @staticmethod
    def __build_handler_dict(handler, **filters):
        """
        Builds a dictionary for a handler
        :param handler: functions name
        :param filters: functions filters
        :return: Return Dictionary type for handlers
        :rtype: dict
        """
        return {'function': handler, 'filters': filters}

    def update_handler(self, update_type=None, chat_type=None, bot_command=None, regexp=None, func=None):
        """
        Update handler decorator
        :param str or list[str] or None update_type: specify one of allowed_updates to take action, Default 'message'
        :param str or list or None chat_type: list of chat types (private, supergroup, group, channel), works only with
                                              these updates ['message', 'edited_message', 'channel_post',
                                              'edited_channel_post','my_chat_member','chat_member','chat_join_request']
        :param str or list or None bot_command: Bot Commands like (/start, /help)
        :param str or None regexp: Sequence of characters that define a search pattern
        :param function or None func: any python function that return True On success like (lambda)
        :return: filtered Update
        """
        if update_type is None:
            if self.__allowed_updates is None:
                update_type = 'message'
            else:
                update_type = self.__allowed_updates

        def decorator(handler):
            if 'message' in update_type:
                self.__message_handlers.append(self.__build_handler_dict(handler, chat_type=chat_type,
                                                                         bot_command=bot_command, regexp=regexp,
                                                                         func=func))
            elif 'edited_message' in update_type:
                self.__edited_message_handlers.append(self.__build_handler_dict(handler, chat_type=chat_type,
                                                                                bot_command=bot_command, regexp=regexp,
                                                                                func=func))
            elif 'channel_post' in update_type:
                self.__channel_post_handlers.append(self.__build_handler_dict(handler, regexp=regexp, func=func))
            elif 'edited_channel_post' in update_type:
                self.__edited_channel_post_handlers.append(self.__build_handler_dict(handler, regexp=regexp, func=func))
            elif 'inline_query' in update_type:
                self.__inline_query_handlers.append(self.__build_handler_dict(handler, func=func))
            elif 'chosen_inline' in update_type:
                self.__chosen_inline_handlers.append(self.__build_handler_dict(handler, func=func))
            elif 'callback_query' in update_type:
                self.__callback_query_handlers.append(self.__build_handler_dict(handler, func=func))
            elif 'shipping_query' in update_type:
                self.__shipping_query_handlers.append(self.__build_handler_dict(handler, func=func))
            elif 'pre_check_query' in update_type:
                self.__pre_checkout_query_handlers.append(self.__build_handler_dict(handler, func=func))
            elif 'poll' in update_type:
                self.__poll_handlers.append(self.__build_handler_dict(handler, func=func))
            elif 'poll_answer' in update_type:
                self.__poll_answer_handlers.append(self.__build_handler_dict(handler, func=func))
            elif 'my_chat_member' in update_type:
                self.__my_chat_member_handlers.append(self.__build_handler_dict(handler, chat_type=chat_type,
                                                                                func=func))
            elif 'chat_member' in update_type:
                self.__chat_member_handlers.append(self.__build_handler_dict(handler, chat_type=chat_type,
                                                                             func=func))
            elif 'chat_join_request' in update_type:
                self.__chat_join_request_handlers.append(self.__build_handler_dict(handler, chat_type=chat_type,
                                                                                   func=func))
            else:
                self.__message_handlers.append(self.__build_handler_dict(handler, chat_type=chat_type,
                                                                         bot_command=bot_command, regexp=regexp,
                                                                         func=func))
            return handler

        return decorator

    def __exec_task(self, task, *args, **kwargs):
        self.__worker_pool.put(task, *args, **kwargs)

    def __check_update_handler(self, update_handler, update):
        """
        check update handler
        :param update_handler:
        :param update:
        :return:
        """
        for filters, filter_value in update_handler['filters'].items():
            if filter_value is None:
                continue

            if not self.__check_filter(filters, filter_value, update):
                return False

        return True

    @staticmethod
    def __check_filter(filters, filter_value, update):
        """
        check filters if filter_value in update
        :param str filters: filter name
        :param any filter_value: filter value
        :param any update: class object
        :return: True on Success
        :rtype: bool
        """
        if filters == 'chat_type':
            try:
                ttype = update.chat.ttype
            except AssertionError:
                ttype = update.message.chat.ttype

            return ttype in filter_value
        elif filters == 'regexp':
            return update.text and re.search(filter_value, update.text, re.IGNORECASE)
        elif filters == 'func':
            return filter_value(update)
        elif filters == 'bot_command':
            entity = update.entities
            if entity:
                return entity[0].ttype == 'bot_command' and update.text in filter_value
            else:
                return False
        else:
            return False

    def __notify_update_handlers(self, handlers, new_updates):
        """
        Notifies command handlers
        :param handlers:
        :param new_updates:
        :return:
        """
        for update_type in new_updates:
            for update_handler in handlers:
                if self.__check_update_handler(update_handler, update_type):
                    self.__exec_task(update_handler['function'], update_type)
                    break

    def __process_new_messages(self, new_messages):
        self.__notify_update_handlers(self.__message_handlers, new_messages)

    def __process_new_edited_messages(self, edited_message):
        self.__notify_update_handlers(self.__edited_message_handlers, edited_message)

    def __process_new_channel_posts(self, channel_post):
        self.__notify_update_handlers(self.__channel_post_handlers, channel_post)

    def __process_new_edited_channel_posts(self, edited_channel_post):
        self.__notify_update_handlers(self.__edited_channel_post_handlers, edited_channel_post)

    def __process_new_inline_query(self, new_inline_queries):
        self.__notify_update_handlers(self.__inline_query_handlers, new_inline_queries)

    def __process_new_chosen_inline_query(self, new_chosen_inline_queries):
        self.__notify_update_handlers(self.__chosen_inline_handlers, new_chosen_inline_queries)

    def __process_new_callback_query(self, new_callback_queries):
        self.__notify_update_handlers(self.__callback_query_handlers, new_callback_queries)

    def __process_new_shipping_query(self, new_shipping_queries):
        self.__notify_update_handlers(self.__shipping_query_handlers, new_shipping_queries)

    def __process_new_pre_checkout_query(self, pre_checkout_queries):
        self.__notify_update_handlers(self.__pre_checkout_query_handlers, pre_checkout_queries)

    def __process_new_poll(self, poll):
        self.__notify_update_handlers(self.__poll_handlers, poll)

    def __process_new_poll_answer(self, poll_answer):
        self.__notify_update_handlers(self.__poll_answer_handlers, poll_answer)

    def __process_new_my_chat_member(self, my_chat_member):
        self.__notify_update_handlers(self.__my_chat_member_handlers, my_chat_member)

    def __process_new_chat_member(self, chat_member):
        self.__notify_update_handlers(self.__chat_member_handlers, chat_member)

    def __process_new_chat_join_request(self, chat_join_request):
        self.__notify_update_handlers(self.__chat_join_request_handlers, chat_join_request)

    def __process_new_updates(self, updates):
        new_messages = []
        new_edited_messages = []
        new_channel_posts = []
        new_edited_channel_posts = []
        new_inline_queries = []
        new_chosen_inline_results = []
        new_callback_queries = []
        new_shipping_queries = []
        new_pre_checkout_queries = []
        new_polls = []
        new_poll_answers = []
        new_my_chat_member = []
        new_chat_member = []
        new_chat_join_request = []

        for update in updates:
            if update.update_id > self.__last_update_id:
                self.__last_update_id = update.update_id
            if update.message:
                new_messages.append(update.message)
            if update.edited_message:
                new_edited_messages.append(update.edited_message)
            if update.channel_post:
                new_channel_posts.append(update.channel_post)
            if update.edited_channel_post:
                new_edited_channel_posts.append(update.edited_channel_post)
            if update.inline_query:
                new_inline_queries.append(update.inline_query)
            if update.chosen_inline_result:
                new_chosen_inline_results.append(update.chosen_inline_result)
            if update.callback_query:
                new_callback_queries.append(update.callback_query)
            if update.shipping_query:
                new_shipping_queries.append(update.shipping_query)
            if update.pre_checkout_query:
                new_pre_checkout_queries.append(update.pre_checkout_query)
            if update.poll:
                new_polls.append(update.poll)
            if update.poll_answer:
                new_poll_answers.append(update.poll_answer)
            if update.my_chat_member:
                new_my_chat_member.append(update.my_chat_member)
            if update.chat_member:
                new_chat_member.append(update.chat_member)
            if update.chat_join_request:
                new_chat_join_request.append(update.chat_join_request)

        if len(updates) > 0:
            if len(new_messages) > 0:
                self.__process_new_messages(new_messages)
            if len(new_edited_messages) > 0:
                self.__process_new_edited_messages(new_edited_messages)
            if len(new_channel_posts) > 0:
                self.__process_new_channel_posts(new_channel_posts)
            if len(new_edited_channel_posts) > 0:
                self.__process_new_edited_channel_posts(new_edited_channel_posts)
            if len(new_inline_queries) > 0:
                self.__process_new_inline_query(new_inline_queries)
            if len(new_chosen_inline_results) > 0:
                self.__process_new_chosen_inline_query(new_chosen_inline_results)
            if len(new_callback_queries) > 0:
                self.__process_new_callback_query(new_callback_queries)
            if len(new_pre_checkout_queries) > 0:
                self.__process_new_pre_checkout_query(new_pre_checkout_queries)
            if len(new_shipping_queries) > 0:
                self.__process_new_shipping_query(new_shipping_queries)
            if len(new_polls) > 0:
                self.__process_new_poll(new_polls)
            if len(new_poll_answers) > 0:
                self.__process_new_poll_answer(new_poll_answers)
            if len(new_my_chat_member) > 0:
                self.__process_new_my_chat_member(new_my_chat_member)
            if len(new_chat_member) > 0:
                self.__process_new_chat_member(new_chat_member)
            if len(new_chat_join_request) > 0:
                self.__process_new_chat_join_request(new_chat_join_request)

    def __get_updates(self, offset, limit, timeout, allowed_updates):
        """
        Use this method to receive incoming updates using long polling
        :param int offset:
        :param int limit: Limits the number of updates to be retrieved
        :param int timeout: Timeout in seconds for long polling
        :param list[str] or None allowed_updates: A JSON-serialized list of the update types you want your bot to
                                                  receive, For example, specify [“message”, “edited_channel_post”,
                                                  “callback_query”] to only receive updates of these types
        :return: An Array of Update objects
        """
        offset = (self.__last_update_id + offset)

        updates = []
        for data in methods.get_updates(self.__api_url, self.__proxies, offset, limit, timeout, allowed_updates):
            updates.append(types.Update.de_json(data))

        total = 0
        if self.__skip_pending:
            while updates:
                total += len(updates)
                for update in updates:
                    if update.update_id > self.__last_update_id:
                        self.__last_update_id = update.update_id
                    updates.pop()

            utils.logger.info(f'SKIPPED {total} PENDING MESSAGES')
            self.__skip_pending = False

        self.__process_new_updates(updates)

    def polling(self, stop=True, skip_pending=False, offset=1, limit=100, timeout=5, allowed_updates=None):
        """
        This method starts a new polling thread,
        and allows the bot to retrieve Updates automatically and notify listeners and message handlers accordingly
        Warning: Do not call this function more than once
        :param bool stop: Stop polling when an ApiException occurs
        :param bool skip_pending: Pass True to drop all pending Updates
        :param int offset: Identifier of the first update to be returned, default 1
        :param int limit: Limits the number of updates to be retrieved, default 100 updates
        :param int timeout: Timeout in seconds for long polling, default 5 milliseconds
        :param list[str] or None allowed_updates: A JSON-serialized list of the update types you want your bot to
                                                  receive, For example, specify [“message”, “edited_channel_post”,
                                                  “callback_query”] to only receive updates of these types
        """
        if skip_pending:
            self.__skip_pending = True

        if allowed_updates:
            self.__allowed_updates = allowed_updates

        utils.logger.info('POLLING STARTED')
        self.__stop_polling.set()
        error_interval = 0.25

        polling_thread = utils.ThreadWorker(name="PollingThread")
        event = utils.events_handler(polling_thread.event_completed, polling_thread.event_exception,
                                     self.__worker_pool.event_exception)

        while self.__stop_polling.is_set():
            event.clear()
            try:
                polling_thread.put(self.__get_updates, offset, limit, timeout, allowed_updates)
                event.wait()  # wait for polling thread finish, polling thread error or thread pool error
                polling_thread.raise_exceptions()
                self.__worker_pool.raise_exceptions()
            except KeyboardInterrupt:
                utils.logger.info("KeyboardInterrupt Occurred, STOPPING")
                self.__stop_polling.clear()
                break
            except Exception or utils.TelegramAPIError:
                if stop:
                    self.__stop_polling.clear()
                    utils.logger.info("Exception Occurred, STOPPING")
                else:
                    polling_thread.clear_exceptions()
                    self.__worker_pool.clear_exceptions()
                    utils.logger.info(f"Waiting for {error_interval} seconds until retry")
                    time.sleep(error_interval)
                    error_interval *= 2

        polling_thread.stop()
        utils.logger.info('POLLING STOPPED')

    def set_webhook(self, url, certificate=None, ip_address=None, max_connections=40, allowed_updates=None,
                    drop_pending_updates=False):
        """
        Use this method to specify an url and receive incoming updates via an outgoing webhook
        :param str url: HTTPS url to send updates to. Use an empty string to remove webhook integration
        :param types.InputFile or None certificate: Upload your public key [InputFile] certificate
        :param str or None ip_address: The fixed IP address which will be used to send webhook requests
        :param int max_connections: Maximum allowed number of simultaneous HTTPS connections to the webhook for update
        :param list or None allowed_updates: A JSON-serialized list of the update types you want your bot to receive
        :param bool drop_pending_updates: Pass True to drop all pending updates
        :return: True On success
        :rtype: bool
        """
        data = methods.set_webhook(self.__api_url, self.__proxies, url, certificate, ip_address, max_connections,
                                   allowed_updates, drop_pending_updates)
        return data

    def delete_webhook(self, drop_pending_updates=False):
        """
        Use this method to remove webhook integration if you decide to switch back to getUpdates
        :param bool drop_pending_updates: Pass True to drop all pending updates
        :return: True On success
        :rtype: bool
        """
        return methods.delete_webhook(self.__api_url, self.__proxies, drop_pending_updates)

    def get_webhook_info(self):
        """
        Use this method to get current webhook status
        :return: a WebhookInfo object, otherwise an object with the url field empty
        :rtype: types.WebhookInfo
        """
        return types.WebhookInfo.de_json(methods.get_webhook_info(self.__api_url, self.__proxies))

    def get_me(self):
        """
        A simple method for testing your bots auth token
        :return: a User object
        :rtype: types.User
        """
        return types.User.de_json(methods.get_me(self.__api_url, self.__proxies))

    def log_out(self):
        """
        Use this method to log out from the cloud Bot API server before launching the bot locally
        :return: True on success
        :rtype: bool
        """
        return methods.log_out(self.__api_url, self.__proxies)

    def close(self):
        """
        Use this method to close the bot instance before moving it from one local server to another
        :return: True on success
        :rtype: bool
        """
        return types.User.de_json(methods.close(self.__api_url, self.__proxies))

    def send_message(self, chat_id, text, parse_mode=None, entities=None, disable_web_page_preview=False,
                     disable_notification=False, protect_content=False, reply_to_message_id=None,
                     allow_sending_without_reply=False, reply_markup=None):
        """
        Use this method to send text messages. On success, the sent Message is returned
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param str text: Text of the message to be sent, 1-4096 characters after entities parsing
        :param str or None parse_mode: Send Markdown or HTML
        :param list[MessageEntity] or None entities: A JSON-serialized list of special entities
        :param bool disable_web_page_preview: Disables link previews for links in this message
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound
        :param bool protect_content: Protects the contents of the sent message from forwarding and saving
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message
        :param bool allow_sending_without_reply: Pass True, if  not replied_to_message_id even set
        :param types.InlineKeyboardMarkup or types.ReplyKeyboardMarkup or types.ReplyKeyboardRemove or types.ForceReply or None reply_markup:
        :return: a Message object
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_message(self.__api_url, self.__proxies, chat_id, text, parse_mode, entities,
                                 disable_web_page_preview,
                                 disable_notification, protect_content, reply_to_message_id,
                                 allow_sending_without_reply, reply_markup))

    def forward_message(self, chat_id, from_chat_id, message_id, disable_notification=False, protect_content=False):
        """
        Use this method to forward messages of any kind
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param int or str from_chat_id: Unique identifier for the chat where the original message was sent
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound
        :param bool protect_content: Protects the contents of the forwarded message from forwarding and saving
        :param int message_id: Message identifier in the chat specified in from_chat_id
        :return: a Message object
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.forward_message(self.__api_url, self.__proxies, chat_id, from_chat_id, message_id,
                                    disable_notification, protect_content))

    def copy_message(self, chat_id, from_chat_id, message_id, caption=None, parse_mode=None, caption_entities=None,
                     disable_notification=False, protect_content=False, reply_to_message_id=None,
                     allow_sending_without_reply=False, reply_markup=None):
        """
        Use this method to copy messages of any kind
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param int or str from_chat_id: Unique identifier for the chat where the original message was sent
        :param int message_id: Message identifier in the chat specified in from_chat_id
        :param str or None caption: New caption for media, 0-1024 characters after entities parsing
        :param str or None parse_mode: Mode for parsing entities in the new caption
        :param list or None caption_entities: A JSON-serialized list of special entities that appear in the new caption
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound
        :param bool protect_content: Protects the contents of the sent message from forwarding and saving
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message
        :param bool allow_sending_without_reply: Pass True, if  not replied_to_message_id even set
        :param types.InlineKeyboardMarkup or types.ReplyKeyboardMarkup or types.ReplyKeyboardRemove or types.ForceReply or None reply_markup:
        :return: a MessageId object
        :rtype: types.MessageId
        """
        return types.MessageId.de_json(
            methods.copy_message(self.__api_url, self.__proxies, chat_id, from_chat_id, message_id, caption,
                                 parse_mode, caption_entities, disable_notification, protect_content,
                                 reply_to_message_id, allow_sending_without_reply, reply_markup))

    def send_photo(self, chat_id, photo, caption=None, parse_mode=None, caption_entities=None,
                   disable_notification=False, protect_content=False, reply_to_message_id=None,
                   allow_sending_without_reply=False, reply_markup=None):
        """
        Use this method to send photos
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param types.InputFile or str photo: Photo [file_id or file_url or InputFile] to send
        :param str or None caption: Photo caption, 0-1024 characters after entities parsing
        :param str or None parse_mode: Send Markdown or HTML
        :param list[MessageEntity] or None caption_entities: A JSON-serialized list of special entities
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound
        :param bool protect_content: Protects the contents of the forwarded message from forwarding and saving
        :param bool protect_content: Protects the contents of the forwarded message from forwarding and saving
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message
        :param bool allow_sending_without_reply: Pass True, if  not replied_to_message_id even set
        :param types.InlineKeyboardMarkup or types.ReplyKeyboardMarkup or types.ReplyKeyboardRemove or types.ForceReply or None reply_markup:
        :return: a Message object
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_photo(self.__api_url, self.__proxies, chat_id, photo, caption, parse_mode, caption_entities,
                               disable_notification, protect_content, reply_to_message_id, allow_sending_without_reply,
                               reply_markup))

    def send_audio(self, chat_id, audio, caption=None, parse_mode=None, caption_entities=None, duration=None,
                   performer=None, title=None, thumb=None, disable_notification=False, protect_content=False,
                   reply_to_message_id=None, allow_sending_without_reply=False, reply_markup=None):
        """
        Use this method to send audio files
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param types.InputFile or str audio: Audio [file_id or file_url or InputFile] to send
        :param str or None caption: Photo caption, 0-1024 characters after entities parsing
        :param str or None parse_mode: Send Markdown or HTML
        :param list[MessageEntity] or None caption_entities: A JSON-serialized list of special entities
        :param int or None duration: Duration of the audio in seconds
        :param str or None performer: Performer
        :param str or None title: Track Name
        :param any or None thumb: Thumbnail [file_id or InputFile] of the file sent
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound
        :param bool protect_content: Protects the contents of the forwarded message from forwarding and saving
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message
        :param bool allow_sending_without_reply: Pass True, if  not replied_to_message_id even set
        :param types.InlineKeyboardMarkup or types.ReplyKeyboardMarkup or types.ReplyKeyboardRemove or types.ForceReply or None reply_markup:
        :return: a Message object
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_audio(self.__api_url, self.__proxies, chat_id, audio, caption, parse_mode, caption_entities,
                               duration, performer, title, thumb, disable_notification, protect_content,
                               reply_to_message_id, allow_sending_without_reply, reply_markup))

    def send_document(self, chat_id, document, thumb=None, caption=None, parse_mode=None, caption_entities=None,
                      disable_content_type_detection=False, disable_notification=False, protect_content=False,
                      reply_to_message_id=None, allow_sending_without_reply=False, reply_markup=None):
        """
        Use this method to send general files
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param types.InputFile or str document: File [file_id or file_url or InputFile] to send
        :param types.InputFile or str or None thumb: Thumbnail [file_id or file_url or InputFile] of the file sent
        :param str or None caption: Document caption, 0-1024 characters after entities parsing
        :param str or None parse_mode: Send Markdown or HTML
        :param list[MessageEntity] or None caption_entities: A JSON-serialized list of special entities
        :param bool disable_content_type_detection: Disables automatic server-side content type detection
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound
        :param bool protect_content: Protects the contents of the forwarded message from forwarding and saving
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message
        :param bool allow_sending_without_reply: Pass True, if  not replied_to_message_id even set
        :param types.InlineKeyboardMarkup or types.ReplyKeyboardMarkup or types.ReplyKeyboardRemove or types.ForceReply or None reply_markup:
        :return: a Message object
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_document(self.__api_url, self.__proxies, chat_id, document, thumb, caption, parse_mode,
                                  caption_entities, disable_content_type_detection, disable_notification,
                                  protect_content, reply_to_message_id, allow_sending_without_reply, reply_markup))

    def send_video(self, chat_id, video, duration=None, width=None, height=None, thumb=None, caption=None,
                   parse_mode=None, caption_entities=None, supports_streaming=None, disable_notification=False,
                   protect_content=False, reply_to_message_id=None, allow_sending_without_reply=False,
                   reply_markup=None):
        """
        Use this method to send video files
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param types.InputFile or str video: Video [file_id or file_url or InputFile] to send
        :param int or None duration: Duration of the video in seconds
        :param int or None width: Video width
        :param int or None height: Video height
        :param types.InputFile or str or None thumb: Thumbnail [file_id or file_url or InputFile] of the file sent
        :param str or None caption: Video caption, 0-1024 characters after entities parsing
        :param str or None parse_mode: Send Markdown or HTML
        :param list[MessageEntity] or None caption_entities: A JSON-serialized list of special entities
        :param bool supports_streaming: Pass True, if the uploaded video is suitable for streaming
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound
        :param bool protect_content: Protects the contents of the forwarded message from forwarding and saving
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message
        :param bool allow_sending_without_reply: Pass True, if  not replied_to_message_id even set
        :param types.InlineKeyboardMarkup or types.ReplyKeyboardMarkup or types.ReplyKeyboardRemove or types.ForceReply or None reply_markup:
        :return: a Message object
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_video(self.__api_url, self.__proxies, chat_id, video, duration, width, height, thumb,
                               caption, parse_mode, caption_entities, supports_streaming, disable_notification,
                               protect_content, reply_to_message_id, allow_sending_without_reply, reply_markup))

    def send_animation(self, chat_id, animation, duration=None, width=None, height=None, thumb=None, caption=None,
                       parse_mode=None, caption_entities=None, disable_notification=False, protect_content=False,
                       reply_to_message_id=None, allow_sending_without_reply=False, reply_markup=None):
        """
        Use this method to send animation files
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param types.InputFile or str animation: Animation [file_id or file_url or InputFile] to send
        :param int or None duration: Duration of the animation in seconds
        :param int or None width: Animation width
        :param int or None height: Animation height
        :param types.InputFile or str or None thumb: Thumbnail [file_id or file_url or InputFile] of the file sent
        :param str or None caption: Video caption, 0-1024 characters after entities parsing
        :param str or None parse_mode: Send Markdown or HTML
        :param list[MessageEntity] or None caption_entities: A JSON-serialized list of special entities
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound
        :param bool protect_content: Protects the contents of the forwarded message from forwarding and saving
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message
        :param bool allow_sending_without_reply: Pass True, if  not replied_to_message_id even set
        :param types.InlineKeyboardMarkup or types.ReplyKeyboardMarkup or types.ReplyKeyboardRemove or types.ForceReply or None reply_markup:
        :return: a Message object
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_animation(self.__api_url, self.__proxies, chat_id, animation, duration, width, height, thumb,
                                   caption, parse_mode, caption_entities, disable_notification, protect_content,
                                   reply_to_message_id, allow_sending_without_reply, reply_markup))

    def send_voice(self, chat_id, voice, caption=None, parse_mode=None, caption_entities=None, duration=None,
                   disable_notification=False, protect_content=False, reply_to_message_id=None,
                   allow_sending_without_reply=False, reply_markup=None):
        """
        Use this method to send audio files
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param types.InputFile or str voice: Audio [file_id or file_url or InputFile] to send
        :param str or None caption: Voice caption, 0-1024 characters after entities parsing
        :param str or None parse_mode: Send Markdown or HTML
        :param list[MessageEntity] or None caption_entities: A JSON-serialized list of special entities
        :param int or None duration: Duration of the voice in seconds
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound
        :param bool protect_content: Protects the contents of the forwarded message from forwarding and saving
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message
        :param bool allow_sending_without_reply: Pass True, if  not replied_to_message_id even set
        :param types.InlineKeyboardMarkup or types.ReplyKeyboardMarkup or types.ReplyKeyboardRemove or types.ForceReply or None reply_markup:
        :return: a Message object
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_voice(self.__api_url, self.__proxies, chat_id, voice, caption, parse_mode, caption_entities,
                               duration, disable_notification, protect_content, reply_to_message_id,
                               allow_sending_without_reply, reply_markup))

    def send_video_note(self, chat_id, video_note, duration=None, length=None, thumb=None, disable_notification=False,
                        protect_content=False, reply_to_message_id=None, allow_sending_without_reply=False,
                        reply_markup=None):
        """
        Use this method to send video messages
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param types.InputFile or str video_note: Video note [file_id or file_url or InputFile] to send
        :param int or None duration: Duration of the VideoNote in seconds
        :param int or None length: Video width and height, i.e. diameter of the video message
        :param types.InputFile or str or None thumb: Thumbnail [file_id or file_url or InputFile] of the file sent
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound
        :param bool protect_content: Protects the contents of the forwarded message from forwarding and saving
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message
        :param bool allow_sending_without_reply: Pass True, if  not replied_to_message_id even set
        :param types.InlineKeyboardMarkup or types.ReplyKeyboardMarkup or types.ReplyKeyboardRemove or types.ForceReply or None reply_markup:
        :return: a Message object
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_video_note(self.__api_url, self.__proxies, chat_id, video_note, duration, length, thumb,
                                    disable_notification, protect_content, reply_to_message_id,
                                    allow_sending_without_reply, reply_markup))

    def send_media_group(self, chat_id, media, disable_notification=False, protect_content=False,
                         reply_to_message_id=None, allow_sending_without_reply=False):
        """
        Use this method to send a group of photos or videos as an album
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param list[types.InputMedia] media: A JSON-serialized array describing messages to be sent,
                                             must include 2-10 items
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound
        :param bool protect_content: Protects the contents of the forwarded message from forwarding and saving
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message
        :param bool allow_sending_without_reply: Pass True, if  not replied_to_message_id even set
        :return: On success, an array of Messages that were sent is returned
        :rtype: list[types.Message]
        """
        resp = methods.send_media_group(self.__api_url, self.__proxies, chat_id, media, disable_notification,
                                        protect_content, reply_to_message_id, allow_sending_without_reply)
        result = []
        for x in resp:
            result.append(types.Message.de_json(x))
        return result

    def send_location(self, chat_id, latitude, longitude, horizontal_accuracy=None, live_period=None, heading=None,
                      proximity_alert_radius=None, disable_notification=False, protect_content=False,
                      reply_to_message_id=None, allow_sending_without_reply=False, reply_markup=None):
        """
        Use this method to send point on the map
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param float latitude: Latitude of the location
        :param float longitude: Longitude of the location
        :param float or None horizontal_accuracy: The radius of uncertainty for the location
        :param int or None live_period: Period in seconds for which the location will be updated
        :param str or None heading: For live locations, a direction in which the user is moving, in degrees
        :param int or None proximity_alert_radius: a maximum distance proximity alerts about approaching another member
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound
        :param bool protect_content: Protects the contents of the forwarded message from forwarding and saving
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message
        :param bool allow_sending_without_reply: Pass True, if  not replied_to_message_id even set
        :param types.InlineKeyboardMarkup or types.ReplyKeyboardMarkup or types.ReplyKeyboardRemove or types.ForceReply or None reply_markup:
        :return: a Message object
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_location(self.__api_url, self.__proxies, chat_id, latitude, longitude, horizontal_accuracy,
                                  live_period, heading, proximity_alert_radius, disable_notification, protect_content,
                                  reply_to_message_id, allow_sending_without_reply, reply_markup))

    def edit_message_live_location(self, latitude, longitude, horizontal_accuracy=None, heading=None,
                                   proximity_alert_radius=None, chat_id=None, message_id=None, inline_message_id=None,
                                   reply_markup=None):
        """
        Use this method to edit live location messages
        :param int or str chat_id: Required if inline_message_id is not specified, Unique identifier for the target chat
        :param int or None message_id: Required if inline_message_id is not specified, Identifier of the message to edit
        :param str or None inline_message_id: Required if chat_id and message_id are not specified
        :param float latitude: Latitude of the location
        :param float longitude: Longitude of the location
        :param float or None horizontal_accuracy: The radius of uncertainty for the location
        :param str or None heading: For live locations, a direction in which the user is moving, in degrees
        :param int or None proximity_alert_radius: a maximum distance proximity alerts about approaching another member
        :param types.InlineKeyboardMarkup or None reply_markup: A JSON-serialized object for an InlineKeyboardMarkup
        :return: a Message object, otherwise True
        :rtype: types.Message or bool
        """
        result = methods.edit_message_live_location(self.__api_url, self.__proxies, latitude, longitude,
                                                    horizontal_accuracy, heading, proximity_alert_radius, chat_id,
                                                    message_id, inline_message_id, reply_markup)
        if type(result) is bool:
            return result
        return types.Message.de_json(result)

    def stop_message_live_location(self, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        """
        Use this method to stop updating a live location message before live_period expires
        :param int or str chat_id: Required if inline_message_id is not specified,Unique identifier for the target chat
        :param int or None message_id: Required if inline_message_id is not specified,Identifier of the message to edit
        :param str or None inline_message_id: Required if chat_id and message_id are not specified
        :param types.InlineKeyboardMarkup or None reply_markup: A JSON-serialized object for an InlineKeyboardMarkup
        :return: a Message object, otherwise True
        :rtype: types.Message or bool
        """
        result = methods.stop_message_live_location(self.__api_url, self.__proxies, chat_id, message_id,
                                                    inline_message_id, reply_markup)
        if type(result) is bool:
            return result
        return types.Message.de_json(result)

    def send_venue(self, chat_id, latitude, longitude, title, address, foursquare_id=None, foursquare_type=None,
                   google_place_id=None, google_place_type=None, disable_notification=False, protect_content=False,
                   reply_to_message_id=None, allow_sending_without_reply=False, reply_markup=None):
        """
        Use this method to send information about a venue
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param float latitude: Latitude of the location
        :param float longitude: Longitude of the location
        :param str or None title: Name of the venue
        :param str address: Address of the venue
        :param str or None foursquare_id: Foursquare identifier of the venue
        :param str or None foursquare_type: Foursquare type of the venue, if known
        :param str or None google_place_id: Google Places identifier of the venue
        :param str or None google_place_type: Google Places type of the venue
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound
        :param bool protect_content: Protects the contents of the forwarded message from forwarding and saving
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message
        :param bool allow_sending_without_reply: Pass True, if  not replied_to_message_id even set
        :param types.InlineKeyboardMarkup or types.ReplyKeyboardMarkup or types.ReplyKeyboardRemove or types.ForceReply or None reply_markup:
        :return: a Message object
        :rtype: types.Message
        """
        return types.Message.de_json(methods.send_venue(self.__api_url, self.__proxies, chat_id, latitude, longitude,
                                                        title, address, foursquare_id, foursquare_type,
                                                        google_place_id, google_place_type, disable_notification,
                                                        protect_content, reply_to_message_id,
                                                        allow_sending_without_reply, reply_markup))

    def send_contact(self, chat_id, phone_number, first_name, last_name=None, vcard=None, disable_notification=False,
                     protect_content=False, reply_to_message_id=None, allow_sending_without_reply=False,
                     reply_markup=None):
        """
        Use this method to send phone contacts
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param str phone_number: Contact's phone number
        :param str first_name: Contact's first name
        :param str or None last_name: Contact's last name
        :param str or None vcard: Additional data about the contact in the form of a vCard, 0-2048 bytes
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound
        :param bool protect_content: Protects the contents of the forwarded message from forwarding and saving
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message
        :param bool allow_sending_without_reply: Pass True, if  not replied_to_message_id even set
        :param types.InlineKeyboardMarkup or types.ReplyKeyboardMarkup or types.ReplyKeyboardRemove or types.ForceReply or None reply_markup:
        :return: a Message object
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_contact(self.__api_url, self.__proxies, chat_id, phone_number, first_name, last_name, vcard,
                                 disable_notification, protect_content, reply_to_message_id,
                                 allow_sending_without_reply, reply_markup))

    def send_poll(self, chat_id, question, options, is_anonymous=True, ttype='regular', allows_multiple_answers=False,
                  correct_option_id=None, explanation=None, explanation_parse_mode=None, explanation_entities=None,
                  open_period=None, close_date=None, is_closed=True, disable_notifications=False, protect_content=False,
                  reply_to_message_id=None, allow_sending_without_reply=False, reply_markup=None):
        """
        Use this method to send a native poll
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param str question: Poll question, 1-300 characters
        :param list options: A JSON-serialized list of answer options, 2-10 strings 1-100 characters each
        :param bool is_anonymous: True, if the poll needs to be anonymous, defaults to True
        :param str or None ttype: Poll type, “quiz” or “regular”, defaults to “regular”
        :param bool allows_multiple_answers: True, if the poll allows multiple answers, ignored for polls in quiz mode
        :param int or None correct_option_id: 0-based identifier of the correct answer option, required for polls in
        quiz mode
        :param str or None explanation: Text that is shown when a user chooses an incorrect answer or taps on the lamp
        icon in a quiz-style poll
        :param str or None explanation_parse_mode: Mode for parsing entities in the explanation
        :param list[MessageEntity] or None explanation_entities: A JSON-serialized list of special entities that appear
        in message text, which can be specified instead of parse_mode
        :param int or None open_period: Amount of time in seconds the poll will be active after creation, 5-600.
        Can't be used together with close_date
        :param int or None close_date: Point in time (Unix timestamp) when the poll will be automatically closed.
        Must be at least 5 and no more than 600 seconds in the future. Can't be used together with open_period
        :param bool is_closed: Pass True, if the poll needs to be immediately closed. This can be useful for poll
        preview
        :param bool disable_notifications: Sends the message silently. Users will receive a notification with no sound
        :param bool protect_content: Protects the contents of the forwarded message from forwarding and saving
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message
        :param bool allow_sending_without_reply: Pass True, if  not replied_to_message_id even set
        replied-to message is not found
        :param dict or None reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or
        ForceReply.
        :return: a Message object
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_poll(self.__api_url, self.__proxies, chat_id, question, options, is_anonymous, ttype,
                              allows_multiple_answers, correct_option_id, explanation, explanation_parse_mode,
                              explanation_entities,
                              open_period, close_date, is_closed, disable_notifications, protect_content,
                              reply_to_message_id,
                              allow_sending_without_reply, reply_markup))

    def send_dice(self, chat_id, emoji='🎲', disable_notification=False, protect_content=False,
                  reply_to_message_id=None, allow_sending_without_reply=False, reply_markup=None):
        """
        Use this method to send a dice
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param str or None emoji: Emoji on which the dice throw animation is based. Currently, must be one of
                                  “🎲”, “🎯”, “🏀”, “⚽”, “🎳”, or “🎰”. Dice can have values 1-6 for “🎲”, “🎯” and
                                  “🎳”, values 1-5 for “🏀” and “⚽”, and values 1-64 for “🎰”. Defaults to “🎲”
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound
        :param bool protect_content: Protects the contents of the forwarded message from forwarding and saving
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message
        :param bool allow_sending_without_reply: Pass True, if  not replied_to_message_id even set
        :param types.InlineKeyboardMarkup or types.ReplyKeyboardMarkup or types.ReplyKeyboardRemove or types.ForceReply or None reply_markup:
        :return: a Message object
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_dice(self.__api_url, self.__proxies, chat_id, emoji, disable_notification, protect_content,
                              reply_to_message_id, allow_sending_without_reply, reply_markup))

    def send_chat_action(self, chat_id, action):
        """
        Use this method when you need to tell the user that something is happening on the bots side
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param str action: Type of action to broadcast. Choose one, depending on what the user is about to receive:
                           typing for text messages, upload_photo for photos, record_video or upload_video for videos,
                           record_voice or upload_voice for voice notes, upload_document for general files,
                           choose_sticker for stickers, find_location for location data, record_video_note or
                           upload_video_note for video notes
        :return: True On success
        :rtype: bool
        """
        return methods.send_chat_action(self.__api_url, self.__proxies, chat_id, action)

    def get_user_profile_photos(self, user_id, offset=None, limit=100):
        """
        Use this method to get a list of profile pictures for a user
        :param int or str user_id: Unique identifier of the target user
        :param int or None offset: Sequential number of the first photo to be returned. By default,
                                   all photos are returned
        :param int or None limit: Limits the number of photos to be retrieved. Values between 1—100 are accepted.
                                  Defaults to 100
        :return: a UserProfilePhoto object.
        :rtype: types.Message
        """
        return types.UserProfilePhotos.de_json(
            methods.get_user_profile_photos(self.__api_url, self.__proxies, user_id, offset, limit))

    def get_file(self, file_id):
        """
        Use this method to get basic info about a file and prepare it for downloading
        :param str file_id: File identifier to get info about
        :return: a File object
        :rtype: types.File
        """
        return types.File.de_json(methods.get_file(self.__api_url, self.__proxies, file_id))

    def ban_chat_member(self, chat_id, user_id, until_date=None, revoke_messages=False):
        """
        Use this method to ban a user from a group, a supergroup or a channel
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param int user_id: Unique identifier of the target user
        :param int or None until_date: Date when the user will be unbanned, unix time
        :param bool revoke_messages: Pass True to delete all messages from the chat for the user that is being removed.
                                    If False, the user will be able to see messages in the group that were sent before
                                    the user was removed. Always True for supergroups and channels
        :return: True On success
        :rtype: bool
        """
        return methods.ban_chat_member(self.__api_url, self.__proxies, chat_id, user_id, until_date, revoke_messages)

    def unban_chat_member(self, chat_id, user_id, only_if_banned=False):
        """
        Use this method to unban a previously banned user in a supergroup or channel
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param int user_id: Unique identifier of the target user
        :param bool only_if_banned: Do nothing if the user is not banned
        :return: True On success
        :rtype: bool
        """
        return methods.unban_chat_member(self.__api_url, self.__proxies, chat_id, user_id, only_if_banned)

    def restrict_chat_member(self, chat_id, user_id, permissions, until_date=None):
        """
        Use this method to restrict a user in a supergroup
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param int user_id: Unique identifier of the target user
        :param dict permissions: New user permissions must be ChatPermissions object
        :param int or None until_date: 	Date when restrictions will be lifted for the user, unix time
        :return: True On success
        :rtype: bool
        """
        return methods.restrict_chat_member(self.__api_url, self.__proxies, chat_id, user_id, permissions, until_date)

    def promote_chat_member(self, chat_id, user_id, is_anonymous=False, can_manage_chat=False, can_change_info=False,
                            can_post_messages=False, can_edit_messages=False, can_delete_messages=False,
                            can_manage_video_chats=False, can_invite_users=False, can_restrict_members=False,
                            can_pin_messages=False, can_promote_members=False):
        """
        Use this method to promote or demote a user in a supergroup or a channel
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param int user_id: Unique identifier of the target user
        :param bool is_anonymous: Pass True, if the administrator's presence in the chat is hidden
        :param bool can_manage_chat: Pass True, if the administrator can access the chat event log, chat statistics,
                                     message statistics in channels, see channel members, see anonymous administrators
                                     in supergroups and ignore slow mode. Implied by any other administrator privilege
        :param bool can_change_info: Pass True, if the administrator can change chat title, photo and other settings
        :param bool can_post_messages: Pass True, if the administrator can create channel posts, channels only
        :param bool can_edit_messages: Pass True, if the administrator can edit messages of other users and
                                       can pin messages, channels only
        :param bool can_delete_messages: Pass True, if the administrator can delete messages of other users
        :param bool can_manage_video_chats: True, if the administrator can manage voice chats
        :param bool can_invite_users: Pass True, if the administrator can invite new users to the chat
        :param bool can_restrict_members: Pass True, if the administrator can restrict, ban or unban chat members
        :param bool can_pin_messages: Pass True, if the administrator can pin messages, supergroups only
        :param bool can_promote_members: Pass True, if the administrator can add new administrators with a subset
                                         of his own privileges or demote administrators that he has promoted,
                                         directly or indirectly (promoted by administrators that were appointed by him)
        :return: True On success
        :rtype: bool
        """
        return methods.promote_chat_member(self.__api_url, self.__proxies, chat_id, user_id, is_anonymous,
                                           can_manage_chat, can_change_info, can_post_messages, can_edit_messages,
                                           can_delete_messages, can_manage_video_chats, can_invite_users,
                                           can_restrict_members, can_pin_messages, can_promote_members)

    def set_chat_administrator_custom_title(self, chat_id, user_id, custom_title):
        """
        Use this method to set a custom title for an administrator in a supergroup promoted by the bot
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param int user_id: Unique identifier of the target user
        :param str custom_title: New custom title for the administrator; 0-16 characters
        :return: True On success
        :rtype: bool
        """
        return methods.set_chat_administrator_custom_title(self.__api_url, self.__proxies, chat_id, user_id,
                                                           custom_title)

    def ban_chat_sender_chat(self, chat_id, sender_chat_id):
        """
        Use this method to ban a channel chat in a supergroup or a channel.
        Until the chat is unbanned, the owner of the banned chat won't be able to send messages on behalf of their
        channels. The bot must be an administrator in the supergroup or channel for this to work and must have the
        appropriate administrator rights
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
                                   (in the format @channel_username)
        :param int sender_chat_id: Unique identifier of the target sender chat
        :return: Returns True on success
        :rtype: bool
        """
        return methods.ban_chat_sender_chat(self.__api_url, self.__proxies, chat_id, sender_chat_id)

    def unban_chat_sender_chat(self, chat_id, sender_chat_id):
        """
        Use this method to unban a previously banned channel chat in a supergroup or channel.
        The bot must be an administrator for this to work and must have the appropriate administrator rights
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
                                   (in the format @channel_username)
        :param int sender_chat_id: Unique identifier of the target sender chat
        :return: Returns True on success
        :rtype: bool
        """
        return methods.unban_chat_sender_chat(self.__api_url, self.__proxies, chat_id, sender_chat_id)

    def set_chat_permissions(self, chat_id, permissions):
        """
        Use this method to set default chat permissions for all members
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param types.ChatPermission permissions: New default chat permissions must be a ChatPermissions object
        :return: True On success
        :rtype: bool
        """
        return methods.set_chat_permissions(self.__api_url, self.__proxies, chat_id, permissions)

    def export_chat_invite_link(self, chat_id):
        """
        Use this method to generate a new invite link for a chat
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :return: new link as String on success
        :rtype: str
        """
        return methods.export_chat_invite_link(self.__api_url, self.__proxies, chat_id)

    def create_chat_invite_link(self, chat_id, name=None, expire_date=None, member_limit=None,
                                creates_join_request=False):
        """
        Use this method to create an additional invite link for a chat
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param name: Invite link name; 0-32 characters
        :param int or None expire_date: Point in time (Unix timestamp) when the link will expire
        :param int or None member_limit: Maximum number of users that can be members of the chat simultaneously after
                                         joining the chat via this invite link; 1-99999
        :param bool creates_join_request: True, if users joining the chat via the link need to be approved by chat
                                          administrators. If True, member_limit can't be specified
        :return: Returns the new invite link as ChatInviteLink object
        :rtype: types.ChatInviteLink
        """
        return types.ChatInviteLink.de_json(methods.create_chat_invite_link(self.__api_url, self.__proxies, chat_id,
                                                                            name, expire_date, member_limit,
                                                                            creates_join_request))

    def edit_chat_invite_link(self, chat_id, invite_link, name=None, expire_date=None, member_limit=None,
                              creates_join_request=False):
        """
        Use this method to create an additional invite link for a chat
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param str invite_link: The invite link to edit
        :param str or None name: Invite link name; 0-32 characters
        :param int or None expire_date: Point in time (Unix timestamp) when the link will expire
        :param int or None member_limit: Maximum number of users that can be members of the chat simultaneously after
                                         joining the chat via this invite link; 1-99999
        :param bool creates_join_request: True, if users joining the chat via the link need to be approved by chat
                                          administrators. If True, member_limit can't be specified
        :return: Returns the new invite link as ChatInviteLink object
        :rtype: types.ChatInviteLink
        """
        return types.ChatInviteLink.de_json(methods.edit_chat_invite_link(self.__api_url, self.__proxies, chat_id,
                                                                          invite_link, name, expire_date, member_limit,
                                                                          creates_join_request))

    def revoke_chat_invite_link(self, chat_id, invite_link):
        """
        Use this method to revoke an invitation link created by the bot
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param str invite_link: The invite link to edit
        :return: Returns the revoked invite link as ChatInviteLink object
        :rtype: types.ChatInviteLink
        """
        return types.ChatInviteLink.de_json(methods.revoke_chat_invite_link(self.__api_url, self.__proxies, chat_id,
                                                                            invite_link))

    def approve_chat_join_request(self, chat_id, user_id):
        """
        Use this method to approve a chat join request,
        The bot must be an administrator in the chat for this to work
        and must have the can_invite_users administrator right
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
                                   (in the format @channel_username)
        :param int user_id: Unique identifier of the target user
        :return: True on success
        :rtype: bool
        """
        return methods.approve_chat_join_request(self.__api_url, self.__proxies, chat_id, user_id)

    def decline_chat_join_request(self, chat_id, user_id):
        """
        Use this method to decline a chat join request,
        The bot must be an administrator in the chat for this to work
        and must have the can_invite_users administrator right
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
                                   (in the format @channel_username)
        :param int user_id: Unique identifier of the target user
        :return: True on success
        :rtype: bool
        """
        return methods.decline_chat_join_request(self.__api_url, self.__proxies, chat_id, user_id)

    def set_chat_photo(self, chat_id, photo):
        """
        Use this method to set a new profile photo for the chat
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param types.InputFile photo: Use this method to set a new profile photo for the chat
        :return: True On success
        :rtype: bool
        """
        return methods.set_chat_photo(self.__api_url, self.__proxies, chat_id, photo)

    def delete_chat_photo(self, chat_id):
        """
        Use this method to delete a chat photo
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :return: True On success
        :rtype: bool
        """
        return methods.delete_chat_photo(self.__api_url, self.__proxies, chat_id)

    def set_chat_title(self, chat_id, title):
        """
        Use this method to change the title of a chat
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param str title: New chat title, 1-255 characters
        :return: True On success
        :rtype: bool
        """
        return methods.set_chat_title(self.__api_url, self.__proxies, chat_id, title)

    def set_chat_description(self, chat_id, description):
        """
        Use this method to change the description of a group, a supergroup or a channel
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param str description: New chat description, 0-255 characters
        :return: True On success
        :rtype: bool
        """
        return methods.set_chat_description(self.__api_url, self.__proxies, chat_id, description)

    def pin_chat_message(self, chat_id, message_id, disable_notification=False):
        """
        Use this method to pin a message in a group, a supergroup, or a channel
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param int message_id: Identifier of a message to pin
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound
        :return: True On success
        :rtype: bool
        """
        return methods.pin_chat_message(self.__api_url, self.__proxies, chat_id, message_id, disable_notification)

    def unpin_chat_message(self, chat_id, message_id=None):
        """
        Use this method to unpin a message in a group, a supergroup, or a channel
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param str or None message_id: Identifier of a message to unpin. If not specified,
                                       the most recent pinned message (by sending date) will be unpinned
        :return: True On success
        :rtype: bool
        """
        return methods.unpin_chat_message(self.__api_url, self.__proxies, chat_id, message_id)

    def unpin_all_chat_message(self, chat_id):
        """
        Use this method to clear the list of pinned messages in a chat
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :return: True On success
        :rtype: bool
        """
        return methods.unpin_all_chat_message(self.__api_url, self.__proxies, chat_id)

    def leave_chat(self, chat_id):
        """
        Use this method for your bot to leave a group, supergroup or channel
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :return: True On success
        :rtype: bool
        """
        return methods.leave_chat(self.__api_url, self.__proxies, chat_id)

    def get_chat(self, chat_id):
        """
        Use this method to get up-to-date information about the chat
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :return: a Chat object
        :rtype: types.Chat
        """
        return types.Chat.de_json(methods.get_chat(self.__api_url, self.__proxies, chat_id))

    def get_chat_administrators(self, chat_id):
        """
        Use this method to get a list of administrators in a chat
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :return: an Array of ChatMember object
        :rtype: list[types.ChatMember]
        """
        result = methods.get_chat_administrators(
            self.__api_url, self.__proxies, chat_id)
        ret = []
        for r in result:
            ret.append(types.ChatMember.de_json(r))
        return ret

    def get_chat_member_count(self, chat_id):
        """
        Use this method to get the number of members in a chat
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :return: Integer On success
        :rtype: int
        """
        return methods.get_chat_member_count(self.__api_url, self.__proxies, chat_id)

    def get_chat_member(self, chat_id, user_id):
        """
        Use this method to get information about a member of a chat
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param int user_id: Unique identifier of the target user
        :return: a ChatMember object On success
        :rtype: types.ChatMember
        """
        return types.ChatMember.de_json(methods.get_chat_member(self.__api_url, self.__proxies, chat_id, user_id))

    def set_chat_sticker_set(self, chat_id, sticker_set_name):
        """
        Use this method to set a new group sticker set for a supergroup
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param str sticker_set_name: Name of the sticker set to be set as the group sticker set
        :return: True On success
        :rtype: bool
        """
        return methods.set_chat_sticker_set(self.__api_url, self.__proxies, chat_id, sticker_set_name)

    def delete_chat_sticker_set(self, chat_id):
        """
        Use this method to delete a group sticker set from a supergroup
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :return: True On success
        :rtype: bool
        """
        return methods.delete_chat_sticker_set(self.__api_url, self.__proxies, chat_id)

    def answer_callback_query(self, callback_query_id, text=None, show_alert=False, url=None, cache_time=None):
        """
        Use this method to send answers to callback queries sent from inline keyboards
        :param str callback_query_id: Unique identifier for the query to be answered
        :param str or None text: Text of the notification. If not specified, nothing will be shown to the user,
                                 0-200 characters
        :param bool show_alert: If true, an alert will be shown by the client instead of a notification at the top of
                                the chat screen. Defaults to false
        :param str or None url: URL that will be opened by the user's client
        :param int or None cache_time: The maximum amount of time in seconds that the result of the callback query may
                                       be cached client-side
        :return: True On success
        :rtype: bool
        """
        return methods.answer_callback_query(self.__api_url, self.__proxies, callback_query_id, text, show_alert, url,
                                             cache_time)

    def set_my_commands(self, commands, scope=None, language_code=None):
        """
        Use this method to change the list of the bots commands
        :param list[types.BotCommand] commands: A JSON-serialized list of bot commands to be set as the list of
                                                the bots commands
        :param types.BotCommandScope or None scope: A JSON-serialized object, describing scope of users for which the
                                                    commands are relevant. Defaults to BotCommandScopeDefault
        :param str or None language_code: A two-letter ISO 639-1 language code. If empty, commands will be applied to
                                          all users from the given scope, for whose language there are no dedicated
                                          commands
        :return: True On success
        :rtype: bool
        """
        return methods.set_my_commands(self.__api_url, self.__proxies, commands, scope, language_code)

    def delete_my_commands(self, scope=None, language_code=None):
        """
        Use this method to delete the list of the bots commands for the given scope and user language
        :param types.BotCommandScope or None scope: A JSON-serialized object, describing scope of users.
                                                    Defaults to BotCommandScopeDefault
        :param str or None language_code: A two-letter ISO 639-1 language code If empty, commands will be applied to all
                                          users from the given scope, for whose language there are no dedicated commands
        :return: True on success
        :rtype: bool
        """
        return methods.delete_my_commands(self.__api_url, self.__proxies, scope, language_code)

    def get_my_commands(self, scope=None, language_code=None):
        """
        Use this method to get the current list of the bots commands
        :param types.BotCommandScope or None scope: A JSON-serialized object, describing scope of users.
                                                    Defaults to BotCommandScopeDefault
        :param str or None language_code: A two-letter ISO 639-1 language code or an empty string
        :return: Array of BotCommand On success
        :rtype: list[tgbotapi.types.BotCommand]
        """
        resp = methods.get_my_commands(self.__api_url, self.__proxies, scope, language_code)
        result = []
        for x in resp:
            result.append(types.BotCommand.de_json(x))
        return result

    def set_chat_menu_button(self, chat_id=None, menu_button=None):
        """
        Use this method to change the bots' menu button in a private chat, or the default menu button.
        Returns True on success
        :param int or str or None chat_id: Unique identifier for the target private chat. If not specified,
                                           default bots' menu button will be returned
        :param types.MenuButton or None menu_button: A JSON-serialized object for the new menu
        :return: True on success
        :rtype: bool
        """
        data = methods.set_chat_menu_button(self.__api_url, self.__proxies, chat_id, menu_button)
        return data

    def get_chat_menu_button(self, chat_id=None):
        """
        Use this method to get the current value of the bots' menu button in a private chat, or the default menu button.
        Returns MenuButton on success
        :param int or str or None chat_id: Unique identifier for the target private chat. If not specified,
                                           default bots' menu button will be returned
        :return: MenuButton on success
        :rtype: types.MenuButton
        """
        data = methods.get_chat_menu_button(self.__api_url, self.__proxies, chat_id)
        return types.MenuButton.de_json(data)

    def set_my_default_administrator_rights(self, rights=None, for_channel=False):
        """
        Use this method to change the default administrator rights requested by the bot when it's added as an
        administrator to groups or channels. These rights will be suggested to users,
        but they  are free to modify the list before adding the bot.
        Returns True on success
        :param types.ChatAdministratorRights or None rights: New default administrator rights
        :param bool for_channel: Pass True to change the default administrator rights of the bot in channels.
                                 Otherwise, the default administrator rights of the bot for groups and supergroups
                                 will be changed.

        :return: True on success
        :rtype: bool
        """
        data = methods.set_my_default_administrator_rights(self.__api_url, self.__proxies, rights, for_channel)
        return data

    def get_my_default_administrator_rights(self, for_channel=False):
        """
        Use this method to get the current default administrator rights of the bot.
        Returns ChatAdministratorRights on success
        :param bool for_channel: Pass True to change the default administrator rights of the bot in channels.
                                 Otherwise, the default administrator rights of the bot for groups and supergroups
                                 will be changed.
        :return: ChatAdministratorRights on success
        :rtype: types.ChatAdministratorRights
        """
        data = methods.get_my_default_administrator_rights(self.__api_url, self.__proxies, for_channel)
        return types.ChatAdministratorRights.de_json(data)

    def edit_message_text(self, text, chat_id=None, message_id=None, inline_message_id=None, parse_mode=None,
                          entities=None, disable_web_page_preview=False, reply_markup=None):
        """
        Use this method to edit text and game messages
        :param int or str chat_id: Required if inline_message_id is not specified,Unique identifier for the target chat
        :param int or None message_id: Required if inline_message_id is not specified,Identifier of the message to edit
        :param str or None inline_message_id: Required if chat_id and message_id are not specified
        :param str text: Text of the message to be sent, 1-4096 characters after entities parsing
        :param str or None parse_mode: Send Markdown or HTML
        :param list[MessageEntity] or None entities: A JSON-serialized list of special entities that appear in message
        :param bool disable_web_page_preview: Disables link previews for links in this message
        :param types.InlineKeyboardMarkup or None reply_markup: A JSON-serialized object for an InlineKeyboardMarkup
        :return: a Message object On success, otherwise True
        :rtype: types.Message or bool
        """
        result = methods.edit_message_text(self.__api_url, self.__proxies, text, chat_id, message_id,
                                           inline_message_id, parse_mode, entities, disable_web_page_preview,
                                           reply_markup)
        if type(result) is bool:
            return result
        return types.Message.de_json(result)

    def edit_message_caption(self, chat_id=None, message_id=None, inline_message_id=None, caption=None, parse_mode=None,
                             caption_entities=None,
                             reply_markup=None):
        """
        Use this method to edit captions of messages
        :param int or str chat_id: Required if inline_message_id is not specified,Unique identifier for the target chat
        :param int or None message_id: Required if inline_message_id is not specified,Identifier of the message to edit
        :param str or None inline_message_id: Required if chat_id and message_id are not specified
        :param str or None caption: New caption of the message, 0-1024 characters after entities parsing
        :param str or None parse_mode: Send Markdown or HTML
        :param list[MessageEntity] or None caption_entities: A JSON-serialized list of special entities
        :param types.InlineKeyboardMarkup or None reply_markup: A JSON-serialized object for an InlineKeyboardMarkup
        :return: a Message object On success, otherwise True
        :rtype: types.Message or bool
        """
        result = methods.edit_message_caption(self.__api_url, self.__proxies, chat_id, message_id,
                                              inline_message_id,
                                              caption, parse_mode,
                                              caption_entities,
                                              reply_markup)
        if type(result) is bool:
            return result
        return types.Message.de_json(result)

    def edit_message_media(self, media, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        """
        Use this method to edit animation, audio, document, photo, or video messages
        :param int or str chat_id: Required if inline_message_id is not specified,Unique identifier for the target chat
        :param int or None message_id: Required if inline_message_id is not specified,Identifier of the message to edit
        :param str or None inline_message_id: Required if chat_id and message_id are not specified
        :param types.InputFile media: A JSON-serialized object for a new media content of the message must be InputMedia
        :param types.InlineKeyboardMarkup or None reply_markup: A JSON-serialized object for an InlineKeyboardMarkup
        :return: a Message object On success, otherwise True
        :rtype: types.Message or bool
        """
        result = methods.edit_message_media(
            self.__api_url, self.__proxies, media, chat_id, message_id, inline_message_id, reply_markup)
        if type(result) is bool:
            return result
        return types.Message.de_json(result)

    def edit_message_reply_markup(self, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        """
        Use this method to edit only the reply markup of messages
        :param int or str chat_id: Required if inline_message_id is not specified,Unique identifier for the target chat
        :param int or None message_id: Required if inline_message_id is not specified,Identifier of the message to edit
        :param str or None inline_message_id: Required if chat_id and message_id are not specified
        :param types.InlineKeyboardMarkup or None reply_markup: A JSON-serialized object for an InlineKeyboardMarkup
        :return: a Message object On success, otherwise True
        :rtype: types.Message or bool
        """
        result = methods.edit_message_reply_markup(
            self.__api_url, self.__proxies, chat_id, message_id, inline_message_id, reply_markup)
        if type(result) is bool:
            return result
        return types.Message.de_json(result)

    def stop_poll(self, chat_id, message_id, reply_markup=None):
        """
        Use this method to stop a poll which was sent by the bot
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param int or None message_id: Identifier of the original message with the poll
        :param types.InlineKeyboardMarkup or None reply_markup: A JSON-serialized object for an InlineKeyboardMarkup
        :return: a Poll object On success
        :rtype: types.Poll
        """
        return types.Poll.de_json(methods.stop_poll(self.__api_url, self.__proxies, chat_id, message_id,
                                                    reply_markup))

    def delete_message(self, chat_id, message_id):
        """
        Use this method to delete a message, including service messages, with the following limitations:
            - A message can only be deleted if it was sent less than 48 hours ago.
            - A dice message in a private chat can only be deleted if it was sent more than 24 hours ago.
            - Bots can delete outgoing messages in private chats, groups, and supergroups.
            - Bots can delete incoming messages in private chats.
            - Bots granted can_post_messages permissions can delete outgoing messages in channels.
            - If the bot is an administrator of a group, it can delete any message there.
            - If the bot has can_delete_messages permission in a supergroup or a channel,it can delete any message there
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param int message_id: Identifier of the message to delete
        :return: True On success
        :rtype: bool
        """
        return methods.delete_message(self.__api_url, self.__proxies, chat_id, message_id)

    def send_sticker(self, chat_id, sticker, disable_notification=False, protect_content=False,
                     reply_to_message_id=None, allow_sending_without_reply=False, reply_markup=None):
        """
        Use this method to send static .WEBP or animated .TGS stickers
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param types.InputFile or str sticker: Sticker [file_id or file_url or InputFile] to send
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound
        :param bool protect_content: Protects the contents of the forwarded message from forwarding and saving
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message
        :param bool allow_sending_without_reply: Pass True, if  not replied_to_message_id even set
        :param types.InlineKeyboardMarkup or types.ReplyKeyboardMarkup or types.ReplyKeyboardRemove or types.ForceReply or None reply_markup:
        :return: a Message object On success
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_sticker(self.__api_url, self.__proxies, chat_id, sticker, disable_notification,
                                 protect_content, reply_to_message_id, allow_sending_without_reply, reply_markup))

    def get_sticker_set(self, name):
        """
        Use this method to get a sticker set
        :param str name:  Name of the sticker set
        :return: a StickerSet object On success
        :rtype: types.StickerSet
        """
        return types.StickerSet.de_json(methods.get_sticker_set(self.__api_url, self.__proxies, name))

    def upload_sticker_file(self, user_id, png_sticker):
        """
        Use this method to upload a .PNG file with a sticker
        :param int user_id: Unique identifier of the target user
        :param types.InputFile png_sticker: Png image with the sticker
        :return: a File object On success
        :rtype: types.File
        """
        return types.File.de_json(methods.upload_sticker_file(self.__api_url, self.__proxies, user_id, png_sticker))

    def create_new_sticker_set(self, user_id, name, title, emojis=None, png_sticker=None, tgs_sticker=None,
                               webm_sticker=None, contains_masks=False, mask_position=None):
        """
        Use this method to create a new sticker set owned by a user
        :param int user_id: Unique identifier of the target user
        :param str name: Short name of sticker set
        :param str title: New chat title, 1-255 characters
        :param types.InputFile or str or None png_sticker: PNG image with the sticker, must be up to 512 kilobytes in
                                                           size, dimensions must not exceed 512px, and either width or
                                                           height must be exactly 512px
        :param types.InputFile or None tgs_sticker: TGS animation with the sticker, uploaded using multipart/form-data
        :param types.InputFile or None webm_sticker: WEBM video with the sticker, uploaded using multipart/form-data
        :param str emojis: One or more emoji corresponding to the sticker
        :param bool contains_masks: Pass True, if a set of mask stickers should be created
        :param types.MaskPosition or None mask_position: A JSON-serialized object for position where the mask should be
                                                         placed on faces
        :return: True On success
        :rtype: bool
        """
        return methods.create_new_sticker_set(self.__api_url, self.__proxies, user_id, name, title, png_sticker,
                                              tgs_sticker, webm_sticker, emojis, contains_masks, mask_position)

    def add_sticker_to_set(self, user_id, name, emojis, png_sticker=None, tgs_sticker=None, webm_sticker=None,
                           mask_position=None):
        """
        Use this method to add a new sticker to a set created by the bot
        :param int user_id: Unique identifier of the target user
        :param str name: Short name of sticker set
        :param types.InputFile or str or None png_sticker: PNG image with the sticker, must be up to 512 kilobytes in
                                                           size, dimensions must not exceed 512px, and either width or
                                                           height must be exactly 512px
        :param types.InputFile or None tgs_sticker: TGS animation with the sticker, uploaded using multipart/form-data
        :param types.InputFile or None webm_sticker: WEBM video with the sticker, uploaded using multipart/form-data
        :param str emojis: One or more emoji corresponding to the sticker
        :param types.MaskPosition or None mask_position: A JSON-serialized object for position where the mask should be
                                                         placed on faces
        :return: True On success
        :rtype: bool
        """
        return methods.add_sticker_to_set(self.__api_url, self.__proxies, user_id, name, png_sticker, tgs_sticker,
                                          webm_sticker, emojis, mask_position)

    def set_sticker_position_in_set(self, sticker, position):
        """
        Use this method to move a sticker in a set created by the bot to a specific position
        :param str sticker: File identifier of the sticker
        :param int position: New sticker position in the set, zero-based
        :return: True On success
        :rtype: bool
        """
        return methods.set_sticker_position_in_set(self.__api_url, self.__proxies, sticker, position)

    def delete_sticker_from_set(self, sticker):
        """
        Use this method to delete a sticker from a set created by the bot
        :param str sticker: File identifier of the sticker
        :return: True On success
        :rtype: bool
        """
        return methods.delete_sticker_from_set(self.__api_url, self.__proxies, sticker)

    def set_sticker_set_thumb(self, name, user_id, thumb=None):
        """
        Use this method to set the thumbnail of a sticker set
        :param str name: Short name of sticker set
        :param int user_id: Unique identifier of the target user
        :param types.InputFile or str or None thumb: Thumbnail [file_id or file_url or InputFile] of the file sent
        :return: True On success
        :rtype: bool
        """
        return methods.set_sticker_set_thumb(self.__api_url, self.__proxies, name, user_id, thumb)

    def answer_inline_query(self, inline_query_id, results, cache_time=300, is_personal=False, next_offset=None,
                            switch_pm_text=None, switch_pm_parameter=None):
        """
        Use this method to send answers to an inline query
        :param str inline_query_id: Unique identifier for the answered query
        :param list results: A JSON-serialized array of [InlineQueryResult] results for the inline query
        :param int or None cache_time: The maximum amount of time in seconds result of inline query maybe cached server
        :param bool is_personal: results may be cached on the server side only for the user that sent the query
        :param str or None next_offset: Pass the offset that a client should send in the next query
        :param str or None switch_pm_text: If passed, clients will display a button with specified text
        :param str or None switch_pm_parameter: Deep-linking parameter for the /start message sent to the bot
        :return: True On success
        :rtype: bool
        """
        return methods.answer_inline_query(self.__api_url, self.__proxies, inline_query_id, results, cache_time,
                                           is_personal, next_offset,
                                           switch_pm_text, switch_pm_parameter)

    def answer_web_app_query(self, web_app_query_id, result):
        """
        Use this method to set the result of an interaction with a Web App and send a corresponding message
        on behalf of the user to the chat from which the query originated.
        On success, a SentWebAppMessage object is returned
        :param str web_app_query_id: Unique identifier for the query
        :param types.InlineQueryResult result: The result of the query
        """
        data = methods.answer_web_app_query(self.__based_url, self.__proxies, web_app_query_id, result)
        return types.SentWebAppMessage.de_json(data)

    def send_invoice(self, chat_id, title, description, payload, provider_token, currency, prices, max_tip_amount=None,
                     suggested_tip_amounts=None, start_parameter=None, provider_data=None, photo_url=None,
                     photo_size=None, photo_width=None, photo_height=None, need_name=False, need_phone_number=False,
                     need_email=False, need_shipping_address=False, send_phone_number_to_provider=False,
                     send_email_to_provider=False, is_flexible=False, disable_notification=False, protect_content=False,
                     reply_to_message_id=None, allow_sending_without_reply=False, reply_markup=None):
        """
        Use this method to send invoices. On success, the sent Message is returned
        :param int chat_id: Unique identifier for the target chat or username of the target channel
        :param str title: New chat title, 1-255 characters
        :param str description: Product description, 1-255 characters
        :param str payload: Bot-defined invoice payload, 1-128 bytes
        :param str provider_token: Payments provider token, obtained via Bot father
        :param str currency: Three-letter ISO 4217 currency code
        :param list[types.LabeledPrice] prices: Price breakdown, a JSON-serialized list of components
        :param int or None max_tip_amount: The maximum accepted amount for tips in the smallest units of the currency
                                           (integer, not float/double).
        :param list[int] or None suggested_tip_amounts: A JSON-serialized array of suggested amounts of tips in the
                                                        smallest units of the currency (integer, not float/double).
        :param str start_parameter: Unique deep-linking parameter
        :param dict provider_data: JSON-encoded data about the invoice, which will be shared with the payment provider
        :param str photo_url: URL of the product photo for the invoice
        :param int photo_size: Photo Size
        :param int photo_width: Photo Width
        :param int photo_height: Photo Height
        :param need_name: Pass True, if you require the user's full name to complete the order
        :param need_phone_number: Pass True, if you require the user's phone number to complete the order
        :param need_email: Pass True, if you require the user's email address to complete the order
        :param need_shipping_address: Pass True, if you require the user's shipping address to complete the order
        :param send_phone_number_to_provider: Pass True, if user's phone number should be sent to provider
        :param send_email_to_provider: Pass True, if user's email address should be sent to provider
        :param is_flexible: Pass True, if the final price depends on the shipping method
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound
        :param bool protect_content: Protects the contents of the forwarded message from forwarding and saving
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message
        :param bool allow_sending_without_reply: Pass True, if  not replied_to_message_id even set
        :param types.InlineKeyboardMarkup or None reply_markup: A JSON-serialized object for an InlineKeyboardMarkup
        :return: a Message object
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_invoice(self.__api_url, self.__proxies, chat_id, title, description, payload, provider_token,
                                 currency, prices, max_tip_amount, suggested_tip_amounts, start_parameter,
                                 provider_data, photo_url, photo_size, photo_width, photo_height, need_name,
                                 need_phone_number, need_email, need_shipping_address, send_phone_number_to_provider,
                                 send_email_to_provider, is_flexible, disable_notification, protect_content,
                                 reply_to_message_id, allow_sending_without_reply, reply_markup))

    def answer_shipping_query(self, shipping_query_id, ok, shipping_options=None, error_message=None):
        """
        Use this method to reply to shipping queries,
        If you sent an invoice requesting a shipping address and the parameter is_flexible was specified,
        the Bot API will send an Update with a shipping_query field to the bot
        :param str shipping_query_id: Unique identifier for the query to be answered
        :param bool ok: Delivery to the specified address is possible and False if there are any problems
        :param list[types.ShippingOption] or None shipping_options: Required ok is True,
                                                                   A JSON-serialized array of available shipping options
        :param str or None error_message: Required if ok is False. Error message in human-readable
        :return: True, On success
        :rtype: bool
        """
        return methods.answer_shipping_query(self.__api_url, self.__proxies, shipping_query_id, ok, shipping_options,
                                             error_message)

    def answer_pre_checkout_query(self, pre_checkout_query_id, ok, error_message=None):
        """
        Use this method to respond to such pre-checkout queries
        :param str pre_checkout_query_id: Unique identifier for the query to be answered
        :param bool ok: Specify True if delivery to the specified address is possible
        :param str or None error_message: Required if ok is False. Error message in human-readable
        :return: True On success
        :rtype: bool
        """
        return methods.answer_pre_checkout_query(self.__api_url, self.__proxies, pre_checkout_query_id, ok,
                                                 error_message)

    def set_passport_data_errors(self, user_id, errors):
        """
        Use this if the data submitted by the user doesn't satisfy the standards your service requires for any reason
        :param int user_id: Unique identifier of the target user
        :param list[types.PassportElementError] errors: A JSON-serialized array of [PassportElementError]
                                                        describing the errors
        :return: True On success
        :rtype: bool
        """
        return methods.set_passport_data_errors(self.__api_url, self.__proxies, user_id, errors)

    def send_game(self, chat_id, game_short_name, disable_notification=False, protect_content=False,
                  reply_to_message_id=None, allow_sending_without_reply=False, reply_markup=None):
        """
        Use this method to send a game
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel
        :param str game_short_name: Short name of the game, serves as the unique identifier for the game
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound
        :param bool protect_content: Protects the contents of the forwarded message from forwarding and saving
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message
        :param bool allow_sending_without_reply: Pass True, if  not replied_to_message_id even set
        :param dict or None reply_markup: A JSON-serialized object for an InlineKeyboardMarkup
        :return: a Message object On success
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_game(self.__api_url, self.__proxies, chat_id, game_short_name, disable_notification,
                              protect_content, reply_to_message_id, allow_sending_without_reply, reply_markup))

    def set_game_score(self, user_id, score, force=False, disable_edit_message=False, chat_id=None, message_id=None,
                       inline_message_id=None):
        """
        Use this method to set the score of the specified user in a game
        :param int user_id: Unique identifier of the target user
        :param int score: New score, must be non-negative
        :param bool force: Pass True, if the high score is allowed to decrease
        :param bool disable_edit_message: Game message shouldn't be automatically edited
        :param int chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat
        :param int or None message_id: Required if inline_message_id is not specified,Identifier of the message to edit
        :param str or None inline_message_id: Required if chat_id and message_id are not specified
        :return: On success a Message object, otherwise returns True
        :rtype: types.Message or bool
        """
        result = methods.set_game_score(self.__api_url, self.__proxies, user_id, score, force, disable_edit_message,
                                        chat_id, message_id,
                                        inline_message_id)
        if type(result) is bool:
            return result
        return types.Message.de_json(result)

    def get_game_high_scores(self, user_id, chat_id=None, message_id=None, inline_message_id=None):
        """
        Use this method to get data for high score tables
        :param int user_id: Unique identifier of the target user
        :param int or None chat_id: Required if inline_message_id is not specified,Unique identifier for the target chat
        :param int or None message_id: Required if inline_message_id is not specified,Identifier of the message to edit
        :param str or None inline_message_id: Required if chat_id and message_id are not specified
        :return: an Array of GameHighScore objects
        :rtype: list[types.GameHighScore]
        """
        resp = methods.get_game_high_scores(self.__api_url, self.__proxies, user_id, chat_id, message_id,
                                            inline_message_id)
        result = []
        for x in resp:
            result.append(types.GameHighScore.de_json(x))
        return result
