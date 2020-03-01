import json
import six
from .utilities import is_string, generate_random_token

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


class Audio(JsonDeserializable):
    """ This object represents an audio file to be treated as music by the Telegram clients 
        :param file_id: [STRING] Identifier for this file, which can be used to download or reuse the file.
        :param file_unique_id: [STRING] Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file..
        :param duration: [INTEGER] Duration of the video in seconds as defined by sender.
        :param performer: [STRING] Optional. Performer of the audio as defined by sender or by audio tags.
        :param title: [STRING] Optional. Title of the audio as defined by sender or by audio tags.
        :param mime_type: [STRING] Optional. MIME type of the file as defined by sender.
        :param file_size: [INTEGER] Optional. File size.
        :param thumb: [PhotoSize] Optional. Thumbnail of the album cover to which the music file belongs
        :return JSON_OBJECT:
    """

    def __init__(self, file_id, file_unique_id, duration, performer=None, title=None, mime_type=None, file_size=None, thumb=None):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.duration = duration
        self.performer = performer
        self.title = title
        self.mime_type = mime_type
        self.file_size = file_size
        self.thumb = thumb

    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        file_unique_id = obj['file_unique_id']
        duration = obj['duration']
        performer = None
        if 'performer' in obj:
            performer = obj.get('performer')
        title = None
        if 'title' in obj:
            title = obj.get('title')
        mime_type = None
        if 'mime_type' in obj:
            mime_type = obj.get('mime_type')
        file_size = None
        if 'file_size' in obj:
            file_size = obj.get('file_size')
        thumb = None
        if 'thumb' in obj:
            thumb = PhotoSize.de_json(obj['thumb'])
        return cls(file_id, file_unique_id, duration, performer, title, mime_type, file_size, thumb)


class Document(JsonDeserializable):
    """ This object represents a general file (as opposed to photos, voice messages and audio files) """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        file_unique_id = obj['file_unique_id']
        thumb = None
        if 'thumb' in obj and 'file_id' in obj['thumb']:
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
        return cls(file_id, file_unique_id, thumb, file_name, mime_type, file_size)

    def __init__(self, file_id, file_unique_id, thumb=None, file_name=None, mime_type=None, file_size=None):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.thumb = thumb
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size


class Video(JsonDeserializable):
    """ This object represents a video file """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        file_unique_id = obj['file_unique_id']
        width = obj['width']
        height = obj['height']
        duration = obj['duration']
        thumb = None
        if 'thumb' in obj:
            thumb = PhotoSize.de_json(obj['thumb'])
        mime_type = None
        if 'mime_type' in obj:
            mime_type = obj.get('mime_type')
        file_size = None
        if 'file_size' in obj:
            file_size = obj.get('file_size')
        return cls(file_id, file_unique_id, width, height, duration, thumb, mime_type, file_size)

    def __init__(self, file_id, file_unique_id, width, height, duration, thumb=None, mime_type=None, file_size=None):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.duration = duration
        self.thumb = thumb
        self.mime_type = mime_type
        self.file_size = file_size


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


class Voice(JsonDeserializable):
    """ This object represents a voice note """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        file_unique_id = obj['file_unique_id']
        duration = obj['duration']
        mime_type = None
        if 'mime_type' in obj:
            mime_type = obj.get('mime_type')
        file_size = None
        if 'file_size' in obj:
            file_size = obj.get('file_size')
        return cls(file_id, file_unique_id, duration, mime_type, file_size)

    def __init__(self, file_id, file_unique_id, duration, mime_type=None, file_size=None):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.duration = duration
        self.mime_type = mime_type
        self.file_size = file_size


class VideoNote(JsonDeserializable):
    """ This object represents a video message """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        file_unique_id = obj['file_unique_id']
        length = obj['length']
        duration = obj['duration']
        thumb = None
        if 'thumb' in obj:
            thumb = PhotoSize.de_json(obj['thumb'])
        file_size = None
        if 'file_size' in obj:
            file_size = obj.get('file_size')
        return cls(file_id, file_unique_id, length, duration, thumb, file_size)

    def __init__(self, file_id, file_unique_id, length, duration, thumb=None, file_size=None):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.length = length
        self.duration = duration
        self.thumb = thumb
        self.file_size = file_size


class Contact(JsonDeserializable):
    """ This object represents a phone contact """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        phone_number = obj['phone_number']
        first_name = obj['first_name']
        last_name = None
        if 'last_name' in obj:
            last_name = obj.get('last_name')
        user_id = None
        if 'user_id' in obj:
            user_id = obj.get('user_id')
        vcard = None
        if 'vcard' in obj:
            vcard = obj.get('vcard')
        return cls(phone_number, first_name, last_name, user_id, vcard)

    def __init__(self, phone_number, first_name, last_name=None, user_id=None, vcard=None):
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id
        self.vcard = vcard


class Location(JsonDeserializable):
    """ This object represents a point on the map """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        longitude = obj['longitude']
        latitude = obj['latitude']
        return cls(longitude, latitude)

    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude


class Venue(JsonDeserializable):
    """ This object represents a venue """
    @classmethod
    def de_json(cls, json_type):
        obj = cls.check_json(json_type)
        location = Location.de_json(obj['location'])
        title = obj['title']
        address = obj['address']
        foursquare_id = None
        if 'foursquare_id' in obj:
            foursquare_id = obj.get('foursquare_id')
        foursquare_type = None
        if 'foursquare_type' in obj:
            foursquare_type = obj.get('foursquare_type')
        return cls(location, title, address, foursquare_id, foursquare_type)

    def __init__(self, location, title, address, foursquare_id=None, foursquare_type=None):
        self.location = location
        self.title = title
        self.address = address
        self.foursquare_id = foursquare_id
        self.foursquare_type = foursquare_type


class PollOption(JsonDeserializable):
    """ This object contains information about one answer option in a poll """
    @classmethod
    def de_json(cls, json_type):
        obj = cls.check_json(json_type)
        text = obj['text']
        voter_count = obj['voter_count']
        return cls(text, voter_count)

    def __init__(self, text, voter_count):
        self.text = text
        self.voter_count = voter_count


class PollAnswer(JsonDeserializable):
    """ This object represents an answer of a user in a non-anonymous poll """
    @classmethod
    def de_json(cls, json_type):
        obj = cls.check_json(json_type)
        poll_id = obj['poll_id']
        user = User.de_json(obj['user'])
        option_ids = None
        if 'option_ids' in obj:
            option_ids = obj['option_ids']
        return cls(poll_id, user, option_ids)

    def __init__(self, poll_id, user, option_ids):
        self.poll_id = poll_id
        self.user = user
        self.option_ids = option_ids


class Poll(JsonDeserializable):
    """ This object contains information about a poll """
    @classmethod
    def de_json(cls, json_type):
        obj = cls.check_json(json_type)
        poll_id = obj['id']
        question = obj['question']
        options = Poll.parse_options(obj['options'])
        is_closed = obj['is_closed']
        is_anonymous = obj['is_anonymous']
        type = obj['type']
        allows_multiple_answers = obj['allows_multiple_answers']
        correct_option_id = None
        if 'correct_option_id' in obj:
            correct_option_id = obj['correct_option_id']
        return cls(poll_id, question, options, is_closed, is_anonymous, type, allows_multiple_answers, correct_option_id)

    def __init__(self, poll_id, question, options, is_closed, is_anonymous, type, allows_multiple_answers, correct_option_id=None):
        self.poll_id = poll_id
        self.question = question
        self.options = options
        self.is_closed = is_closed
        self.is_anonymous = is_anonymous
        self.type = type
        self.allows_multiple_answers = allows_multiple_answers
        self.correct_option_id = correct_option_id

    @classmethod
    def parse_options(cls, options):
        op = []
        for option in options:
            op.append(PollOption.de_json(option))
        return op


class UserProfilePhotos(JsonDeserializable):
    """ This object represents one size of a photo or a file / sticker thumbnail """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        total_count = obj['total_count']
        photos = UserProfilePhotos.prase_photos(obj['photos'])
        return cls(total_count, photos)

    def __init__(self, total_count, photos):
        self.total_count = total_count
        self.photos = photos

    @classmethod
    def prase_photos(cls, objs):
        photos = [[PhotoSize.de_json(y) for y in x] for x in objs]
        return photos


class File(JsonDeserializable):
    """ 
    This object represents a file ready to be downloaded,
    The file can be downloaded via the link https://api.telegram.org/file/bot<token>/<file_path>,
    It is guaranteed that the link will be valid for at least 1 hour,
    When the link expires, a new one can be requested by calling getFile,
    Maximum file size to download is 20 MB.
    """
    @classmethod
    def de_json(cls, json_type):
        obj = cls.check_json(json_type)
        file_id = obj['file_id']
        file_unique_id = obj['file_unique_id']
        file_size = None
        if 'file_size' in obj:
            file_size = obj.get('file_size')
        file_path = None
        if 'file_path' in obj:
            file_path = obj.get('file_path')
        return cls(file_id, file_unique_id, file_size, file_path)

    def __init__(self, file_id, file_unique_id, file_size, file_path):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.file_size = file_size
        self.file_path = file_path


