import json
import six

""" Telegram Available methods
    All methods in the Bot API are case-insensitive. We support GET and POST HTTP methods. 
    Use either URL query string or application/json or application/x-www-form-urlencoded or multipart/form-data for passing parameters in Bot API requests.
    On successful call, a JSON-object containing the result will be returned.
"""


class Dictionaryable(object):
    """
    Subclasses of this class are guaranteed to be able to be converted to dictionary,
    All subclasses of this class must override to_dic.
    """

    def to_dic(self):
        """
        Returns a JSON string representation of this class.

        This function must be overridden by subclasses.
        :return: a JSON formatted string.
        """
        raise NotImplementedError


class JsonDeserializable(object):
    """
    Subclasses of this class are guaranteed to be able to be created from a json-style dict or json formatted string,
    All subclasses of this class must override de_json.
    """

    @classmethod
    def de_json(cls, json_type):
        """
        Returns an instance of this class from the given json dict or string.

        This function must be overridden by subclasses.
        :return: an instance of this class created from the given json dict or string.
        """
        raise NotImplementedError

    @staticmethod
    def check_json(json_type):
        """
        Checks whether json_type is a dict or a string. If it is already a dict, it is returned as-is,
        If it is not, it is converted to a dict by means of json.loads(json_type),
        :param json_type:
        :return:
        """
        try:
            str_types = (str, unicode)
        except NameError:
            str_types = (str,)

        if type(json_type) == dict:
            return json_type
        elif type(json_type) in str_types:
            return json.loads(json_type)
        else:
            raise ValueError("json_type should be a json dict or string.")

    def __str__(self):
        d = {}
        for x, y in six.iteritems(self.__dict__):
            if hasattr(y, '__dict__'):
                d[x] = y.__dict__
            else:
                d[x] = y

        return six.text_type(d)


class JsonSerializable(object):
    """
    Subclasses of this class are guaranteed to be able to be converted to JSON format,
    All subclasses of this class must override to_json.
    """

    def to_json(self):
        """
        Returns a JSON string representation of this class.

        This function must be overridden by subclasses.
        :return: a JSON formatted string.
        """
        raise NotImplementedError


class Update(JsonDeserializable):
    """ 
    This object represents an incoming update,
    At most one of the optional parameters can be present in any given update.
    """

    def __init__(self, update_id, message, edited_message, channel_post, edited_channel_post, inline_query,
                 chosen_inline_result, callback_query, shipping_query, pre_checkout_query, poll, poll_answer):
        self.update_id = update_id
        self.message = message
        self.edited_message = edited_message
        self.channel_post = channel_post
        self.edited_channel_post = edited_channel_post
        self.inline_query = inline_query
        self.chosen_inline_result = chosen_inline_result
        self.callback_query = callback_query
        self.shipping_query = shipping_query
        self.pre_checkout_query = pre_checkout_query
        self.poll = poll
        self.poll_anwser = poll_answer

    @classmethod
    def de_json(cls, json_type):
        obj = cls.check_json(json_type)
        update_id = obj['update_id']
        message = None
        if 'message' in obj:
            message = Message.de_json(obj['message'])
        edited_message = None
        if 'edited_message' in obj:
            edited_message = Message.de_json(obj['edited_message'])
        channel_post = None
        if 'channel_post' in obj:
            channel_post = Message.de_json(obj['channel_post'])
        edited_channel_post = None
        if 'edited_channel_post' in obj:
            edited_channel_post = Message.de_json(obj['edited_channel_post'])
        inline_query = None
        if 'inline_query' in obj:
            inline_query = InlineQuery.de_json(obj['inline_query'])
        chosen_inline_result = None
        if 'chosen_inline_result' in obj:
            chosen_inline_result = ChosenInlineResult.de_json(
                obj['chosen_inline_result'])
        callback_query = None
        if 'callback_query' in obj:
            callback_query = CallbackQuery.de_json(obj['callback_query'])
        shipping_query = None
        if 'shipping_query' in obj:
            shipping_query = ShippingQuery.de_json(obj['shipping_query'])
        pre_checkout_query = None
        if 'pre_checkout_query' in obj:
            pre_checkout_query = PreCheckoutQuery.de_json(
                obj['pre_checkout_query'])
        poll = None
        if 'poll' in obj:
            poll = Poll.de_json(obj['poll'])
        poll_answer = None
        if 'poll_answer' in obj:
            poll_answer = PollAnswer.de_json(obj['poll_answer'])
        return cls(update_id, message, edited_message, channel_post, edited_channel_post, inline_query,
                   chosen_inline_result, callback_query, shipping_query, pre_checkout_query, poll, poll_answer)


class WebhookInfo(JsonDeserializable):
    """ Contains information about the current status of a webhook """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        url = obj['url']
        has_custom_certificate = obj['has_custom_certificate']
        pending_update_count = obj['pending_update_count']
        last_error_date = None
        if 'last_error_message' in obj:
            last_error_date = obj['last_error_date']
        last_error_message = None
        if 'last_error_message' in obj:
            last_error_message = obj['last_error_message']
        max_connections = None
        if 'max_connections' in obj:
            max_connections = obj['max_connections']
        allowed_updates = None
        if 'allowed_updates' in obj:
            allowed_updates = obj['allowed_updates']
        return cls(url, has_custom_certificate, pending_update_count, last_error_date, last_error_message,
                   max_connections, allowed_updates)

    def __init__(self, url, has_custom_certificate, pending_update_count, last_error_date, last_error_message,
                 max_connections, allowed_updates):
        self.url = url
        self.has_custom_certificate = has_custom_certificate
        self.pending_update_count = pending_update_count
        self.last_error_date = last_error_date
        self.last_error_message = last_error_message
        self.max_connections = max_connections
        self.allowed_updates = allowed_updates


