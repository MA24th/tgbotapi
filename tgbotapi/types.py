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


class Chat(JsonDeserializable):
    """ This object represents a chat """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        id = obj['id']
        type = obj['type']
        title = None
        if 'title' in obj:
            title = obj.get('title')
        username = None
        if 'username' in obj:
            username = obj.get('username')
        first_name = None
        if 'first_name' in obj:
            first_name = obj.get('first_name')
        last_name = None
        if 'last_name' in obj:
            last_name = obj.get('last_name')
        photo = None
        if 'photo' in obj:
            photo = ChatPhoto.de_json(obj['photo'])
        description = None
        if 'description' in obj:
            description = obj.get('description')
        invite_link = None
        if 'invite_link' in obj:
            invite_link = obj.get('invite_link')
        pinned_message = None
        if 'pinned_message' in obj:
            pinned_message = Message.de_json(obj['pinned_message'])
        sticker_set_name = obj.get('sticker_set_name')
        permissions = None
        if 'permissions' in obj:
            permissions = ChatPermissions.de_json(obj['permissions'])
        slow_mode_delay = None
        if 'slow_mode_delay' in obj:
            slow_mode_delay = obj.get('slow_mode_delay')
        sticker_set_name = None
        if 'sticker_set_name' in obj:
            sticker_set_name = obj.get('sticker_set_name')
        can_set_sticker_set = None
        if 'can_set_sticker_set' in obj:
            can_set_sticker_set = obj.get('can_set_sticker_set')
        return cls(id, type, title, username, first_name, last_name, photo, description, invite_link, pinned_message,
                   permissions, slow_mode_delay, sticker_set_name, can_set_sticker_set)

    def __init__(self, id, type, title=None, username=None, first_name=None, last_name=None,
                 photo=None, description=None, invite_link=None, pinned_message=None, permissions=None,
                 slow_mode_delay=None, sticker_set_name=None, can_set_sticker_set=None):
        self.id = id
        self.type = type
        self.title = title
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.photo = photo
        self.description = description
        self.invite_link = invite_link
        self.pinned_message = pinned_message
        self.permissions = permissions
        self.slow_mode_delay = slow_mode_delay
        self.sticker_set_name = sticker_set_name
        self.can_set_sticker_set = can_set_sticker_set