class ReplyKeyboardMarkup(JsonSerializable):
    """ This object represents a custom keyboard with reply options (see Introduction to bots for details and examples) """

    def __init__(self, resize_keyboard=None, one_time_keyboard=None, selective=None, row_width=3):
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard
        self.selective = selective
        self.row_width = row_width

        self.keyboard = []

    def add(self, *args):
        """
        This function adds strings to the keyboard, while not exceeding row_width.
        E.g. ReplyKeyboardMarkup#add("A", "B", "C") yields the json result {keyboard: [["A"], ["B"], ["C"]]}
        when row_width is set to 1.
        When row_width is set to 2, the following is the result of this function: {keyboard: [["A", "B"], ["C"]]}
        See https://core.telegram.org/bots/api#replykeyboardmarkup
        :param args: KeyboardButton to append to the keyboard
        """
        i = 1
        row = []
        for button in args:
            if is_string(button):
                row.append({'text': button})
            elif isinstance(button, bytes):
                row.append({'text': button.decode('utf-8')})
            else:
                row.append(button.to_dic())
            if i % self.row_width == 0:
                self.keyboard.append(row)
                row = []
            i += 1
        if len(row) > 0:
            self.keyboard.append(row)

    def row(self, *args):
        """
        Adds a list of KeyboardButton to the keyboard. This function does not consider row_width.
        ReplyKeyboardMarkup#row("A")#row("B", "C")#to_json() outputs '{keyboard: [["A"], ["B", "C"]]}'
        See https://core.telegram.org/bots/api#replykeyboardmarkup
        :param args: strings
        :return: self, to allow function chaining.
        """
        btn_array = []
        for button in args:
            if is_string(button):
                btn_array.append({'text': button})
            else:
                btn_array.append(button.to_dic())
        self.keyboard.append(btn_array)
        return self

    def to_json(self):
        """
        Converts this object to its json representation following the Telegram API guidelines described here:
        https://core.telegram.org/bots/api#replykeyboardmarkup
        :return:
        """
        json_dict = {'keyboard': self.keyboard}
        if self.one_time_keyboard:
            json_dict['one_time_keyboard'] = True

        if self.resize_keyboard:
            json_dict['resize_keyboard'] = True

        if self.selective:
            json_dict['selective'] = True

        return json.dumps(json_dict)


class KeyboardButton(Dictionaryable, JsonSerializable):
    """ 
    This object represents one button of the reply keyboard,
    For simple text buttons String can be used instead of this object to specify text of the button,
    Optional fields request_contact, request_location, and request_poll are mutually exclusive.
    """

    def __init__(self, text, request_contact=None, request_location=None, request_poll=None):
        self.text = text
        self.request_contact = request_contact
        self.request_location = request_location
        self.request_poll = request_poll

    def to_json(self):
        return json.dumps(self.to_dic())

    def to_dic(self):
        json_dic = {'text': self.text}
        if self.request_contact:
            json_dic['request_contact'] = self.request_contact
        if self.request_location:
            json_dic['request_location'] = self.request_location
        if self.request_poll:
            json_dic['request_poll'] = KeyboardButtonPollType(
                self.request_poll)
        return json_dic


class KeyboardButtonPollType(JsonDeserializable):
    """ This object represents type of a poll, 
    which is allowed to be created and sent when the corresponding button is pressed """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        poll_type = obj['type']
        return cls(poll_type)

    def __init__(self, poll_type):
        self.poll_type = poll_type


class ReplyKeyboardRemove(JsonSerializable):
    """ 
    Upon receiving a message with this object, 
    Telegram clients will remove the current custom keyboard and display the default letter-keyboard,
    By default, custom keyboards are displayed until a new keyboard is sent by a bot,
    An exception is made for one-time keyboards that are hidden immediately after the user presses a button (see ReplyKeyboardMarkup).
    """

    def __init__(self, selective=None):
        self.selective = selective

    def to_json(self):
        json_dict = {'remove_keyboard': True}
        if self.selective:
            json_dict['selective'] = True
        return json.dumps(json_dict)


class InlineKeyboardMarkup(Dictionaryable, JsonSerializable):
    """ This object represents an inline keyboard that appears right next to the message it belongs to. """

    def __init__(self, row_width=3):
        self.row_width = row_width

        self.keyboard = []

    def add(self, *args):
        """
        This function adds strings to the keyboard, while not exceeding row_width.
        E.g. ReplyKeyboardMarkup#add("A", "B", "C") yields the json result {keyboard: [["A"], ["B"], ["C"]]}
        when row_width is set to 1.
        When row_width is set to 2, the following is the result of this function: {keyboard: [["A", "B"], ["C"]]}
        See https://core.telegram.org/bots/api#replykeyboardmarkup
        :param args: KeyboardButton to append to the keyboard
        """
        i = 1
        row = []
        for button in args:
            row.append(button.to_dic())
            if i % self.row_width == 0:
                self.keyboard.append(row)
                row = []
            i += 1
        if len(row) > 0:
            self.keyboard.append(row)

    def row(self, *args):
        """
        Adds a list of KeyboardButton to the keyboard. This function does not consider row_width.
        ReplyKeyboardMarkup#row("A")#row("B", "C")#to_json() outputs '{keyboard: [["A"], ["B", "C"]]}'
        See https://core.telegram.org/bots/api#inlinekeyboardmarkup
        :param args: strings
        :return: self, to allow function chaining.
        """
        btn_array = []
        for button in args:
            btn_array.append(button.to_dic())
        self.keyboard.append(btn_array)
        return self

    def to_json(self):
        """
        Converts this object to its json representation following the Telegram API guidelines described here:
        https://core.telegram.org/bots/api#inlinekeyboardmarkup
        :return:
        """
        json_dict = {'inline_keyboard': self.keyboard}
        return json.dumps(json_dict)

    def to_dic(self):
        json_dict = {'inline_keyboard': self.keyboard}
        return json_dict


class InlineKeyboardButton(JsonSerializable):
    """ 
    This object represents one button of an inline keyboard, 
    You must use exactly one of the optional fields.
    """

    def __init__(self, text, url=None, callback_data=None, switch_inline_query=None,
                 switch_inline_query_current_chat=None, callback_game=None, pay=None, login_url=None):
        self.text = text
        self.url = url
        self.login_url = login_url
        self.callback_data = callback_data
        self.switch_inline_query = switch_inline_query
        self.switch_inline_query_current_chat = switch_inline_query_current_chat
        self.callback_game = callback_game
        self.pay = pay

    def to_json(self):
        return json.dumps(self.to_dic())

    def to_dic(self):
        json_dic = {'text': self.text}
        if self.url:
            json_dic['url'] = self.url
        if self.callback_data:
            json_dic['callback_data'] = self.callback_data
        if self.switch_inline_query is not None:
            json_dic['switch_inline_query'] = self.switch_inline_query
        if self.switch_inline_query_current_chat is not None:
            json_dic['switch_inline_query_current_chat'] = self.switch_inline_query_current_chat
        if self.callback_game is not None:
            json_dic['callback_game'] = self.callback_game
        if self.pay is not None:
            json_dic['pay'] = self.pay
        if self.login_url is not None:
            json_dic['login_url'] = self.login_url
        return json_dic


class LoginUrl(JsonSerializable):
    """ 
    This object represents a parameter of the inline keyboard button used to automatically authorize a user,
    Serves as a great replacement for the Telegram Login Widget when the user is coming from Telegram.
    """

    def __init__(self, url, forward_text=None, bot_username=None, request_write_access=None):
        self.url = url
        self.forward_text = forward_text
        self.bot_username = bot_username
        self.request_write_access = request_write_access

    def to_json(self):
        return json.dumps(self.to_dic())

    def to_dic(self):
        json_dic = {'url': self.url}
        if self.forward_text:
            json_dic['forward_text'] = self.forward_text
        if self.bot_username:
            json_dic['bot_username'] = self.bot_username
        if self.request_write_access:
            json_dic['request_write_access'] = self.request_write_access
        return json_dic


class CallbackQuery(JsonDeserializable):
    """ This object represents an incoming callback query from a callback button in an inline keyboard,
        If the button that originated the query was attached to a message sent by the bot, 
        the field message will be present,
        If the button was attached to a message sent via the bot (in inline mode), 
        the field inline_message_id will be present,
        Exactly one of the fields data or game_short_name will be present. 
        :param id: [STRING] Unique identifier for this query.
        :param from: [User] Sender.
        :param message: [Message] Optional. Message with the callback button that originated the query,
            Note: that message content and message date will not be available if the message is too old.
        :param inline_message_id: [STRING] Optional. Identifier of the message sent via the bot in inline mode, that originated the query.
        :param chat_instance: [STRING] Global identifier, uniquely corresponding to the chat to which the message with the callback button was sent.
        :param data: [STRING] Optional. Data associated with the callback button. Be aware that a bad client can send arbitrary data in this field.
        :param game_short_name: [STRING] Optional. Short name of a Game to be returned, serves as the unique identifier for the game.
        :return JSON_OBJECT:
    """

    def __init__(self, id, from_user, data, chat_instance, message=None, inline_message_id=None, game_short_name=None):
        self.game_short_name = game_short_name
        self.chat_instance = chat_instance
        self.id = id
        self.from_user = from_user
        self.message = message
        self.data = data
        self.inline_message_id = inline_message_id

    @classmethod
    def de_json(cls, json_type):
        obj = cls.check_json(json_type)
        id = obj['id']
        from_user = User.de_json(obj['from'])
        message = None
        if 'message' in obj:
            message = Message.de_json(obj['message'])
        inline_message_id = None
        if 'inline_message_id' in obj:
            inline_message_id = obj.get('inline_message_id')
        chat_instance = obj['chat_instance']
        data = None
        if 'data' in obj:
            data = obj.get('data')
        game_short_name = None
        if 'game_short_name' in obj:
            game_short_name = obj.get('game_short_name')
        return cls(id, from_user, data, chat_instance, message, inline_message_id, game_short_name)


class ForceReply(JsonSerializable):
    """
    Upon receiving a message with this object, 
    Telegram clients will display a reply interface to the user,
    (act as if the user has selected the bot‘s message and tapped ’Reply'),
    This can be extremely useful if you want to create user-friendly step-by-step,
    interfaces without having to sacrifice privacy mode.
    """

    def __init__(self, selective=None):
        self.selective = selective

    def to_json(self):
        json_dict = {'force_reply': True}
        if self.selective:
            json_dict['selective'] = True
        return json.dumps(json_dict)