class User(JsonDeserializable):
    """ This object represents a Telegram user or bot """

    def __init__(self, id, is_bot, first_name, last_name=None, username=None, language_code=None, can_join_groups=None, can_read_all_group_messages=None, supports_inline_queries=None):
        """
        :param id: [Integer] Unique identifier for this user or bot.
        :param is_bot: [Boolean] True, if this user is a bot.
        :param first_name: [String] User‘s or bot’s first name.
        :param last_name: [String] Optional. User‘s or bot’s last name.
        :param username: [String] Optional. User‘s or bot’s username.
        :param language_code: [String] Optional. IETF language tag of the user's language.
        :param can_join_groups: [Boolean] Optional. True, if the bot can be invited to groups. Returned only in getMe.
        :param can_read_all_group_messages: [Boolean] Optional. True, if privacy mode is disabled for the bot. Returned only in getMe.
        :param supports_inline_queries: [Boolean] Optional. True, if the bot supports inline queries. Returned only in getMe.
        """

        self.id = id
        self.is_bot = is_bot
        self.first_name = first_name
        self.username = username
        self.last_name = last_name
        self.language_code = language_code
        self.can_join_groups = can_join_groups
        self.can_read_all_group_messages = can_read_all_group_messages
        self.supports_inline_queries = supports_inline_queries

    @classmethod
    def de_json(cls, json_string):
        """ :return JSON-object """
        obj = cls.check_json(json_string)
        id = obj['id']
        is_bot = obj['is_bot']
        first_name = obj['first_name']
        last_name = None
        if 'last_name' in obj:
            last_name = obj.get('last_name')
        username = None
        if 'username' in obj:
            username = obj.get('username')
        language_code = None
        if 'language_code' in obj:
            language_code = obj.get('language_code')
        can_join_groups = None
        if 'can_join_groups' in obj:
            can_join_groups = obj.get('can_join_groups')
        can_read_all_group_messages = None
        if 'can_read_all_group_messages' in obj:
            can_read_all_group_messages = obj.get(
                'can_read_all_group_messages')
        supports_inline_queries = None
        if 'supports_inline_queries' in obj:
            supports_inline_queries = obj.get('supports_inline_queries')
        return cls(id, is_bot, first_name, last_name, username, language_code, can_join_groups, can_read_all_group_messages, supports_inline_queries)


class Animation(JsonDeserializable):
    """ This object represents an animation file (GIF or H.264/MPEG-4 AVC video without sound) """

    def __init__(self, file_id, file_unique_id, width, height, duration, thumb, file_name, mime_type, file_size):
        """
        :param file_id: [STRING] Identifier for this file, which can be used to download or reuse the file.
        :param file_unique_id: [STRING] Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file..
        :param width: [INTEGER] Video width as defined by sender.
        :param height: [INTEGER] Video height as defined by sender.
        :param duration: [INTEGER] Duration of the video in seconds as defined by sender.
        :param thumb: [PhotoSize] Optional. Animation thumbnail as defined by sender.
        :param file_name: [STRING] Optional. Original animation filename as defined by sender.
        :param mime_type: [STRING] Optional. MIME type of the file as defined by sender.
        :param file_size: [INTEGER] Optional. File size.
        """
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.duration = duration
        self.thumb = thumb
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size

    @classmethod
    def de_json(cls, json_string):
        """ :return JSON-object """
        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        file_unique_id = obj['file_unique_id']
        width = obj['width']
        height = obj['height']
        duration = obj['duration']
        thumb = None
        if 'thumb' in obj:
            thumb = PhotoSize.de_json(obj['thumb'])
        file_name = None
        if 'file_name' in obj:
            file_name = obj.get('file_name')
        mime_type = None
        if 'mime_type' in obj:
            mime_type = obj.get('mime_type')
        file_size = None
        if 'file_size' in obj:
            file_size = obj.get('file_size')
        return cls(file_id, file_unique_id, width, height, duration, thumb, file_name, mime_type, file_size)


class PhotoSize(JsonDeserializable):
    """ This object represents one size of a photo or a file / sticker thumbnail """

    def __init__(self, file_id, file_unique_id, width, height, file_size=None):
        """
        :param file_id: [STRING] Identifier for this file, which can be used to download or reuse the file.
        :param file_unique_id: [STRING] Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file..
        :param width: [INTEGER] Photo width.
        :param height: [INTEGER] Phot height.
        :param file_size: [INTEGER] Optional. File size.
        """

        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.file_size = file_size

    @classmethod
    def de_json(cls, json_string):
        """ :return JSON-object """
        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        file_unique_id = obj['file_unique_id']
        width = obj['width']
        height = obj['height']
        file_size = obj.get('file_size')
        return cls(file_id, file_unique_id, width, height, file_size)
