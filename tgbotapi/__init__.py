import threading
import pickle
import os
from .utils import ThreadPool, logger, WorkerThread, OrEvent, extract_command, async_dec
from . import methods, types
import time
import six
import re

"""
Module : tgbotapi
"""


class Handler:
    """
    Class for (next step|reply) handlers
    """

    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def __getitem__(self, item):
        return getattr(self, item)


class Saver:
    """
    Class for saving (next step|reply) handlers
    """

    def __init__(self, handlers, filename, delay):
        self.handlers = handlers
        self.filename = filename
        self.delay = delay
        self.timer = threading.Timer(delay, self.save_handlers)

    def start_save_timer(self):
        if not self.timer.is_alive():
            if self.delay <= 0:
                self.save_handlers()
            else:
                self.timer = threading.Timer(self.delay, self.save_handlers)
                self.timer.start()

    def save_handlers(self):
        self.dump_handlers(self.handlers, self.filename)

    def load_handlers(self, filename, del_file_after_loading=True):
        tmp = self.return_load_handlers(
            filename, del_file_after_loading=del_file_after_loading)
        if tmp is not None:
            self.handlers.update(tmp)

    @staticmethod
    def dump_handlers(handlers, filename, file_mode="wb"):
        dirs = filename.rsplit('/', maxsplit=1)[0]
        os.makedirs(dirs, exist_ok=True)

        with open(filename + ".tmp", file_mode) as file:
            pickle.dump(handlers, file)

        if os.path.isfile(filename):
            os.remove(filename)

        os.rename(filename + ".tmp", filename)

    @staticmethod
    def return_load_handlers(filename, del_file_after_loading=True):
        if os.path.isfile(filename) and os.path.getsize(filename) > 0:
            with open(filename, "rb") as file:
                handlers = pickle.load(file)

            if del_file_after_loading:
                os.remove(filename)

            return handlers