class ChatPhoto(JsonDeserializable):
    """ This object represents a chat photo """
    @classmethod
    def de_json(cls, json_type):
        obj = cls.check_json(json_type)
        small_file_id = obj['small_file_id']
        small_file_unique_id = obj['small_file_unique_id']
        big_file_id = obj['big_file_id']
        big_file_unique_id = obj['big_file_unique_id']
        return cls(small_file_id, small_file_unique_id, big_file_id, big_file_unique_id)

    def __init__(self, small_file_id, small_file_unique_id, big_file_id, big_file_unique_id):
        self.small_file_id = small_file_id
        self.small_file_unique_id = small_file_unique_id
        self.big_file_id = big_file_id
        self.big_file_unique_id = big_file_unique_id


class ChatMember(JsonDeserializable):
    """ This object contains information about one member of a chat """
    @classmethod
    def de_json(cls, json_type):
        obj = cls.check_json(json_type)
        user = User.de_json(obj['user'])
        status = obj['status']
        custom_title = None
        if 'custom_title' in obj:
            custom_title = obj.get('custom_title')
        until_date = None
        if 'until_date' in obj:
            until_date = obj.get('until_date')
        can_be_edited = None
        if 'can_be_edited' in obj:
            can_be_edited = obj.get('can_be_edited')
        can_post_messages = None
        if 'can_post_messages' in obj:
            can_post_messages = obj.get('can_post_messages')
        can_edit_messages = None
        if 'can_edit_messages' in obj:
            can_edit_messages = obj.get('can_edit_messages')
        can_delete_messages = None
        if 'can_delete_messages' in obj:
            can_delete_messages = obj.get('can_delete_messages')
        can_restrict_members = None
        if 'can_restrict_members' in obj:
            can_restrict_members = obj.get('can_restrict_members')
        can_promote_members = None
        if 'can_promote_members' in obj:
            can_promote_members = obj.get('can_promote_members')
        can_change_info = None
        if 'can_change_info' in obj:
            can_change_info = obj.get('can_change_info')
        can_invite_users = None
        if 'can_invite_users' in obj:
            can_invite_users = obj.get('can_invite_users')
        can_pin_messages = None
        if 'can_pin_messages' in obj:
            can_pin_messages = obj.get('can_pin_messages')
        is_member = None
        if 'is_member' in obj:
            is_member = obj.get('is_member')
        can_send_messages = None
        if 'can_send_messages' in obj:
            can_send_messages = obj.get('can_send_messages')
        can_send_media_messages = None
        if 'can_send_media_messages' in obj:
            can_send_media_messages = obj.get('can_send_media_messages')
        can_send_polls = None
        if 'can_send_polls' in obj:
            can_send_polls = obj.get('can_send_polls')
        can_send_other_messages = None
        if 'can_send_other_messages' in obj:
            can_send_other_messages = obj.get('can_send_other_messages')
        can_add_web_page_previews = None
        if 'can_add_web_page_previews' in obj:
            can_add_web_page_previews = obj.get('can_add_web_page_previews')
        return cls(user, status, custom_title, until_date, can_be_edited, can_change_info, can_post_messages, can_edit_messages,
                   can_delete_messages, can_invite_users, can_restrict_members, is_member, can_pin_messages, can_promote_members,
                   can_send_messages, can_send_media_messages, can_send_other_messages, can_add_web_page_previews, can_send_polls)

    def __init__(self, user, status, custom_title, until_date, can_be_edited, can_change_info, can_post_messages, can_edit_messages,
                 can_delete_messages, can_invite_users, can_restrict_members, is_member, can_pin_messages, can_promote_members,
                 can_send_messages, can_send_media_messages, can_send_polls, can_send_other_messages, can_add_web_page_previews):
        self.user = user
        self.status = status
        self.custom_title = custom_title
        self.until_date = until_date
        self.can_be_edited = can_be_edited
        self.can_change_info = can_change_info
        self.can_post_messages = can_post_messages
        self.can_edit_messages = can_edit_messages
        self.can_delete_messages = can_delete_messages
        self.can_invite_users = can_invite_users
        self.can_restrict_members = can_restrict_members
        self.can_pin_messages = can_pin_messages
        self.is_member = is_member
        self.can_promote_members = can_promote_members
        self.can_send_messages = can_send_messages
        self.can_send_media_messages = can_send_media_messages
        self.can_send_polls = can_send_polls
        self.can_send_other_messages = can_send_other_messages
        self.can_add_web_page_previews = can_add_web_page_previews


class ChatPermissions(JsonDeserializable):
    """ Describes actions that a non-administrator user is allowed to take in a chat """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        can_send_messages = None
        if 'can_send_messages' in obj:
            can_send_messages = obj['can_send_messages']
        can_send_media_messages = None
        if 'can_send_media_messages' in obj:
            can_send_media_messages = obj['can_send_media_messages']
        can_send_polls = None
        if 'can_send_polls' in obj:
            can_send_polls = obj['can_send_polls']
        can_send_other_messages = None
        if 'can_send_other_messages' in obj:
            can_send_other_messages = obj.get('can_send_other_messages')
        can_add_web_page_previews = None
        if 'can_add_web_page_previews' in obj:
            can_add_web_page_previews = obj.get('can_add_web_page_previews')
        can_change_info = None
        if 'can_change_info' in obj:
            can_change_info = obj.get('can_change_info')
        can_invite_users = None
        if 'can_invite_users' in obj:
            can_invite_users = obj.get('can_invite_users')
        can_pin_messages = None
        if 'can_pin_messages' in obj:
            can_pin_messages = obj.get('can_pin_messages')
        return cls(can_send_messages, can_send_media_messages, can_send_polls, can_send_other_messages, can_add_web_page_previews, can_change_info, can_invite_users, can_pin_messages)

    def __init__(self, can_send_messages=None, can_send_media_messages=None, can_send_polls=None, can_send_other_messages=None, can_add_web_page_previews=None, can_change_info=None, can_invite_users=None, can_pin_messages=None):
        self.can_send_messages = can_send_messages
        self.can_send_media_messages = can_send_media_messages
        self.can_send_polls = can_send_polls
        self.can_send_other_messages = can_send_other_messages
        self.can_add_web_page_previews = can_add_web_page_previews
        self.can_change_info = can_change_info
        self.can_invite_users = can_invite_users
        self.can_pin_messages = can_pin_messages


class ResponseParameters(JsonDeserializable):
    """ Contains information about why a request was unsuccessful """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        migrate_to_chat_id = None
        if 'migrate_to_chat_id' in obj:
            migrate_to_chat_id = obj['migrate_to_chat_id']
        retry_after = None
        if 'retry_after' in obj:
            retry_after = obj['retry_after']
        return cls(migrate_to_chat_id, retry_after)

    def __init__(self, migrate_to_chat_id, retry_after):
        self.migrate_to_chat_id = migrate_to_chat_id
        self.retry_after = retry_after


class InputMedia(JsonSerializable):
    """ 
    This object represents the content of a media message to be sent,
    It should be one of:

        InputMediaAnimation
        InputMediaDocument
        InputMediaAudio
        InputMediaPhoto
        InputMediaVideo
    """

    def __init__(self, type, media, caption=None, parse_mode=None):
        self.type = type
        self.media = media
        self.caption = caption
        self.parse_mode = parse_mode

        if is_string(self.media):
            self._media_name = ''
            self._media_dic = self.media
        else:
            self._media_name = generate_random_token()
            self._media_dic = 'attach://{0}'.format(self._media_name)

    def to_json(self):
        return json.dumps(self.to_dic())

    def to_dic(self):
        ret = {'type': self.type, 'media': self._media_dic}
        if self.caption:
            ret['caption'] = self.caption
        if self.parse_mode:
            ret['parse_mode'] = self.parse_mode
        return ret

    def _convert_input_media(self):
        if is_string(self.media):
            return self.to_json(), None

        return self.to_json(), {self._media_name: self.media}


class InputMediaPhoto(InputMedia):
    """ Represents a photo to be sent """

    def __init__(self, media, caption=None, parse_mode=None):
        super(InputMediaPhoto, self).__init__(type="photo",
                                              media=media, caption=caption, parse_mode=parse_mode)

    def to_dic(self):
        ret = super(InputMediaPhoto, self).to_dic()
        return ret


class InputMediaVideo(InputMedia):
    """ Represents a video to be sent """

    def __init__(self, media, thumb=None, caption=None, parse_mode=None, width=None, height=None, duration=None,
                 supports_streaming=None):
        super(InputMediaVideo, self).__init__(type="video",
                                              media=media, caption=caption, parse_mode=parse_mode)
        self.thumb = thumb
        self.width = width
        self.height = height
        self.duration = duration
        self.supports_streaming = supports_streaming

    def to_dic(self):
        ret = super(InputMediaVideo, self).to_dic()
        if self.thumb:
            ret['thumb'] = self.thumb
        if self.width:
            ret['width'] = self.width
        if self.height:
            ret['height'] = self.height
        if self.duration:
            ret['duration'] = self.duration
        if self.supports_streaming:
            ret['supports_streaming'] = self.supports_streaming
        return ret


class InputMediaAnimation(InputMedia):
    """ Represents an animation file (GIF or H.264/MPEG-4 AVC video without sound) to be sent """

    def __init__(self, media, thumb=None, caption=None, parse_mode=None, width=None, height=None, duration=None):
        super(InputMediaAnimation, self).__init__(type="animation",
                                                  media=media, caption=caption, parse_mode=parse_mode)
        self.thumb = thumb
        self.width = width
        self.height = height
        self.duration = duration

    def to_dic(self):
        ret = super(InputMediaAnimation, self).to_dic()
        if self.thumb:
            ret['thumb'] = self.thumb
        if self.width:
            ret['width'] = self.width
        if self.height:
            ret['height'] = self.height
        if self.duration:
            ret['duration'] = self.duration
        return ret