class Message(JsonDeserializable):
    """This object represents a message"""
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        message_id = obj['message_id']
        from_user = None
        if 'from' in obj:
            from_user = User.de_json(obj['from'])
        date = obj['date']
        chat = Chat.de_json(obj['chat'])
        content_type = None
        opts = {}
        if 'forward_from' in obj:
            opts['forward_from'] = User.de_json(obj['forward_from'])
        if 'forward_from_chat' in obj:
            opts['forward_from_chat'] = Chat.de_json(obj['forward_from_chat'])
        if 'forward_from_message_id' in obj:
            opts['forward_from_message_id'] = obj.get(
                'forward_from_message_id')
        if 'forward_sender_name' in obj:
            opts['forward_sender_name'] = obj.get('forward_sender_name')
        if 'forward_signature' in obj:
            opts['forward_signature'] = obj.get('forward_signature')
        if 'forward_date' in obj:
            opts['forward_date'] = obj.get('forward_date')
        if 'reply_to_message' in obj:
            opts['reply_to_message'] = Message.de_json(obj['reply_to_message'])
        if 'edit_date' in obj:
            opts['edit_date'] = obj.get('edit_date')
        if 'media_group_id' in obj:
            opts['media_group_id'] = obj.get('media_group_id')
        if 'author_signature' in obj:
            opts['author_signature'] = obj.get('author_signature')
        if 'text' in obj:
            opts['text'] = obj['text']
            content_type = 'text'
        if 'entities' in obj:
            opts['entities'] = Message.parse_entities(obj['entities'])
        if 'caption_entities' in obj:
            opts['caption_entities'] = Message.parse_entities(
                obj['caption_entities'])
        if 'audio' in obj:
            opts['audio'] = Audio.de_json(obj['audio'])
            content_type = 'audio'
        if 'document' in obj:
            opts['document'] = Document.de_json(obj['document'])
            content_type = 'document'
        if 'animation' in obj:
            opts['animation'] = Animation.de_json(obj['animation'])
            content_type = 'animation'
        if 'game' in obj:
            opts['game'] = Game.de_json(obj['game'])
            content_type = 'game'
        if 'photo' in obj:
            opts['photo'] = Message.parse_photo(obj['photo'])
            content_type = 'photo'
        if 'sticker' in obj:
            opts['sticker'] = Sticker.de_json(obj['sticker'])
            content_type = 'sticker'
        if 'video' in obj:
            opts['video'] = Video.de_json(obj['video'])
            content_type = 'video'
        if 'voice' in obj:
            opts['voice'] = Audio.de_json(obj['voice'])
            content_type = 'voice'
        if 'video_note' in obj:
            opts['video_note'] = VideoNote.de_json(obj['video_note'])
            content_type = 'video_note'
        if 'caption' in obj:
            opts['caption'] = obj['caption']
        if 'contact' in obj:
            opts['contact'] = Contact.de_json(json.dumps(obj['contact']))
            content_type = 'contact'
        if 'location' in obj:
            opts['location'] = Location.de_json(obj['location'])
            content_type = 'location'
        if 'venue' in obj:
            opts['venue'] = Venue.de_json(obj['venue'])
            content_type = 'venue'
        if 'poll' in obj:
            opts['poll'] = Poll.de_json(obj['poll'])
            content_type = 'poll'
        if 'new_chat_members' in obj:
            opts['new_chat_members'] = Message.parse_chat_members(
                obj['new_chat_members'])
            content_type = 'new_chat_members'
        if 'left_chat_member' in obj:
            opts['left_chat_member'] = User.de_json(obj['left_chat_member'])
            content_type = 'left_chat_member'
        if 'new_chat_title' in obj:
            opts['new_chat_title'] = obj['new_chat_title']
            content_type = 'new_chat_title'
        if 'new_chat_photo' in obj:
            opts['new_chat_photo'] = Message.parse_photo(obj['new_chat_photo'])
            content_type = 'new_chat_photo'
        if 'delete_chat_photo' in obj:
            opts['delete_chat_photo'] = obj['delete_chat_photo']
            content_type = 'delete_chat_photo'
        if 'group_chat_created' in obj:
            opts['group_chat_created'] = obj['group_chat_created']
            content_type = 'group_chat_created'
        if 'supergroup_chat_created' in obj:
            opts['supergroup_chat_created'] = obj['supergroup_chat_created']
            content_type = 'supergroup_chat_created'
        if 'channel_chat_created' in obj:
            opts['channel_chat_created'] = obj['channel_chat_created']
            content_type = 'channel_chat_created'
        if 'migrate_to_chat_id' in obj:
            opts['migrate_to_chat_id'] = obj['migrate_to_chat_id']
            content_type = 'migrate_to_chat_id'
        if 'migrate_from_chat_id' in obj:
            opts['migrate_from_chat_id'] = obj['migrate_from_chat_id']
            content_type = 'migrate_from_chat_id'
        if 'pinned_message' in obj:
            opts['pinned_message'] = Message.de_json(obj['pinned_message'])
            content_type = 'pinned_message'
        if 'invoice' in obj:
            opts['invoice'] = Invoice.de_json(obj['invoice'])
            content_type = 'invoice'
        if 'successful_payment' in obj:
            opts['successful_payment'] = SuccessfulPayment.de_json(
                obj['successful_payment'])
            content_type = 'successful_payment'
        if 'connected_website' in obj:
            opts['connected_website'] = obj['connected_website']
            content_type = 'connected_website'
        if 'passport_data' in obj:
            opts['passport_data'] = obj['passport_data']
            content_type = 'passport_data'
        if 'reply_markup' in obj:
            opts['reply_markup'] = InlineKeyboardMarkup(obj['reply_markup'])
            content_type = 'reply_markup'
        return cls(message_id, from_user, date, chat, content_type, opts, json_string)

    @classmethod
    def parse_photo(cls, photo_size_array):
        ret = []
        for ps in photo_size_array:
            ret.append(PhotoSize.de_json(ps))
        return ret

    @classmethod
    def parse_entities(cls, message_entity_array):
        ret = []
        for en in message_entity_array:
            ret.append(MessageEntity.de_json(en))
        return ret

    @classmethod
    def parse_chat_members(cls, new_chat_members):
        ret = []
        for cm in new_chat_members:
            ret.append(ChatMember.de_json(cm))
        return ret

    def __init__(self, message_id, from_user, date, chat, content_type, options, json_string):
        self.content_type = content_type
        self.message_id = message_id
        self.from_user = from_user
        self.date = date
        self.chat = chat
        self.forward_from_chat = None
        self.forward_from_message_id = None
        self.forward_from = None
        self.forward_date = None
        self.reply_to_message = None
        self.edit_date = None
        self.media_group_id = None
        self.author_signature = None
        self.text = None
        self.entities = None
        self.caption_entities = None
        self.audio = None
        self.document = None
        self.photo = None
        self.sticker = None
        self.video = None
        self.video_note = None
        self.voice = None
        self.caption = None
        self.contact = None
        self.location = None
        self.venue = None
        self.animation = None
        self.new_chat_members = None
        self.left_chat_member = None
        self.new_chat_title = None
        self.new_chat_photo = None
        self.delete_chat_photo = None
        self.group_chat_created = None
        self.supergroup_chat_created = None
        self.channel_chat_created = None
        self.migrate_to_chat_id = None
        self.migrate_from_chat_id = None
        self.pinned_message = None
        self.invoice = None
        self.successful_payment = None
        self.connected_website = None
        self.reply_markup = None
        for key in options:
            setattr(self, key, options[key])
        self.json = json_string

    def __html_text(self, text, entities):
        """
        Author: @sviat9440
        Message: "*Test* parse _formatting_, [url](https://example.com), [text_mention](tg://user?id=123456) and mention @username"

        Example:
            message.html_text
            >> "<b>Test</b> parse <i>formatting</i>, <a href=\"https://example.com\">url</a>, <a href=\"tg://user?id=123456\">text_mention</a> and mention @username"

        Cusom subs:
            You can customize the substitutes. By default, there is no substitute for the entities: hashtag, bot_command, email. You can add or modify substitute an existing entity.
        Example:
            message.custom_subs = {"bold": "<strong class=\"example\">{text}</strong>", "italic": "<i class=\"example\">{text}</i>", "mention": "<a href={url}>{text}</a>"}
            message.html_text
            >> "<strong class=\"example\">Test</strong> parse <i class=\"example\">formatting</i>, <a href=\"https://example.com\">url</a> and <a href=\"tg://user?id=123456\">text_mention</a> and mention <a href=\"https://t.me/username\">@username</a>"
        """
        self.custom_subs = ''
        if not entities:
            return text
        _subs = {
            "bold": "<b>{text}</b>",
            "italic": "<i>{text}</i>",
            "pre": "<pre>{text}</pre>",
            "code": "<code>{text}</code>",
            "url": "<a href=\"{url}\">{text}</a>",
            "text_link": "<a href=\"{url}\">{text}</a>"
        }
        if hasattr(self, "custom_subs"):
            for type in self.custom_subs:
                _subs[type] = self.custom_subs[type]
        utf16_text = text.encode("utf-16-le")
        html_text = ""

        def func(text, type=None, url=None, user=None):
            text = text.decode("utf-16-le")
            if type == "text_mention":
                type = "url"
                url = "tg://user?id={0}".format(user.id)
            elif type == "mention":
                url = "https://t.me/{0}".format(text[1:])
            text = text.replace("&", "&amp;").replace(
                "<", "&lt;").replace(">", "&gt;")
            if not type or not _subs.get(type):
                return text
            subs = _subs.get(type)
            return subs.format(text=text, url=url)

        offset = 0
        for entity in entities:
            if entity.offset > offset:
                html_text += func(utf16_text[offset * 2: entity.offset * 2])
                offset = entity.offset
            html_text += func(utf16_text[offset * 2: (offset + entity.length)
                                         * 2], entity.type, entity.url, entity.user)
            offset += entity.length
        if offset * 2 < len(utf16_text):
            html_text += func(utf16_text[offset * 2:])
        return html_text

    @property
    def html_text(self):
        return self.__html_text(self.text, self.entities)

    @property
    def html_caption(self):
        return self.__html_text(self.caption, self.caption_entities)


class MessageEntity(JsonDeserializable):
    """ This object represents one special entity in a text message. For example, hashtags, usernames, URLs, etc """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        type = obj['type']
        offset = obj['offset']
        length = obj['length']
        url = obj.get('url')
        user = None
        if 'user' in obj:
            user = User.de_json(obj['user'])
        language = None
        if 'language' in obj:
            language = obj['language']
        return cls(type, offset, length, url, user, language)

    def __init__(self, type, offset, length, url=None, user=None, language=None):
        self.type = type
        self.offset = offset
        self.length = length
        self.url = url
        self.user = user
        self.language = language


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