class TBot:
    """ This is TBot Class """

    def __init__(self, token, threaded=True, skip_pending=False, num_threads=2, proxies=None):
        """
        :param str token: Required, The bot's API token. (Created with @BotFather)
        :param bool threaded:
        :param bool skip_pending:
        :param int num_threads:
        :param dict or None proxies:
        :return: a Tbot object.
        :rtype: TBot
        """

        self.__token = token
        self.__proxies = proxies
        self.__threaded = threaded
        self.__skip_pending = skip_pending
        if self.__threaded:
            self.__worker_pool = ThreadPool(num_threads=num_threads)

        self.__update_listener = []
        self.__stop_polling = threading.Event()
        self.__last_update_id = 0
        self.__exc_info = None

        # key: message_id, value: handler list
        self.__reply_handlers = {}

        # key: chat_id, value: handler list
        self.__next_step_handlers = {}
        self.__next_step_saver = None
        self.__reply_saver = None

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

    def get_updates(self, offset=None, limit=None, timeout=20, allowed_updates=None):
        """
        Use this method to receive incoming updates using long polling.
        :param int or None offset: Identifier of the first update to be returned.
        :param int or None limit: Limits the number of updates to be retrieved.
        :param int or None timeout: Timeout in seconds for long polling, Defaults to 0.
        :param list or None allowed_updates: An Array of String.
        :return: An Array of Update objects.
        :rtype: list[types.Update]
        """
        json_updates = methods.get_updates(self.__token, self.__proxies, offset, limit, timeout, allowed_updates)
        updates = []
        for x in json_updates:
            updates.append(types.Update.de_json(x))
        return updates

    def __skip_updates(self):
        """
        Get and discard all pending updates before first poll of the bot
        :return: total updates skipped
        """
        total = 0
        updates = self.get_updates(offset=self.__last_update_id, timeout=1)
        while updates:
            total += len(updates)
            for update in updates:
                if update.update_id > self.__last_update_id:
                    self.__last_update_id = update.update_id
            updates = self.get_updates(
                offset=self.__last_update_id + 1, timeout=1)
        return total

    def __retrieve_updates(self, timeout=20):
        """
        Retrieves any updates from the Telegram API.
        Registered listeners and applicable message handlers will be notified when a new message arrives.
        :raises ApiException when a call has failed.
        """
        if self.__skip_pending:
            logger.debug('Skipped {0} pending messages'.format(
                self.__skip_updates()))
            self.__skip_pending = False
        updates = self.get_updates(offset=(self.__last_update_id + 1), timeout=timeout)
        self.__process_new_updates(updates)

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
        new_poll = []
        new_poll_answer = []

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
                new_poll.append(update.poll)
            if update.poll_answer:
                new_poll_answer.append(update.poll_answer)

        logger.debug('Received {0} new updates'.format(len(updates)))
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
        if len(new_poll) > 0:
            self.__process_new_poll(new_poll)
        if len(new_poll_answer) > 0:
            self.__process_new_poll_answer(new_poll_answer)

    def __process_new_messages(self, new_messages):
        self._notify_next_handlers(new_messages)
        self._notify_reply_handlers(new_messages)
        self.__notify_update(new_messages)
        self._notify_command_handlers(self.__message_handlers, new_messages)

    def __process_new_edited_messages(self, edited_message):
        self._notify_command_handlers(
            self.__edited_message_handlers, edited_message)

    def __process_new_channel_posts(self, channel_post):
        self._notify_command_handlers(self.__channel_post_handlers, channel_post)

    def __process_new_edited_channel_posts(self, edited_channel_post):
        self._notify_command_handlers(
            self.__edited_channel_post_handlers, edited_channel_post)

    def __process_new_inline_query(self, new_inline_queries):
        self._notify_command_handlers(self.__inline_query_handlers, new_inline_queries)

    def __process_new_chosen_inline_query(self, new_chosen_inline_queries):
        self._notify_command_handlers(
            self.__chosen_inline_handlers, new_chosen_inline_queries)

    def __process_new_callback_query(self, new_callback_queries):
        self._notify_command_handlers(
            self.__callback_query_handlers, new_callback_queries)

    def __process_new_shipping_query(self, new_shipping_queries):
        self._notify_command_handlers(
            self.__shipping_query_handlers, new_shipping_queries)

    def __process_new_pre_checkout_query(self, pre_checkout_queries):
        self._notify_command_handlers(
            self.__pre_checkout_query_handlers, pre_checkout_queries)

    def __process_new_poll(self, poll):
        self._notify_command_handlers(self.__poll_handlers, poll)

    def __process_new_poll_answer(self, poll_answer):
        self._notify_command_handlers(self.__poll_answer_handlers, poll_answer)

    def __notify_update(self, new_messages):
        for listener in self.__update_listener:
            self._exec_task(listener, new_messages)

    def infinity_polling(self, timeout=20, *args, **kwargs):
        while not self.__stop_polling.is_set():
            try:
                self.polling(timeout=timeout, *args, **kwargs)
            except ConnectionError or ConnectionAbortedError or ConnectionRefusedError or ConnectionResetError:
                time.sleep(timeout)
                pass
        logger.info("Break infinity polling")

    def polling(self, none_stop=False, interval=0, timeout=20):
        """
        This function creates a new Thread that calls an internal __retrieve_updates function.
        This allows the bot to retrieve Updates automatically and notify listeners and message handlers accordingly.

        Warning: Do not call this function more than once!

        Always get updates.
        :param none_stop: Boolean: Do not stop polling when an ApiException occurs.
        :param interval: Integer:
        :param timeout: Integer: Timeout in seconds for long polling.
        :return:
        """
        if self.__threaded:
            self.__threaded_polling(none_stop, interval, timeout)
        else:
            self.__non_threaded_polling(none_stop, interval, timeout)

    def __threaded_polling(self, none_stop=False, interval=0, timeout=3):
        logger.info('Started polling.')
        self.__stop_polling.clear()
        error_interval = 0.25

        polling_thread = WorkerThread(name="PollingThread")
        or_event = OrEvent(
            polling_thread.done_event,
            polling_thread.exception_event,
            self.__worker_pool.exception_event
        )

        while not self.__stop_polling.wait(interval):
            or_event.clear()
            try:
                polling_thread.put(self.__retrieve_updates, timeout)

                or_event.wait()  # wait for polling thread finish, polling thread error or thread pool error

                polling_thread.raise_exceptions()
                self.__worker_pool.raise_exceptions()

                error_interval = 0.25
            except methods.ApiException as e:
                logger.error(e)
                if not none_stop:
                    self.__stop_polling.set()
                    logger.info("Exception occurred. Stopping.")
                else:
                    polling_thread.clear_exceptions()
                    self.__worker_pool.clear_exceptions()
                    logger.info(
                        "Waiting for {0} seconds until retry".format(error_interval))
                    time.sleep(error_interval)
                    error_interval *= 2
            except KeyboardInterrupt:
                logger.info("KeyboardInterrupt received.")
                self.__stop_polling.set()
                break

        polling_thread.stop()
        logger.info('Stopped polling.')

    def __non_threaded_polling(self, none_stop=False, interval=0, timeout=3):
        logger.info('Started polling.')
        self.__stop_polling.clear()
        error_interval = 0.25

        while not self.__stop_polling.wait(interval):
            try:
                self.__retrieve_updates(timeout)
                error_interval = 0.25
            except methods.ApiException as e:
                logger.error(e)
                if not none_stop:
                    self.__stop_polling.set()
                    logger.info("Exception occurred. Stopping.")
                else:
                    logger.info(
                        "Waiting for {0} seconds until retry".format(error_interval))
                    time.sleep(error_interval)
                    error_interval *= 2
            except KeyboardInterrupt:
                logger.info("KeyboardInterrupt received.")
                self.__stop_polling.set()
                break

        logger.info('Stopped polling.')

    def _exec_task(self, task, *args, **kwargs):
        if self.__threaded:
            self.__worker_pool.put(task, *args, **kwargs)
        else:
            task(*args, **kwargs)

    def stop_polling(self):
        self.__stop_polling.set()

    def stop_bot(self):
        self.stop_polling()
        if self.__worker_pool:
            self.__worker_pool.close()

    def set_update_listener(self, listener):
        self.__update_listener.append(listener)

    def set_webhook(self, url=None, certificate=None, max_connections=40, allowed_updates=None):
        """
        Use this method to specify a url and receive incoming updates via an outgoing webhook.
        :param str url: HTTPS url to send updates to. Use an empty string to remove webhook integration.
        :param any or None certificate: Upload your public key [InputFile] certificate so that the root certificate in use can be checked.
        :param int max_connections: Maximum allowed number of simultaneous HTTPS connections to the webhook for update delivery, 1-100. Defaults to 40.
        :param list or None allowed_updates: A JSON-serialized list of the update types you want your bot to receive.
        :return: True On success.
        :rtype: dict
        """
        return methods.set_webhook(self.__token, self.__proxies, url, certificate, max_connections, allowed_updates)

    def delete_webhook(self):
        """
        Use this method to remove webhook integration if you decide to switch back to getUpdates.
        :return: True on success.
        :rtype: dict
        """
        return methods.delete_webhook(self.__token, self.__proxies)

    def get_webhook_info(self):
        """
        Use this method to get current webhook status.
        :return: a WebhookInfo object, otherwise an object with the url field empty.
        :rtype: types.WebhookInfo
        """
        return types.WebhookInfo.de_json(methods.get_webhook_info(self.__token, self.__proxies))

    def get_me(self):
        """
        A simple method for testing your bot's auth token.
        :return: a User object.
        :rtype: types.User
        """
        return types.User.de_json(methods.get_me(self.__token, self.__proxies))

    def send_message(self, chat_id, text, parse_mode=None, disable_web_page_preview=False, disable_notification=False,
                     reply_to_message_id=None, reply_markup=None):
        """
        Use this method to send text messages. On success, the sent Message is returned.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param str text: Text of the message to be sent, 1-4096 characters after entities parsing.
        :param str or None parse_mode: Send Markdown or HTML.
        :param bool disable_web_page_preview: Disables link previews for links in this message.
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message.
        :param dict or None reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
        :return: a Message object.
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_message(self.__token, self.__proxies, chat_id, text, parse_mode, disable_web_page_preview,
                                 disable_notification, reply_to_message_id, reply_markup))

    def forward_message(self, chat_id, from_chat_id, message_id, disable_notification=False):
        """
        Use this method to forward messages of any kind.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param int or str from_chat_id: Unique identifier for the chat where the original message was sent.
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param int message_id: Message identifier in the chat specified in from_chat_id.
        :return: a Message object.
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.forward_message(self.__token, self.__proxies, chat_id, from_chat_id, message_id,
                                    disable_notification))

    def send_photo(self, chat_id, photo, caption=None, parse_mode=None, disable_notification=False,
                   reply_to_message_id=None, reply_markup=None):
        """
        Use this method to send photos.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param any photo: Photo [file_id or InputFile] to send.
        :param str or None caption: Photo caption, 0-1024 characters after entities parsing
        :param str or None parse_mode: Send Markdown or HTML.
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message.
        :param dict or None reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
        :return: a Message object.
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_photo(self.__token, self.__proxies, chat_id, photo, caption, parse_mode, disable_notification,
                               reply_to_message_id, reply_markup))

    def send_audio(self, chat_id, audio, caption=None, parse_mode=None, duration=None, performer=None, title=None,
                   thumb=None, disable_notification=False, reply_to_message_id=None, reply_markup=None):
        """
        Use this method to send audio files.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param any audio: Audio [file_id or InputFile] to send.
        :param str or None caption: Photo caption, 0-1024 characters after entities parsing
        :param str or None parse_mode: Send Markdown or HTML.
        :param int or None duration: Duration of the audio in seconds.
        :param str or None performer: Performer.
        :param str or None title: Track Name.
        :param any or None thumb: Thumbnail [file_id or InputFile] of the file sent.
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message.
        :param dict or None reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
        :return: a Message object.
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_audio(self.__token, self.__proxies, chat_id, audio, caption, parse_mode, duration, performer,
                               title, thumb,
                               disable_notification, reply_to_message_id, reply_markup))

    def send_document(self, chat_id, document, thumb=None, caption=None, parse_mode=None, disable_notification=False,
                      reply_to_message_id=None, reply_markup=None):
        """
        Use this method to send general files.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param any document: File [file_id or InputFile] to send.
        :param any or None thumb: Thumbnail [file_id or InputFile] of the file sent.
        :param str or None caption: Document caption, 0-1024 characters after entities parsing
        :param str or None parse_mode: Send Markdown or HTML.
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message.
        :param dict or None reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
        :return: a Message object.
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_document(self.__token, self.__proxies, chat_id, document, thumb, caption, parse_mode,
                                  disable_notification,
                                  reply_to_message_id, reply_markup))

    def send_video(self, chat_id, video, duration=None, width=None, height=None, thumb=None, caption=None,
                   parse_mode=None, supports_streaming=None, disable_notification=False, reply_to_message_id=None,
                   reply_markup=None):
        """
        Use this method to send video files.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param any video: Video [file_id or InputFile] to send.
        :param int or None duration: Duration of the video in seconds.
        :param int or None width: Video width.
        :param int or None height: Video height.
        :param any or None thumb: Thumbnail [file_id or InputFile] of the file sent.
        :param str or None caption: Video caption, 0-1024 characters after entities parsing.
        :param str or None parse_mode: Send Markdown or HTML.
        :param bool supports_streaming: Pass True, if the uploaded video is suitable for streaming.
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message.
        :param dict or None reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
        :return: a Message object.
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_video(self.__token, self.__proxies, chat_id, video, duration, width, height, thumb, caption,
                               parse_mode,
                               supports_streaming, disable_notification, reply_to_message_id, reply_markup))

    def send_animation(self, chat_id, animation, duration=None, width=None, height=None, thumb=None, caption=None,
                       parse_mode=None, disable_notification=False, reply_to_message_id=None, reply_markup=None):
        """
        Use this method to send animation files.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param any animation: Animation [file_id or InputFile] to send.
        :param int or None duration: Duration of the animation in seconds.
        :param int or None width: Animation width.
        :param int or None height: Animation height.
        :param any or None thumb: Thumbnail [file_id or InputFile] of the file sent.
        :param str or None caption: Video caption, 0-1024 characters after entities parsing.
        :param str or None parse_mode: Send Markdown or HTML.
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message.
        :param dict or None reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
        :return: a Message object.
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_animation(self.__token, self.__proxies, chat_id, animation, duration, width, height, thumb,
                                   caption,
                                   parse_mode,
                                   disable_notification, reply_to_message_id, reply_markup))

    def send_voice(self, chat_id, voice, caption=None, parse_mode=None, duration=None, disable_notification=False,
                   reply_to_message_id=None, reply_markup=None):
        """
        Use this method to send audio files.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param any voice: Audio [file_id or InputFile] to send.
        :param str or None caption: Voice caption, 0-1024 characters after entities parsing.
        :param str or None parse_mode: Send Markdown or HTML.
        :param int or None duration: Duration of the voice in seconds.
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message.
        :param dict or None reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
        :return: a Message object.
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_voice(self.__token, self.__proxies, chat_id, voice, caption, parse_mode, duration,
                               disable_notification,
                               reply_to_message_id, reply_markup))

    def send_video_note(self, chat_id, video_note, duration=None, length=None, thumb=None, disable_notification=False,
                        reply_to_message_id=None, reply_markup=None):
        """
        Use this method to send video messages.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param any video_note: Video note [file_id or InputFile] to send.
        :param int or None duration: Duration of the VideoNote in seconds.
        :param int or None length: Video width and height, i.e. diameter of the video message.
        :param any or None thumb: Thumbnail [file_id or InputFile] of the file sent.
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message.
        :param dict or None reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
        :return: a Message object.
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_video_note(self.__token, self.__proxies, chat_id, video_note, duration, length, thumb,
                                    disable_notification,
                                    reply_to_message_id, reply_markup))

    def send_media_group(self, chat_id, media, disable_notification=False, reply_to_message_id=None):
        """
        Use this method to send a group of photos or videos as an album.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param list media: A JSON-serialized array of [InputMediaPhoto or InputMediaVideo] to be sent, must include 2–10 items
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message.
        :return: a Messages object.
        :rtype: types.Message
        """
        result = methods.send_media_group(
            self.__token, self.__proxies, chat_id, media, disable_notification, reply_to_message_id)
        ret = []
        for msg in result:
            ret.append(types.Message.de_json(msg))
        return ret

    def send_location(self, chat_id, latitude, longitude, live_period=None, disable_notification=False,
                      reply_to_message_id=None, reply_markup=None):
        """
        Use this method to send point on the map.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param float latitude: Latitude of the location.
        :param float longitude: Longitude of the location.
        :param int or None live_period: Period in seconds for which the location will be updated, should be between 60 and 86400.
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message.
        :param dict or None reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
        :return: a Message object.
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_location(self.__token, self.__proxies, chat_id, latitude, longitude, live_period,
                                  disable_notification,
                                  reply_to_message_id, reply_markup))

    def edit_message_live_location(self, latitude, longitude, chat_id=None, message_id=None, inline_message_id=None,
                                   reply_markup=None):
        """
        Use this method to edit live location messages.
        :param int or str chat_id: Required if inline_message_id is not specified, Unique identifier for the target chat.
        :param int or None message_id: Required if inline_message_id is not specified, Identifier of the message to edit.
        :param str or None inline_message_id: Required if chat_id and message_id are not specified, Identifier of the inline message.
        :param float latitude: Latitude of the location.
        :param float longitude: Longitude of the location.
        :param dict reply_markup: A JSON-serialized object for an InlineKeyboardMarkup.
        :return: a Message object, otherwise True.
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.edit_message_live_location(self.__token, self.__proxies, latitude, longitude, chat_id, message_id,
                                               inline_message_id, reply_markup))

    def stop_message_live_location(self, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        """
        Use this method to stop updating a live location message before live_period expires.
        :param int or str chat_id: Required if inline_message_id is not specified, Unique identifier for the target chat.
        :param int or None message_id: Required if inline_message_id is not specified, Identifier of the message to edit.
        :param str or None inline_message_id: Required if chat_id and message_id are not specified, Identifier of the inline message.
        :param dict reply_markup: A JSON-serialized object for an InlineKeyboardMarkup.
        :return: a Message object, otherwise True.
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.stop_message_live_location(self.__token, self.__proxies, chat_id, message_id, inline_message_id,
                                               reply_markup))

    def send_venue(self, chat_id, latitude, longitude, title, address, foursquare_id=None, foursquare_type=None,
                   disable_notification=False, reply_to_message_id=None, reply_markup=None):
        """
        Use this method to send information about a venue.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param float latitude: Latitude of the location.
        :param float longitude: Longitude of the location.
        :param str or None title: Name of the venue.
        :param str address: Address of the venue.
        :param str or None foursquare_id: Foursquare identifier of the venue.
        :param str or None foursquare_type: Foursquare type of the venue, if known.
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message.
        :param dict or None reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
        :return: a Message object.
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_venue(self.__token, self.__proxies, chat_id, latitude, longitude, title, address,
                               foursquare_id,
                               foursquare_type,
                               disable_notification, reply_to_message_id, reply_markup))

    def send_contact(self, chat_id, phone_number, first_name, last_name=None, vcard=None, disable_notification=False,
                     reply_to_message_id=None, reply_markup=None):
        """
        Use this method to send phone contacts.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param str phone_number: Contact's phone number.
        :param str first_name: Contact's first name.
        :param str or None last_name: Contact's last name.
        :param str or None vcard: Additional data about the contact in the form of a vCard, 0-2048 bytes.
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message.
        :param dict or None reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
        :return: a Message object.
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_contact(self.__token, self.__proxies, chat_id, phone_number, first_name, last_name, vcard,
                                 disable_notification,
                                 reply_to_message_id, reply_markup))

    def send_poll(self, chat_id, question, options, is_anonymous=True, type='regular', allows_multiple_answers=False,
                  correct_option_id=None, explanation=None, explanation_parse_mode=None, open_period=None,
                  close_date=None, is_closed=True, disable_notifications=False, reply_to_message_id=None,
                  reply_markup=None):
        """
        Use this method to send a native poll.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param str question: Poll question, 1-255 characters.
        :param list options: A JSON-serialized list of answer options, 2-10 strings 1-100 characters each.
        :param bool is_anonymous: True, if the poll needs to be anonymous, defaults to True.
        :param str or None type: Poll type, “quiz” or “regular”, defaults to “regular”.
        :param bool allows_multiple_answers: True, if the poll allows multiple answers, ignored for polls in quiz mode, defaults to False.
        :param int or None correct_option_id: 0-based identifier of the correct answer option, required for polls in quiz mode.
        :param str or None explanation: Text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style poll.
        :param str or None explanation_parse_mode: Mode for parsing entities in the explanation.
        :param int or None open_period: Amount of time in seconds the poll will be active after creation, 5-600. Can't be used together with close_date.
        :param int or None close_date: Point in time (Unix timestamp) when the poll will be automatically closed. Must be at least 5 and no more than 600 seconds in the future. Can't be used together with open_period.
        :param bool is_closed: Pass True, if the poll needs to be immediately closed. This can be useful for poll preview.
        :param bool disable_notifications: Sends the message silently. Users will receive a notification with no sound.
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message.
        :param dict or None reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
        :return: a Message object.
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_poll(self.__token, self.__proxies, chat_id, question, options, is_anonymous, type,
                              allows_multiple_answers, correct_option_id, explanation, explanation_parse_mode,
                              open_period, close_date, is_closed, disable_notifications, reply_to_message_id,
                              reply_markup))

    def send_dice(self, chat_id, emoji='🎲', disable_notification=False, reply_to_message_id=None, reply_markup=None):
        """
        Use this method to send a dice.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param str or None emoji: Emoji on which the dice throw animation is based. Currently, must be one of “🎲” or “🎯”, Defaults to “🎲” .
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message.
        :param dict or None reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
        :return: a Message object.
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_dice(self.__token, self.__proxies, chat_id, emoji, disable_notification, reply_to_message_id,
                              reply_markup))

    def send_chat_action(self, chat_id, action):
        """
        Use this method when you need to tell the user that something is happening on the bot's side.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param str action: Type of action to broadcast.
        :return: True On success.
        :rtype: types.Message
        """
        return methods.send_chat_action(self.__token, self.__proxies, chat_id, action)

    def get_user_profile_photos(self, user_id, offset=None, limit=100):
        """
        Use this method to get a list of profile pictures for a user.
        :param int or str user_id: Unique identifier of the target user.
        :param int or None offset: Sequential number of the first photo to be returned. By default, all photos are returned.
        :param int or None limit: Limits the number of photos to be retrieved. Values between 1—100 are accepted. Defaults to 100.
        :return: a UserProfilePhoto object.
        :rtype: types.Message
        """
        return types.UserProfilePhotos.de_json(
            methods.get_user_profile_photos(self.__token, self.__proxies, user_id, offset, limit))

    def get_file(self, file_id):
        """
        Use this method to get basic info about a file and prepare it for downloading.
        :param str file_id: File identifier to get info about
        :return: a File object.
        :rtype: types.File
        """
        return types.File.de_json(methods.get_file(self.__token, self.__proxies, file_id))

    def download_file(self, file_path):
        """
        Use this method to download file with specified file_path.
        :param str file_path: File path, User https://api.telegram.org/file/bot<token>/<file_path> to get the file.
        :return: any, On success.
        :rtype: bytearray
        """
        return methods.download_file(self.__token, self.__proxies, file_path)

    def kick_chat_member(self, chat_id, user_id, until_date=None):
        """
        Use this method to kick a user from a group, a supergroup or a channel.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param int user_id: Unique identifier of the target user.
        :param int or None until_date: Date when the user will be unbanned, unix time.
        :return: True On success.
        :rtype: dict
        """
        return methods.kick_chat_member(self.__token, self.__proxies, chat_id, user_id, until_date)

    def unban_chat_member(self, chat_id, user_id):
        """
        Use this method to unban a previously kicked user in a supergroup or channel.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param int user_id: Unique identifier of the target user.
        :return: True On success.
        :rtype: dict
        """
        return methods.unban_chat_member(self.__token, self.__proxies, chat_id, user_id)

    def restrict_chat_member(self, chat_id, user_id, permissions, until_date=None):
        """
        Use this method to restrict a user in a supergroup.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param int user_id: Unique identifier of the target user.
        :param dict permissions: New user permissions must be ChatPermissions object.
        :param int or None until_date: 	Date when restrictions will be lifted for the user, unix time.
        :return: True On success.
        :rtype: dict
        """
        return methods.restrict_chat_member(self.__token, self.__proxies, chat_id, user_id, permissions, until_date)

    def promote_chat_member(self, chat_id, user_id, can_change_info=None, can_post_messages=None,
                            can_edit_messages=None, can_delete_messages=None, can_invite_users=None,
                            can_restrict_members=None, can_pin_messages=None, can_promote_members=None):
        """
        Use this method to promote or demote a user in a supergroup or a channel.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param int user_id: Unique identifier of the target user.
        :param bool can_change_info: Pass True, if the administrator can change chat title, photo and other settings.
        :param bool can_post_messages: Pass True, if the administrator can create channel posts, channels only.
        :param bool can_edit_messages: Pass True, if the administrator can edit messages of other users and can pin messages, channels only.
        :param bool can_delete_messages: Pass True, if the administrator can delete messages of other users.
        :param bool can_invite_users: Pass True, if the administrator can invite new users to the chat.
        :param bool can_restrict_members: Pass True, if the administrator can restrict, ban or unban chat members.
        :param bool can_pin_messages: Pass True, if the administrator can pin messages, supergroups only.
        :param bool can_promote_members: Pass True, if the administrator can add new administrators with a subset of his own privileges or demote administrators that he has promoted, directly or indirectly (promoted by administrators that were appointed by him).
        :return: True On success.
        :rtype: dict
        """
        return methods.promote_chat_member(self.__token, self.__proxies, chat_id, user_id, can_change_info,
                                           can_post_messages,
                                           can_edit_messages, can_delete_messages, can_invite_users,
                                           can_restrict_members, can_pin_messages, can_promote_members)

    def set_chat_administrator_custom_title(self, chat_id, user_id, custom_title):
        """
        Use this method to set a custom title for an administrator in a supergroup promoted by the bot.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param int user_id: Unique identifier of the target user.
        :param str custom_title: New custom title for the administrator; 0-16 characters.
        :return: True on success.
        :rtype: dict
        """
        return methods.set_chat_administrator_custom_title(self.__token, self.__proxies, chat_id, user_id, custom_title)

    def set_chat_permissions(self, chat_id, permissions):
        """
        Use this method to set default chat permissions for all members.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param dict permissions: New default chat permissions must be a ChatPermissions object
        :return: True on success.
        :rtype: dict
        """
        return methods.set_chat_permissions(self.__token, self.__proxies, chat_id, permissions)

    def export_chat_invite_link(self, chat_id):
        """
        Use this method to generate a new invite link for a chat.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :return: new link as String on success.
        :rtype: dict
        """
        return methods.export_chat_invite_link(self.__token, self.__proxies, chat_id)

    def set_chat_photo(self, chat_id, photo):
        """
        Use this method to set a new profile photo for the chat.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param any photo: Use this method to set a new profile photo for the chat.
        :return: True on success.
        :rtype: dict
        """
        return methods.set_chat_photo(self.__token, self.__proxies, chat_id, photo)

    def delete_chat_photo(self, chat_id):
        """
        Use this method to delete a chat photo.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :return: True on success.
        :rtype: dict
        """
        return methods.delete_chat_photo(self.__token, self.__proxies, chat_id)

    def set_chat_title(self, chat_id, title):
        """
        Use this method to change the title of a chat.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param str title: New chat title, 1-255 characters.
        :return: True on success.
        :rtype: dict
        """
        return methods.set_chat_title(self.__token, self.__proxies, chat_id, title)

    def set_chat_description(self, chat_id, description):
        """
        Use this method to change the description of a group, a supergroup or a channel.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param str description: New chat description, 0-255 characters.
        :return: True on success.
        :rtype: dict
        """
        return methods.set_chat_description(self.__token, self.__proxies, chat_id, description)

    def pin_chat_message(self, chat_id, message_id, disable_notification=False):
        """
        Use this method to pin a message in a group, a supergroup, or a channel.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param int message_id: Identifier of a message to pin.
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :return: True on success.
        :rtype: dict
        """
        return methods.pin_chat_message(self.__token, self.__proxies, chat_id, message_id, disable_notification)

    def unpin_chat_message(self, chat_id):
        """
        Use this method to unpin a message in a group, a supergroup, or a channel.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :return: True on success.
        :rtype: dict
        """
        return methods.unpin_chat_message(self.__token, self.__proxies, chat_id)

    def leave_chat(self, chat_id):
        """
        Use this method for your bot to leave a group, supergroup or channel.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :return: True on success.
        :rtype: dict
        """
        return methods.leave_chat(self.__token, self.__proxies, chat_id)

    def get_chat(self, chat_id):
        """
        Use this method to get up to date information about the chat.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :return: a Chat object.
        :rtype: types.Chat
        """
        return types.Chat.de_json(methods.get_chat(self.__token, self.__proxies, chat_id))

    def get_chat_administrators(self, chat_id):
        """
        Use this method to get a list of administrators in a chat.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :return: an Array of ChatMember object.
        :rtype: list[types.ChatMember]
        """
        result = methods.get_chat_administrators(self.__token, self.__proxies, chat_id)
        ret = []
        for r in result:
            ret.append(types.ChatMember.de_json(r))
        return ret

    def get_chat_members_count(self, chat_id):
        """
        Use this method to get the number of members in a chat.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :return: Integer On success.
        :rtype: dict
        """
        return methods.get_chat_members_count(self.__token, self.__proxies, chat_id)

    def get_chat_member(self, chat_id, user_id):
        """
        Use this method to get information about a member of a chat.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param int user_id: Unique identifier of the target user.
        :return: a ChatMember object On success.
        :rtype: types.ChatMember
        """
        return types.ChatMember.de_json(methods.get_chat_member(self.__token, self.__proxies, chat_id, user_id))

    def set_chat_sticker_set(self, chat_id, sticker_set_name):
        """
        Use this method to set a new group sticker set for a supergroup.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param str sticker_set_name: Name of the sticker set to be set as the group sticker set.
        :return: True On success.
        :rtype: dict
        """
        return methods.set_chat_sticker_set(self.__token, self.__proxies, chat_id, sticker_set_name)

    def delete_chat_sticker_set(self, chat_id):
        """
        Use this method to delete a group sticker set from a supergroup.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :return: True On success.
        :rtype: dict
        """
        return methods.delete_chat_sticker_set(self.__token, self.__proxies, chat_id)

    def answer_callback_query(self, callback_query_id, text=None, show_alert=False, url=None, cache_time=None):
        """
        Use this method to send answers to callback queries sent from inline keyboards.
        :param str callback_query_id: Unique identifier for the query to be answered.
        :param str or None text: Text of the notification. If not specified, nothing will be shown to the user, 0-200 characters.
        :param bool show_alert: If true, an alert will be shown by the client instead of a notification at the top of the chat screen. Defaults to false.
        :param str or None url: URL that will be opened by the user's client.
        :param int or None cache_time: The maximum amount of time in seconds that the result of the callback query may be cached client-side.
        :return: True On success.
        :rtype: dict
        """
        return methods.answer_callback_query(self.__token, self.__proxies, callback_query_id, text, show_alert, url,
                                             cache_time)

    def set_my_commands(self, commands):
        """
        Use this method to change the list of the bot's commands.
        :param list commands: A JSON-serialized list of bot commands to be set as the list of the bot's commands. At most 100 commands can be specified.
        :return: True On success.
        :rtype: dict
        """
        return methods.set_my_commands(self.__token, self.__proxies, commands)

    def get_my_commands(self):
        """
        Use this method to get the current list of the bot's commands.
        :return: Array of BotCommand On success.
        :rtype: tgbotapi.types.BotCommand
        """
        return methods.get_my_commands(self.__token, self.__proxies)

    def edit_message_text(self, text, chat_id=None, message_id=None, inline_message_id=None, parse_mode=None,
                          disable_web_page_preview=False, reply_markup=None):
        """
        Use this method to edit text and game messages.
        :param int or str chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat.
        :param int or None message_id: Required if inline_message_id is not specified. Identifier of the message to edit.
        :param str or None inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
        :param str text: Text of the message to be sent, 1-4096 characters after entities parsing.
        :param str or None parse_mode: Send Markdown or HTML.
        :param bool disable_web_page_preview: Disables link previews for links in this message
        :param types.InlineKeyboardMarkup or None reply_markup: A JSON-serialized object for an InlineKeyboardMarkup.
        :return: a Message object On success, otherwise True.
        :rtype: types.Message or dict
        """
        result = methods.edit_message_text(self.__token, self.__proxies, text, chat_id, message_id, inline_message_id,
                                           parse_mode,
                                           disable_web_page_preview, reply_markup)
        # if edit inline message return is bool not Message.
        if type(result) == bool:
            return result
        return types.Message.de_json(result)

    def edit_message_caption(self, caption, chat_id=None, message_id=None, inline_message_id=None, parse_mode=None,
                             reply_markup=None):
        """
        Use this method to edit captions of messages.
        :param int or str chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat.
        :param int or None message_id: Required if inline_message_id is not specified. Identifier of the message to edit.
        :param str or None inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
        :param str or None caption: New caption of the message, 0-1024 characters after entities parsing.
        :param str or None parse_mode: Send Markdown or HTML.
        :param types.InlineKeyboardMarkup or None reply_markup: A JSON-serialized object for an InlineKeyboardMarkup.
        :return: a Message object On success, otherwise True.
        :rtype: tgbotapi.types.Message or dict
        """
        result = methods.edit_message_caption(self.__token, self.__proxies, caption, chat_id, message_id,
                                              inline_message_id, parse_mode,
                                              reply_markup)
        if type(result) == bool:
            return result
        return types.Message.de_json(result)

    def edit_message_media(self, media, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        """
        Use this method to edit animation, audio, document, photo, or video messages.
        :param int or str chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat.
        :param int or None message_id: Required if inline_message_id is not specified. Identifier of the message to edit.
        :param str or None inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
        :param any media: A JSON-serialized object for a new media content of the message must be InputMedia.
        :param types.InlineKeyboardMarkup or None reply_markup: A JSON-serialized object for an InlineKeyboardMarkup.:
        :return: a Message object On success, otherwise True.
        :rtype: types.Message or dict
        """
        result = methods.edit_message_media(
            self.__token, self.__proxies, media, chat_id, message_id, inline_message_id, reply_markup)
        # if edit inline message return is bool not Message.
        if type(result) == bool:
            return result
        return types.Message.de_json(result)

    def edit_message_reply_markup(self, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        """
        Use this method to edit only the reply markup of messages.
        :param int or str chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat.
        :param int or None message_id: Required if inline_message_id is not specified. Identifier of the message to edit.
        :param str or None inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
        :param types.InlineKeyboardMarkup or None reply_markup: A JSON-serialized object for an InlineKeyboardMarkup.
        :return: a Message object On success, otherwise True.
        :rtype: types.Message or dict
        """
        result = methods.edit_message_reply_markup(
            self.__token, self.__proxies, chat_id, message_id, inline_message_id, reply_markup)
        if type(result) == bool:
            return result
        return types.Message.de_json(result)

    def stop_poll(self, chat_id, message_id, reply_markup=None):
        """
        Use this method to stop a poll which was sent by the bot.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param int or None message_id: Identifier of the original message with the poll.
        :param types.InlineKeyboardMarkup or None reply_markup: A JSON-serialized object for an InlineKeyboardMarkup.
        :return: a Poll object On success.
        :rtype: tgbotapi.types.Poll
        """
        return types.Poll.de_json(methods.stop_poll(self.__token, self.__proxies, chat_id, message_id, reply_markup))

    def delete_message(self, chat_id, message_id):
        """
        Use this method to delete a message, including service messages, with the following limitations:
            - A message can only be deleted if it was sent less than 48 hours ago.
            - A dice message in a private chat can only be deleted if it was sent more than 24 hours ago.
            - Bots can delete outgoing messages in private chats, groups, and supergroups.
            - Bots can delete incoming messages in private chats.
            - Bots granted can_post_messages permissions can delete outgoing messages in channels.
            - If the bot is an administrator of a group, it can delete any message there.
            - If the bot has can_delete_messages permission in a supergroup or a channel, it can delete any message there.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param int message_id: Identifier of the message to delete
        :return: True On success.
        :rtype: dict
        """
        return methods.delete_message(self.__token, self.__proxies, chat_id, message_id)

    def send_sticker(self, chat_id, sticker, disable_notification=False, reply_to_message_id=None, reply_markup=None):
        """
        Use this method to send static .WEBP or animated .TGS stickers.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param any sticker: Sticker [file_id or InputFile] to send.
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message.
        :param dict or None reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
        :return: a Message object On success.
        :rtype: tgbotapi.types.Message
        """
        return types.Message.de_json(
            methods.send_sticker(self.__token, self.__proxies, chat_id, sticker, disable_notification,
                                 reply_to_message_id,
                                 reply_markup))

    def get_sticker_set(self, name):
        """
        Use this method to get a sticker set.
        :param str name:  Name of the sticker set.
        :return: a StickerSet object On success.
        :rtype: tgbotapi.types.StickerSet
        """
        return types.StickerSet.de_json(methods.get_sticker_set(self.__token, self.__proxies, name))

    def upload_sticker_file(self, user_id, png_sticker):
        """
        Use this method to upload a .PNG file with a sticker.
        :param int user_id: Unique identifier of the target user.
        :param any png_sticker: Png image with the sticker,
        :return: a File object On success.
        :rtype: types.File
        """
        return types.File.de_json(methods.upload_sticker_file(self.__token, self.__proxies, user_id, png_sticker))

    def create_new_sticker_set(self, user_id, name, title, png_sticker, tgs_sticker, emojis, contains_masks=None,
                               mask_position=False):
        """
        Use this method to create a new sticker set owned by a user.
        :param int user_id: Unique identifier of the target user.
        :param str name: Short name of sticker set.
        :param str title: New chat title, 1-255 characters.
        :param any or None png_sticker: PNG image [file_id or InputFile] with the sticker.
        :param any or None tgs_sticker: TGS animation [InputFile] with the sticker.
        :param str emojis: One or more emoji corresponding to the sticker.
        :param bool contains_masks: Pass True, if a set of mask stickers should be created.
        :param any or None mask_position: A JSON-serialized object for position where the mask should be placed on faces.
        :return: True On success.
        :rtype: dict
        """
        return methods.create_new_sticker_set(self.__token, self.__proxies, user_id, name, title, png_sticker,
                                              tgs_sticker, emojis,
                                              contains_masks, mask_position)

    def add_sticker_to_set(self, user_id, name, png_sticker, tgs_sticker, emojis, mask_position=False):
        """
        Use this method to add a new sticker to a set created by the bot.
        :param int user_id: Unique identifier of the target user.
        :param str name: Short name of sticker set.
        :param any png_sticker: PNG image [file_id or InputFile] with the sticker.
        :param any or None tgs_sticker: TGS animation [InputFile] with the sticker.
        :param str emojis: One or more emoji corresponding to the sticker.
        :param any or None mask_position: A JSON-serialized object for position where the mask should be placed on faces.
        :return: True on success.
        :rtype: dict
        """
        return methods.add_sticker_to_set(self.__token, self.__proxies, user_id, name, png_sticker, tgs_sticker, emojis,
                                          mask_position)

    def set_sticker_position_in_set(self, sticker, position):
        """
        Use this method to move a sticker in a set created by the bot to a specific position.
        :param str sticker: File identifier of the sticker.
        :param int position: New sticker position in the set, zero-based.
        :return: True on success.
        :rtype: dict
        """
        return methods.set_sticker_position_in_set(self.__token, self.__proxies, sticker, position)

    def delete_sticker_from_set(self, sticker):
        """
        Use this method to delete a sticker from a set created by the bot.
        :param str sticker: File identifier of the sticker.
        :return: True on success.
        :rtype: dict
        """
        return methods.delete_sticker_from_set(self.__token, self.__proxies, sticker)

    def set_sticker_set_thumb(self, name, user_id, thumb=None):
        """
        Use this method to set the thumbnail of a sticker set.
        :param str name: Short name of sticker set.
        :param int user_id: Unique identifier of the target user.
        :param str or bytearray or None thumb: Thumbnail [file_id or InputFile] of the file sent.
        :return: True on success.
        :rtype: dict
        """
        return methods.set_sticker_set_thumb(self.__token, self.__proxies, name, user_id, thumb)

    def answer_inline_query(self, inline_query_id, results, cache_time=300, is_personal=False, next_offset=None,
                            switch_pm_text=None, switch_pm_parameter=None):
        """
        Use this method to send answers to an inline query.
        :param str inline_query_id: Unique identifier for the answered query.
        :param list results: A JSON-serialized array of [InlineQueryResult] results for the inline query.
        :param int or None cache_time: The maximum amount of time in seconds that the result of the inline query may be cached on the server. Defaults to 300.
        :param bool is_personal: Pass True, if results may be cached on the server side only for the user that sent the query.
        :param str or None next_offset: Pass the offset that a client should send in the next query with the same text to receive more results.
        :param str or None switch_pm_text: If passed, clients will display a button with specified text that switches the user to a private chat with the bot and sends the bot a start message with the parameter switch_pm_parameter.
        :param str or None switch_pm_parameter: 	Deep-linking parameter for the /start message sent to the bot when user presses the switch button. 1-64 characters, only A-Z, a-z, 0-9, _ and - are allowed.
        :return: True on success.
        :rtype: dict
        """
        return methods.answer_inline_query(self.__token, self.__proxies, inline_query_id, results, cache_time,
                                           is_personal, next_offset,
                                           switch_pm_text, switch_pm_parameter)

    def send_invoice(self, chat_id, title, description, payload, provider_token, start_parameter, currency, prices,
                     provider_data=None, photo_url=None, photo_size=None, photo_width=None, photo_height=None,
                     need_name=False, need_phone_number=False, need_email=False, need_shipping_address=False,
                     send_phone_number_to_provider=False, send_email_to_provider=False, is_flexible=False,
                     disable_notification=False, reply_to_message_id=None, reply_markup=None):
        """
        Use this method to send invoices. On success, the sent Message is returned.
        :param int chat_id: Unique identifier for the target chat or username of the target channel.
        :param str title: New chat title, 1-255 characters.
        :param str description: Product description, 1-255 characters
        :param str payload: Bot-defined invoice payload, 1-128 bytes.
        :param str provider_token: Payments provider token, obtained via Botfather.
        :param str start_parameter: Unique deep-linking parameter that can be used to generate this invoice when used as a start parameter.
        :param str currency: Three-letter ISO 4217 currency code.
        :param list prices: Price breakdown, a JSON-serialized list of components.
        :param dict provider_data: JSON-encoded data about the invoice, which will be shared with the payment provider.
        :param str photo_url: URL of the product photo for the invoice.
        :param int photo_size: Photo Size.
        :param int photo_width: Photo Width.
        :param int photo_height: Photo Height.
        :param need_name: Pass True, if you require the user's full name to complete the order
        :param need_phone_number: Pass True, if you require the user's phone number to complete the order.
        :param need_email: Pass True, if you require the user's email address to complete the order
        :param need_shipping_address: Pass True, if you require the user's shipping address to complete the order.
        :param send_phone_number_to_provider: Pass True, if user's phone number should be sent to provider.
        :param send_email_to_provider: Pass True, if user's email address should be sent to provider.
        :param is_flexible: Pass True, if the final price depends on the shipping method.
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message.
        :param types.InlineKeyboardMarkup or None reply_markup: A JSON-serialized object for an InlineKeyboardMarkup.
        :return: a Message object.
        :rtype: types.Message
        """
        return types.Message.de_json(
            methods.send_invoice(self.__token, self.__proxies, chat_id, title, description, payload, provider_token,
                                 start_parameter,
                                 currency, prices, provider_data, photo_url, photo_size, photo_width, photo_height,
                                 need_name, need_phone_number, need_email, need_shipping_address,
                                 send_phone_number_to_provider, send_email_to_provider, is_flexible,
                                 disable_notification,
                                 reply_to_message_id, reply_markup))

    def answer_shipping_query(self, shipping_query_id, ok, shipping_options=None, error_message=None):
        """
        Use this method to reply to shipping queries,
        If you sent an invoice requesting a shipping address and the parameter is_flexible was specified,
        the Bot API will send an Update with a shipping_query field to the bot.
        :param str shipping_query_id: Unique identifier for the query to be answered
        :param bool ok: Specify True if delivery to the specified address is possible and False if there are any problems.
        :param list or None shipping_options: Required if ok is True. A JSON-serialized array of available shipping options.
        :param str or None error_message: Required if ok is False. Error message in human readable form that explains why it is impossible to complete the order.
        :return: True, On success.
        :rtype: dict
        """
        return methods.answer_shipping_query(self.__token, self.__proxies, shipping_query_id, ok, shipping_options,
                                             error_message)

    def answer_pre_checkout_query(self, pre_checkout_query_id, ok, error_message=None):
        """
        Use this method to respond to such pre-checkout queries.
        :param str pre_checkout_query_id: Unique identifier for the query to be answered.
        :param bool ok: Specify True if delivery to the specified address is possible and False if there are any problems.
        :param str or None error_message: Required if ok is False. Error message in human readable form that explains why it is impossible to complete the order.
        :return: True On success.
        :rtype: dict
        """
        return methods.answer_pre_checkout_query(self.__token, self.__proxies, pre_checkout_query_id, ok, error_message)

    def set_passport_data_errors(self, user_id, errors):
        """
        Use this if the data submitted by the user doesn't satisfy the standards your service requires for any reason.
        :param int user_id: Unique identifier of the target user.
        :param list errors: A JSON-serialized array of [PassportElementError] describing the errors.
        :return: True On success.
        :rtype: dict
        """
        return methods.set_passport_data_errors(self.__token, self.__proxies, user_id, errors)

    def send_game(self, chat_id, game_short_name, disable_notification=False, reply_to_message_id=None,
                  reply_markup=None):
        """
        Use this method to send a game.
        :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
        :param str game_short_name: Short name of the game, serves as the unique identifier for the game.
        :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param int or None reply_to_message_id: If the message is a reply, ID of the original message.
        :param dict or None reply_markup: A JSON-serialized object for an InlineKeyboardMarkup.
        :return: a Message object On success.
        :rtype: tgbotapi.types.Message
        """
        return types.Message.de_json(
            methods.send_game(self.__token, self.__proxies, chat_id, game_short_name, disable_notification,
                              reply_to_message_id, reply_markup))

    def set_game_score(self, user_id, score, force=False, disable_edit_message=False, chat_id=None, message_id=None,
                       inline_message_id=None):
        """
        Use this method to set the score of the specified user in a game.
        :param int user_id: Unique identifier of the target user.
        :param int score: New score, must be non-negative.
        :param bool force: Pass True, if the high score is allowed to decrease.
        :param bool disable_edit_message: Pass True, if the game message should not be automatically edited to include the current scoreboard.
        :param int chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat.
        :param int or None message_id: Required if inline_message_id is not specified. Identifier of the message to edit.
        :param str or None inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
        :return: On success a Message object, otherwise returns True.
        :rtype: types.Message or dict
        """
        result = methods.set_game_score(self.__token, self.__proxies, user_id, score, force, disable_edit_message,
                                        chat_id, message_id,
                                        inline_message_id)
        if type(result) == bool:
            return result
        return types.Message.de_json(result)

    def get_game_high_scores(self, user_id, chat_id=None, message_id=None, inline_message_id=None):
        """
        Use this method to get data for high score tables.
        :param int user_id: Unique identifier of the target user.
        :param int or None chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat.
        :param int or None message_id: Required if inline_message_id is not specified. Identifier of the message to edit.
        :param str or None inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
        :return: an Array of GameHighScore objects.
        :rtype: list[tgbotapi.types.GameHighScore]
        """
        result = methods.get_game_high_scores(self.__token, self.__proxies, user_id, chat_id, message_id,
                                              inline_message_id)
        ret = []
        for r in result:
            ret.append(types.GameHighScore.de_json(r))
        return ret

    def enable_save_reply_handlers(self, delay=120, filename="./.handler-saves/reply.save"):
        """
        Enable saving reply handlers (by default saving disable)

        :param delay: Integer: Required, Delay between changes in handlers and saving
        :param filename: Data: Required, Filename of save file
        """
        self.__reply_saver = Saver(self.__reply_handlers, filename, delay)

    def disable_save_reply_handlers(self):
        """
        Disable saving next step handlers (by default saving disable)
        """
        self.__reply_saver = None

    def load_reply_handlers(self, filename="./.handler-saves/reply.save", del_file_after_loading=True):
        """
        Load reply handlers from save file

        :param filename: Data: Required, Filename of the file where handlers was saved
        :param del_file_after_loading: Boolean: Required, Is passed True, after loading save file will be deleted
        """
        self.__reply_saver.load_handlers(filename)

    def register_for_reply(self, message, callback, *args, **kwargs):
        """
        Registers a callback function to be notified when a reply to `message` arrives.

        Warning: In case `callback` as lambda function, saving reply handlers will not work.

        :param message:     The message for which we are awaiting a reply.
        :param callback:    The callback function to be called when a reply arrives. Must accept one `message`
                            parameter, which will contain the replied message.
        """
        message_id = message.message_id
        self.register_for_reply_by_message_id(
            message_id, callback, *args, **kwargs)

    def register_for_reply_by_message_id(self, message_id, callback, *args, **kwargs):
        """
        Registers a callback function to be notified when a reply to `message` arrives.

        Warning: In case `callback` as lambda function, saving reply handlers will not work.

        :param message_id:  The id of the message for which we are awaiting a reply.
        :param callback:    The callback function to be called when a reply arrives. Must accept one `message`
                            parameter, which will contain the replied message.
        """
        if message_id in self.__reply_handlers.keys():
            self.__reply_handlers[message_id].append(
                Handler(callback, *args, **kwargs))
        else:
            self.__reply_handlers[message_id] = [
                Handler(callback, *args, **kwargs)]
        if self.__reply_saver is not None:
            self.__reply_saver.start_save_timer()

    def clear_reply_handlers(self, message):
        """
        Clears all callback functions registered by register_for_reply() and register_for_reply_by_message_id().

        :param message: The message for which we want to clear reply handlers
        """
        message_id = message.message_id
        self.clear_reply_handlers_by_message_id(message_id)

    def clear_reply_handlers_by_message_id(self, message_id):
        """
        Clears all callback functions registered by register_for_reply() and register_for_reply_by_message_id().

        :param message_id: The message id for which we want to clear reply handlers
        """
        self.__reply_handlers[message_id] = []

        if self.__reply_saver is not None:
            self.__reply_saver.start_save_timer()

    def _notify_reply_handlers(self, new_messages):
        """
        Notify handlers of the answers
        :param any new_messages:
        :return:
        """
        for message in new_messages:
            if message.reply_to_message is not None:
                reply_mid = message.reply_to_message.message_id
                if reply_mid in self.__reply_handlers.keys():
                    handlers = self.__reply_handlers[reply_mid]
                    for handler in handlers:
                        self._exec_task(handler["callback"], message, *handler["args"], **handler["kwargs"])
                    self.__reply_handlers.pop(reply_mid)
                    if self.__reply_saver is not None:
                        self.__reply_saver.start_save_timer()

    def enable_save_next_step_handlers(self, delay=120, filename="./.handler-saves/step.save"):
        """
        Enable saving next step handlers (by default saving disable)

        :param delay: Integer: Required, Delay between changes in handlers and saving
        :param filename: Data: Required, Filename of save file
        """
        self.__next_step_saver = Saver(self.__next_step_handlers, filename, delay)

    def disable_save_next_step_handlers(self):
        """
        Disable saving next step handlers (by default saving disable)
        """
        self.__next_step_saver = None

    def load_next_step_handlers(self, filename="./.handler-saves/step.save", del_file_after_loading=True):
        """
        Load next step handlers from save file

        :param filename: Data: Required, Filename of the file where handlers was saved
        :param del_file_after_loading: Boolean: Required, Is passed True, after loading save file will be deleted
        """
        self.__next_step_saver.load_handlers(filename, del_file_after_loading)

    def register_next_step_handler(self, message, callback, *args, **kwargs):
        """
        Registers a callback function to be notified when new message arrives after `message`.

        Warning: In case `callback` as lambda function, saving next step handlers will not work.

        :param message:     The message for which we want to handle new message in the same chat.
        :param callback:    The callback function which next new message arrives.
        :param args:        Args to pass in callback func
        :param kwargs:      Args to pass in callback func
        """
        chat_id = message.chat.id
        self.register_next_step_handler_by_chat_id(
            chat_id, callback, *args, **kwargs)

    def register_next_step_handler_by_chat_id(self, chat_id, callback, *args, **kwargs):
        """
        Registers a callback function to be notified when new message arrives after `message`.

        Warning: In case `callback` as lambda function, saving next step handlers will not work.

        :param chat_id:     The chat for which we want to handle new message.
        :param callback:    The callback function which next new message arrives.
        :param args:        Args to pass in callback func
        :param kwargs:      Args to pass in callback func
        """
        if chat_id in self.__next_step_handlers.keys():
            self.__next_step_handlers[chat_id].append(
                Handler(callback, *args, **kwargs))
        else:
            self.__next_step_handlers[chat_id] = [
                Handler(callback, *args, **kwargs)]

        if self.__next_step_saver is not None:
            self.__next_step_saver.start_save_timer()

    def clear_step_handler(self, message):
        """
        Clears all callback functions registered by register_next_step_handler().

        :param message:     The message for which we want to handle new message after that in same chat.
        """
        chat_id = message.chat.id
        self.clear_step_handler_by_chat_id(chat_id)

    def clear_step_handler_by_chat_id(self, chat_id):
        """
        Clears all callback functions registered by register_next_step_handler().

        :param chat_id: The chat for which we want to clear next step handlers
        """
        self.__next_step_handlers[chat_id] = []

        if self.__next_step_saver is not None:
            self.__next_step_saver.start_save_timer()

    def _notify_next_handlers(self, new_messages):
        """
        Description: TBD
        :param new_messages:
        :return:
        """
        i = 0
        while i < len(new_messages):
            message = new_messages[i]
            chat_id = message.chat.id
            was_poped = False
            if chat_id in self.__next_step_handlers.keys():
                handlers = self.__next_step_handlers.pop(chat_id, None)
                if handlers:
                    for handler in handlers:
                        self._exec_task(
                            handler["callback"], message, *handler["args"], **handler["kwargs"])
                    # removing message that detects with next_step_handler
                    new_messages.pop(i)
                    was_poped = True
                if self.__next_step_saver is not None:
                    self.__next_step_saver.start_save_timer()
            if not was_poped:
                i += 1

    @staticmethod
    def _build_handler_dict(handler, **filters):
        """
        Builds a dictionary for a handler
        :param handler:
        :param filters:
        :return:
        """
        return {
            'function': handler,
            'filters': filters
        }

    def message_handler(self, commands=None, regexp=None, func=None, content_types=None, **kwargs):
        """
        Message handler decorator.
        This decorator can be used to decorate functions that must handle certain types of messages.
        :param str commands: Bot Commands like (/start, /help).
        :param str regexp: Sequence of characters that define a search pattern.
        :param str func: any python function that return True On success like (lambda).
        :param str content_types: This commands' supported content types. Must be a list. Defaults to ['text'].
        :return: filtered Message.
        """

        if content_types is None:
            content_types = ["text"]

        def decorator(handler):
            handler_dict = self._build_handler_dict(handler,
                                                    commands=commands,
                                                    regexp=regexp,
                                                    func=func,
                                                    content_types=content_types,
                                                    **kwargs)

            self.__add_message_handler(handler_dict)

            return handler

        return decorator

    def __add_message_handler(self, handler_dict):
        """
        Adds a message handler
        :param dict handler_dict:
        :return:
        """
        self.__message_handlers.append(handler_dict)

    def edited_message_handler(self, commands=None, regexp=None, func=None, content_types=None, **kwargs):
        """
        Edited message handler decorator.
        This decorator can be used to decorate functions that must handle certain types of edited messages.
        :param str commands: Bot Commands like (/start, /help).
        :param str regexp: Sequence of characters that define a search pattern.
        :param str func: any python function that return True On success like (lambda).
        :param str content_types: This commands' supported content types. Must be a list. Defaults to ['text'].
        :return: filtered Message.
        """

        if content_types is None:
            content_types = ["text"]

        def decorator(handler):
            handler_dict = self._build_handler_dict(handler,
                                                    commands=commands,
                                                    regexp=regexp,
                                                    func=func,
                                                    content_types=content_types,
                                                    **kwargs)
            self.__add_edited_message_handler(handler_dict)
            return handler

        return decorator

    def __add_edited_message_handler(self, handler_dict):
        """
        Adds the edit message handler
        :param dict handler_dict:
        :return:
        """
        self.__edited_message_handlers.append(handler_dict)

    def channel_post_handler(self, commands=None, regexp=None, func=None, content_types=None, **kwargs):
        """
        Channel post handler decorator.
        This decorator can be used to decorate functions that must handle certain types of channel post.
        :param str commands: Bot Commands like (/start, /help).
        :param str regexp: Sequence of characters that define a search pattern.
        :param str func: any python function that return True On success like (lambda).
        :param str content_types: This commands' supported content types. Must be a list. Defaults to ['text'].
        :return: filtered Message.
        """

        if content_types is None:
            content_types = ["text"]

        def decorator(handler):
            handler_dict = self._build_handler_dict(handler,
                                                    commands=commands,
                                                    regexp=regexp,
                                                    func=func,
                                                    content_types=content_types,
                                                    **kwargs)
            self.__add_channel_post_handler(handler_dict)
            return handler

        return decorator

    def __add_channel_post_handler(self, handler_dict):
        """
        Adds channel post handler
        :param dict handler_dict:
        :return:
        """
        self.__channel_post_handlers.append(handler_dict)

    def edited_channel_post_handler(self, commands=None, regexp=None, func=None, content_types=None, **kwargs):
        """
        Edited channel post handler decorator.
        This decorator can be used to decorate functions that must handle certain types of edited channel post.
        :param str commands: Bot Commands like (/start, /help).
        :param str regexp: Sequence of characters that define a search pattern.
        :param str func: any python function that return True On success like (lambda).
        :param str content_types: This commands' supported content types. Must be a list. Defaults to ['text'].
        :return: filtered Message.
        """

        if content_types is None:
            content_types = ["text"]

        def decorator(handler):
            handler_dict = self._build_handler_dict(handler,
                                                    commands=commands,
                                                    regexp=regexp,
                                                    func=func,
                                                    content_types=content_types,
                                                    **kwargs)
            self.__add_edited_channel_post_handler(handler_dict)
            return handler

        return decorator

    def __add_edited_channel_post_handler(self, handler_dict):
        """
        Adds the edit channel post handler
        :param dict handler_dict:
        :return:
        """
        self.__edited_channel_post_handlers.append(handler_dict)

    def inline_query_handler(self, func, **kwargs):
        """
        inline handler decorator.
        This decorator can be used to decorate functions that must handle certain types of inline query.
        :param str func: any python function that return True On success like (lambda).
        :param str kwargs:
        :return: filtered Message.
        """

        def decorator(handler):
            handler_dict = self._build_handler_dict(
                handler, func=func, **kwargs)
            self.__add_inline_query_handler(handler_dict)
            return handler

        return decorator

    def __add_inline_query_handler(self, handler_dict):
        """
        Adds inline call handler
        :param dict handler_dict:
        :return:
        """
        self.__inline_query_handlers.append(handler_dict)

    def chosen_inline_handler(self, func, **kwargs):
        """
        Chosen inline handler decorator.
        This decorator can be used to decorate functions that must handle certain types of messages.
        :param str func: any python function that return True On success like (lambda).
        :param str kwargs:
        :return: filtered Message.
        """

        def decorator(handler):
            handler_dict = self._build_handler_dict(
                handler, func=func, **kwargs)
            self.__add_chosen_inline_handler(handler_dict)
            return handler

        return decorator

    def __add_chosen_inline_handler(self, handler_dict):
        """
        Description: TBD
        :param dict handler_dict:
        :return:
        """
        self.__chosen_inline_handlers.append(handler_dict)

    def callback_query_handler(self, func, **kwargs):
        """
        Callback query handler decorator.
        This decorator can be used to decorate functions that must handle certain types of messages.
        :param str func: any python function that return True On success like (lambda).
        :param str kwargs:
        :return: filtered Message.
        """

        def decorator(handler):
            handler_dict = self._build_handler_dict(
                handler, func=func, **kwargs)
            self.__add_callback_query_handler(handler_dict)
            return handler

        return decorator

    def __add_callback_query_handler(self, handler_dict):
        """
        Adds a callback request handler
        :param dict handler_dict:
        :return:
        """
        self.__callback_query_handlers.append(handler_dict)

    def shipping_query_handler(self, func, **kwargs):
        """
        shipping query handler decorator.
        This decorator can be used to decorate functions that must handle certain types of messages.
        :param str func: any python function that return True On success like (lambda).
        :param str kwargs:
        :return: filtered Message.
        """

        def decorator(handler):
            handler_dict = self._build_handler_dict(
                handler, func=func, **kwargs)
            self.__add_shipping_query_handler(handler_dict)
            return handler

        return decorator

    def __add_shipping_query_handler(self, handler_dict):
        """
        Adds a shipping request handler
        :param dict handler_dict:
        :return:
        """
        self.__shipping_query_handlers.append(handler_dict)

    def pre_checkout_query_handler(self, func, **kwargs):
        """
        Pre checkout query handler decorator.
        This decorator can be used to decorate functions that must handle certain types of messages.
        :param str func: any python function that return True On success like (lambda).
        :param str kwargs:
        :return: filtered Message.
        """

        def decorator(handler):
            handler_dict = self._build_handler_dict(
                handler, func=func, **kwargs)
            self.__add_pre_checkout_query_handler(handler_dict)
            return handler

        return decorator

    def __add_pre_checkout_query_handler(self, handler_dict):
        """
        Adds a pre-checkout request handler
        :param dict handler_dict:
        :return:
        """
        self.__pre_checkout_query_handlers.append(handler_dict)

    def poll_handler(self, func, **kwargs):
        """
        Poll handler decorator.
        This decorator can be used to decorate functions that must handle certain types of poll.
        :param str func: any python function that return True On success like (lambda).
        :param str kwargs:
        :return: filtered Message.
        """

        def decorator(handler):
            handler_dict = self._build_handler_dict(handler, func=func, **kwargs)
            self.__add_poll_handler(handler_dict)
            return handler

        return decorator

    def __add_poll_handler(self, handler_dict):
        """
        Adds a poll request handler
        :param dict handler_dict:
        :return:
        """
        self.__poll_handlers.append(handler_dict)

    def poll_answer_handler(self, func, **kwargs):
        """
        Poll answer handler decorator.
        This decorator can be used to decorate functions that must handle certain types of messages.
        :param str func: any python function that return True On success like (lambda).
        :param str kwargs:
        :return: filtered Message.
        """

        def decorator(handler):
            handler_dict = self._build_handler_dict(handler, func=func, **kwargs)
            self.__add_poll_answer_handler(handler_dict)
            return handler

        return decorator

    def __add_poll_answer_handler(self, handler_dict):
        """
        Adds a poll request handler
        :param dict handler_dict:
        :return:
        """
        self.__poll_answer_handlers.append(handler_dict)

    def _test_message_handler(self, message_handler, message):
        """
        Test message handler
        :param message_handler:
        :param message:
        :return:
        """
        for filterr, filter_value in six.iteritems(message_handler['filters']):
            if filter_value is None:
                continue

            if not self._test_filter(filterr, filter_value, message):
                return False

        return True

    @staticmethod
    def _test_filter(filterr, filter_value, message):
        """
        Test filters
        :param filterr:
        :param filter_value:
        :param message:
        :return:
        """
        test_cases = {
            'content_types': lambda msg: msg.content_type in filter_value,
            'regexp': lambda msg: msg.content_type == 'text' and re.search(filter_value, msg.text, re.IGNORECASE),
            'commands': lambda msg: msg.content_type == 'text' and extract_command(msg.text) in filter_value,
            'func': lambda msg: filter_value(msg)
        }

        return test_cases.get(filterr, lambda msg: False)(message)

    def _notify_command_handlers(self, handlers, new_messages):
        """
        Notifies command handlers
        :param handlers:
        :param new_messages:
        :return:
        """
        for message in new_messages:
            for message_handler in handlers:
                if self._test_message_handler(message_handler, message):
                    self._exec_task(message_handler['function'], message)
                    break


class AsyncTBot(TBot):
    def __init__(self, *args, **kwargs):
        TBot.__init__(self, *args, **kwargs)

    @async_dec()
    def enable_save_next_step_handlers(self, delay=120, filename="./.handler-saves/step.save"):
        return TBot.enable_save_next_step_handlers(self, delay, filename)

    @async_dec()
    def enable_save_reply_handlers(self, delay=120, filename="./.handler-saves/reply.save"):
        return TBot.enable_save_reply_handlers(self, delay, filename)

    @async_dec()
    def disable_save_next_step_handlers(self):
        return TBot.disable_save_next_step_handlers(self)

    @async_dec()
    def disable_save_reply_handlers(self):
        return TBot.disable_save_reply_handlers(self)

    @async_dec()
    def load_next_step_handlers(self, filename="./.handler-saves/step.save", del_file_after_loading=True):
        return TBot.load_next_step_handlers(self, filename, del_file_after_loading)

    @async_dec()
    def load_reply_handlers(self, filename="./.handler-saves/reply.save", del_file_after_loading=True):
        return TBot.load_reply_handlers(self, filename, del_file_after_loading)

    @async_dec()
    def get_me(self):
        return TBot.get_me(self)

    @async_dec()
    def send_message(self, *args, **kwargs):
        return TBot.send_message(self, *args, **kwargs)

    @async_dec()
    def forward_message(self, *args, **kwargs):
        return TBot.forward_message(self, *args, **kwargs)

    @async_dec()
    def send_photo(self, *args, **kwargs):
        return TBot.send_photo(self, *args, **kwargs)

    @async_dec()
    def send_audio(self, *args, **kwargs):
        return TBot.send_audio(self, *args, **kwargs)

    @async_dec()
    def send_document(self, *args, **kwargs):
        return TBot.send_document(self, *args, **kwargs)

    @async_dec()
    def send_video(self, *args, **kwargs):
        return TBot.send_video(self, *args, **kwargs)

    @async_dec()
    def sen_animation(self, *args, **kwargs):
        return TBot.send_animation(self, *args, **kwargs)

    @async_dec()
    def send_voice(self, *args, **kwargs):
        return TBot.send_voice(self, *args, **kwargs)

    @async_dec()
    def send_video_note(self, *args, **kwargs):
        return TBot.send_video_note(self, *args, **kwargs)

    @async_dec()
    def send_media_group(self, *args, **kwargs):
        return TBot.send_media_group(self, *args, **kwargs)

    @async_dec()
    def send_location(self, *args, **kwargs):
        return TBot.send_location(self, *args, **kwargs)

    @async_dec()
    def edit_message_live_location(self, *args, **kwargs):
        return TBot.edit_message_live_location(self, *args, **kwargs)

    @async_dec()
    def stop_message_live_location(self, *args, **kwargs):
        return TBot.stop_message_live_location(self, *args, **kwargs)

    @async_dec()
    def send_venue(self, *args, **kwargs):
        return TBot.send_venue(self, *args, **kwargs)

    @async_dec()
    def send_contact(self, *args, **kwargs):
        return TBot.send_contact(self, *args, **kwargs)

    @async_dec()
    def send_poll(self, *args, **kwargs):
        return TBot.send_poll(self, *args, **kwargs)

    @async_dec()
    def send_dice(self, *args, **kwargs):
        return TBot.send_dice(self, *args, **kwargs)

    @async_dec()
    def send_chat_action(self, *args, **kwargs):
        return TBot.send_chat_action(self, *args, **kwargs)

    @async_dec()
    def get_user_profile_photos(self, *args, **kwargs):
        return TBot.get_user_profile_photos(self, *args, **kwargs)

    @async_dec()
    def get_file(self, *args):
        return TBot.get_file(self, *args)

    @async_dec()
    def download_file(self, *args):
        return TBot.download_file(self, *args)

    @async_dec()
    def kick_chat_member(self, *args, **kwargs):
        return TBot.kick_chat_member(self, *args, **kwargs)

    @async_dec()
    def unban_chat_member(self, *args):
        return TBot.unban_chat_member(self, *args)

    @async_dec()
    def restrict_chat_member(self, *args, **kwargs):
        return TBot.restrict_chat_member(self, *args, **kwargs)

    @async_dec()
    def promote_chat_member(self, *args, **kwargs):
        return TBot.promote_chat_member(self, *args, **kwargs)

    @async_dec()
    def set_chat_permissions(self, *args, **kwargs):
        return TBot.set_chat_permissions(self, *args, **kwargs)

    @async_dec()
    def export_chat_invite_link(self, *args):
        return TBot.export_chat_invite_link(self, *args)

    @async_dec()
    def set_chat_photo(self, *args):
        return TBot.set_chat_photo(self, *args)

    @async_dec()
    def delete_chat_photo(self, *args):
        return TBot.delete_chat_photo(self, *args)

    @async_dec()
    def set_chat_title(self, *args):
        return TBot.set_chat_title(self, *args)

    @async_dec()
    def set_chat_description(self, *args):
        return TBot.set_chat_description(self, *args)

    @async_dec()
    def pin_chat_message(self, *args, **kwargs):
        return TBot.pin_chat_message(self, *args, **kwargs)

    @async_dec()
    def unpin_chat_message(self, *args):
        return TBot.unpin_chat_message(self, *args)

    @async_dec()
    def leave_chat(self, *args):
        return TBot.leave_chat(self, *args)

    @async_dec()
    def get_chat(self, *args):
        return TBot.get_chat(self, *args)

    @async_dec()
    def get_chat_administrators(self, *args):
        return TBot.get_chat_administrators(self, *args)

    @async_dec()
    def get_chat_members_count(self, *args):
        return TBot.get_chat_members_count(self, *args)

    @async_dec()
    def send_sticker(self, *args, **kwargs):
        return TBot.send_sticker(self, *args, **kwargs)

    @async_dec()
    def get_chat_member(self, *args):
        return TBot.get_chat_member(self, *args)

    @async_dec()
    def set_chat_sticker_set(self, *args):
        return TBot.set_chat_sticker_set(self, *args)

    @async_dec()
    def delete_chat_sticker_set(self, *args):
        return TBot.delete_chat_sticker_set(self, *args)

    @async_dec()
    def answer_callback_query(self, *args, **kwargs):
        return TBot.answer_callback_query(self, *args, **kwargs)

    @async_dec()
    def set_my_commands(self, *args):
        return TBot.set_my_commands(self, *args)

    @async_dec()
    def get_my_commands(self):
        return TBot.get_my_commands(self)

    @async_dec()
    def edit_message_text(self, *args, **kwargs):
        return TBot.edit_message_text(self, *args, **kwargs)

    @async_dec()
    def edit_message_caption(self, *args, **kwargs):
        return TBot.edit_message_caption(self, *args, **kwargs)

    @async_dec()
    def edit_message_media(self, *args, **kwargs):
        return TBot.edit_message_media(self, *args, **kwargs)

    @async_dec()
    def edit_message_reply_markup(self, *args, **kwargs):
        return TBot.edit_message_reply_markup(self, *args, **kwargs)

    @async_dec()
    def stop_poll(self, *args, **kwargs):
        return TBot.stop_poll(self, *args, **kwargs)

    @async_dec()
    def delete_message(self, *args):
        return TBot.delete_message(self, *args)

    @async_dec()
    def send_sticker(self, *args, **kwargs):
        return TBot.send_sticker(self, *args, **kwargs)

    @async_dec()
    def get_sticker_set(self, *args, **kwargs):
        return TBot.get_sticker_set(self, *args, **kwargs)

    @async_dec()
    def upload_sticker_file(self, *args, **kwargs):
        return TBot.upload_sticker_file(self, *args, **kwargs)

    @async_dec()
    def create_new_sticker_set(self, *args, **kwargs):
        return TBot.create_new_sticker_set(self, *args, **kwargs)

    @async_dec()
    def add_sticker_to_set(self, *args, **kwargs):
        return TBot.add_sticker_to_set(self, *args, **kwargs)

    @async_dec()
    def set_sticker_position_in_set(self, *args, **kwargs):
        return TBot.set_sticker_position_in_set(self, *args, **kwargs)

    @async_dec()
    def delete_sticker_from_set(self, *args, **kwargs):
        return TBot.delete_sticker_from_set(self, *args, **kwargs)

    @async_dec()
    def set_sticker_set_thumb(self, *args, **kwargs):
        return TBot.set_sticker_set_thumb(self, *args, **kwargs)

    @async_dec()
    def answer_inline_query(self, *args, **kwargs):
        return TBot.answer_inline_query(self, *args, **kwargs)

    @async_dec()
    def send_invoice(self, *args, **kwargs):
        return TBot.send_invoice(self, *args, **kwargs)

    @async_dec()
    def answer_shipping_query(self, *args, **kwargs):
        return TBot.answer_shipping_query(self, *args, **kwargs)

    @async_dec()
    def answer_pre_checkout_query(self, *args, **kwargs):
        return TBot.answer_pre_checkout_query(self, *args, **kwargs)

    @async_dec()
    def set_passport_data_errors(self, *args, **kwargs):
        return TBot.set_passport_data_errors(self, *args, **kwargs)

    @async_dec()
    def send_game(self, *args, **kwargs):
        return TBot.send_game(self, *args, **kwargs)

    @async_dec()
    def set_game_score(self, *args, **kwargs):
        return TBot.set_game_score(self, *args, **kwargs)

    @async_dec()
    def get_game_high_scores(self, *args, **kwargs):
        return TBot.get_game_high_scores(self, *args, **kwargs)