class InputMediaAudio(InputMedia):
    """ Represents an audio file to be treated as music to be sent """

    def __init__(self, media, thumb=None, caption=None, parse_mode=None, duration=None, performer=None, title=None):
        super(InputMediaAudio, self).__init__(type="audio",
                                              media=media, caption=caption, parse_mode=parse_mode)
        self.thumb = thumb
        self.duration = duration
        self.performer = performer
        self.title = title

    def to_dic(self):
        ret = super(InputMediaAudio, self).to_dic()
        if self.thumb:
            ret['thumb'] = self.thumb
        if self.duration:
            ret['duration'] = self.duration
        if self.performer:
            ret['performer'] = self.performer
        if self.title:
            ret['title'] = self.title
        return ret


class InputMediaDocument(InputMedia):
    """ Represents a general file to be sent """

    def __init__(self, media, thumb=None, caption=None, parse_mode=None):
        super(InputMediaDocument, self).__init__(type="document",
                                                 media=media, caption=caption, parse_mode=parse_mode)
        self.thumb = thumb

    def to_dic(self):
        ret = super(InputMediaDocument, self).to_dic()
        if self.thumb:
            ret['thumb'] = self.thumb
        return ret


# InputFile
""" This object represents the contents of a file to be uploaded. 
    Must be posted using multipart/form-data in the usual way that files are uploaded via the browser.
"""


class Sticker(JsonDeserializable):
    """ This object represents a sticker """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        file_unique_id = obj['file_unique_id']
        width = obj['width']
        height = obj['height']
        is_animated = obj['is_animated']
        thumb = None
        if 'thumb' in obj:
            thumb = PhotoSize.de_json(obj['thumb'])
        emoji = None
        if 'emoji' in obj:
            emoji = obj.get('emoji')
        set_name = None
        if 'set_name' in obj:
            set_name = obj.get('set_name')
        mask_position = None
        if 'mask_position' in obj:
            mask_position = MaskPosition.de_json(obj['mask_position'])
        file_size = None
        if 'file_size' in obj:
            file_size = obj.get('file_size')
        return cls(file_id, file_unique_id, width, height, thumb, emoji, set_name, mask_position, file_size, is_animated)

    def __init__(self, file_id, file_unique_id, width, height, thumb, emoji, set_name, mask_position, file_size, is_animated):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.thumb = thumb
        self.emoji = emoji
        self.set_name = set_name
        self.mask_position = mask_position
        self.file_size = file_size
        self.is_animated = is_animated


class StickerSet(JsonDeserializable):
    """ This object represents a sticker set """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        name = obj['name']
        title = obj['title']
        contains_masks = obj['contains_masks']
        stickers = StickerSet.parse_stickers(obj['stickers'])
        return cls(name, title, contains_masks, stickers)

    def __init__(self, name, title, contains_masks, stickers):
        self.stickers = stickers
        self.contains_masks = contains_masks
        self.title = title
        self.name = name

    @classmethod
    def parse_stickers(cls, objs):
        stickers = []
        for sticker in objs:
            stickers.append(Sticker.de_json(sticker))
        return stickers


class MaskPosition(JsonDeserializable, JsonSerializable):
    """ This object describes the position on faces where a mask should be placed by default """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        point = obj['point']
        x_shift = obj['x_shift']
        y_shift = obj['y_shift']
        scale = obj['scale']
        return cls(point, x_shift, y_shift, scale)

    def __init__(self, point, x_shift, y_shift, scale):
        self.point = point
        self.x_shift = x_shift
        self.y_shift = y_shift
        self.scale = scale

    def to_json(self):
        return json.dumps(self.to_dic())

    def to_dic(self):
        return {'point': self.point, 'x_shift': self.x_shift, 'y_shift': self.y_shift, 'scale': self.scale}


class InlineQuery(JsonDeserializable):
    """
    This object represents an incoming inline query,
    When the user sends an empty query,
    your bot could return some default or trending results.
    """
    @classmethod
    def de_json(cls, json_type):
        obj = cls.check_json(json_type)
        id = obj['id']
        from_user = User.de_json(obj['from'])
        location = None
        if 'location' in obj:
            location = Location.de_json(obj['location'])
        query = obj['query']
        offset = obj['offset']
        return cls(id, from_user, location, query, offset)

    def __init__(self, id, from_user, location, query, offset):
        """
        :param id: string Unique identifier for this query
        :param from_user: User Sender
        :param location: Sender location, only for bots that request user location
        :param query: String Text of the query
        :param offset: String Offset of the results to be returned, can be controlled by the bot
        :return: InlineQuery Object
        """
        self.id = id
        self.from_user = from_user
        self.location = location
        self.query = query
        self.offset = offset


class InlineQueryResult():
    """ This object represents one result of an inline query. 
        Telegram clients currently support results of the following 20 types:
            InlineQueryResultArticle
            InlineQueryResultAudio
            InlineQueryResultCachedAudio
            InlineQueryResultCachedDocument
            InlineQueryResultCachedGif
            InlineQueryResultCachedMpeg4Gif
            InlineQueryResultCachedPhoto
            InlineQueryResultCachedSticker
            InlineQueryResultCachedVideo
            InlineQueryResultCachedVoice
            InlineQueryResultContact
            InlineQueryResultGame
            InlineQueryResultDocument
            InlineQueryResultGif
            InlineQueryResultLocation
            InlineQueryResultMpeg4Gif
            InlineQueryResultPhoto
            InlineQueryResultVenue
            InlineQueryResultVideo
            InlineQueryResultVoice
    """
    pass


class InlineQueryResultArticle(JsonSerializable):
    def __init__(self, id, title, input_message_content, reply_markup=None, url=None,
                 hide_url=None, description=None, thumb_url=None, thumb_width=None, thumb_height=None):
        """
        Represents a link to an article or web page.
        :param id: Unique identifier for this result, 1-64 Bytes.
        :param title: Title of the result.
        :param input_message_content: InputMessageContent : Content of the message to be sent
        :param reply_markup: InlineKeyboardMarkup : Inline keyboard attached to the message
        :param url: URL of the result.
        :param hide_url: Pass True, if you don't want the URL to be shown in the message.
        :param description: Short description of the result.
        :param thumb_url: Url of the thumbnail for the result.
        :param thumb_width: Thumbnail width.
        :param thumb_height: Thumbnail height
        :return:
        """
        self.type = 'article'
        self.id = id
        self.title = title
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup
        self.url = url
        self.hide_url = hide_url
        self.description = description
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

    def to_json(self):
        json_dict = {'type': self.type, 'id': self.id, 'title': self.title,
                     'input_message_content': self.input_message_content}
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup
        if self.url:
            json_dict['url'] = self.url
        if self.hide_url:
            json_dict['hide_url'] = self.hide_url
        if self.description:
            json_dict['description'] = self.description
        if self.thumb_url:
            json_dict['thumb_url'] = self.thumb_url
        if self.thumb_width:
            json_dict['thumb_width'] = self.thumb_width
        if self.thumb_height:
            json_dict['thumb_height'] = self.thumb_height
        return json.dumps(json_dict)


class InlineQueryResultAudio(JsonSerializable):
    """ Represents a link to an MP3 audio file. 
        By default, this audio file will be sent by the user. 
        Alternatively, you can use input_message_content to send a message with the specified content instead of the audio.
    """

    def __init__(self, id, audio_url, title, caption=None, parse_mode=None, performer=None, audio_duration=None,
                 reply_markup=None, input_message_content=None):
        self.type = 'audio'
        self.id = id
        self.audio_url = audio_url
        self.title = title
        self.caption = caption
        self.parse_mode = parse_mode
        self.performer = performer
        self.audio_duration = audio_duration
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    def to_json(self):
        json_dict = {'type': self.type, 'id': self.id,
                     'audio_url': self.audio_url, 'title': self.title}
        if self.caption:
            json_dict['caption'] = self.caption
        if self.parse_mode:
            json_dict['parse_mode'] = self.parse_mode
        if self.performer:
            json_dict['performer'] = self.performer
        if self.audio_duration:
            json_dict['audio_duration'] = self.audio_duration
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup.to_dic()
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content.to_dic()
        return json.dumps(json_dict)


class InlineQueryResultCachedAudio(JsonSerializable):
    """ Represents a link to an MP3 audio file stored on the Telegram servers. 
        By default, this audio file will be sent by the user. 
        Alternatively, you can use input_message_content to send a message with the specified content instead of the audio.
    """

    def __init__(self, type, id, audio_file_id, title=None, description=None, caption=None, parse_mode=None, reply_markup=None, input_message_content=None):
        self.type = type
        self.id = id
        self.audio_file_id = audio_file_id
        self.title = title
        self.description = description
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    def to_dict(self):
        json_dict = {'type': self.type, 'id': self.id,
                     'audio_file_id': self.audio_file_id}
        if self.title:
            json_dict['title'] = self.title
        if self.description:
            json_dict['description'] = self.description
        if self.caption:
            json_dict['caption'] = self.caption
        if self.parse_mode:
            json_dict['parse_mode'] = self.parse_mode
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content
        return json_dict

    def to_json(self):
        return json.dumps(self.to_dict())


class InlineQueryResultCachedDocument(JsonSerializable):
    """ Represents a link to a file stored on the Telegram servers. 
        By default, this file will be sent by the user with an optional caption. 
        Alternatively, you can use input_message_content to send a message with the specified content instead of the file.
    """

    def __init__(self, type, id, document_file_id, title=None, description=None, caption=None, parse_mode=None, reply_markup=None, input_message_content=None):
        self.type = type
        self.id = id
        self.document_file_id = document_file_id
        self.title = title
        self.description = description
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    def to_dict(self):
        json_dict = {'type': self.type, 'id': self.id,
                     'document_file_id': self.document_file_id}
        if self.title:
            json_dict['title'] = self.title
        if self.description:
            json_dict['description'] = self.description
        if self.caption:
            json_dict['caption'] = self.caption
        if self.parse_mode:
            json_dict['parse_mode'] = self.parse_mode
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content
        return json_dict

    def to_json(self):
        return json.dumps(self.to_dict())


class InlineQueryResultCachedGif(JsonSerializable):
    """ Represents a link to an animated GIF file stored on the Telegram servers. 
        By default, this animated GIF file will be sent by the user with an optional caption. 
        Alternatively, you can use input_message_content to send a message with specified content instead of the animation.
    """

    def __init__(self, type, id, gif_file_id, title=None, caption=None, parse_mode=None, reply_markup=None, input_message_content=None):
        self.type = type
        self.id = id
        self.gif_file_id = gif_file_id
        self.title = title
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    def to_dict(self):
        json_dict = {'type': self.type, 'id': self.id,
                     'gif_file_id': self.gif_file_id}
        if self.title:
            json_dict['title'] = self.title
        if self.caption:
            json_dict['caption'] = self.caption
        if self.parse_mode:
            json_dict['parse_mode'] = self.parse_mode
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content
        return json_dict

    def to_json(self):
        return json.dumps(self.to_dict())


class InlineQueryResultCachedMpeg4Gif(JsonSerializable):
    """ Represents a link to a video animation (H.264/MPEG-4 AVC video without sound) stored on the Telegram servers. 
        By default, this animated MPEG-4 file will be sent by the user with an optional caption. Alternatively, 
        you can use input_message_content to send a message with the specified content instead of the animation.
    """

    def __init__(self, type, id, mpeg4_file_id, title=None, caption=None, parse_mode=None, reply_markup=None, input_message_content=None):
        self.type = type
        self.id = id
        self.mpeg4_file_id = mpeg4_file_id
        self.title = title
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    def to_dict(self):
        json_dict = {'type': self.type, 'id': self.id,
                     'mpeg4_file_id': self.mpeg4_file_id}
        if self.title:
            json_dict['title'] = self.title
        if self.caption:
            json_dict['caption'] = self.caption
        if self.parse_mode:
            json_dict['parse_mode'] = self.parse_mode
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content
        return json_dict

    def to_json(self):
        return json.dumps(self.to_dict())


class InlineQueryResultCachedPhoto(JsonSerializable):
    """ Represents a link to a photo. By default, this photo will be sent by the user with optional caption. 
        Alternatively, you can use input_message_content to send a message with the specified content instead of the photo.
    """

    def __init__(self, type, id, photo_url, thumb_url, photo_width=None, photo_height=None, title=None, description=None, caption=None, parse_mode=None, reply_markup=None, input_message_content=None):
        self.type = type
        self.id = id
        self.photo_url = photo_url
        self.thumb_url = thumb_url
        self.photo_width = photo_width
        self.photo_height = photo_height
        self.title = title
        self.description = description
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    def to_dict(self):
        json_dict = {'type': self.type, 'id': self.id,
                     'photo_url': self.photo_url, 'thumb_url': self.thumb_url}
        if self.title:
            json_dict['title'] = self.title
        if self.description:
            json_dict['description'] = self.description
        if self.caption:
            json_dict['caption'] = self.caption
        if self.parse_mode:
            json_dict['parse_mode'] = self.parse_mode
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content
        return json_dict

    def to_json(self):
        return json.dumps(self.to_dict())


class InlineQueryResultCachedSticker(JsonSerializable):
    """ Represents a link to a sticker stored on the Telegram servers. 
        By default, this sticker will be sent by the user. 
        Alternatively, you can use input_message_content to send a message with the specified content instead of the sticker.
    """

    def __init__(self, type, id, sticker_file_id, reply_markup=None, input_message_content=None):
        self.type = type
        self.id = id
        self.sticker_file_id = sticker_file_id
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    def to_dict(self):
        json_dict = {'type': self.type, 'id': self.id,
                     'sticker_file_id': self.sticker_file_id}
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content
        return json_dict

    def to_json(self):
        return json.dumps(self.to_dict())


class InlineQueryResultCachedVideo(JsonSerializable):
    """ Represents a link to a video file stored on the Telegram servers. 
        By default, this video file will be sent by the user with an optional caption. 
        Alternatively, you can use input_message_content to send a message with the specified content instead of the video.
    """

    def __init__(self, type, id, video_file_id, title=None, description=None, caption=None, parse_mode=None, reply_markup=None, input_message_content=None):
        self.type = type
        self.id = id
        self.video_file_id = video_file_id
        self.title = title
        self.description = description
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    def to_dict(self):
        json_dict = {'type': self.type, 'id': self.id,
                     'video_file_id': self.video_file_id}
        if self.title:
            json_dict['title'] = self.title
        if self.description:
            json_dict['description'] = self.description
        if self.caption:
            json_dict['caption'] = self.caption
        if self.parse_mode:
            json_dict['parse_mode'] = self.parse_mode
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content
        return json_dict

    def to_json(self):
        return json.dumps(self.to_dict())


class InlineQueryResultCachedVoice(JsonSerializable):
    """ Represents a link to a voice message stored on the Telegram servers. 
        By default, this voice message will be sent by the user. 
        Alternatively, you can use input_message_content to send a message with the specified content instead of the voice message.
    """

    def __init__(self, type, id, voice_file_id, title=None, description=None, caption=None, parse_mode=None, reply_markup=None, input_message_content=None):
        self.type = type
        self.id = id
        self.voice_file_id = voice_file_id
        self.title = title
        self.description = description
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    def to_dict(self):
        json_dict = {'type': self.type, 'id': self.id,
                     'voice_file_id': self.voice_file_id}
        if self.title:
            json_dict['title'] = self.title
        if self.description:
            json_dict['description'] = self.description
        if self.caption:
            json_dict['caption'] = self.caption
        if self.parse_mode:
            json_dict['parse_mode'] = self.parse_mode
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content
        return json_dict

    def to_json(self):
        return json.dumps(self.to_dict())


class InlineQueryResultContact(JsonSerializable):
    """ Represents a contact with a phone number. 
        By default, this contact will be sent by the user. 
        Alternatively, you can use input_message_content to send a message with the specified content instead of the contact.
    """

    def __init__(self, id, phone_number, first_name, last_name=None, reply_markup=None,
                 input_message_content=None, thumb_url=None, thumb_width=None, thumb_height=None):
        self.type = 'contact'
        self.id = id
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

    def to_json(self):
        json_dict = {'type': self.type, 'id': self.id,
                     'phone_number': self.phone_number, 'first_name': self.first_name}
        if self.last_name:
            json_dict['last_name'] = self.last_name
        if self.thumb_url:
            json_dict['thumb_url'] = self.thumb_url
        if self.thumb_width:
            json_dict['thumb_width'] = self.thumb_width
        if self.thumb_height:
            json_dict['thumb_height'] = self.thumb_height
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content
        return json.dumps(json_dict)


class InlineQueryResultGame(JsonSerializable):
    """ Represents a Game """

    def __init__(self, id, game_short_name, reply_markup=None):
        self.type = 'game'
        self.id = id
        self.game_short_name = game_short_name
        self.reply_markup = reply_markup

    def to_json(self):
        json_dic = {'type': self.type, 'id': self.id,
                    'game_short_name': self.game_short_name}
        if self.reply_markup:
            json_dic['reply_markup'] = self.reply_markup.to_dic()
        return json.dumps(json_dic)


class InlineQueryResultDocument(JsonSerializable):
    """ Represents a link to a file. 
        By default, this file will be sent by the user with an optional caption. 
        Alternatively, you can use input_message_content to send a message with the specified content instead of the file. 
        Currently, only .PDF and .ZIP files can be sent using this method.
    """

    def __init__(self, id, title, document_url, mime_type, caption=None, parse_mode=None, description=None,
                 reply_markup=None, input_message_content=None, thumb_url=None, thumb_width=None, thumb_height=None):
        self.type = 'document'
        self.id = id
        self.title = title
        self.document_url = document_url
        self.mime_type = mime_type
        self.caption = caption
        self.parse_mode = parse_mode
        self.description = description
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

    def to_json(self):
        json_dict = {'type': self.type, 'id': self.id, 'title': self.title, 'document_url': self.document_url,
                     'mime_type': self.mime_type}
        if self.caption:
            json_dict['caption'] = self.caption
        if self.parse_mode:
            json_dict['parse_mode'] = self.parse_mode
        if self.description:
            json_dict['description'] = self.description
        if self.thumb_url:
            json_dict['thumb_url'] = self.thumb_url
        if self.thumb_width:
            json_dict['thumb_width'] = self.thumb_width
        if self.thumb_height:
            json_dict['thumb_height'] = self.thumb_height
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup.to_dic()
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content.to_dic()
        return json.dumps(json_dict)


class InlineQueryResultGif(JsonSerializable):
    """ Represents a link to an animated GIF file. 
        By default, this animated GIF file will be sent by the user with optional caption. 
        Alternatively, you can use input_message_content to send a message with the specified content instead of the animation.
    """

    def __init__(self, id, gif_url, thumb_url, gif_width=None, gif_height=None, title=None, caption=None,
                 reply_markup=None, input_message_content=None, gif_duration=None):
        """
        :param id: Unique identifier for this result, 1-64 bytes.
        :param gif_url: A valid URL for the GIF file. File size must not exceed 1MB
        :param thumb_url: URL of the static thumbnail (jpeg or gif) for the result.
        :param gif_width: Width of the GIF.
        :param gif_height: Height of the GIF.
        :param title: Title for the result.
        :param caption:  Caption of the GIF file to be sent, 0-200 characters
        :param reply_markup: InlineKeyboardMarkup : Inline keyboard attached to the message
        :param input_message_content: InputMessageContent : Content of the message to be sent instead of the photo
        :return:
        """
        self.type = 'gif'
        self.id = id
        self.gif_url = gif_url
        self.gif_width = gif_width
        self.gif_height = gif_height
        self.thumb_url = thumb_url
        self.title = title
        self.caption = caption
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.gif_duration = gif_duration

    def to_json(self):
        json_dict = {'type': self.type, 'id': self.id,
                     'gif_url': self.gif_url, 'thumb_url': self.thumb_url}
        if self.gif_height:
            json_dict['gif_height'] = self.gif_height
        if self.gif_width:
            json_dict['gif_width'] = self.gif_width
        if self.title:
            json_dict['title'] = self.title
        if self.caption:
            json_dict['caption'] = self.caption
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup.to_dic()
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content.to_dic()
        if self.gif_duration:
            json_dict['gif_duration'] = self.gif_duration
        return json.dumps(json_dict)


class InlineQueryResultLocation(JsonSerializable):
    """ Represents a location on a map. 
        By default, the location will be sent by the user. 
        Alternatively, you can use input_message_content to send a message with the specified content instead of the location.
    """

    def __init__(self, id, title, latitude, longitude, live_period=None, reply_markup=None,
                 input_message_content=None, thumb_url=None, thumb_width=None, thumb_height=None):
        self.type = 'location'
        self.id = id
        self.title = title
        self.latitude = latitude
        self.longitude = longitude
        self.live_period = live_period
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

    def to_json(self):
        json_dict = {'type': self.type, 'id': self.id, 'title': self.title,
                     'latitude': self.latitude, 'longitude': self.longitude}
        if self.live_period:
            json_dict['live_period'] = self.live_period
        if self.thumb_url:
            json_dict['thumb_url'] = self.thumb_url
        if self.thumb_width:
            json_dict['thumb_width'] = self.thumb_width
        if self.thumb_height:
            json_dict['thumb_height'] = self.thumb_height
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup.to_dic()
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content.to_dic()
        return json.dumps(json_dict)


class InlineQueryResultMpeg4Gif(JsonSerializable):
    """ Represents a link to a video animation (H.264/MPEG-4 AVC video without sound). 
        By default, this animated MPEG-4 file will be sent by the user with optional caption. 
        Alternatively, you can use input_message_content to send a message with the specified content instead of the animation.
    """

    def __init__(self, id, mpeg4_url, thumb_url, mpeg4_width=None, mpeg4_height=None, title=None, caption=None,
                 parse_mode=None, reply_markup=None, input_message_content=None, mpeg4_duration=None):
        """
        Represents a link to a video animation (H.264/MPEG-4 AVC video without sound).
        :param id: Unique identifier for this result, 1-64 bytes
        :param mpeg4_url: A valid URL for the MP4 file. File size must not exceed 1MB
        :param thumb_url: URL of the static thumbnail (jpeg or gif) for the result
        :param mpeg4_width: Video width
        :param mpeg4_height: Video height
        :param title: Title for the result
        :param caption: Caption of the MPEG-4 file to be sent, 0-200 characters
        :param parse_mode: Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text
        or inline URLs in the media caption.
        :param reply_markup: InlineKeyboardMarkup : Inline keyboard attached to the message
        :param input_message_content: InputMessageContent : Content of the message to be sent instead of the photo
        :return:
        """
        self.type = 'mpeg4_gif'
        self.id = id
        self.mpeg4_url = mpeg4_url
        self.mpeg4_width = mpeg4_width
        self.mpeg4_height = mpeg4_height
        self.thumb_url = thumb_url
        self.title = title
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.mpeg4_duration = mpeg4_duration

    def to_json(self):
        json_dict = {'type': self.type, 'id': self.id,
                     'mpeg4_url': self.mpeg4_url, 'thumb_url': self.thumb_url}
        if self.mpeg4_width:
            json_dict['mpeg4_width'] = self.mpeg4_width
        if self.mpeg4_height:
            json_dict['mpeg4_height'] = self.mpeg4_height
        if self.title:
            json_dict['title'] = self.title
        if self.caption:
            json_dict['caption'] = self.caption
        if self.parse_mode:
            json_dict['parse_mode'] = self.parse_mode
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup.to_dic()
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content.to_dic()
        if self.mpeg4_duration:
            json_dict['mpeg4_duration '] = self.mpeg4_duration
        return json.dumps(json_dict)


class InlineQueryResultPhoto(JsonSerializable):
    """ Represents a link to a photo. 
        By default, this photo will be sent by the user with optional caption. 
        Alternatively, you can use input_message_content to send a message with the specified content instead of the photo.
    """

    def __init__(self, id, photo_url, thumb_url, photo_width=None, photo_height=None, title=None,
                 description=None, caption=None, parse_mode=None, reply_markup=None, input_message_content=None):
        """
        Represents a link to a photo.
        :param id: Unique identifier for this result, 1-64 bytes
        :param photo_url: A valid URL of the photo. Photo must be in jpeg format. Photo size must not exceed 5MB
        :param thumb_url: URL of the thumbnail for the photo
        :param photo_width: Width of the photo.
        :param photo_height: Height of the photo.
        :param title: Title for the result.
        :param description: Short description of the result.
        :param caption: Caption of the photo to be sent, 0-200 characters.
        :param parse_mode: Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or
        inline URLs in the media caption.
        :param reply_markup: InlineKeyboardMarkup : Inline keyboard attached to the message
        :param input_message_content: InputMessageContent : Content of the message to be sent instead of the photo
        :return:
        """
        self.type = 'photo'
        self.id = id
        self.photo_url = photo_url
        self.photo_width = photo_width
        self.photo_height = photo_height
        self.thumb_url = thumb_url
        self.title = title
        self.description = description
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    def to_json(self):
        json_dict = {'type': self.type, 'id': self.id,
                     'photo_url': self.photo_url, 'thumb_url': self.thumb_url}
        if self.photo_width:
            json_dict['photo_width'] = self.photo_width
        if self.photo_height:
            json_dict['photo_height'] = self.photo_height
        if self.title:
            json_dict['title'] = self.title
        if self.description:
            json_dict['description'] = self.description
        if self.caption:
            json_dict['caption'] = self.caption
        if self.parse_mode:
            json_dict['parse_mode'] = self.parse_mode
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup.to_dic()
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content.to_dic()
        return json.dumps(json_dict)


class InlineQueryResultVenue(JsonSerializable):
    """ Represents a venue. 
        By default, the venue will be sent by the user. 
        Alternatively, you can use input_message_content to send a message with the specified content instead of the venue.
    """

    def __init__(self, id, title, latitude, longitude, address, foursquare_id=None, reply_markup=None,
                 input_message_content=None, thumb_url=None, thumb_width=None, thumb_height=None):
        self.type = 'venue'
        self.id = id
        self.title = title
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.foursquare_id = foursquare_id
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

    def to_json(self):
        json_dict = {'type': self.type, 'id': self.id, 'title': self.title, 'latitude': self.latitude,
                     'longitude': self.longitude, 'address': self.address}
        if self.foursquare_id:
            json_dict['foursquare_id'] = self.foursquare_id
        if self.thumb_url:
            json_dict['thumb_url'] = self.thumb_url
        if self.thumb_width:
            json_dict['thumb_width'] = self.thumb_width
        if self.thumb_height:
            json_dict['thumb_height'] = self.thumb_height
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup.to_dic()
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content.to_dic()
        return json.dumps(json_dict)


class InlineQueryResultVideo(JsonSerializable):
    """ Represents a link to a page containing an embedded video player or a video file. 
        By default, this video file will be sent by the user with an optional caption. 
        Alternatively, you can use input_message_content to send a message with the specified content instead of the video.

        If an InlineQueryResultVideo message contains an embedded video (e.g., YouTube), 
        you must replace its content using input_message_content.
    """

    def __init__(self, id, video_url, mime_type, thumb_url, title,
                 caption=None, parse_mode=None, video_width=None, video_height=None, video_duration=None,
                 description=None, reply_markup=None, input_message_content=None):
        """
        Represents link to a page containing an embedded video player or a video file.
        :param id: Unique identifier for this result, 1-64 bytes
        :param video_url: A valid URL for the embedded video player or video file
        :param mime_type: Mime type of the content of video url, “text/html” or “video/mp4”
        :param thumb_url: URL of the thumbnail (jpeg only) for the video
        :param title: Title for the result
        :param parse_mode: Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or
        inline URLs in the media caption.
        :param video_width: Video width
        :param video_height: Video height
        :param video_duration: Video duration in seconds
        :param description: Short description of the result
        :return:
        """
        self.type = 'video'
        self.id = id
        self.video_url = video_url
        self.mime_type = mime_type
        self.video_width = video_width
        self.video_height = video_height
        self.video_duration = video_duration
        self.thumb_url = thumb_url
        self.title = title
        self.caption = caption
        self.parse_mode = parse_mode
        self.description = description
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup

    def to_json(self):
        json_dict = {'type': self.type, 'id': self.id, 'video_url': self.video_url, 'mime_type': self.mime_type,
                     'thumb_url': self.thumb_url, 'title': self.title}
        if self.video_width:
            json_dict['video_width'] = self.video_width
        if self.video_height:
            json_dict['video_height'] = self.video_height
        if self.video_duration:
            json_dict['video_duration'] = self.video_duration
        if self.description:
            json_dict['description'] = self.description
        if self.caption:
            json_dict['caption'] = self.caption
        if self.parse_mode:
            json_dict['parse_mode'] = self.parse_mode
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup.to_dic()
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content.to_dic()
        return json.dumps(json_dict)


class InlineQueryResultVoice(JsonSerializable):
    """ Represents a link to a voice recording in an .ogg container encoded with OPUS. 
        By default, this voice recording will be sent by the user. 
        Alternatively, you can use input_message_content to send a message with the specified content instead of the the voice message.
    """

    def __init__(self, id, voice_url, title, caption=None, parse_mode=None, performer=None, voice_duration=None,
                 reply_markup=None, input_message_content=None):
        self.type = 'voice'
        self.id = id
        self.voice_url = voice_url
        self.title = title
        self.caption = caption
        self.parse_mode = parse_mode
        self.performer = performer
        self.voice_duration = voice_duration
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    def to_json(self):
        json_dict = {'type': self.type, 'id': self.id,
                     'voice_url': self.voice_url, 'title': self.title}
        if self.caption:
            json_dict['caption'] = self.caption
        if self.parse_mode:
            json_dict['parse_mode'] = self.parse_mode
        if self.performer:
            json_dict['performer'] = self.performer
        if self.voice_duration:
            json_dict['voice_duration'] = self.voice_duration
        if self.reply_markup:
            json_dict['reply_markup'] = self.reply_markup.to_dic()
        if self.input_message_content:
            json_dict['input_message_content'] = self.input_message_content.to_dic()
        return json.dumps(json_dict)


class InputMessageContent():
    """
    This object represents the content of a message to be sent as a result of an inline query. 
    Telegram clients currently support the following 4 types:

        InputContactMessageContent
        InputLocationMessageContent
        InputTextMessageContent
        InputVenueMessageContent

   """
    pass


class InputTextMessageContent(Dictionaryable):
    """
        Represents the content of a text message to be sent as the result of an inline query.
    """

    def __init__(self, message_text, parse_mode=None, disable_web_page_preview=None):
        self.message_text = message_text
        self.parse_mode = parse_mode
        self.disable_web_page_preview = disable_web_page_preview

    def to_dic(self):
        json_dic = {'message_text': self.message_text}
        if self.parse_mode:
            json_dic['parse_mode'] = self.parse_mode
        if self.disable_web_page_preview:
            json_dic['disable_web_page_preview'] = self.disable_web_page_preview
        return json_dic


class InputLocationMessageContent(Dictionaryable):
    """ Represents the content of a location message to be sent as the result of an inline query """

    def __init__(self, latitude, longitude, live_period=None):
        self.latitude = latitude
        self.longitude = longitude
        self.live_period = live_period

    def to_dic(self):
        json_dic = {'latitude': self.latitude, 'longitude': self.longitude}
        if self.live_period:
            json_dic['live_period'] = self.live_period
        return json_dic


class InputVenueMessageContent(Dictionaryable):
    """ Represents the content of a venue message to be sent as the result of an inline query """

    def __init__(self, latitude, longitude, title, address, foursquare_id=None, foursquare_type=None):
        self.latitude = latitude
        self.longitude = longitude
        self.title = title
        self.address = address
        self.foursquare_id = foursquare_id
        self.foursquare_type = foursquare_type

    def to_dic(self):
        json_dic = {'latitude': self.latitude, 'longitude': self.longitude, 'title': self.title,
                    'address': self.address}
        if self.foursquare_id:
            json_dic['foursquare_id'] = self.foursquare_id
        if self.foursquare_type:
            json_dic['foursquare_type'] = self.foursquare_type
        return json_dic


class InputContactMessageContent(Dictionaryable):
    """ Represents a result of an inline query that was chosen by the user and sent to their chat partner """

    def __init__(self, phone_number, first_name, last_name=None):
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name

    def to_dic(self):
        json_dic = {'phone_number': self.phone_number,
                    'first_name': self.first_name}
        if self.last_name:
            json_dic['last_name'] = self.last_name
        return json_dic


class ChosenInlineResult(JsonDeserializable):
    """ Represents a result of an inline query that was chosen by the user and sent to their chat partner """
    @classmethod
    def de_json(cls, json_type):
        obj = cls.check_json(json_type)
        result_id = obj['result_id']
        from_user = User.de_json(obj['from'])
        query = obj['query']
        location = None
        if 'location' in obj:
            location = Location.de_json(obj['location'])
        inline_message_id = obj.get('inline_message_id')
        return cls(result_id, from_user, query, location, inline_message_id)

    def __init__(self, result_id, from_user, query, location=None, inline_message_id=None):
        """
        :param result_id: string The unique identifier for the result that was chosen.
        :param from_user: User The user that chose the result.
        :param query: String The query that was used to obtain the result.
        :return: ChosenInlineResult Object.
        """
        self.result_id = result_id
        self.from_user = from_user
        self.query = query
        self.location = location
        self.inline_message_id = inline_message_id


class LabeledPrice(JsonSerializable):
    """ This object represents a portion of the price for goods or services """

    def __init__(self, label, amount):
        self.label = label
        self.amount = amount

    def to_json(self):
        return json.dumps(self.to_dic())

    def to_dic(self):
        return {'label': self.label, 'amount': self.amount}


class Invoice(JsonDeserializable):
    """ This object contains basic information about an invoice """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        title = obj['title']
        description = obj['description']
        start_parameter = obj['start_parameter']
        currency = obj['currency']
        total_amount = obj['total_amount']
        return cls(title, description, start_parameter, currency, total_amount)

    def __init__(self, title, description, start_parameter, currency, total_amount):
        self.title = title
        self.description = description
        self.start_parameter = start_parameter
        self.currency = currency
        self.total_amount = total_amount


class ShippingAddress(JsonDeserializable):
    """ This object represents a shipping address """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        country_code = obj['country_code']
        state = obj['state']
        city = obj['city']
        street_line1 = obj['street_line1']
        street_line2 = obj['street_line2']
        post_code = obj['post_code']
        return cls(country_code, state, city, street_line1, street_line2, post_code)

    def __init__(self, country_code, state, city, street_line1, street_line2, post_code):
        self.country_code = country_code
        self.state = state
        self.city = city
        self.street_line1 = street_line1
        self.street_line2 = street_line2
        self.post_code = post_code


class OrderInfo(JsonDeserializable):
    """ This object represents information about an order """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        name = None
        if 'name' in obj:
            name = obj.get('name')
        phone_number = None
        if 'phone_number' in obj:
            phone_number = obj.get('phone_number')
        email = None
        if 'email' in obj:
            email = obj.get('email')
        shipping_address = None
        if 'shipping_address' in obj:
            shipping_address = ShippingAddress.de_json(obj['shipping_address'])
        return cls(name, phone_number, email, shipping_address)

    def __init__(self, name, phone_number, email, shipping_address):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.shipping_address = shipping_address


class ShippingOption(JsonSerializable):
    """ This object represents one shipping option """

    def __init__(self, id, title):
        self.id = id
        self.title = title
        self.prices = []

    def add_price(self, *args):
        """
        Add LabeledPrice to ShippingOption
        :param args: LabeledPrices
        """
        for price in args:
            self.prices.append(price)
        return self

    def to_json(self):
        price_list = []
        for p in self.prices:
            price_list.append(p.to_dic())
        json_dict = json.dumps(
            {'id': self.id, 'title': self.title, 'prices': price_list})
        return json_dict


class SuccessfulPayment(JsonDeserializable):
    """ This object contains basic information about a successful payment """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        currency = obj['currency']
        total_amount = obj['total_amount']
        invoice_payload = obj['invoice_payload']
        shipping_option_id = None
        if 'shipping_option_id' in obj:
            shipping_option_id = obj.get('shipping_option_id')
        order_info = None
        if 'order_info' in obj:
            order_info = OrderInfo.de_json(obj['order_info'])
        telegram_payment_charge_id = obj['telegram_payment_charge_id']
        provider_payment_charge_id = obj['provider_payment_charge_id']
        return cls(currency, total_amount, invoice_payload, shipping_option_id, order_info,
                   telegram_payment_charge_id, provider_payment_charge_id)

    def __init__(self, currency, total_amount, invoice_payload, shipping_option_id, order_info,
                 telegram_payment_charge_id, provider_payment_charge_id):
        self.currency = currency
        self.total_amount = total_amount
        self.invoice_payload = invoice_payload
        self.shipping_option_id = shipping_option_id
        self.order_info = order_info
        self.telegram_payment_charge_id = telegram_payment_charge_id
        self.provider_payment_charge_id = provider_payment_charge_id


class ShippingQuery(JsonDeserializable):
    """ This object contains information about an incoming shipping query """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        id = obj['id']
        from_user = User.de_json(obj['from'])
        invoice_payload = obj['invoice_payload']
        shipping_address = ShippingAddress.de_json(obj['shipping_address'])
        return cls(id, from_user, invoice_payload, shipping_address)

    def __init__(self, id, from_user, invoice_payload, shipping_address):
        self.id = id
        self.from_user = from_user
        self.invoice_payload = invoice_payload
        self.shipping_address = shipping_address


class PreCheckoutQuery(JsonDeserializable):
    """ This object contains information about an incoming pre-checkout query """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        id = obj['id']
        from_user = User.de_json(obj['from'])
        currency = obj['currency']
        total_amount = obj['total_amount']
        invoice_payload = obj['invoice_payload']
        shipping_option_id = None
        if 'shipping_option_id' in obj:
            shipping_option_id = obj.get('shipping_option_id')
        order_info = None
        if 'order_info' in obj:
            order_info = OrderInfo.de_json(obj['order_info'])
        return cls(id, from_user, currency, total_amount, invoice_payload, shipping_option_id, order_info)

    def __init__(self, id, from_user, currency, total_amount, invoice_payload, shipping_option_id, order_info):
        self.id = id
        self.from_user = from_user
        self.currency = currency
        self.total_amount = total_amount
        self.invoice_payload = invoice_payload
        self.shipping_option_id = shipping_option_id
        self.order_info = order_info


class PassportData(JsonDeserializable):
    """ Contains information about Telegram Passport data shared with the bot by the user """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        data = obj['EncryptedPassportElement']
        credentials = obj['EncryptedCredentials']
        return cls(data, credentials)

    def __init__(self, data, credentials):
        self.data = data
        self.credentials = credentials


class PassportFile(JsonDeserializable):
    """This object represents a file uploaded to Telegram Passport,
    Currently all Telegram Passport files are in JPEG format when decrypted and don't exceed 10MB."""
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        file_unique_id = obj['file_unique_id']
        file_size = obj['file_size']
        file_date = obj['file_date']
        return cls(file_id, file_unique_id, file_size, file_date)

    def __init__(self, file_id, file_unique_id, file_size, file_date):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.file_size = file_size
        self.file_date = file_date


class EncryptedPassportElement(JsonDeserializable):
    """ Contains information about documents or other Telegram Passport elements shared with the bot by the user """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        type = obj['type']
        data = None
        if 'data' in obj:
            data = obj['data']
        phone_number = None
        if 'phone_number' in obj:
            phone_number = obj['phone_number']
        files = None
        if 'files' in obj:
            files = EncryptedPassportElement.parse_files(obj['files'])
        front_side = None
        if 'front_side' in obj:
            front_side = PassportFile.de_json(obj['front_side'])
        reverse_side = None
        if 'reverse_side' in obj:
            reverse_side = PassportFile.de_json(obj['reverse_side'])
        selfie = None
        if 'selfie' in obj:
            selfie = PassportFile.de_json(obj['selfie'])
        translation = None
        if 'translation' in obj:
            translation = EncryptedPassportElement.parse_translation(
                obj['translation'])
        hash = obj.get('hash')
        return cls(type, data, phone_number, files, front_side, reverse_side, selfie, translation, hash)

    def __init__(self, type, data, phone_number, files, front_side, reverse_side, selfie, translation, hash):
        self.type = type
        self.data = data
        self.phone_number = phone_number
        self.files = files
        self.front_side = front_side
        self.reverse_side = reverse_side
        self.selfie = selfie
        self.translation = translation
        self.hash = hash

    @classmethod
    def parse_files(cls, objs):
        files = []
        for x in objs:
            file = PassportFile.de_json(x)
            files.append(file)
        return files

    @classmethod
    def parse_translation(cls, objs):
        translations = []
        for x in objs:
            translation = PassportFile.de_json(x)
            translations.append(translation)
        return translations


class EncryptedCredentials(JsonDeserializable):
    """Contains data required for decrypting and authenticating EncryptedPassportElement. 
    See the Telegram Passport Documentation for a complete description of the data decryption and authentication processes."""
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        data = obj['data']
        hash = obj['hash']
        secret = obj['secret']
        return cls(data, hash, secret)

    def __init__(self, data, hash, secret):
        self.data = data
        self.hash = hash
        self.secret = secret


class PassportElementError(JsonDeserializable):
    """ This object represents an error in the Telegram Passport element 
    which was submitted that should be resolved by the user. 
    It should be one of:
        PassportElementErrorDataField
        PassportElementErrorFrontSide
        PassportElementErrorReverseSide
        PassportElementErrorSelfie
        PassportElementErrorFile
        PassportElementErrorFiles
        PassportElementErrorTranslationFile
        PassportElementErrorTranslationFiles
        PassportElementErrorUnspecified
    """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        source = None
        if 'source' in obj:
            source = obj['source']

        if source == 'data':
            return PassportElementErrorDataField.de_json(json_string)
        elif source == 'front_side':
            return PassportElementErrorFrontSide.de_json(json_string)
        elif source == 'reverse_side':
            return PassportElementErrorReverseSide.de_json(json_string)
        elif source == 'selfie':
            return PassportElementErrorSelfie.de_json(json_string)
        elif source == 'file_hashe':
            return PassportElementErrorFile.de_json(json_string)
        elif source == 'file_hashes':
            return PassportElementErrorFiles.de_json(json_string)
        elif source == 'translation_files':
            return PassportElementErrorTranslationFile.de_json(json_string)
        elif source == 'translation_files':
            return PassportElementErrorTranslationFiles.de_json(json_string)
        elif source == 'unspecified':
            return PassportElementErrorUnspecified.de_json(json_string)
        else:
            return None


class PassportElementErrorDataField(JsonDeserializable):
    """ Represents an issue in one of the data fields that was provided by the user. 
    The error is considered resolved when the field's value changes """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        source = obj['source']  # Error source, must be data
        type = obj['type']
        field_name = obj['field_name']
        data_hash = obj['data_hash']
        message = obj['message']
        return cls(source, type, field_name, data_hash, message)

    def __init__(self, source, type, field_name, data_hash, message):
        self.source = source
        self.type = type
        self.field_name = field_name
        self.data_hash = data_hash
        self.message = message


class PassportElementErrorFrontSide(JsonDeserializable):
    """ Represents an issue with the front side of a document,
    The error is considered resolved when the file with the front side of the document changes.
    """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        source = obj['source']  # Error source, must be front_side
        type = obj['type']
        file_hash = obj['file_hash']
        message = obj['message']
        return cls(source, type, file_hash, message)

    def __init__(self, source, type, file_hash, message):
        self.source = source
        self.type = type
        self.file_hash = file_hash
        self.message = message


class PassportElementErrorFile(JsonDeserializable):
    """ Represents an issue with a document scan. 
    The error is considered resolved when the file with the document scan changes.
    """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        source = obj['source']  # Error source, must be file
        type = obj['type']
        file_hash = obj['file_hash']
        message = obj['message']
        return cls(source, type, file_hash, message)

    def __init__(self, source, type, file_hash, message):
        self.source = source
        self.type = type
        self.file_hash = file_hash
        self.message = message


class PassportElementErrorFiles(JsonDeserializable):
    """ Represents an issue with a list of scans. 
    The error is considered resolved when the list of files containing the scans changes.
    """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        source = obj['source']  # Error source, must be files
        type = obj['type']
        file_hashes = obj['file_hashes']
        message = obj['message']
        return cls(source, type, file_hashes, message)

    def __init__(self, source, type, file_hashes, message):
        self.source = source
        self.type = type
        self.file_hashes = file_hashes
        self.message = message


class PassportElementErrorReverseSide(JsonDeserializable):
    """ Represents an issue with the reverse side of a document,
    The error is considered resolved when the file with reverse side of the document changes.
    """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        source = obj['source']  # Error source, must be reverse_side
        type = obj['type']
        file_hash = obj['file_hash']
        message = obj['message']
        return cls(source, type, file_hash, message)

    def __init__(self, source, type, file_hash, message):
        self.source = source
        self.type = type
        self.file_hash = file_hash
        self.message = message


class PassportElementErrorSelfie(JsonDeserializable):
    """ Represents an issue with the selfie with a document. 
    The error is considered resolved when the file with the selfie changes.
    """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        source = obj['source']  # Error source, must be selfie
        type = obj['type']
        file_hash = obj['file_hash']
        message = obj['message']
        return cls(source, type, file_hash, message)

    def __init__(self, source, type, file_hash, message):
        self.source = source
        self.type = type
        self.file_hash = file_hash
        self.message = message


class PassportElementErrorTranslationFile(JsonDeserializable):
    """ Represents an issue with one of the files that constitute the translation of a document,
    The error is considered resolved when the file changes.
    """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        source = obj['source']  # Error source, must be translation_file
        type = obj['type']
        file_hash = obj['file_hash']
        message = obj['message']
        return cls(source, type, file_hash, message)

    def __init__(self, source, type, file_hash, message):
        self.source = source
        self.type = type
        self.file_hash = file_hash
        self.message = message


class PassportElementErrorTranslationFiles(JsonDeserializable):
    """ Represents an issue with the translated version of a document. 
    The error is considered resolved when a file with the document translation change.
    """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        source = obj['source']  # Error source, must be translation_files
        type = obj['type']
        file_hashes = obj['file_hashes']
        message = obj['message']
        return cls(source, type, file_hashes, message)

    def __init__(self, source, type, file_hashes, message):
        self.source = source
        self.type = type
        self.file_hashes = file_hashes
        self.message = message


class PassportElementErrorUnspecified(JsonDeserializable):
    """ Represents an issue in an unspecified place. 
    The error is considered resolved when new data is added.
    """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        source = obj['source']  # Error source, must be unspecified
        type = obj['type']
        element_hash = obj['element_hash']
        message = obj['message']
        return cls(source, type, element_hash, message)

    def __init__(self, source, type, element_hash, message):
        self.source = source
        self.type = type
        self.element_hash = element_hash
        self.message = message


class Game(JsonDeserializable):
    """ This object represents a game. Use BotFather to create and edit games, their short names will act as unique identifiers """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        title = obj['title']
        description = obj['description']
        photo = Game.parse_photo(obj['photo'])
        text = obj['text']
        text_entities = None
        if 'text_entities' in obj:
            text_entities = Game.parse_entities(obj['text_entities'])
        animation = None
        if 'animation' in obj:
            animation = Animation.de_json(obj['animation'])
        return cls(title, description, photo, text, text_entities, animation)

    @classmethod
    def parse_photo(cls, objs):
        photos = []
        for x in objs:
            photos.append(PhotoSize.de_json(x))
        return photos

    @classmethod
    def parse_entities(cls, objs):
        entities = []
        for x in objs:
            entities.append(MessageEntity.de_json(x))
        return entities

    def __init__(self, title, description, photo, text=None, text_entities=None, animation=None):
        self.title = title
        self.description = description
        self.photo = photo
        self.text = text
        self.text_entities = text_entities
        self.animation = animation


class CallbackGame:
    """ A placeholder, currently holds no information. Use BotFather to set up your game. """
    pass


class GameHighScore(JsonDeserializable):
    """ This object represents one row of the high scores table for a game """
    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        position = obj['position']
        user = User.de_json(obj['user'])
        score = obj['score']
        return cls(position, user, score)

    def __init__(self, position, user, score):
        self.position = position
        self.user = user
        self.score = score
