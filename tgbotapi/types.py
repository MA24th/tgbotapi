# -*- coding: utf-8 -*-

"""
tgbotapi.types
~~~~~~~~~~~~~~
This module contains the basic types of Telegram Bot API used in tgbotapi,
such as Update, Message, etc.

:copyright: (c) 2022 by Mustafa Asaad.
:license: GPLv2, see LICENSE for more details.
"""
from .utils import JsonDeserializable, JsonSerializable


class Update(JsonDeserializable):
    """
    This object represents an incoming update
    """

    def __init__(self, update_id, message, edited_message, channel_post, edited_channel_post, inline_query,
                 chosen_inline_result, callback_query, shipping_query, pre_checkout_query, poll, poll_answer,
                 my_chat_member, chat_member, chat_join_request):
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
        self.poll_answer = poll_answer
        self.my_chat_member = my_chat_member
        self.chat_member = chat_member
        self.chat_join_request = chat_join_request

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
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
            pre_checkout_query = PreCheckoutQuery.de_json(obj['pre_checkout_query'])
        poll = None
        if 'poll' in obj:
            poll = Poll.de_json(obj['poll'])
        poll_answer = None
        if 'poll_answer' in obj:
            poll_answer = PollAnswer.de_json(obj['poll_answer'])
        my_chat_member = None
        if 'my_chat_member' in obj:
            my_chat_member = ChatMemberUpdated.de_json(obj['my_chat_member'])
        chat_member = None
        if 'chat_member' in obj:
            chat_member = ChatMemberUpdated.de_json(obj['chat_member'])
        chat_join_request = None
        if 'chat_join_request' in obj:
            chat_join_request = ChatJoinRequest.de_json(obj['chat_join_request'])
        return cls(update_id, message, edited_message, channel_post, edited_channel_post, inline_query,
                   chosen_inline_result, callback_query, shipping_query, pre_checkout_query, poll, poll_answer,
                   my_chat_member, chat_member, chat_join_request)


class WebhookInfo(JsonDeserializable):
    def __init__(self, url, has_custom_certificate, pending_update_count, ip_address, last_error_date,
                 last_error_message, last_synchronization_error_date, max_connections, allowed_updates):
        """
        Contains information about the current status of a webhook
        """
        self.url = url
        self.has_custom_certificate = has_custom_certificate
        self.pending_update_count = pending_update_count
        self.ip_address = ip_address
        self.last_error_date = last_error_date
        self.last_error_message = last_error_message
        self.last_synchronization_error_date = last_synchronization_error_date
        self.max_connections = max_connections
        self.allowed_updates = allowed_updates

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        url = obj['url']
        has_custom_certificate = False
        if 'has_custom_certificate' in obj:
            has_custom_certificate = obj['has_custom_certificate']
        pending_update_count = obj['pending_update_count']
        ip_address = None
        if 'ip_address' in obj:
            ip_address = obj['ip_address']
        last_error_date = None
        if 'last_error_message' in obj:
            last_error_date = obj['last_error_date']
        last_error_message = None
        if 'last_error_message' in obj:
            last_error_message = obj['last_error_message']
        last_synchronization_error_date = None
        if 'last_synchronization_error_date' in obj:
            last_synchronization_error_date = obj['last_synchronization_error_date']
        max_connections = None
        if 'max_connections' in obj:
            max_connections = obj['max_connections']
        allowed_updates = None
        if 'allowed_updates' in obj:
            allowed_updates = obj['allowed_updates']
        return cls(url, has_custom_certificate, pending_update_count, ip_address, last_error_date, last_error_message,
                   last_synchronization_error_date, max_connections, allowed_updates)


class User(JsonDeserializable):
    def __init__(self, uid, is_bot, first_name, last_name, username, language_code, can_join_groups,
                 can_read_all_group_messages, supports_inline_queries):
        """
        This object represents a Telegram user or bot
        """
        self.uid = uid
        self.is_bot = is_bot
        self.first_name = first_name
        self.username = username
        self.last_name = last_name
        self.language_code = language_code
        self.can_join_groups = can_join_groups
        self.can_read_all_group_messages = can_read_all_group_messages
        self.supports_inline_queries = supports_inline_queries

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        uid = obj['id']
        is_bot = obj['is_bot']
        first_name = obj['first_name']
        last_name = None
        if 'last_name' in obj:
            last_name = obj['last_name']
        username = None
        if 'username' in obj:
            username = obj['username']
        language_code = None
        if 'language_code' in obj:
            language_code = obj['language_code']
        can_join_groups = False
        if 'can_join_groups' in obj:
            can_join_groups = obj['can_join_groups']
        can_read_all_group_messages = False
        if 'can_read_all_group_messages' in obj:
            can_read_all_group_messages = obj['can_read_all_group_messages']
        supports_inline_queries = False
        if 'supports_inline_queries' in obj:
            supports_inline_queries = obj['supports_inline_queries']
        return cls(uid, is_bot, first_name, last_name, username, language_code, can_join_groups,
                   can_read_all_group_messages, supports_inline_queries)


class Chat(JsonDeserializable):
    def __init__(self, uid, ttype, title, username, first_name, last_name, photo, bio, has_private_forwards,
                 description, invite_link, pinned_message, permissions, slow_mode_delay, message_auto_delete_time,
                 has_protected_content, sticker_set_name, can_set_sticker_set, linked_chat_id, location):
        """
        This object represents a chat
        """
        self.uid = uid
        self.ttype = ttype
        self.title = title
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.photo = photo
        self.bio = bio
        self.has_private_forwards = has_private_forwards
        self.description = description
        self.invite_link = invite_link
        self.pinned_message = pinned_message
        self.permissions = permissions
        self.slow_mode_delay = slow_mode_delay
        self.message_auto_delete_time = message_auto_delete_time
        self.has_protected_content = has_protected_content
        self.sticker_set_name = sticker_set_name
        self.can_set_sticker_set = can_set_sticker_set
        self.linked_chat_id = linked_chat_id
        self.location = location

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        uid = obj['id']
        ttype = obj['type']
        title = None
        if 'title' in obj:
            title = obj['title']
        username = None
        if 'username' in obj:
            username = obj['username']
        first_name = None
        if 'first_name' in obj:
            first_name = obj['first_name']
        last_name = None
        if 'last_name' in obj:
            last_name = obj['last_name']
        photo = None
        if 'photo' in obj:
            photo = ChatPhoto.de_json(obj['photo'])
        bio = None
        if 'bio' in obj:
            bio = obj['bio']
        has_private_forwards = False
        if 'has_private_forwards' in obj:
            has_private_forwards = obj['has_private_forwards']
        description = None
        if 'description' in obj:
            description = obj['description']
        invite_link = None
        if 'invite_link' in obj:
            invite_link = obj['invite_link']
        pinned_message = None
        if 'pinned_message' in obj:
            pinned_message = Message.de_json(obj['pinned_message'])
        permissions = None
        if 'permissions' in obj:
            permissions = ChatPermissions.de_json(obj['permissions'])
        slow_mode_delay = None
        if 'slow_mode_delay' in obj:
            slow_mode_delay = obj['slow_mode_delay']
        message_auto_delete_time = None
        if 'message_auto_delete_time' in obj:
            message_auto_delete_time = obj['message_auto_delete_time']
        has_protected_content = False
        if 'has_protected_content' in obj:
            has_protected_content = obj['has_protected_content']
        sticker_set_name = None
        if 'sticker_set_name' in obj:
            sticker_set_name = obj['sticker_set_name']
        can_set_sticker_set = False
        if 'can_set_sticker_set' in obj:
            can_set_sticker_set = obj['can_set_sticker_set']
        linked_chat_id = None
        if 'linked_chat_id' in obj:
            linked_chat_id = obj['linked_chat_id']
        location = None
        if 'location' in obj:
            location = ChatLocation.de_json(obj['location'])
        return cls(uid, ttype, title, username, first_name, last_name, photo, bio, has_private_forwards, description,
                   invite_link, pinned_message, permissions, slow_mode_delay, message_auto_delete_time,
                   has_protected_content, sticker_set_name, can_set_sticker_set, linked_chat_id, location)


class Message(JsonDeserializable):
    """
    This object represents a message
    """

    def __init__(self, message_id, attrs):
        """
        Initializes a Message object
        :param int message_id: Unique message identifier
        """
        self.message_id = message_id
        self.ffrom = None
        self.sender_chat = None
        self.date = None
        self.chat = None
        self.forward_from = None
        self.forward_from_chat = None
        self.forward_from_message_id = None
        self.forward_signature = None
        self.forward_sender_name = None
        self.forward_date = None
        self.is_automatic_forward = False
        self.reply_to_message = None
        self.via_bot = None
        self.edit_date = None
        self.has_protected_content = False
        self.media_group_id = None
        self.author_signature = None
        self.text = None
        self.entities = None
        self.animation = None
        self.audio = None
        self.document = None
        self.photo = None
        self.sticker = None
        self.video = None
        self.video_note = None
        self.voice = None
        self.caption = None
        self.caption_entities = None
        self.contact = None
        self.dice = None
        self.game = None
        self.poll = None
        self.venue = None
        self.location = None
        self.new_chat_members = None
        self.left_chat_member = None
        self.new_chat_title = None
        self.new_chat_photo = None
        self.delete_chat_photo = False
        self.group_chat_created = False
        self.supergroup_chat_created = False
        self.channel_chat_created = False
        self.message_auto_delete_timer_changed = None
        self.migrate_to_chat_id = None
        self.migrate_from_chat_id = None
        self.pinned_message = None
        self.invoice = None
        self.successful_payment = None
        self.connected_website = None
        self.passport_data = None
        self.proximity_alert_triggered = None
        self.video_chat_scheduled = None
        self.video_chat_started = None
        self.video_chat_ended = None
        self.video_chat_participants_invited = None
        self.web_app_data = None
        self.reply_markup = None
        for key in attrs:
            setattr(self, key, attrs[key])

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        message_id = obj['message_id']
        attrs = {}
        if 'from' in obj:
            attrs['ffrom'] = User.de_json(obj['from'])
        if 'sender_chat' in obj:
            attrs['sender_chat'] = Chat.de_json(obj['sender_chat'])
        if 'data' in obj:
            attrs['date'] = obj['data']
        if 'chat' in obj:
            attrs['chat'] = Chat.de_json(obj['chat'])
        if 'forward_from' in obj:
            attrs['forward_from'] = User.de_json(obj['forward_from'])
        if 'forward_from_chat' in obj:
            attrs['forward_from_chat'] = Chat.de_json(obj['forward_from_chat'])
        if 'forward_from_message_id' in obj:
            attrs['forward_from_message_id'] = obj['forward_from_message_id']
        if 'forward_signature' in obj:
            attrs['forward_signature'] = obj['forward_signature']
        if 'forward_sender_name' in obj:
            attrs['forward_sender_name'] = obj['forward_sender_name']
        if 'forward_date' in obj:
            attrs['forward_date'] = obj['forward_date']
        if 'is_automatic_forward' in obj:
            attrs['is_automatic_forward'] = obj['is_automatic_forward']
        if 'reply_to_message' in obj:
            attrs['reply_to_message'] = Message.de_json(obj['reply_to_message'])
        if 'via_bot' in obj:
            attrs['via_bot'] = User.de_json(obj['via_bot'])
        if 'edit_date' in obj:
            attrs['edit_date'] = obj['edit_date']
        if 'has_protected_content' in obj:
            attrs['has_protected_content'] = obj['has_protected_content']
        if 'media_group_id' in obj:
            attrs['media_group_id'] = obj['media_group_id']
        if 'author_signature' in obj:
            attrs['author_signature'] = obj['author_signature']
        if 'text' in obj:
            attrs['text'] = obj['text']
        if 'entities' in obj:
            attrs['entities'] = Message.parse_entities(obj['entities'])
        if 'animation' in obj:
            attrs['animation'] = Animation.de_json(obj['animation'])
        if 'audio' in obj:
            attrs['audio'] = Audio.de_json(obj['audio'])
        if 'document' in obj:
            attrs['document'] = Document.de_json(obj['document'])
        if 'photo' in obj:
            attrs['photo'] = Message.parse_photo(obj['photo'])
        if 'sticker' in obj:
            attrs['sticker'] = Sticker.de_json(obj['sticker'])
        if 'video' in obj:
            attrs['video'] = Video.de_json(obj['video'])
        if 'video_note' in obj:
            attrs['video_note'] = VideoNote.de_json(obj['video_note'])
        if 'voice' in obj:
            attrs['voice'] = Audio.de_json(obj['voice'])
        if 'caption' in obj:
            attrs['caption'] = obj['caption']
        if 'caption_entities' in obj:
            attrs['caption_entities'] = Message.parse_entities(obj['caption_entities'])
        if 'contact' in obj:
            attrs['contact'] = Contact.de_json(obj['contact'])
        if 'dice' in obj:
            attrs['dice'] = Dice.de_json(obj['dice'])
        if 'game' in obj:
            attrs['game'] = Game.de_json(obj['game'])
        if 'poll' in obj:
            attrs['poll'] = Poll.de_json(obj['poll'])
        if 'venue' in obj:
            attrs['venue'] = Venue.de_json(obj['venue'])
        if 'location' in obj:
            attrs['location'] = Location.de_json(obj['location'])
        if 'new_chat_members' in obj:
            attrs['new_chat_members'] = Message.parse_users(obj['new_chat_members'])
        if 'left_chat_member' in obj:
            attrs['left_chat_member'] = User.de_json(obj['left_chat_member'])
        if 'new_chat_title' in obj:
            attrs['new_chat_title'] = obj['new_chat_title']
        if 'new_chat_photo' in obj:
            attrs['new_chat_photo'] = Message.parse_photo(obj['new_chat_photo'])
        if 'delete_chat_photo' in obj:
            attrs['delete_chat_photo'] = obj['delete_chat_photo']
        if 'group_chat_created' in obj:
            attrs['group_chat_created'] = obj['group_chat_created']
        if 'supergroup_chat_created' in obj:
            attrs['supergroup_chat_created'] = obj['supergroup_chat_created']
        if 'channel_chat_created' in obj:
            attrs['channel_chat_created'] = obj['channel_chat_created']
        if 'message_auto_delete_timer_changed' in obj:
            attrs['message_auto_delete_timer_changed'] = MessageAutoDeleteTimerChanged.de_json(
                obj['message_auto_delete_timer_changed'])
        if 'migrate_to_chat_id' in obj:
            attrs['migrate_to_chat_id'] = obj['migrate_to_chat_id']
        if 'migrate_from_chat_id' in obj:
            attrs['migrate_from_chat_id'] = obj['migrate_from_chat_id']
        if 'pinned_message' in obj:
            attrs['pinned_message'] = Message.de_json(obj['pinned_message'])
        if 'invoice' in obj:
            attrs['invoice'] = Invoice.de_json(obj['invoice'])
        if 'successful_payment' in obj:
            attrs['successful_payment'] = SuccessfulPayment.de_json(obj['successful_payment'])
        if 'connected_website' in obj:
            attrs['connected_website'] = obj['connected_website']
        if 'passport_data' in obj:
            attrs['passport_data'] = obj['passport_data']
        if 'proximity_alert_triggered' in obj:
            attrs['proximity_alert_triggered'] = ProximityAlertTriggered.de_json(obj['proximity_alert_triggered'])
        if 'video_chat_scheduled' in obj:
            attrs['video_chat_scheduled'] = VideoChatScheduled.de_json(obj['video_chat_scheduled'])
        if 'video_chat_started' in obj:
            attrs['video_chat_started'] = VideoChatStarted.de_json(obj['video_chat_started'])
        if 'video_chat_ended' in obj:
            attrs['video_chat_ended'] = VideoChatEnded.de_json(obj['video_chat_ended'])
        if 'video_chat_participants_invited' in obj:
            attrs['video_chat_participants_invited'] = VideoChatParticipantsInvited.de_json(
                obj['video_chat_participants_invited'])
        if 'web_app_data' in obj:
            attrs['web_app_data'] = obj['web_app_data']
        if 'reply_markup' in obj:
            attrs['reply_markup'] = InlineKeyboardMarkup.de_json(obj['reply_markup'])
        return cls(message_id, attrs)

    @classmethod
    def parse_photo(cls, obj):
        photos = []
        for x in obj:
            photos.append(PhotoSize.de_json(x))
        return photos

    @classmethod
    def parse_entities(cls, obj):
        entities = []
        for x in obj:
            entities.append(MessageEntity.de_json(x))
        return entities

    @classmethod
    def parse_users(cls, obj):
        users = []
        for x in obj:
            users.append(User.de_json(x))
        return users


class MessageId(JsonDeserializable):
    """
    This object represents a unique message identifier.
    """

    def __init__(self, message_id):
        self.message_id = message_id

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        message_id = obj['message_id']
        return cls(message_id)


class MessageEntity(JsonSerializable, JsonDeserializable):
    def __init__(self, ttype, offset, length, url, user, language):
        """
        This object represents one special entity in a text message. For example, hashtags, usernames, URLs, etc.
        :param str ttype: Type of the entity. Currently, can be “mention” (@username), “hashtag” (#hashtag), “cash-tag”
                         ($USD), “bot_command” (/start@jobs_bot), “url” (https://telegram.org),
                         “email” (do-not-reply@telegram.org), “phone_number” (+1-212-555-0123), “bold” (bold text),
                         “italic” (italic text), “underline” (underlined text), “strikethrough” (strikethrough text),
                         “spoiler” (spoiler message), “code” (mono-width string), “pre” (mono-width block),
                         “text_link” (for clickable text URLs), “text_mention” (for users without usernames)
        :param int offset: Offset in UTF-16 code units to the start of the entity
        :param int length: Length of the entity in UTF-16 code units
        :param str or None url: Optional. For “text_link” only, url that will be opened after user taps on the text
        :param User or None user: Optional. For “text_mention” only, the mentioned user
        :param str or None language: Optional. For “pre” only, the programming language of the entity text
        """
        self.ttype = ttype
        self.offset = offset
        self.length = length
        self.url = url
        self.user = user
        self.language = language

    def to_dict(self):
        """
        :rtype: dict
        """
        obj = {'type': self.ttype, 'offset': self.offset, 'length': self.length}
        if self.url:
            obj['url'] = self.url
        if self.user:
            obj['user'] = self.user
        if self.language:
            obj['language'] = self.language
        return obj

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        ttype = obj['type']
        offset = obj['offset']
        length = obj['length']
        url = None
        if 'url' in obj:
            url = obj['url']
        user = None
        if 'user' in obj:
            user = User.de_json(obj['user'])
        language = None
        if 'language' in obj:
            language = obj['language']
        return cls(ttype, offset, length, url, user, language)


class PhotoSize(JsonDeserializable):
    def __init__(self, file_id, file_unique_id, width, height, file_size):
        """
        This object represents one size of a photo or a file / sticker thumbnail
        """
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.file_size = file_size

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        file_id = obj['file_id']
        file_unique_id = obj['file_unique_id']
        width = obj['width']
        height = obj['height']
        file_size = None
        if 'file_size' in obj:
            file_size = obj['file_size']
        return cls(file_id, file_unique_id, width, height, file_size)


class Animation(JsonDeserializable):
    def __init__(self, file_id, file_unique_id, width, height, duration, thumb, file_name, mime_type, file_size):
        """
        This object represents an animation file (GIF or H.264/MPEG-4 AVC video without sound)
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
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
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
            file_name = obj['file_name']
        mime_type = None
        if 'mime_type' in obj:
            mime_type = obj['mime_type']
        file_size = None
        if 'file_size' in obj:
            file_size = obj['file_size']
        return cls(file_id, file_unique_id, width, height, duration, thumb, file_name, mime_type, file_size)


class Audio(JsonDeserializable):
    def __init__(self, file_id, file_unique_id, duration, performer, title, file_name, mime_type, file_size, thumb):
        """
        This object represents an audio file to be treated as music by the Telegram clients
        """
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.duration = duration
        self.performer = performer
        self.title = title
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
        self.thumb = thumb

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        file_id = obj['file_id']
        file_unique_id = obj['file_unique_id']
        duration = obj['duration']
        performer = None
        if 'performer' in obj:
            performer = obj['performer']
        title = None
        if 'title' in obj:
            title = obj['title']
        file_name = None
        if 'file_name' in obj:
            file_name = obj['file_name']
        mime_type = None
        if 'mime_type' in obj:
            mime_type = obj['mime_type']
        file_size = None
        if 'file_size' in obj:
            file_size = obj['file_size']
        thumb = None
        if 'thumb' in obj:
            thumb = PhotoSize.de_json(obj['thumb'])
        return cls(file_id, file_unique_id, duration, performer, title, file_name, mime_type, file_size, thumb)


class Document(JsonDeserializable):
    def __init__(self, file_id, file_unique_id, thumb, file_name, mime_type, file_size):
        """
        This object represents a general file
        """
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.thumb = thumb
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        file_id = obj['file_id']
        file_unique_id = obj['file_unique_id']
        thumb = None
        if 'thumb' in obj:
            thumb = PhotoSize.de_json(obj['thumb'])
        file_name = None
        if 'file_name' in obj:
            file_name = obj['file_name']
        mime_type = None
        if 'mime_type' in obj:
            mime_type = obj['mime_type']
        file_size = None
        if 'file_size' in obj:
            file_size = obj['file_size']
        return cls(file_id, file_unique_id, thumb, file_name, mime_type, file_size)


class Video(JsonDeserializable):
    def __init__(self, file_id, file_unique_id, width, height, duration, thumb, file_name, mime_type, file_size):
        """
        This object represents a video file
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
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
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
            file_name = obj['file_name']
        mime_type = None
        if 'mime_type' in obj:
            mime_type = obj['mime_type']
        file_size = None
        if 'file_size' in obj:
            file_size = obj['file_size']
        return cls(file_id, file_unique_id, width, height, duration, thumb, file_name, mime_type, file_size)


class VideoNote(JsonDeserializable):
    def __init__(self, file_id, file_unique_id, length, duration, thumb, file_size):
        """
        This object represents a video message
        """
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.length = length
        self.duration = duration
        self.thumb = thumb
        self.file_size = file_size

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        file_id = obj['file_id']
        file_unique_id = obj['file_unique_id']
        length = obj['length']
        duration = obj['duration']
        thumb = None
        if 'thumb' in obj:
            thumb = PhotoSize.de_json(obj['thumb'])
        file_size = None
        if 'file_size' in obj:
            file_size = obj['file_size']
        return cls(file_id, file_unique_id, length, duration, thumb, file_size)


class Voice(JsonDeserializable):
    def __init__(self, file_id, file_unique_id, duration, mime_type, file_size):
        """
        This object represents a voice note
        """
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.duration = duration
        self.mime_type = mime_type
        self.file_size = file_size

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        file_id = obj['file_id']
        file_unique_id = obj['file_unique_id']
        duration = obj['duration']
        mime_type = None
        if 'mime_type' in obj:
            mime_type = obj['mime_type']
        file_size = None
        if 'file_size' in obj:
            file_size = obj['file_size']
        return cls(file_id, file_unique_id, duration, mime_type, file_size)


class Contact(JsonDeserializable):
    def __init__(self, phone_number, first_name, last_name, user_id, vcard):
        """
        This object represents a phone contact
        """
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id
        self.vcard = vcard

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        phone_number = obj['phone_number']
        first_name = obj['first_name']
        last_name = None
        if 'last_name' in obj:
            last_name = obj['last_name']
        user_id = None
        if 'user_id' in obj:
            user_id = obj['user_id']
        vcard = None
        if 'vcard' in obj:
            vcard = obj['vcard']
        return cls(phone_number, first_name, last_name, user_id, vcard)


class Dice(JsonDeserializable):
    def __init__(self, emoji, value):
        """
        This object represents a dice with random value
        """
        self.emoji = emoji
        self.value = value

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        emoji = obj['emoji']
        value = obj['value']
        return cls(emoji, value)


class PollOption(JsonDeserializable):
    def __init__(self, text, voter_count):
        """
        This object contains information about one answer option in a poll
        """
        self.text = text
        self.voter_count = voter_count

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        text = obj['text']
        voter_count = obj['voter_count']
        return cls(text, voter_count)


class PollAnswer(JsonDeserializable):
    def __init__(self, poll_id, user, option_ids):
        """
        This object represents an answer of a user in a non-anonymous poll
        """
        self.poll_id = poll_id
        self.user = user
        self.option_ids = option_ids

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        poll_id = obj['poll_id']
        user = User.de_json(obj['user'])
        option_ids = None
        if 'option_ids' in obj:
            option_ids = obj['option_ids']
        return cls(poll_id, user, option_ids)


class Poll(JsonDeserializable):
    def __init__(self, uid, question, options, total_voter_count, is_closed, is_anonymous, ttype,
                 allows_multiple_answers, correct_option_id, explanation, explanation_entities, open_period,
                 close_date):
        """
        This object contains information about a poll
        """
        self.uid = uid
        self.question = question
        self.options = options
        self.total_voter_count = total_voter_count
        self.is_closed = is_closed
        self.is_anonymous = is_anonymous
        self.ttype = ttype
        self.allows_multiple_answers = allows_multiple_answers
        self.correct_option_id = correct_option_id
        self.explanation = explanation
        self.explanation_entities = explanation_entities
        self.open_period = open_period
        self.close_date = close_date

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        uid = obj['id']
        question = obj['question']
        options = Poll.parse_options(obj['options'])
        total_voter_count = obj['total_voter_count']
        is_closed = obj['is_closed']
        is_anonymous = obj['is_anonymous']
        ttype = obj['type']
        allows_multiple_answers = True
        if 'allows_multiple_answers' in obj:
            allows_multiple_answers = obj['allows_multiple_answers']
        correct_option_id = None
        if 'correct_option_id' in obj:
            correct_option_id = obj['correct_option_id']
        explanation = None
        if 'explanation' in obj:
            explanation = obj['explanation']
        explanation_entities = None
        if 'explanation_entities' in obj:
            explanation_entities = Poll.parse_explanation_entities(obj['explanation_entities'])
        open_period = None
        if 'open_period' in obj:
            open_period = obj['open_period']
        close_date = None
        if 'close_date' in obj:
            close_date = obj['close_date']
        return cls(uid, question, options, total_voter_count, is_closed, is_anonymous, ttype, allows_multiple_answers,
                   correct_option_id, explanation, explanation_entities, open_period, close_date)

    @classmethod
    def parse_options(cls, obj):
        options = []
        for x in obj:
            options.append(PollOption.de_json(x))
        return options

    @classmethod
    def parse_explanation_entities(cls, obj):
        explanation_entities = []
        for x in obj:
            explanation_entities.append(MessageEntity.de_json(x))
        return explanation_entities


class Location(JsonDeserializable):
    def __init__(self, longitude, latitude, horizontal_accuracy, live_period, heading, proximity_alert_radius):
        """
        This object represents a point on the map
        """
        self.longitude = longitude
        self.latitude = latitude
        self.horizontal_accuracy = horizontal_accuracy
        self.live_period = live_period
        self.heading = heading
        self.proximity_alert_radius = proximity_alert_radius

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        longitude = obj['longitude']
        latitude = obj['latitude']
        horizontal_accuracy = None
        if 'horizontal_accuracy' in obj:
            horizontal_accuracy = obj['horizontal_accuracy']
        live_period = None
        if 'live_period' in obj:
            live_period = obj['live_period']
        heading = None
        if 'heading' in obj:
            heading = obj['heading']
        proximity_alert_radius = None
        if 'proximity_alert_radius' in obj:
            proximity_alert_radius = obj['proximity_alert_radius']
        return cls(longitude, latitude, horizontal_accuracy, live_period, heading, proximity_alert_radius)


class Venue(JsonDeserializable):
    def __init__(self, location, title, address, foursquare_id, foursquare_type, google_place_id, google_place_type):
        """
        This object represents a venue
        """
        self.location = location
        self.title = title
        self.address = address
        self.foursquare_id = foursquare_id
        self.foursquare_type = foursquare_type
        self.google_place_id = google_place_id
        self.google_place_type = google_place_type

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        location = Location.de_json(obj['location'])
        title = obj['title']
        address = obj['address']
        foursquare_id = None
        if 'foursquare_id' in obj:
            foursquare_id = obj['foursquare_id']
        foursquare_type = None
        if 'foursquare_type' in obj:
            foursquare_type = obj['foursquare_type']
        google_place_id = None
        if 'google_place_id' in obj:
            google_place_id = obj['google_place_id']
        google_place_type = None
        if 'google_place_type' in obj:
            google_place_type = obj['google_place_type']
        return cls(location, title, address, foursquare_id, foursquare_type, google_place_id, google_place_type)


class WebAppData(JsonDeserializable):
    """
    Contains data sent from a Web App to the bot.
    """

    def __init__(self, data, button_text):
        """
        Initialize a WebAppData instance
        :param str data: Data sent from the web app
        :param str button_text: Text of the web_app keyboard button
        """
        self.data = data
        self.button_text = button_text

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        data = obj['data']
        button_text = obj['button_text']
        return cls(data, button_text)


class ProximityAlertTriggered(JsonDeserializable):
    def __init__(self, traveler, watcher, distance):
        """
        This object represents the content of a service message,
        sent whenever a user in the chat triggers a proximity alert set by another user
        """
        self.traveler = traveler
        self.watcher = watcher
        self.distance = distance

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        traveler = User.de_json(obj['traveler'])
        watcher = User.de_json(obj['watcher'])
        distance = obj['distance']
        return cls(traveler, watcher, distance)


class MessageAutoDeleteTimerChanged(JsonDeserializable):
    def __init__(self, message_auto_delete_time):
        """
        This object represents a service message about a change in auto-delete timer settings
        """
        self.message_auto_delete_time = message_auto_delete_time

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        message_auto_delete_time = obj['message_auto_delete_time']
        return cls(message_auto_delete_time)


class VideoChatScheduled(JsonDeserializable):
    def __init__(self, start_date):
        """
        This object represents a service message about a voice chat scheduled in the chat
        """
        self.start_date = start_date

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        start_date = obj['start_date']
        return cls(start_date)


class VideoChatStarted(JsonDeserializable):
    def __init__(self, field):
        """
        This object represents a service message about a voice chat started in the chat
        """
        self.field = field

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        field = None
        if obj:
            field = obj
        return cls(field)


class VideoChatEnded(JsonDeserializable):
    def __init__(self, duration):
        """
        This object represents a service message about a voice chat ended in the chat
        """
        self.duration = duration

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        duration = obj['duration']
        return cls(duration)


class VideoChatParticipantsInvited(JsonDeserializable):
    def __init__(self, users):
        """
        This object represents a service message about new members invited to a voice chat
        """
        self.users = users

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        users = None
        if 'users' in obj:
            users = VideoChatParticipantsInvited.parse_users(obj['users'])
        return cls(users)

    @classmethod
    def parse_users(cls, obj):
        users = []
        for x in obj:
            users.append(User.de_json(x))
        return users


class UserProfilePhotos(JsonDeserializable):
    def __init__(self, total_count, photos):
        """
        This object represents one size of a photo or a file / sticker thumbnail
        """
        self.total_count = total_count
        self.photos = photos

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        total_count = obj['total_count']
        photos = UserProfilePhotos.parse_photos(obj['photos'])
        return cls(total_count, photos)

    @classmethod
    def parse_photos(cls, obj):
        photos = [[PhotoSize.de_json(y) for y in x] for x in obj]
        return photos


class File(JsonDeserializable):
    def __init__(self, file_id, file_unique_id, file_size, file_path):
        """
        This object represents a file ready to be downloaded.
        """
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.file_size = file_size
        self.file_path = file_path

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        file_id = obj['file_id']
        file_unique_id = obj['file_unique_id']
        file_size = None
        if 'file_size' in obj:
            file_size = obj['file_size']
        file_path = None
        if 'file_path' in obj:
            file_path = obj['file_path']
        return cls(file_id, file_unique_id, file_size, file_path)


class WebAppInfo(JsonDeserializable):
    """
    Contains information about a Web App
    """

    def __init__(self, url):
        """
        :param str url: Web App url
        """
        self.url = url

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        url = obj['url']
        return cls(url)


class ReplyKeyboardMarkup(JsonSerializable, JsonDeserializable):
    def __init__(self, keyboard, resize_keyboard=False, one_time_keyboard=False, input_field_placeholder=None,
                 selective=False):
        """
        This object represents a custom keyboard with reply options (see Introduction to bots for details and examples)
        :param list[list[KeyboardButton]] keyboard: Array of button rows, each represented by an Array of KeyboardButton
                                                    objects
        :param bool resize_keyboard: Optional. Requests clients to resize the keyboard vertically for optimal fit
        :param bool one_time_keyboard: Optional. Requests clients to hide the keyboard as soon as it's been used
        :param str or None input_field_placeholder: Optional. The placeholder to be shown in the input field when the
                                                    keyboard is active; 1-64 characters
        :param bool selective:Optional. Use this parameter if you want to show the keyboard to specific users only
        """
        self.keyboard = keyboard
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard
        self.input_field_placeholder = input_field_placeholder
        self.selective = selective

    def to_dict(self):
        obj = {'keyboard': self.keyboard}
        if self.one_time_keyboard:
            obj['one_time_keyboard'] = self.one_time_keyboard
        if self.resize_keyboard:
            obj['resize_keyboard'] = self.resize_keyboard
        if self.input_field_placeholder:
            obj['input_field_placeholder'] = self.input_field_placeholder
        if self.selective:
            obj['selective'] = self.selective
        return obj

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        keyboard = ReplyKeyboardMarkup.parse_keyboard_button(obj['keyboard'])
        one_time_keyboard = False
        if 'one_time_keyboard' in obj:
            one_time_keyboard = obj['one_time_keyboard']
        resize_keyboard = False
        if 'resize_keyboard' in obj:
            resize_keyboard = obj['resize_keyboard']
        input_field_placeholder = None
        if 'input_field_placeholder' in obj:
            input_field_placeholder = obj['input_field_placeholder']
        selective = False
        if 'selective' in obj:
            selective = obj['selective']
        return cls(keyboard, one_time_keyboard, resize_keyboard, input_field_placeholder, selective)

    @classmethod
    def parse_keyboard_button(cls, obj):
        row = []
        column = []
        for x in obj:
            for y in x:
                column.append(KeyboardButton.de_json(y))
            row.append(column)
        return row


class KeyboardButton(JsonSerializable, JsonDeserializable):
    def __init__(self, text, request_contact=False, request_location=False, request_poll=None, web_app=None):
        """
        This object represents one button of the reply keyboard
        :param str text: Text of the button
        :param bool request_contact: Optional. If True, the user's phone number will be sent as a contact when the
                                     button is pressed. Available in private chats only
        :param bool request_location: Optional. If True, the user's current location will be sent when the button is
                                      pressed. Available in private chats only
        :param KeyboardButtonPollType or None request_poll: Optional. If specified, the user will be asked to create a
                                                            poll and send it to the bot when the button is pressed.
                                                            Available in private chats only
        :param WebAppInfo or None web_app: Optional. If specified, the described Web App will be launched when the
                                           button is pressed
        :rtype: dict
        """
        self.text = text
        self.request_contact = request_contact
        self.request_location = request_location
        self.request_poll = request_poll
        self.web_app = web_app

    def to_dict(self):
        obj = {'text': self.text}
        if self.request_contact:
            obj['request_contact'] = self.request_contact
        if self.request_location:
            obj['request_location'] = self.request_location
        if self.request_poll:
            obj['request_poll'] = self.request_poll
        if self.web_app:
            obj['web_app'] = self.web_app
        return obj

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        text = obj['text']
        request_contact = False
        if 'request_contact' in obj:
            request_contact = obj['request_contact']
        request_location = False
        if 'request_location' in obj:
            request_location = obj['request_location']
        request_poll = None
        if 'request_poll' in obj:
            request_poll = KeyboardButtonPollType.de_json(obj['request_poll'])
        web_app = None
        if 'web_app' in obj:
            web_app = WebAppInfo.de_json(obj['web_app'])
        return cls(text, request_contact, request_location, request_poll, web_app)


class KeyboardButtonPollType(JsonSerializable, JsonDeserializable):
    def __init__(self, ttype):
        """
        This object represents ttype of poll,
        which is allowed to be created and sent when the corresponding button is pressed
        """
        self.ttype = ttype

    def to_dict(self):
        obj = {'type': self.ttype}
        return obj

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        ttype = obj['type']
        return cls(ttype)


class ReplyKeyboardRemove(JsonSerializable):
    def __init__(self, remove_keyboard=True, selective=False):
        """
        Upon receiving a message with this object,
        Telegram clients will remove the current custom keyboard and display the default letter-keyboard,
        By default, custom keyboards are displayed until a new keyboard is sent by a bot,
        An exception is made for one-time keyboards that are hidden immediately after the user presses a button
        """
        self.remove_keyboard = remove_keyboard
        self.selective = selective

    def to_dict(self):
        obj = {'remove_keyboard': self.remove_keyboard, 'selective': self.selective}
        return obj


class InlineKeyboardMarkup(JsonSerializable, JsonDeserializable):
    def __init__(self, inline_keyboard):
        """
        This object represents an inline keyboard that appears right next to the message it belongs to
        :param list[list[InlineKeyboardButton]] inline_keyboard: Array of button rows, each represented by an Array of
                                                                 InlineKeyboardButton objects
        :rtype: dict
        """
        self.inline_keyboard = inline_keyboard

    def to_dict(self):
        obj = {'inline_keyboard': self.inline_keyboard}
        return obj

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        inline_keyboard = InlineKeyboardMarkup.parse_keyboard_button(obj['inline_keyboard'])
        return cls(inline_keyboard)

    @classmethod
    def parse_keyboard_button(cls, obj):
        row = []
        column = []
        for x in obj:
            for y in x:
                column.append(InlineKeyboardButton.de_json(y))
            row.append(column)
        return row


class InlineKeyboardButton(JsonSerializable, JsonDeserializable):
    def __init__(self, text, url=None, login_url=None, callback_data=None, web_app=None, switch_inline_query=None,
                 switch_inline_query_current_chat=None, callback_game=None, pay=False):
        """
        This object represents one button of an inline keyboard,
        You must use exactly one of the optional fields
        :param str text: Label text on the button
        :param str or None url: Optional. HTTP or tg:// url to be opened when the button is pressed.
                               Links tg://user?id=<user_id> can be used to mention a user by their ID without using a
                               username, if this is allowed by their privacy settings
        :param LoginUrl or None login_url: Optional. An HTTP URL used to automatically authorize the user
        :param str or None callback_data: Optional. Data to be sent in a callback query to the bot when button is
                                          pressed, 1-64 bytes
        :param WebAppInfo or None web_app: Optional. Description of the Web App that will be launched when the user
                                           presses the button
        :param str or None switch_inline_query: Optional. If set, pressing the button will prompt the user to select one
                                                of their chats, open that chat and insert the bots username and the
                                                specified inline query in the input field. Can be empty, in which case
                                                just the bots' username will be inserted
        :param str or None switch_inline_query_current_chat: Optional. If set, pressing the button will insert the bots
                                                             username and the specified inline query in the current
                                                             chat's input field. Can be empty, in which case only the
                                                             bots' username will be inserted
        :param CallbackGame or None callback_game: Optional. Description of the game that will be launched when the user
                                                   presses the button
        :param bool pay: Optional. Specify True, to send a Pay button
        :rtype: dict
        """
        self.text = text
        self.url = url
        self.login_url = login_url
        self.callback_data = callback_data
        self.web_app = web_app
        self.switch_inline_query = switch_inline_query
        self.switch_inline_query_current_chat = switch_inline_query_current_chat
        self.callback_game = callback_game
        self.pay = pay

    def to_dict(self):
        obj = {'text': self.text}
        if self.url:
            obj['url'] = self.url
        if self.login_url:
            obj['login_url'] = self.login_url
        if self.callback_data:
            obj['callback_data'] = self.callback_data
        if self.web_app:
            obj['web_app'] = self.web_app
        if self.switch_inline_query:
            obj['switch_inline_query'] = self.switch_inline_query
        if self.switch_inline_query_current_chat:
            obj['switch_inline_query_current_chat'] = self.switch_inline_query_current_chat
        if self.callback_game:
            obj['callback_game'] = self.callback_game
        if self.pay:
            obj['pay'] = self.pay
        return obj

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        text = obj['text']
        url = None
        if 'url' in obj:
            url = obj['url']
        login_url = None
        if 'login_url' in obj:
            login_url = LoginUrl.de_json(obj['login_url'])
        callback_data = None
        if 'callback_data' in obj:
            callback_data = obj['callback_data']
        web_app = None
        if 'web_app' in obj:
            web_app = WebAppInfo.de_json(obj['web_app'])
        switch_inline_query = None
        if 'switch_inline_query' in obj:
            switch_inline_query = obj['switch_inline_query']
        switch_inline_query_current_chat = None
        if 'switch_inline_query_current_chat' in obj:
            switch_inline_query_current_chat = obj['switch_inline_query_current_chat']
        callback_game = None
        if 'callback_game' in obj:
            callback_game = obj['callback_game']
        pay = False
        if 'pay' in obj:
            pay = obj['pay']
        return cls(text, url, login_url, callback_data, web_app, switch_inline_query, switch_inline_query_current_chat,
                   callback_game, pay)


class LoginUrl(JsonSerializable, JsonDeserializable):
    def __init__(self, url, forward_text=None, bot_username=None, request_write_access=False):
        """
        This object represents a parameter of the inline keyboard button used to automatically authorize a user,
        Serves as a great replacement for the Telegram Login Widget when the user is coming from Telegram
        :param str url: An HTTP URL to be opened with user authorization data added to the query string when the button
                       is pressed
        :param str or None forward_text: Optional. New text of the button in forwarded messages
        :param str or None bot_username: Optional. Username of a bot, which will be used for user authorization
        :param bool request_write_access: Optional. Pass True to request the permission for your bot to send messages
                                          to the user
        :rtype: dict
        """
        self.url = url
        self.forward_text = forward_text
        self.bot_username = bot_username
        self.request_write_access = request_write_access

    def to_dict(self):
        obj = {'url': self.url}
        if self.forward_text:
            obj['forward_text'] = self.forward_text
        if self.bot_username:
            obj['bot_username'] = self.bot_username
        if self.request_write_access:
            obj['request_write_access'] = self.request_write_access
        return obj

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        url = obj['url']
        forward_text = None
        if 'forward_text' in obj:
            forward_text = obj['forward_text']
        bot_username = None
        if 'bot_username' in obj:
            bot_username = obj['bot_username']
        request_write_access = None
        if 'request_write_access' in obj:
            request_write_access = obj['request_write_access']
        return cls(url, forward_text, bot_username, request_write_access)


class CallbackQuery(JsonDeserializable):
    def __init__(self, uid, from_user, data, chat_instance, message, inline_message_id, game_short_name):
        """
        This object represents an incoming callback query from a callback button in an inline keyboard
        """
        self.uid = uid
        self.from_user = from_user
        self.message = message
        self.inline_message_id = inline_message_id
        self.chat_instance = chat_instance
        self.data = data
        self.game_short_name = game_short_name

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        uid = obj['id']
        from_user = User.de_json(obj['from'])
        message = None
        if 'message' in obj:
            message = Message.de_json(obj['message'])
        inline_message_id = None
        if 'inline_message_id' in obj:
            inline_message_id = obj['inline_message_id']
        chat_instance = obj['chat_instance']
        data = None
        if 'data' in obj:
            data = obj['data']
        game_short_name = None
        if 'game_short_name' in obj:
            game_short_name = obj['game_short_name']
        return cls(uid, from_user, data, chat_instance, message, inline_message_id, game_short_name)


class ForceReply(JsonSerializable):
    def __init__(self, force_reply=True, input_field_placeholder=None, selective=False):
        """
        Upon receiving a message with this object,
        Telegram clients will display a reply interface to the user,
        (act as if the user has selected the bot‘s message and tapped ’Reply'),
        This can be extremely useful if you want to create user-friendly step-by-step,
        interfaces without having to sacrifice privacy mode.
        """
        self.force_reply = force_reply
        self.input_field_placeholder = input_field_placeholder
        self.selective = selective

    def to_dict(self):
        obj = {'force_reply': self.force_reply}
        if self.input_field_placeholder:
            obj['input_field_placeholder'] = self.input_field_placeholder
        if self.selective:
            obj['selective'] = True
        return obj


class ChatPhoto(JsonDeserializable):
    def __init__(self, small_file_id, small_file_unique_id, big_file_id, big_file_unique_id):
        """
        This object represents a chat photo
        """
        self.small_file_id = small_file_id
        self.small_file_unique_id = small_file_unique_id
        self.big_file_id = big_file_id
        self.big_file_unique_id = big_file_unique_id

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        small_file_id = obj['small_file_id']
        small_file_unique_id = obj['small_file_unique_id']
        big_file_id = obj['big_file_id']
        big_file_unique_id = obj['big_file_unique_id']
        return cls(small_file_id, small_file_unique_id, big_file_id, big_file_unique_id)


class ChatInviteLink(JsonDeserializable):
    def __init__(self, invite_link, creator, creates_join_request, is_primary, is_revoked, name, expire_date,
                 member_limit, pending_join_request_count):
        """
        Represents an invitation link for a chat
        """
        self.invite_link = invite_link
        self.creator = creator
        self.creates_join_request = creates_join_request
        self.is_primary = is_primary
        self.is_revoked = is_revoked
        self.name = name
        self.expire_date = expire_date
        self.member_limit = member_limit
        self.pending_join_request_count = pending_join_request_count

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        invite_link = obj['invite_link']
        creator = User.de_json(obj['creator'])
        creates_join_request = False
        if 'creates_join_request' in obj:
            creates_join_request = obj['creates_join_request']
        is_primary = False
        if 'is_primary' in obj:
            is_primary = obj['is_primary']
        is_revoked = False
        if 'is_revoked' in obj:
            is_revoked = obj['is_revoked']
        name = None
        if 'name' in obj:
            name = obj['name']
        expire_date = None
        if 'expire_date' in obj:
            expire_date = obj['expire_date']
        member_limit = None
        if 'member_limit' in obj:
            member_limit = obj['member_limit']
        pending_join_request_count = None
        if 'pending_join_request_count' in obj:
            pending_join_request_count = obj['pending_join_request_count']
        return cls(invite_link, creator, creates_join_request, is_primary, is_revoked, name, expire_date, member_limit,
                   pending_join_request_count)


class ChatAdministratorRights(JsonDeserializable, JsonSerializable):
    """
    Represents the rights of an administrator in a chat
    """
    def __init__(self, is_anonymous=False, can_manage_chat=False, can_delete_messages=False,
                 can_manage_video_chats=False, can_restrict_members=False, can_promote_members=False,
                 can_change_info=False, can_invite_users=False, can_post_messages=False, can_edit_messages=False,
                 can_pin_messages=False):
        """
        Initialize the ChatAdministratorRights object
        :param bool is_anonymous: True, if the user's presence in the chat is hidden
        :param bool can_manage_chat: True, if the administrator can access the chat event log
        :param bool can_delete_messages: True, if the administrator can delete messages of other users
        :param bool can_manage_video_chats: True, if the administrator can manage video chats
        :param bool can_restrict_members: True, if the administrator can restrict, ban or unban chat members
        :param bool can_promote_members: True, if the administrator can add new administrators with a subset of their
                                         own privileges or demote administrators that he has promoted
        :param bool can_change_info: True, if the user is allowed to change the chat title, photo and other settings
        :param bool can_invite_users: True, if the user is allowed to invite new users to the chat
        :param bool can_post_messages: True, if the administrator can post in the channel; channels only
        :param bool can_edit_messages: True, if the administrator can edit messages of other users and can pin messages;
                                       channels only
        :param bool can_pin_messages: True, if the user is allowed to pin messages; groups and supergroups only
        """
        self.is_anonymous = is_anonymous
        self.can_manage_chat = can_manage_chat
        self.can_delete_messages = can_delete_messages
        self.can_manage_video_chats = can_manage_video_chats
        self.can_restrict_members = can_restrict_members
        self.can_promote_members = can_promote_members
        self.can_change_info = can_change_info
        self.can_invite_users = can_invite_users
        self.can_post_messages = can_post_messages
        self.can_edit_messages = can_edit_messages
        self.can_pin_messages = can_pin_messages

    def to_dict(self):
        obj = {}
        if self.is_anonymous:
            obj['is_anonymous'] = self.is_anonymous
        if self.can_manage_chat:
            obj['can_manage_chat'] = self.can_manage_chat
        if self.can_delete_messages:
            obj['can_delete_messages'] = self.can_delete_messages
        if self.can_manage_video_chats:
            obj['can_manage_video_chats'] = self.can_manage_video_chats
        if self.can_restrict_members:
            obj['can_restrict_members'] = self.can_restrict_members
        if self.can_promote_members:
            obj['can_promote_members'] = self.can_promote_members
        if self.can_change_info:
            obj['can_change_info'] = self.can_change_info
        if self.can_invite_users:
            obj['can_invite_users'] = self.can_invite_users
        if self.can_post_messages:
            obj['can_post_messages'] = self.can_post_messages
        if self.can_edit_messages:
            obj['can_edit_messages'] = self.can_edit_messages
        if self.can_pin_messages:
            obj['can_pin_messages'] = self.can_pin_messages
        return obj

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        is_anonymous = False
        if 'is_anonymous' in obj:
            is_anonymous = True
        can_manage_chat = False
        if 'can_manage_chat' in obj:
            can_manage_chat = True
        can_delete_messages = False
        if 'can_delete_messages' in obj:
            can_delete_messages = True
        can_manage_video_chats = False
        if 'can_manage_video_chats' in obj:
            can_manage_video_chats = True
        can_restrict_members = False
        if 'can_restrict_members' in obj:
            can_restrict_members = True
        can_promote_members = False
        if 'can_promote_members' in obj:
            can_promote_members = True
        can_change_info = False
        if 'can_change_info' in obj:
            can_change_info = True
        can_invite_users = False
        if 'can_invite_users' in obj:
            can_invite_users = True
        can_post_messages = False
        if 'can_post_messages' in obj:
            can_post_messages = True
        can_edit_messages = False
        if 'can_edit_messages' in obj:
            can_edit_messages = True
        can_pin_messages = False
        if 'can_pin_messages' in obj:
            can_pin_messages = True
        return cls(is_anonymous, can_manage_chat, can_delete_messages, can_manage_video_chats, can_restrict_members,
                   can_promote_members, can_change_info, can_invite_users, can_post_messages, can_edit_messages,
                   can_pin_messages)


class ChatMember(JsonDeserializable):
    """
    This object contains information about one member of a chat.
    Currently, the following 6 types of chat members are supported:
        ChatMemberOwner
        ChatMemberAdministrator
        ChatMemberMember
        ChatMemberRestricted
        ChatMemberLeft
        ChatMemberBanned
    """

    def __int__(self):
        self.Owner = self.__ChatMemberOwner
        self.Administrator = self.__ChatMemberAdministrator
        self.Member = self.__ChatMemberMember
        self.Restricted = self.__ChatMemberRestricted
        self.Left = self.__ChatMemberLeft
        self.Banned = self.__ChatMemberBanned

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        status = obj['status']
        if status == 'creator':
            return cls.__ChatMemberOwner.de_json(obj_type)
        elif status == 'administrator':
            return cls.__ChatMemberAdministrator.de_json(obj_type)
        elif status == 'member':
            return cls.__ChatMemberMember.de_json(obj_type)
        elif status == 'restricted':
            return cls.__ChatMemberRestricted.de_json(obj_type)
        elif status == 'left':
            return cls.__ChatMemberLeft.de_json(obj_type)
        elif status == 'kicked':
            return cls.__ChatMemberBanned.de_json(obj_type)

    class __ChatMemberOwner(JsonDeserializable):
        def __init__(self, status, user, is_anonymous, custom_title):
            """
            Represents a chat member that owns the chat and has all administrator privileges
            """
            self.status = status
            self.user = user
            self.is_anonymous = is_anonymous
            self.custom_title = custom_title

        @classmethod
        def de_json(cls, obj_type):
            obj = cls.check_type(obj_type)
            status = obj['status']
            user = User.de_json(obj['user'])
            is_anonymous = False
            if 'is_anonymous' in obj:
                is_anonymous = obj['is_anonymous']
            custom_title = None
            if 'custom_title' in obj:
                custom_title = obj['custom_title']
            return cls(status, user, is_anonymous, custom_title)

    class __ChatMemberAdministrator(JsonDeserializable):
        def __init__(self, status, user, can_be_edited, is_anonymous, can_manage_chat, can_delete_messages,
                     can_manage_video_chats, can_restrict_members, can_promote_members, can_change_info,
                     can_invite_users, can_post_messages, can_edit_messages, can_pin_messages, custom_title):
            """
            Represents a chat member that has some additional privileges
            """
            self.status = status
            self.user = user
            self.can_be_edited = can_be_edited
            self.is_anonymous = is_anonymous
            self.can_manage_chat = can_manage_chat
            self.can_delete_messages = can_delete_messages
            self.can_manage_video_chats = can_manage_video_chats
            self.can_restrict_members = can_restrict_members
            self.can_promote_members = can_promote_members
            self.can_change_info = can_change_info
            self.can_invite_users = can_invite_users
            self.can_post_messages = can_post_messages
            self.can_edit_messages = can_edit_messages
            self.can_pin_messages = can_pin_messages
            self.custom_title = custom_title

        @classmethod
        def de_json(cls, obj_type):
            obj = cls.check_type(obj_type)
            status = obj['status']
            user = User.de_json(obj['user'])
            can_be_edited = False
            if 'can_be_edited' in obj:
                can_be_edited = obj['can_be_edited']
            is_anonymous = False
            if 'is_anonymous' in obj:
                is_anonymous = obj['is_anonymous']
            can_manage_chat = False
            if 'can_manage_chat' in obj:
                can_manage_chat = obj['can_manage_chat']
            can_delete_messages = False
            if 'can_delete_messages' in obj:
                can_delete_messages = obj['can_delete_messages']
            can_manage_video_chats = False
            if 'can_manage_video_chats' in obj:
                can_manage_video_chats = obj['can_manage_video_chats']
            can_restrict_members = False
            if 'can_restrict_members' in obj:
                can_restrict_members = obj['can_restrict_members']
            can_promote_members = False
            if 'can_promote_members' in obj:
                can_promote_members = obj['can_promote_members']
            can_change_info = False
            if 'can_change_info' in obj:
                can_change_info = obj['can_change_info']
            can_invite_users = False
            if 'can_invite_users' in obj:
                can_invite_users = obj['can_invite_users']
            can_post_messages = False
            if 'can_post_messages' in obj:
                can_post_messages = obj['can_post_messages']
            can_edit_messages = False
            if 'can_edit_messages' in obj:
                can_edit_messages = obj['can_edit_messages']
            can_pin_messages = False
            if 'can_pin_messages' in obj:
                can_pin_messages = obj['can_pin_messages']
            custom_title = None
            if 'custom_title' in obj:
                custom_title = obj['custom_title']
            return cls(status, user, can_be_edited, is_anonymous, can_manage_chat, can_delete_messages,
                       can_manage_video_chats, can_restrict_members, can_promote_members, can_change_info,
                       can_invite_users, can_post_messages, can_edit_messages, can_pin_messages, custom_title)

    class __ChatMemberMember(JsonDeserializable):
        def __init__(self, status, user):
            """
            Represents a chat member that has no additional privileges or restrictions
            """
            self.status = status
            self.user = user

        @classmethod
        def de_json(cls, obj_type):
            obj = cls.check_type(obj_type)
            status = obj['status']
            user = User.de_json(obj['user'])
            return cls(status, user)

    class __ChatMemberRestricted(JsonDeserializable):
        def __init__(self, status, user, is_member, can_change_info, can_invite_users, can_pin_messages,
                     can_send_messages, can_send_media_messages, can_send_polls, can_send_other_messages,
                     can_add_web_page_previews, until_date):
            """
            Represents a chat member that is under certain restrictions in the chat. Supergroups only
            """
            self.status = status
            self.user = user
            self.is_member = is_member
            self.can_change_info = can_change_info
            self.can_invite_users = can_invite_users
            self.can_pin_messages = can_pin_messages
            self.can_send_messages = can_send_messages
            self.can_send_media_messages = can_send_media_messages
            self.can_send_polls = can_send_polls
            self.can_send_other_messages = can_send_other_messages
            self.can_add_web_page_previews = can_add_web_page_previews
            self.until_date = until_date

        @classmethod
        def de_json(cls, obj_type):
            obj = cls.check_type(obj_type)
            status = obj['status']
            user = User.de_json(obj['user'])
            is_member = False
            if 'is_member' in obj:
                is_member = obj['is_member']
            can_change_info = False
            if 'can_change_info' in obj:
                can_change_info = obj['can_change_info']
            can_invite_users = False
            if 'can_invite_users' in obj:
                can_invite_users = obj['can_invite_users']
            can_pin_messages = False
            if 'can_pin_messages' in obj:
                can_pin_messages = obj['can_pin_messages']
            can_send_messages = False
            if 'can_send_messages' in obj:
                can_send_messages = obj['can_send_messages']
            can_send_media_messages = False
            if 'can_send_media_messages' in obj:
                can_send_media_messages = obj['can_send_media_messages']
            can_send_polls = False
            if 'can_send_polls' in obj:
                can_send_polls = obj['can_send_polls']
            can_send_other_messages = False
            if 'can_send_other_messages' in obj:
                can_send_other_messages = obj['can_send_other_messages']
            can_add_web_page_previews = False
            if 'can_add_web_page_previews' in obj:
                can_add_web_page_previews = obj['can_add_web_page_previews']
            until_date = None
            if 'until_date' in obj:
                until_date = obj['until_date']
            return cls(status, user, is_member, can_change_info, can_invite_users, can_pin_messages, can_send_messages,
                       can_send_media_messages, can_send_polls, can_send_other_messages, can_add_web_page_previews,
                       until_date)

    class __ChatMemberLeft(JsonDeserializable):
        def __init__(self, status, user):
            """
            Represents a chat member that isn't currently a member of the chat, but may join it themselves
            """
            self.status = status
            self.user = user

        @classmethod
        def de_json(cls, obj_type):
            obj = cls.check_type(obj_type)
            status = obj['status']
            user = User.de_json(obj['user'])
            return cls(status, user)

    class __ChatMemberBanned(JsonDeserializable):
        def __init__(self, status, user, until_date):
            """
            Represents a chat member that was banned in the chat and can't return to the chat or view chat messages
            """
            self.status = status
            self.user = user
            self.until_date = until_date

        @classmethod
        def de_json(cls, obj_type):
            obj = cls.check_type(obj_type)
            status = obj['status']
            user = User.de_json(obj['user'])
            until_date = obj['until_date']
            return cls(status, user, until_date)


class ChatMemberUpdated(JsonDeserializable):
    def __init__(self, chat, from_user, date, old_chat_member, new_chat_member, invite_link):
        """
        This object represents changes in the status of a chat member
        """
        self.chat = chat
        self.from_user = from_user
        self.date = date
        self.old_chat_member = old_chat_member
        self.new_chat_member = new_chat_member
        self.invite_link = invite_link

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        chat = Chat.de_json(obj['chat'])
        from_user = User.de_json(obj['from'])
        date = obj['date']
        old_chat_member = ChatMember.de_json(obj['old_chat_member'])
        new_chat_member = ChatMember.de_json(obj['new_chat_member'])
        invite_link = None
        if 'invite_link' in obj:
            invite_link = ChatInviteLink.de_json(obj['invite_link'])
        return cls(chat, from_user, date, old_chat_member, new_chat_member, invite_link)


class ChatJoinRequest(JsonSerializable, JsonDeserializable):
    def __init__(self, chat, from_user, date, bio, invite_link):
        """
        Represents a join request sent to a chat
        :param Chat chat: Chat to which the request was sent
        :param User from_user: User that sent the join request
        :param int date: Date the request was sent in Unix time
        :param str or None bio: Optional. Bio of the user
        :param ChatInviteLink or None invite_link: Optional. Chat invite link that was used by the user to send the
                                                   join request
        """
        self.chat = chat
        self.from_user = from_user
        self.date = date
        self.bio = bio
        self.invite_link = invite_link

    def to_dict(self):
        """
        :rtype: dict
        """
        obj = {'chat': self.chat, 'user': self.from_user, 'date': self.date}
        if self.bio:
            obj['bio'] = self.bio
        if self.invite_link:
            obj['invite_link'] = self.invite_link
        return obj

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        chat = Chat.de_json(obj['chat'])
        from_user = User.de_json(obj['user'])
        date = obj['date']
        bio = None
        if 'bio' in obj:
            bio = obj['bio']
        invite_link = None
        if 'invite_link' in obj:
            invite_link = ChatInviteLink.de_json(obj['invite_link'])
        return cls(chat, from_user, date, bio, invite_link)


class ChatPermissions(JsonDeserializable):
    def __init__(self, can_send_messages, can_send_media_messages, can_send_polls, can_send_other_messages,
                 can_add_web_page_previews, can_change_info, can_invite_users, can_pin_messages):
        """
        Describes actions that a non-administrator user is allowed to take in a chat
        """
        self.can_send_messages = can_send_messages
        self.can_send_media_messages = can_send_media_messages
        self.can_send_polls = can_send_polls
        self.can_send_other_messages = can_send_other_messages
        self.can_add_web_page_previews = can_add_web_page_previews
        self.can_change_info = can_change_info
        self.can_invite_users = can_invite_users
        self.can_pin_messages = can_pin_messages

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        can_send_messages = False
        if 'can_send_messages' in obj:
            can_send_messages = obj['can_send_messages']
        can_send_media_messages = False
        if 'can_send_media_messages' in obj:
            can_send_media_messages = obj['can_send_media_messages']
        can_send_polls = False
        if 'can_send_polls' in obj:
            can_send_polls = obj['can_send_polls']
        can_send_other_messages = False
        if 'can_send_other_messages' in obj:
            can_send_other_messages = obj['can_send_other_messages']
        can_add_web_page_previews = False
        if 'can_add_web_page_previews' in obj:
            can_add_web_page_previews = obj['can_add_web_page_previews']
        can_change_info = False
        if 'can_change_info' in obj:
            can_change_info = obj['can_change_info']
        can_invite_users = False
        if 'can_invite_users' in obj:
            can_invite_users = obj['can_invite_users']
        can_pin_messages = False
        if 'can_pin_messages' in obj:
            can_pin_messages = obj['can_pin_messages']
        return cls(can_send_messages, can_send_media_messages, can_send_polls, can_send_other_messages,
                   can_add_web_page_previews, can_change_info, can_invite_users, can_pin_messages)


class ChatLocation(JsonDeserializable):
    def __init__(self, location, address):
        """
        Represents a location to which a chat is connected
        """
        self.location = location
        self.address = address

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        location = Location.de_json(obj['location'])
        address = obj['address']
        return cls(location, address)


class BotCommand(JsonDeserializable):
    def __init__(self, command, description):
        """
        This object represents a bot command
        """
        self.command = command
        self.description = description

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        command = obj['command']
        description = obj['description']
        return cls(command, description)


class BotCommandScope:
    """
    This object represents the scope to which bot commands are applied.
    Currently, the following 7 scopes are supported:
        BotCommandScopeDefault
        BotCommandScopeAllPrivateChats
        BotCommandScopeAllGroupChats
        BotCommandScopeAllChatAdministrators
        BotCommandScopeChat
        BotCommandScopeChatAdministrators
        BotCommandScopeChatMember
    """

    def __init__(self):
        self.Default = self.__BotCommandScopeDefault
        self.AllPrivateChats = self.__BotCommandScopeAllPrivateChats
        self.AllGroupChats = self.__BotCommandScopeAllGroupChats
        self.AllChatAdministrators = self.__BotCommandScopeAllChatAdministrators
        self.Chat = self.__BotCommandScopeChat
        self.ChatAdministrators = self.__BotCommandScopeChatAdministrators
        self.ChatMember = self.__BotCommandScopeChatMember

    def __repr__(self):
        return repr(self.Default())

    class __BotCommandScopeDefault(JsonSerializable):
        def __init__(self):
            """
            Represents the default scope of bot commands
            """
            self.ttype = 'default'

        def to_dict(self):
            obj = {'type': self.ttype}
            return obj

        def __repr__(self):
            return repr(self.to_dict())

    class __BotCommandScopeAllPrivateChats(JsonSerializable):
        def __init__(self):
            """
            Represents the scope of bot commands, covering all private chats
            """
            self.ttype = 'all_private_chats'

        def to_dict(self):
            obj = {'type': self.ttype}
            return obj

    class __BotCommandScopeAllGroupChats(JsonSerializable):
        def __init__(self):
            """
            Represents the scope of bot commands, covering all group and supergroup chats
            """
            self.ttype = 'all_group_chats'

        def to_dict(self):
            obj = {'type': self.ttype}
            return obj

    class __BotCommandScopeAllChatAdministrators(JsonSerializable):
        def __init__(self):
            """
            Represents the scope of bot commands, covering all group and supergroup chat administrators
            """
            self.ttype = 'all_chat_administrators'

        def to_dict(self):
            obj = {'type': self.ttype}
            return obj

    class __BotCommandScopeChat(JsonSerializable):
        def __init__(self, chat_id, ttype='chat'):
            """
            Represents the scope of bot commands, covering a specific chat
            :param str ttype: Scope type, must be chat
            :param str or int chat_id: Unique identifier for the target chat or username of the target supergroup
                                       (in the format @supergroup_username)
            """
            self.ttype = ttype
            self.chat_id = chat_id

        def to_dict(self):
            obj = {'type': self.ttype, 'chat_id': self.chat_id}
            return obj

    class __BotCommandScopeChatAdministrators(JsonSerializable):
        def __init__(self, chat_id, ttype='chat_administrator'):
            """
            Represents the scope of bot commands,
            covering all administrators of a specific group or supergroup chat
            :param str ttype: Scope type, must be chat_administrators
            :param str or int chat_id: Unique identifier for the target chat or username of the target supergroup
                                       (in the format @supergroup_username)
            """
            self.ttype = ttype
            self.chat_id = chat_id

        def to_dict(self):
            obj = {'type': self.ttype, 'chat_id': self.chat_id}
            return obj

    class __BotCommandScopeChatMember(JsonSerializable):
        def __init__(self, chat_id, user_id, ttype='chat_member'):
            """
            Represents the scope of bot commands,
            covering a specific member of a group or supergroup chat
            :param str ttype: Scope type, must be chat_member
            :param str or int chat_id: Unique identifier for the target chat or username of the target supergroup
                                       (in the format @supergroup_username)
            :param int user_id: Unique identifier of the target user
            """
            self.ttype = ttype
            self.chat_id = chat_id
            self.user_id = user_id

        def to_dict(self):
            obj = {'type': self.ttype, 'chat_id': self.chat_id, 'user_id': self.user_id}
            return obj


class MenuButton(JsonDeserializable):
    """
    This object describes the bots' menu button in a private chat. It should be one of
        MenuButtonCommands
        MenuButtonWebApp
        MenuButtonDefault
    If a menu button other than MenuButtonDefault is set for a private chat, then it is applied in the chat.
    Otherwise, the default menu button is applied. By default, the menu button opens the list of bot commands.
    """

    def __init__(self, ttype, text, web_app):
        """
        Initializes a new instance of the MenuButton class
        """
        self.Commands = self.__MenuButtonCommands
        self.WebApp = self.__MenuButtonWebApp
        self.Default = self.__MenuButtonDefault
        self.type = ttype
        self.text = text
        self.web_app = web_app

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        ttype = None
        if 'type' in obj:
            ttype = obj['type']
        text = None
        if 'text' in obj:
            text = obj['text']
        web_app = None
        if 'web_app' in obj:
            web_app = obj['web_app']
        return cls(ttype, text, web_app)

    class __MenuButtonCommands(JsonSerializable):
        """
        Represents a menu button, which opens the bots' list of commands.
        """

        def __init__(self, ttype='commands'):
            """
            Initializes a new instance of the MenuButtonCommands class
            :param str ttype: Type of the button, must be commands
            """
            self.type = ttype

        def to_dict(self):
            obj = {'type': self.type}
            return obj

    class __MenuButtonWebApp(JsonSerializable):
        """
        Represents a menu button, which opens the bots' list of commands.
        """

        def __init__(self, text, web_app, ttype='web_app'):
            """
            Initializes a new instance of the MenuButtonWebApp class
            :param str ttype: Type of the button, must be web_app
            :param str text: Text of the button
            :param WebAppInfo web_app: Description of the Web App that will be launched when the user presses the button
            """
            self.type = ttype
            self.text = text
            self.web_app = web_app

        def to_dict(self):
            obj = {'type': self.type, 'text': self.text, 'web_app': self.web_app}
            return obj

    class __MenuButtonDefault(JsonSerializable):
        """
        Describes that no specific value for the menu button was set.
        """

        def __init__(self, ttype='default'):
            """
            Initializes a new instance of the MenuButtonDefault class
            :param str ttype: Type of the button, must be default
            """
            self.type = ttype

        def to_dict(self):
            obj = {'type': self.type}
            return obj


class ResponseParameters(JsonDeserializable):
    def __init__(self, migrate_to_chat_id, retry_after):
        """
        Contains information about why a request was unsuccessful
        """
        self.migrate_to_chat_id = migrate_to_chat_id
        self.retry_after = retry_after

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        migrate_to_chat_id = None
        if 'migrate_to_chat_id' in obj:
            migrate_to_chat_id = obj['migrate_to_chat_id']
        retry_after = None
        if 'retry_after' in obj:
            retry_after = obj['retry_after']
        return cls(migrate_to_chat_id, retry_after)


class InputMedia:
    """ 
    This object represents the content of a media message to be sent,
    It should be one of:
        InputMediaAnimation
        InputMediaDocument
        InputMediaAudio
        InputMediaPhoto
        InputMediaVideo
    """

    def __init__(self):
        self.Photo = self.__InputMediaPhoto
        self.Video = self.__InputMediaVideo
        self.Animation = self.__InputMediaAnimation
        self.Audio = self.__InputMediaAudio
        self.Document = self.__InputMediaDocument

    class __InputMediaPhoto(JsonSerializable):
        def __init__(self, ttype, media, caption=None, parse_mode=None, caption_entities=None):
            """
            Represents a photo to be sent
            :param str ttype: Type of the result, must be photo
            :param str media: File to send. Pass a file_id to send a file that exists on the Telegram servers
                              (recommended), pass an HTTP URL for Telegram to get a file from the Internet,
                              or pass “attach://<file_attach_name>” to upload a new one using multipart/form-data under
                              <file_attach_name> name
            :param str or None caption: Optional. Caption of the photo to be sent, 0-1024 characters after entities
                                        parsing
            :param str or None parse_mode: Optional. Mode for parsing entities in the photo caption
            :param list[MessageEntity] or None caption_entities: Optional. List of special entities that appear in the
                                                                 caption, which can be specified instead of parse_mode
            :rtype: dict
            """
            self.ttype = ttype
            self.media = media
            self.caption = caption
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities

        def to_dict(self):
            obj = {'type': self.ttype, 'media': self.media}
            if self.caption:
                obj['caption'] = self.caption
            if self.parse_mode:
                obj['parse_mode'] = self.parse_mode
            if self.caption_entities:
                obj['caption_entities'] = self.caption_entities
            return obj

    class __InputMediaVideo(JsonSerializable):
        def __init__(self, ttype, media, thumb=None, caption=None, parse_mode=None, caption_entities=None, width=None,
                     height=None, duration=None, supports_streaming=False):
            """
            Represents a video to be sent
            :param str ttype: Type of the result, must be photo
            :param str media: File to send. Pass a file_id to send a file that exists on the Telegram servers
                              (recommended), pass an HTTP URL for Telegram to get a file from the Internet,
                              or pass “attach://<file_attach_name>” to upload a new one using multipart/form-data under
                              <file_attach_name> name
            :param InputFile or string thumb: Optional. Thumbnail of the file sent; can be ignored if thumbnail
                                              generation for the file is supported server-side.
                                              The thumbnail should be in JPEG format and less than 200 kB in size
            :param str or None caption: Optional. Caption of the video to be sent, 0-1024 characters after entities
                                        parsing
            :param str or None parse_mode: Optional. Mode for parsing entities in the caption
            :param list[MessageEntity] or None caption_entities: Optional. List of special entities that appear in the
                                                                 caption, which can be specified instead of parse_mode
            :param int or None width: Optional. Video width
            :param int or None height: Optional. Video height
            :param int or None duration: Optional. Video duration in seconds
            :param bool supports_streaming: Optional. Pass True, if the uploaded video is suitable for streaming
            :rtype: dict
            """
            self.ttype = ttype
            self.media = media
            self.thumb = thumb
            self.caption = caption
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities
            self.width = width
            self.height = height
            self.duration = duration
            self.supports_streaming = supports_streaming

        def to_dict(self):
            obj = {'type': self.ttype, 'media': self.media}
            if self.thumb:
                obj['thumb'] = self.thumb
            if self.caption:
                obj['caption'] = self.caption
            if self.parse_mode:
                obj['parse_mode'] = self.parse_mode
            if self.caption_entities:
                obj['caption_entities'] = self.caption_entities
            if self.width:
                obj['width'] = self.width
            if self.height:
                obj['height'] = self.height
            if self.duration:
                obj['duration'] = self.duration
            if self.supports_streaming:
                obj['supports_streaming'] = self.supports_streaming
            return obj

    class __InputMediaAnimation(JsonSerializable):
        def __init__(self, ttype, media, thumb=None, caption=None, parse_mode=None, caption_entities=None,
                     width=None, height=None, duration=None):
            """
            Represents an animation file (GIF or H.264/MPEG-4 AVC video without sound) to be sent
            :param str ttype: Type of the result, must be photo
            :param str media: File to send. Pass a file_id to send a file that exists on the Telegram servers
                              (recommended), pass an HTTP URL for Telegram to get a file from the Internet,
                              or pass “attach://<file_attach_name>” to upload a new one using multipart/form-data under
                              <file_attach_name> name
            :param InputFile or string thumb: Optional. Thumbnail of the file sent; can be ignored if thumbnail
                                              generation for the file is supported server-side.
                                              The thumbnail should be in JPEG format and less than 200 kB in size
            :param str or None caption: Optional. Caption of the animation to be sent, 0-1024 characters after entities
                                        parsing
            :param str or None parse_mode: Optional. Mode for parsing entities in the caption
            :param list[MessageEntity] or None caption_entities: Optional. List of special entities that appear in the
                                                                 caption, which can be specified instead of parse_mode
            :param int or None width: Optional. Animation width
            :param int or None height: Optional. Animation height
            :param int or None duration: Optional. Animation duration in seconds
            :rtype: dict
            """
            self.ttype = ttype
            self.media = media
            self.thumb = thumb
            self.caption = caption
            self.caption_entities = caption_entities
            self.parse_mode = parse_mode
            self.width = width
            self.height = height
            self.duration = duration

        def to_dict(self):
            obj = {'type': self.ttype, 'media': self.media}
            if self.thumb:
                obj['thumb'] = self.thumb
            if self.caption:
                obj['caption'] = self.caption
            if self.parse_mode:
                obj['parse_mode'] = self.parse_mode
            if self.caption_entities:
                obj['caption_entities'] = self.caption_entities
            if self.width:
                obj['width'] = self.width
            if self.height:
                obj['height'] = self.height
            if self.duration:
                obj['duration'] = self.duration
            return obj

    class __InputMediaAudio(JsonSerializable):
        def __init__(self, ttype, media, thumb=None, caption=None, parse_mode=None, caption_entities=None,
                     duration=None, performer=None, title=None):
            """
            Represents an audio file to be treated as music to be sent
            :param str ttype: Type of the result, must be photo
            :param str media: File to send. Pass a file_id to send a file that exists on the Telegram servers
                              (recommended), pass an HTTP URL for Telegram to get a file from the Internet,
                              or pass “attach://<file_attach_name>” to upload a new one using multipart/form-data under
                              <file_attach_name> name
            :param InputFile or string thumb: Optional. Thumbnail of the file sent; can be ignored if thumbnail
                                              generation for the file is supported server-side.
                                              The thumbnail should be in JPEG format and less than 200 kB in size
            :param str or None caption: Optional. Caption of the animation to be sent, 0-1024 characters after entities
                                        parsing
            :param str or None parse_mode: Optional. Mode for parsing entities in the caption
            :param list[MessageEntity] or None caption_entities: Optional. List of special entities that appear in the
                                                                 caption, which can be specified instead of parse_mode
            :param int or None duration: Optional. Duration of the audio in seconds
            :param str or None performer: Optional. Performer of the audio
            :param str or None title: Optional. Title of the audio
            :rtype: dict
            """
            self.ttype = ttype
            self.media = media
            self.thumb = thumb
            self.caption = caption
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities
            self.duration = duration
            self.performer = performer
            self.title = title

        def to_dict(self):
            obj = {'type': self.ttype, 'media': self.media}
            if self.thumb:
                obj['thumb'] = self.thumb
            if self.caption:
                obj['caption'] = self.caption
            if self.parse_mode:
                obj['parse_mode'] = self.parse_mode
            if self.caption_entities:
                obj['caption_entities'] = self.caption_entities
            if self.duration:
                obj['duration'] = self.duration
            if self.performer:
                obj['performer'] = self.performer
            if self.title:
                obj['title'] = self.title
            return obj

    class __InputMediaDocument(JsonSerializable):
        def __init__(self, ttype, media, thumb=None, caption=None, parse_mode=None, caption_entities=None,
                     disable_content_type_detection=False):
            """
            Represents a general file to be sent
            :param str ttype: Type of the result, must be photo
            :param str media: File to send. Pass a file_id to send a file that exists on the Telegram servers
                              (recommended), pass an HTTP URL for Telegram to get a file from the Internet,
                              or pass “attach://<file_attach_name>” to upload a new one using multipart/form-data under
                              <file_attach_name> name
            :param InputFile or string thumb: Optional. Thumbnail of the file sent; can be ignored if thumbnail
                                              generation for the file is supported server-side.
                                              The thumbnail should be in JPEG format and less than 200 kB in size
            :param str or None caption: Optional. Caption of the photo to be sent, 0-1024 characters after entities
                                        parsing
            :param str or None parse_mode: Optional. Mode for parsing entities in the photo caption
            :param list[MessageEntity] or None caption_entities: Optional. List of special entities that appear in the
                                                                 caption, which can be specified instead of parse_mode
            :param bool disable_content_type_detection: Optional. Disables automatic server-side content type detection
                                                        for files uploaded using multipart/form-data. Always True,
                                                        if the document is sent as part of an album

            :rtype: dict
            """
            self.ttype = ttype
            self.media = media
            self.thumb = thumb
            self.caption = caption
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities
            self.disable_content_type_detection = disable_content_type_detection

        def to_dict(self):
            obj = {'type': self.ttype, 'media': self.media}
            if self.thumb:
                obj['thumb'] = self.thumb
            if self.caption:
                obj['caption'] = self.caption
            if self.parse_mode:
                obj['parse_mode'] = self.parse_mode
            if self.caption_entities:
                obj['caption_entities'] = self.caption_entities
            if self.disable_content_type_detection:
                obj['disable_content_type_detection'] = self.disable_content_type_detection
            return obj


class InputFile:
    def __new__(cls, path):
        """
        This object represents the contents of a file to be uploaded
        :param str path: file path
        :rtype: bytes
        """
        return open(path, 'rb')


class Sticker(JsonDeserializable):
    def __init__(self, file_id, file_unique_id, width, height, is_animated, is_video, thumb, emoji, set_name,
                 mask_position, file_size):
        """
        This object represents a sticker
        """
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.is_animated = is_animated
        self.is_video = is_video
        self.thumb = thumb
        self.emoji = emoji
        self.set_name = set_name
        self.mask_position = mask_position
        self.file_size = file_size

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        file_id = obj['file_id']
        file_unique_id = obj['file_unique_id']
        width = obj['width']
        height = obj['height']
        is_animated = False
        if 'is_animated' in obj:
            is_animated = obj['is_animated']
        is_video = False
        if 'is_video' in obj:
            is_video = obj['is_video']
        thumb = None
        if 'thumb' in obj:
            thumb = PhotoSize.de_json(obj['thumb'])
        emoji = None
        if 'emoji' in obj:
            emoji = obj['emoji']
        set_name = None
        if 'set_name' in obj:
            set_name = obj['set_name']
        mask_position = None
        if 'mask_position' in obj:
            mask_position = MaskPosition.de_json(obj['mask_position'])
        file_size = None
        if 'file_size' in obj:
            file_size = obj['file_size']
        return cls(file_id, file_unique_id, width, height, is_animated, is_video, thumb, emoji, set_name, mask_position,
                   file_size)


class StickerSet(JsonDeserializable):
    def __init__(self, name, title, is_animated, is_video, contains_masks, stickers, thumb):
        """
        This object represents a sticker set
        """
        self.name = name
        self.title = title
        self.is_animated = is_animated
        self.is_video = is_video
        self.contains_masks = contains_masks
        self.stickers = stickers
        self.thumb = thumb

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        name = obj['name']
        title = obj['title']
        is_animated = False
        if 'is_animated' in obj:
            is_animated = obj['is_animated']
        is_video = False
        if 'is_video' in obj:
            is_video = obj['is_video']
        contains_masks = False
        if 'contains_masks' in obj:
            contains_masks = obj['contains_masks']
        stickers = StickerSet.parse_stickers(obj['stickers'])
        thumb = None
        if 'thumb' in obj:
            thumb = PhotoSize.de_json(obj['thumb'])
        return cls(name, title, is_animated, is_video, contains_masks, stickers, thumb)

    @classmethod
    def parse_stickers(cls, obj):
        stickers = []
        for sticker in obj:
            stickers.append(Sticker.de_json(sticker))
        return stickers


class MaskPosition(JsonSerializable, JsonDeserializable):
    def __init__(self, point, x_shift, y_shift, scale):
        """
        This object describes the position on faces where a mask should be placed by default
        :param point: The part of the face relative to which the mask should be placed.
                      One of “forehead”, “eyes”, “mouth”, or “chin”
        :param x_shift: Shift by X-axis measured in widths of the mask scaled to the face size, from left to right.
                        For example, choosing -1.0 will place mask just to the left of the default mask position
        :param y_shift: Shift by Y-axis measured in heights of the mask scaled to the face size, from top to bottom.
                        For example, 1.0 will place the mask just below the default mask position
        :param scale: Mask scaling coefficient. For example, 2.0 means double size
        """
        self.point = point
        self.x_shift = x_shift
        self.y_shift = y_shift
        self.scale = scale

    def to_dict(self):
        return {'point': self.point, 'x_shift': self.x_shift, 'y_shift': self.y_shift, 'scale': self.scale}

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        point = obj['point']
        x_shift = obj['x_shift']
        y_shift = obj['y_shift']
        scale = obj['scale']
        return cls(point, x_shift, y_shift, scale)


class InlineQuery(JsonDeserializable):
    def __init__(self, uid, from_user, query, offset, chat_type, location):
        """
        This object represents an incoming inline query,
        When the user sends an empty query,
        your bot could return some default or trending results.
        """
        self.uid = uid
        self.from_user = from_user
        self.query = query
        self.offset = offset
        self.chat_type = chat_type
        self.location = location

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        uid = obj['id']
        from_user = User.de_json(obj['from'])
        query = obj['query']
        offset = obj['offset']
        chat_type = None
        if 'chat_type' in obj:
            chat_type = obj['chat_type']
        location = None
        if 'location' in obj:
            location = Location.de_json(obj['location'])
        return cls(uid, from_user, query, offset, chat_type, location)


class InlineQueryResult:
    """ This object represents one result of an inline query. 
        Telegram clients currently support results of the following 20 types:
            InlineQueryResultCachedAudio
            InlineQueryResultCachedDocument
            InlineQueryResultCachedGif
            InlineQueryResultCachedMpeg4Gif
            InlineQueryResultCachedPhoto
            InlineQueryResultCachedSticker
            InlineQueryResultCachedVideo
            InlineQueryResultCachedVoice
            InlineQueryResultArticle
            InlineQueryResultAudio
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

    def __init__(self):
        self.Article = self.__InlineQueryResultArticle
        self.Audio = self.__InlineQueryResultAudio
        self.CachedAudio = self.__InlineQueryResultCachedAudio
        self.CachedDocument = self.__InlineQueryResultCachedDocument
        self.CachedGif = self.__InlineQueryResultCachedGif
        self.CachedMpeg4Gif = self.__InlineQueryResultCachedMpeg4Gif
        self.CachedPhoto = self.__InlineQueryResultCachedPhoto
        self.CachedSticker = self.__InlineQueryResultCachedSticker
        self.CachedVideo = self.__InlineQueryResultCachedVideo
        self.CachedVoice = self.__InlineQueryResultCachedVoice
        self.Contact = self.__InlineQueryResultContact
        self.Game = self.__InlineQueryResultGame
        self.Document = self.__InlineQueryResultDocument
        self.Gif = self.__InlineQueryResultGif
        self.Location = self.__InlineQueryResultLocation
        self.Mpeg4Gif = self.__InlineQueryResultMpeg4Gif
        self.Photo = self.__InlineQueryResultPhoto
        self.Venue = self.__InlineQueryResultVenue
        self.Video = self.__InlineQueryResultVideo
        self.Voice = self.__InlineQueryResultVoice

    class __InlineQueryResultArticle(JsonSerializable):
        def __init__(self, uid, title, input_message_content, reply_markup=None, url=None, hide_url=False,
                     description=None, thumb_url=None, thumb_width=None, thumb_height=None):
            """
            Represents a link to an article or web page
            :param str uid: Unique identifier for this result
            :param str title: Title of the result
            :param InputMessageContent or None input_message_content: Content of the message to be sent
            :param InlineKeyboardMarkup or None reply_markup: Optional. Inline keyboard attached to the message
            :param str or None url: Optional. URL of the result
            :param bool hide_url: Optional. Pass True, if you don't want the URL to be shown in the message
            :param str or None description: Optional. Short description of the result
            :param str or None thumb_url: Optional. Url of the thumbnail for the result
            :param int or None thumb_width: Optional. Thumbnail width
            :param int or None thumb_height: Optional. Thumbnail height
            """
            self.ttype = 'article'
            self.uid = uid
            self.title = title
            self.input_message_content = input_message_content
            self.reply_markup = reply_markup
            self.url = url
            self.hide_url = hide_url
            self.description = description
            self.thumb_url = thumb_url
            self.thumb_width = thumb_width
            self.thumb_height = thumb_height

        def to_dict(self):
            obj = {'type': self.ttype, 'id': self.uid, 'title': self.title,
                   'input_message_content': self.input_message_content}
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup
            if self.url:
                obj['url'] = self.url
            if self.hide_url:
                obj['hide_url'] = self.hide_url
            if self.description:
                obj['description'] = self.description
            if self.thumb_url:
                obj['thumb_url'] = self.thumb_url
            if self.thumb_width:
                obj['thumb_width'] = self.thumb_width
            if self.thumb_height:
                obj['thumb_height'] = self.thumb_height
            return obj

    class __InlineQueryResultPhoto(JsonSerializable):
        def __init__(self, uid, photo_url, thumb_url, photo_width=None, photo_height=None, title=None, description=None,
                     caption=None, parse_mode=None, caption_entities=None, reply_markup=None,
                     input_message_content=None):
            """
            Represents a link to a photo
            :param str uid: Unique identifier for this result
            :param str photo_url: A valid URL of the photo. Photo must be in JPEG format
            :param str thumb_url: URL of the thumbnail for the photo
            :param int or None photo_width: Optional. Width of the photo
            :param int or None photo_height: Optional. Height of the photo
            :param str title: Title of the result
            :param str or None description: Optional. Short description of the result
            :param str or None caption: Optional. Caption of the photo to be sent, 0-1024 characters after
                                        entities parsing
            :param str or None parse_mode: Optional. Mode for parsing entities in the photo caption
            :param list[MessageEntity] caption_entities: Optional. List of special entities that appear in the caption,
                                                          which can be specified instead of parse_mode
            :param InlineKeyboardMarkup or None reply_markup: Optional. Inline keyboard attached to the message
            :param InputMessageContent or None input_message_content: Content of the message to be sent
            """
            self.ttype = 'photo'
            self.uid = uid
            self.photo_url = photo_url
            self.photo_width = photo_width
            self.photo_height = photo_height
            self.thumb_url = thumb_url
            self.title = title
            self.description = description
            self.caption = caption
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities
            self.reply_markup = reply_markup
            self.input_message_content = input_message_content

        def to_dict(self):
            obj = {'type': self.ttype, 'id': self.uid,
                   'photo_url': self.photo_url, 'thumb_url': self.thumb_url}
            if self.photo_width:
                obj['photo_width'] = self.photo_width
            if self.photo_height:
                obj['photo_height'] = self.photo_height
            if self.title:
                obj['title'] = self.title
            if self.description:
                obj['description'] = self.description
            if self.caption:
                obj['caption'] = self.caption
            if self.parse_mode:
                obj['parse_mode'] = self.parse_mode
            if self.caption_entities:
                obj['caption_entities'] = self.caption_entities
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content
            return obj

    class __InlineQueryResultGif(JsonSerializable):
        def __init__(self, uid, gif_url, gif_width=None, gif_height=None, gif_duration=None, thumb_url=None,
                     thumb_mime_type=None, title=None, caption=None, parse_mode=None, caption_entities=None,
                     reply_markup=None, input_message_content=None):
            """
            Represents a link to an animated GIF file
            :param str uid: Unique identifier for this result
            :param str gif_url: A valid URL of the GIF
            :param int or None gif_width: Optional. Width of the GIF
            :param int or None gif_height: Optional. Height of the GIF
            :param int or None gif_duration: Optional. Duration of the GIF in seconds
            :param str thumb_url: URL of the static (JPEG or GIF) or animated (MPEG4) thumbnail for the result
            :param str or None thumb_mime_type: Optional. MIME type of the thumbnail, must be one of “image/jpeg”,
                                                “image/gif”, or “video/mp4”. Defaults to “image/jpeg”
            :param str title: Title of the result
            :param str or None caption: Optional. Caption of the photo to be sent, 0-1024 characters after
                                        entities parsing
            :param str or None parse_mode: Optional. Mode for parsing entities in the photo caption
            :param list[MessageEntity] caption_entities: Optional. List of special entities that appear in the caption,
                                                          which can be specified instead of parse_mode
            :param InlineKeyboardMarkup or None reply_markup: Optional. Inline keyboard attached to the message
            :param InputMessageContent or None input_message_content: Content of the message to be sent
            """
            self.ttype = 'gif'
            self.uid = uid
            self.gif_url = gif_url
            self.gif_width = gif_width
            self.gif_height = gif_height
            self.gif_duration = gif_duration
            self.thumb_url = thumb_url
            self.thumb_mime_type = thumb_mime_type
            self.title = title
            self.caption = caption
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities
            self.reply_markup = reply_markup
            self.input_message_content = input_message_content

        def to_dict(self):
            obj = {'type': self.ttype, 'id': self.uid,
                   'gif_url': self.gif_url, 'thumb_url': self.thumb_url}
            if self.gif_height:
                obj['gif_height'] = self.gif_height
            if self.gif_width:
                obj['gif_width'] = self.gif_width
            if self.gif_duration:
                obj['gif_duration'] = self.gif_duration
            if self.thumb_url:
                obj['thumb_url'] = self.thumb_url
            if self.thumb_mime_type:
                obj['thumb_mime_type'] = self.thumb_mime_type
            if self.title:
                obj['title'] = self.title
            if self.caption:
                obj['caption'] = self.caption
            if self.parse_mode:
                obj['parse_mode'] = self.parse_mode
            if self.caption_entities:
                obj['caption_entities'] = self.caption_entities
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup.to_dict()
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content
            return obj

    class __InlineQueryResultMpeg4Gif(JsonSerializable):
        def __init__(self, uid, mpeg4_url, thumb_url, mpeg4_width=None, mpeg4_height=None, mpeg4_duration=None,
                     thumb_mime_type=None, title=None, caption=None, parse_mode=None, caption_entities=None,
                     reply_markup=None, input_message_content=None):
            """
            Represents a link to a video animation (H.264/MPEG-4 AVC video without sound)
            :param str uid: Unique identifier for this result
            :param str mpeg4_url: A valid URL for the MP4 file
            :param int or None mpeg4_width: Optional. Video width
            :param int or None mpeg4_height: Optional. Video height
            :param int or None mpeg4_duration: Optional. Video duration in seconds
            :param str thumb_url: URL of the static (JPEG or GIF) or animated (MPEG4) thumbnail for the result
            :param str or None thumb_mime_type: Optional. MIME type of the thumbnail, must be one of “image/jpeg”,
                                                “image/gif”, or “video/mp4”. Defaults to “image/jpeg”
            :param str title: Title of the result
            :param str or None caption: Optional. Caption of the photo to be sent, 0-1024 characters after
                                        entities parsing
            :param str or None parse_mode: Optional. Mode for parsing entities in the photo caption
            :param list[MessageEntity] caption_entities: Optional. List of special entities that appear in the caption,
                                                          which can be specified instead of parse_mode
            :param InlineKeyboardMarkup or None reply_markup: Optional. Inline keyboard attached to the message
            :param InputMessageContent or None input_message_content: Content of the message to be sent
            """
            self.ttype = 'mpeg4_gif'
            self.uid = uid
            self.mpeg4_url = mpeg4_url
            self.mpeg4_width = mpeg4_width
            self.mpeg4_height = mpeg4_height
            self.mpeg4_duration = mpeg4_duration
            self.thumb_url = thumb_url
            self.thumb_mime_type = thumb_mime_type
            self.title = title
            self.caption = caption
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities
            self.reply_markup = reply_markup
            self.input_message_content = input_message_content

        def to_dict(self):
            obj = {'type': self.ttype, 'id': self.uid, 'mpeg4_url': self.mpeg4_url, 'thumb_url': self.thumb_url}
            if self.mpeg4_width:
                obj['mpeg4_width'] = self.mpeg4_width
            if self.mpeg4_height:
                obj['mpeg4_height'] = self.mpeg4_height
            if self.mpeg4_duration:
                obj['mpeg4_duration '] = self.mpeg4_duration
            if self.thumb_mime_type:
                obj['thumb_mime_type'] = self.thumb_mime_type
            if self.title:
                obj['title'] = self.title
            if self.caption:
                obj['caption'] = self.caption
            if self.parse_mode:
                obj['parse_mode'] = self.parse_mode
            if self.caption_entities:
                obj['caption_entities'] = self.caption_entities
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup.to_dict()
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content
            if self.mpeg4_duration:
                obj['mpeg4_duration '] = self.mpeg4_duration
            return obj

    class __InlineQueryResultVideo(JsonSerializable):
        def __init__(self, uid, video_url, mime_type, thumb_url, title, caption=None, parse_mode=None,
                     caption_entities=None, video_width=None, video_height=None, video_duration=None, description=None,
                     reply_markup=None, input_message_content=None):
            """
            Represents a link to a page containing an embedded video player or a video file
            :param str uid: Unique identifier for this result
            :param str video_url: A valid URL for the embedded video player or video file
            :param str mime_type: Mime type of the content of video url, “text/html” or “video/mp4”
            :param str thumb_url: URL of the static (JPEG or GIF) or animated (MPEG4) thumbnail for the result
            :param str title: Title of the result
            :param str or None caption: Optional. Caption of the photo to be sent, 0-1024 characters after
                                        entities parsing
            :param str or None parse_mode: Optional. Mode for parsing entities in the photo caption
            :param list[MessageEntity] caption_entities: Optional. List of special entities that appear in the caption,
                                                          which can be specified instead of parse_mode
            :param int or None video_width: Optional. Video width
            :param int or None video_height: Optional. Video height
            :param int or None video_duration: Optional. Video duration in seconds
            :param str or None description: Optional. Short description of the result
            :param InlineKeyboardMarkup or None reply_markup: Optional. Inline keyboard attached to the message
            :param InputMessageContent or None input_message_content: Content of the message to be sent
            """
            self.ttype = 'video'
            self.uid = uid
            self.video_url = video_url
            self.mime_type = mime_type
            self.thumb_url = thumb_url
            self.title = title
            self.caption = caption
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities
            self.video_width = video_width
            self.video_height = video_height
            self.video_duration = video_duration
            self.description = description
            self.input_message_content = input_message_content
            self.reply_markup = reply_markup

        def to_dict(self):
            obj = {'type': self.ttype, 'id': self.uid, 'video_url': self.video_url, 'mime_type': self.mime_type,
                   'thumb_url': self.thumb_url, 'title': self.title}
            if self.caption:
                obj['caption'] = self.caption
            if self.parse_mode:
                obj['parse_mode'] = self.parse_mode
            if self.caption_entities:
                obj['caption_entities'] = self.caption_entities
            if self.video_width:
                obj['video_width'] = self.video_width
            if self.video_height:
                obj['video_height'] = self.video_height
            if self.video_duration:
                obj['video_duration'] = self.video_duration
            if self.description:
                obj['description'] = self.description
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content
            return obj

    class __InlineQueryResultAudio(JsonSerializable):
        def __init__(self, uid, audio_url, title, caption=None, parse_mode=None, caption_entities=None, performer=None,
                     audio_duration=None, reply_markup=None, input_message_content=None):
            """
            Represents a link to an MP3 audio file
            :param str uid: Unique identifier for this result
            :param str audio_url: A valid URL for the audio file
            :param str title: Title
            :param str or None caption: Optional. Caption, 0-1024 characters after entities parsing
            :param str or None parse_mode: Optional. Mode for parsing entities in the audio caption
            :param list[MessageEntity] or None caption_entities: Optional. List of special entities that appear in the
                                                                 caption, which can be specified instead of parse_mode
            :param str or None performer: Optional. Performer
            :param int or None audio_duration: Optional. Audio duration in seconds
            :param InlineKeyboardMarkup or None reply_markup: Optional. Inline keyboard attached to the message
            :param InputMessageContent or None input_message_content: Content of the message to be sent
            """
            self.ttype = 'audio'
            self.uid = uid
            self.audio_url = audio_url
            self.title = title
            self.caption = caption
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities
            self.performer = performer
            self.audio_duration = audio_duration
            self.reply_markup = reply_markup
            self.input_message_content = input_message_content

        def to_dict(self):
            obj = {'type': self.ttype, 'id': self.uid,
                   'audio_url': self.audio_url, 'title': self.title}
            if self.caption:
                obj['caption'] = self.caption
            if self.parse_mode:
                obj['parse_mode'] = self.parse_mode
            if self.caption_entities:
                obj['caption_entities'] = self.caption_entities
            if self.performer:
                obj['performer'] = self.performer
            if self.audio_duration:
                obj['audio_duration'] = self.audio_duration
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup.to_dict()
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content
            return obj

    class __InlineQueryResultVoice(JsonSerializable):
        def __init__(self, uid, voice_url, title, caption=None, parse_mode=None, caption_entities=None,
                     voice_duration=None, reply_markup=None, input_message_content=None):
            """
            Represents a link to a voice recording in an .ogg container encoded with OPUS
            :param str uid: Unique identifier for this result
            :param str voice_url: A valid URL for the voice recording
            :param str title: Recording title
            :param str or None caption: Optional. Caption, 0-1024 characters after entities parsing
            :param str or None parse_mode: Optional. Mode for parsing entities in the audio caption
            :param list[MessageEntity] or None caption_entities: Optional. List of special entities that appear in the
                                                                 caption, which can be specified instead of parse_mode
            :param int or None voice_duration: Optional. Recording duration in seconds
            :param InlineKeyboardMarkup or None reply_markup: Optional. Inline keyboard attached to the message
            :param InputMessageContent or None input_message_content: Content of the message to be sent
            """
            self.ttype = 'voice'
            self.uid = uid
            self.voice_url = voice_url
            self.title = title
            self.caption = caption
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities
            self.voice_duration = voice_duration
            self.reply_markup = reply_markup
            self.input_message_content = input_message_content

        def to_dict(self):
            obj = {'type': self.ttype, 'id': self.uid,
                   'voice_url': self.voice_url, 'title': self.title}
            if self.caption:
                obj['caption'] = self.caption
            if self.parse_mode:
                obj['parse_mode'] = self.parse_mode
            if self.caption_entities:
                obj['caption_entities'] = self.caption_entities
            if self.voice_duration:
                obj['voice_duration'] = self.voice_duration
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content
            return obj

    class __InlineQueryResultDocument(JsonSerializable):
        def __init__(self, uid, title, document_url, mime_type, caption=None, parse_mode=None, caption_entities=None,
                     description=None, reply_markup=None, input_message_content=None, thumb_url=None, thumb_width=None,
                     thumb_height=None):
            """
            Represents a link to a file
            :param str uid: Unique identifier for this result
            :param str title: Recording title
            :param str or None caption: Optional. Caption, 0-1024 characters after entities parsing
            :param str or None parse_mode: Optional. Mode for parsing entities in the audio caption
            :param list[MessageEntity] or None caption_entities: Optional. List of special entities that appear in the
                                                                 caption, which can be specified instead of parse_mode
            :param str document_url: A valid URL for the file
            :param str mime_type: Mime type of the content of the file, either “application/pdf” or “application/zip”
            :param str or None description: Optional. Short description of the result
            :param InlineKeyboardMarkup or None reply_markup: Optional. Inline keyboard attached to the message
            :param InputMessageContent or None input_message_content: Content of the message to be sent
            :param str or None thumb_url: Optional. Url of the thumbnail for the result
            :param int or None thumb_width: Optional. Thumbnail width
            :param int or None thumb_height: Optional. Thumbnail height
            """
            self.ttype = 'document'
            self.uid = uid
            self.title = title
            self.caption = caption
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities
            self.document_url = document_url
            self.mime_type = mime_type
            self.description = description
            self.reply_markup = reply_markup
            self.input_message_content = input_message_content
            self.thumb_url = thumb_url
            self.thumb_width = thumb_width
            self.thumb_height = thumb_height

        def to_dict(self):
            obj = {'type': self.ttype, 'id': self.uid, 'title': self.title, 'document_url': self.document_url,
                   'mime_type': self.mime_type}
            if self.caption:
                obj['caption'] = self.caption
            if self.parse_mode:
                obj['parse_mode'] = self.parse_mode
            if self.caption_entities:
                obj['caption_entities'] = self.caption_entities
            if self.description:
                obj['description'] = self.description
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content
            if self.thumb_url:
                obj['thumb_url'] = self.thumb_url
            if self.thumb_width:
                obj['thumb_width'] = self.thumb_width
            if self.thumb_height:
                obj['thumb_height'] = self.thumb_height
            return obj

    class __InlineQueryResultLocation(JsonSerializable):
        def __init__(self, uid, title, latitude, longitude, horizontal_accuracy=None, live_period=None, heading=None,
                     proximity_alert_radius=None, reply_markup=None, input_message_content=None, thumb_url=None,
                     thumb_width=None, thumb_height=None):
            """
            Represents a location on a map
            :param str uid: Unique identifier for this result
            :param int latitude: Location latitude in degrees
            :param int longitude: Location longitude in degrees
            :param str title: Location title
            :param int or None horizontal_accuracy: Optional. The radius of uncertainty for the location, measured in
                                                    meters; 0-1500
            :param int or None live_period: Optional. Period in seconds for which the location can be updated,
                                            should be between 60 and 86400
            :param int or None heading: Optional. For live locations, a direction in which the user is moving,
                                        in degrees. Must be between 1 and 360 if specified
            :param int or None proximity_alert_radius: Optional. For live locations, a maximum distance for proximity
                                                       alerts about approaching another chat member, in meters.
                                                       Must be between 1 and 100000 if specified
            :param InlineKeyboardMarkup or None reply_markup: Optional. Inline keyboard attached to the message
            :param InputMessageContent or None input_message_content: Content of the message to be sent
            :param str or None thumb_url: Optional. Url of the thumbnail for the result
            :param int or None thumb_width: Optional. Thumbnail width
            :param int or None thumb_height: Optional. Thumbnail height
            """
            self.ttype = 'location'
            self.uid = uid
            self.latitude = latitude
            self.longitude = longitude
            self.title = title
            self.horizontal_accuracy = horizontal_accuracy
            self.live_period = live_period
            self.heading = heading
            self.proximity_alert_radius = proximity_alert_radius
            self.reply_markup = reply_markup
            self.input_message_content = input_message_content
            self.thumb_url = thumb_url
            self.thumb_width = thumb_width
            self.thumb_height = thumb_height

        def to_dict(self):
            obj = {'type': self.ttype, 'id': self.uid, 'latitude': self.latitude, 'longitude': self.longitude,
                   'title': self.title}
            if self.horizontal_accuracy:
                obj['horizontal_accuracy'] = self.horizontal_accuracy
            if self.live_period:
                obj['live_period'] = self.live_period
            if self.heading:
                obj['heading'] = self.heading
            if self.proximity_alert_radius:
                obj['proximity_alert_radius'] = self.proximity_alert_radius
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content
            if self.thumb_url:
                obj['thumb_url'] = self.thumb_url
            if self.thumb_width:
                obj['thumb_width'] = self.thumb_width
            if self.thumb_height:
                obj['thumb_height'] = self.thumb_height
            return obj

    class __InlineQueryResultVenue(JsonSerializable):
        def __init__(self, uid, latitude, longitude, title, address, foursquare_id=None, foursquare_type=None,
                     google_place_id=None, google_place_type=None, reply_markup=None, input_message_content=None,
                     thumb_url=None, thumb_width=None, thumb_height=None):
            """
            Represents a venue
            :param str uid: Unique identifier for this result
            :param int latitude: Location latitude in degrees
            :param int longitude: Location longitude in degrees
            :param str title: Location title
            :param str address: Address of the venue
            :param str or None foursquare_id: Optional. Foursquare identifier of the venue if known
            :param str or None foursquare_type: Optional. Foursquare type of the venue, if known. For example,
                                                “arts_entertainment/default”, “arts_entertainment/aquarium” or
                                                “food/icecream”
            :param str or None google_place_id: Optional. Google Places identifier of the venue
            :param str or None google_place_type: Optional. Google Places type of the venue
            :param InlineKeyboardMarkup or None reply_markup: Optional. Inline keyboard attached to the message
            :param InputMessageContent or None input_message_content: Content of the message to be sent
            :param str or None thumb_url: Optional. Url of the thumbnail for the result
            :param int or None thumb_width: Optional. Thumbnail width
            :param int or None thumb_height: Optional. Thumbnail height
            """
            self.ttype = 'venue'
            self.uid = uid
            self.latitude = latitude
            self.longitude = longitude
            self.title = title
            self.address = address
            self.foursquare_id = foursquare_id
            self.foursquare_type = foursquare_type
            self.google_place_id = google_place_id
            self.google_place_type = google_place_type
            self.reply_markup = reply_markup
            self.input_message_content = input_message_content
            self.thumb_url = thumb_url
            self.thumb_width = thumb_width
            self.thumb_height = thumb_height

        def to_dict(self):
            obj = {
                'type': self.ttype, 'id': self.uid, 'latitude': self.latitude,
                'longitude': self.longitude,
                'title': self.title,
                'address': self.address}
            if self.foursquare_id:
                obj['foursquare_id'] = self.foursquare_id
            if self.foursquare_type:
                obj['foursquare_type'] = self.foursquare_type
            if self.google_place_id:
                obj['google_place_id'] = self.google_place_id
            if self.google_place_type:
                obj['google_place_type'] = self.google_place_type
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content
            if self.thumb_url:
                obj['thumb_url'] = self.thumb_url
            if self.thumb_width:
                obj['thumb_width'] = self.thumb_width
            if self.thumb_height:
                obj['thumb_height'] = self.thumb_height
            return obj

    class __InlineQueryResultContact(JsonSerializable):
        def __init__(self, uid, phone_number, first_name, last_name=None, vcard=None, reply_markup=None,
                     input_message_content=None, thumb_url=None, thumb_width=None, thumb_height=None):
            """
            Represents a contact with a phone number
            :param str uid: Unique identifier for this result
            :param str phone_number: Contact's phone number
            :param str first_name:Contact's first name
            :param str or None last_name:Optional. Contact's last name
            :param str or None vcard: Optional. Additional data about the contact in the form of a vCard, 0-2048 bytes
            :param InlineKeyboardMarkup or None reply_markup: Optional. Inline keyboard attached to the message
            :param InputMessageContent or None input_message_content: Content of the message to be sent
            :param str or None thumb_url: Optional. Url of the thumbnail for the result
            :param int or None thumb_width: Optional. Thumbnail width
            :param int or None thumb_height: Optional. Thumbnail height
            """
            self.ttype = 'contact'
            self.uid = uid
            self.phone_number = phone_number
            self.first_name = first_name
            self.last_name = last_name
            self.vcard = vcard
            self.reply_markup = reply_markup
            self.input_message_content = input_message_content
            self.thumb_url = thumb_url
            self.thumb_width = thumb_width
            self.thumb_height = thumb_height

        def to_dict(self):
            obj = {'type': self.ttype, 'id': self.uid, 'phone_number': self.phone_number, 'first_name': self.first_name}
            if self.last_name:
                obj['last_name'] = self.last_name
            if self.vcard:
                obj['vcard'] = self.vcard
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content
            if self.thumb_url:
                obj['thumb_url'] = self.thumb_url
            if self.thumb_width:
                obj['thumb_width'] = self.thumb_width
            if self.thumb_height:
                obj['thumb_height'] = self.thumb_height
            return obj

    class __InlineQueryResultGame(JsonSerializable):
        def __init__(self, uid, game_short_name, reply_markup=None):
            """
            Represents a Game
            :param str uid: Unique identifier for this result
            :param str game_short_name: Short name of the game
            :param InlineKeyboardMarkup or None reply_markup: Optional. Inline keyboard attached to the message
            """
            self.ttype = 'game'
            self.uid = uid
            self.game_short_name = game_short_name
            self.reply_markup = reply_markup

        def to_dict(self):
            obj = {'type': self.ttype, 'id': self.uid, 'game_short_name': self.game_short_name}
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup.to_dict()
            return obj

    class __InlineQueryResultCachedPhoto(JsonSerializable):
        def __init__(self, uid, photo_file_id, title=None, description=None, caption=None, parse_mode=None,
                     caption_entities=None, reply_markup=None, input_message_content=None):
            """
            Represents a link to a photo. By default, this photo will be sent by the user with optional caption
            :param str uid: Unique identifier for this result
            :param str photo_file_id: A valid file identifier of the photo
            :param str or None title: Optional. Title for the result
            :param str or None description: Optional. Short description of the result
            :param str or None caption: Optional. Caption of the photo to be sent, 0-1024 characters after entities
                                        parsing
            :param str or None parse_mode: 	Optional. Mode for parsing entities in the photo caption
            :param str or None caption_entities: Optional. List of special entities that appear in the caption,
                                                 which can be specified instead of parse_mode
            :param InlineKeyboardMarkup or None reply_markup: Optional. Inline keyboard attached to the message
            :param InputMessageContent or None input_message_content: Content of the message to be sent
            """
            self.ttype = 'photo'
            self.uid = uid
            self.photo_file_id = photo_file_id
            self.title = title
            self.description = description
            self.caption = caption
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities
            self.reply_markup = reply_markup
            self.input_message_content = input_message_content

        def to_dict(self):
            obj = {'type': self.ttype, 'id': self.uid, 'photo_file_id': self.photo_file_id}
            if self.title:
                obj['title'] = self.title
            if self.description:
                obj['description'] = self.description
            if self.caption:
                obj['caption'] = self.caption
            if self.parse_mode:
                obj['parse_mode'] = self.parse_mode
            if self.caption_entities:
                obj['caption_entities'] = self.caption_entities
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content
            return obj

    class __InlineQueryResultCachedGif(JsonSerializable):
        def __init__(self, uid, gif_file_id, title=None, caption=None, parse_mode=None, caption_entities=None,
                     reply_markup=None, input_message_content=None):
            """
            Represents a link to an animated GIF file stored on the Telegram servers
            :param str uid: Unique identifier for this result
            :param str gif_file_id: A valid file identifier for the GIF file
            :param str or None title: Optional. Title for the result
            :param str or None caption: Optional. Caption of the GIF to be sent, 0-1024 characters after entities
                                        parsing
            :param str or None parse_mode: 	Optional. Mode for parsing entities in the caption
            :param str or None caption_entities: Optional. List of special entities that appear in the caption,
                                                 which can be specified instead of parse_mode
            :param InlineKeyboardMarkup or None reply_markup: Optional. Inline keyboard attached to the message
            :param InputMessageContent or None input_message_content: Content of the message to be sent
            """
            self.ttype = 'gif'
            self.uid = uid
            self.gif_file_id = gif_file_id
            self.title = title
            self.caption = caption
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities
            self.reply_markup = reply_markup
            self.input_message_content = input_message_content

        def to_dict(self):
            obj = {'type': self.ttype, 'id': self.uid,
                   'gif_file_id': self.gif_file_id}
            if self.title:
                obj['title'] = self.title
            if self.caption:
                obj['caption'] = self.caption
            if self.parse_mode:
                obj['parse_mode'] = self.parse_mode
            if self.caption_entities:
                obj['caption_entities'] = self.caption_entities
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content
            return obj

    class __InlineQueryResultCachedMpeg4Gif(JsonSerializable):
        def __init__(self, uid, mpeg4_file_id, title=None, caption=None, parse_mode=None, caption_entities=None,
                     reply_markup=None, input_message_content=None):
            """
            Represents a link to a video animation (H.264/MPEG-4 AVC video without sound) stored on the Telegram servers
            :param str uid: Unique identifier for this result
            :param str mpeg4_file_id: A valid file identifier for the MP4 file
            :param str or None title: Optional. Title for the result
            :param str or None caption: Optional. Caption of the MPEG-4 to be sent, 0-1024 characters after entities
                                        parsing
            :param str or None parse_mode: 	Optional. Mode for parsing entities in the caption
            :param str or None caption_entities: Optional. List of special entities that appear in the caption,
                                                 which can be specified instead of parse_mode
            :param InlineKeyboardMarkup or None reply_markup: Optional. Inline keyboard attached to the message
            :param InputMessageContent or None input_message_content: Content of the message to be sent
            """
            self.ttype = 'mpeg4_gif'
            self.uid = uid
            self.mpeg4_file_id = mpeg4_file_id
            self.title = title
            self.caption = caption
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities
            self.reply_markup = reply_markup
            self.input_message_content = input_message_content

        def to_dict(self):
            obj = {'type': self.ttype, 'id': self.uid, 'mpeg4_file_id': self.mpeg4_file_id}
            if self.title:
                obj['title'] = self.title
            if self.caption:
                obj['caption'] = self.caption
            if self.parse_mode:
                obj['parse_mode'] = self.parse_mode
            if self.caption_entities:
                obj['caption_entities'] = self.caption_entities
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content
            return obj

    class __InlineQueryResultCachedSticker(JsonSerializable):
        def __init__(self, uid, sticker_file_id, reply_markup=None, input_message_content=None):
            """
            Represents a link to a sticker stored on the Telegram servers
            :param str uid: Unique identifier for this result
            :param str sticker_file_id: A valid file identifier for the sticker
            :param InlineKeyboardMarkup or None reply_markup: Optional. Inline keyboard attached to the message
            :param InputMessageContent or None input_message_content: Content of the message to be sent
            """
            self.ttype = 'sticker'
            self.uid = uid
            self.sticker_file_id = sticker_file_id
            self.reply_markup = reply_markup
            self.input_message_content = input_message_content

        def to_dict(self):
            obj = {'type': self.ttype, 'id': self.uid, 'sticker_file_id': self.sticker_file_id}
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content
            return obj

    class __InlineQueryResultCachedDocument(JsonSerializable):
        def __init__(self, uid, title, document_file_id, description=None, caption=None, parse_mode=None,
                     caption_entities=None, reply_markup=None, input_message_content=None):
            """
            Represents a link to a file stored on the Telegram servers
            :param str uid: Unique identifier for this result
            :param str or None title: Optional. Title for the result
            :param str document_file_id: A valid file identifier for the file
            :param str or None description: Optional. Short description of the result
            :param str or None caption: Optional. Caption of the document to be sent, 0-1024 characters after entities
                                        parsing
            :param str or None parse_mode: 	Optional. Mode for parsing entities in the document caption
            :param str or None caption_entities: Optional. List of special entities that appear in the caption,
                                                 which can be specified instead of parse_mode
            :param InlineKeyboardMarkup or None reply_markup: Optional. Inline keyboard attached to the message
            :param InputMessageContent or None input_message_content: Content of the message to be sent
            """
            self.ttype = 'document'
            self.uid = uid
            self.title = title
            self.document_file_id = document_file_id
            self.description = description
            self.caption = caption
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities
            self.reply_markup = reply_markup
            self.input_message_content = input_message_content

        def to_dict(self):
            obj = {'type': self.ttype, 'id': self.uid, 'document_file_id': self.document_file_id}
            if self.title:
                obj['title'] = self.title
            if self.description:
                obj['description'] = self.description
            if self.caption:
                obj['caption'] = self.caption
            if self.parse_mode:
                obj['parse_mode'] = self.parse_mode
            if self.caption_entities:
                obj['caption_entities'] = self.caption_entities
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content
            return obj

    class __InlineQueryResultCachedVideo(JsonSerializable):
        def __init__(self, uid, video_file_id, title, description=None, caption=None, parse_mode=None,
                     caption_entities=None, reply_markup=None, input_message_content=None):
            """
            Represents a link to a video file stored on the Telegram servers
            :param str uid: Unique identifier for this result
            :param str video_file_id: A valid file identifier for the video file
            :param str or None title: Optional. Title for the result
            :param str or None description: Optional. Short description of the result
            :param str or None caption: Optional. Caption of the video to be sent, 0-1024 characters after entities
                                        parsing
            :param str or None parse_mode: 	Optional. Mode for parsing entities in the caption
            :param str or None caption_entities: Optional. List of special entities that appear in the caption,
                                                 which can be specified instead of parse_mode
            :param InlineKeyboardMarkup or None reply_markup: Optional. Inline keyboard attached to the message
            :param InputMessageContent or None input_message_content: Content of the message to be sent
            """
            self.ttype = 'video'
            self.uid = uid
            self.video_file_id = video_file_id
            self.title = title
            self.description = description
            self.caption = caption
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities
            self.reply_markup = reply_markup
            self.input_message_content = input_message_content

        def to_dict(self):
            obj = {'type': self.ttype, 'id': self.uid, 'video_file_id': self.video_file_id}
            if self.title:
                obj['title'] = self.title
            if self.description:
                obj['description'] = self.description
            if self.caption:
                obj['caption'] = self.caption
            if self.parse_mode:
                obj['parse_mode'] = self.parse_mode
            if self.caption_entities:
                obj['caption_entities'] = self.caption_entities
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content
            return obj

    class __InlineQueryResultCachedVoice(JsonSerializable):
        def __init__(self, uid, voice_file_id, title, caption=None, parse_mode=None, caption_entities=None,
                     reply_markup=None, input_message_content=None):
            """
            Represents a link to a voice message stored on the Telegram servers
            :param str uid: Unique identifier for this result
            :param str voice_file_id: A valid file identifier for the voice file
            :param str or None title: Optional. Title for the result
            :param str or None caption: Optional. Caption of the voice to be sent, 0-1024 characters after entities
                                        parsing
            :param str or None parse_mode: 	Optional. Mode for parsing entities in the caption
            :param str or None caption_entities: Optional. List of special entities that appear in the caption,
                                                 which can be specified instead of parse_mode
            :param InlineKeyboardMarkup or None reply_markup: Optional. Inline keyboard attached to the message
            :param InputMessageContent or None input_message_content: Content of the message to be sent
            """
            self.ttype = 'voice'
            self.uid = uid
            self.voice_file_id = voice_file_id
            self.title = title
            self.caption = caption
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities
            self.reply_markup = reply_markup
            self.input_message_content = input_message_content

        def to_dict(self):
            obj = {'type': self.ttype, 'id': self.uid,
                   'voice_file_id': self.voice_file_id}
            if self.title:
                obj['title'] = self.title
            if self.caption:
                obj['caption'] = self.caption
            if self.parse_mode:
                obj['parse_mode'] = self.parse_mode
            if self.caption_entities:
                obj['caption_entities'] = self.caption_entities
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content
            return obj

    class __InlineQueryResultCachedAudio(JsonSerializable):
        def __init__(self, uid, audio_file_id, caption=None, parse_mode=None, caption_entities=None,
                     reply_markup=None, input_message_content=None):
            """
            Represents a link to an MP3 audio file stored on the Telegram servers
            :param str uid: Unique identifier for this result
            :param str audio_file_id: A valid file identifier for the audio file
            :param str or None caption: Optional. Caption of the audio to be sent, 0-1024 characters after entities
                                        parsing
            :param str or None parse_mode: 	Optional. Mode for parsing entities in the caption
            :param str or None caption_entities: Optional. List of special entities that appear in the caption,
                                                 which can be specified instead of parse_mode
            :param InlineKeyboardMarkup or None reply_markup: Optional. Inline keyboard attached to the message
            :param InputMessageContent or None input_message_content: Content of the message to be sent
            """
            self.ttype = 'audio'
            self.uid = uid
            self.audio_file_id = audio_file_id
            self.caption = caption
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities
            self.reply_markup = reply_markup
            self.input_message_content = input_message_content

        def to_dict(self):
            obj = {'type': self.ttype, 'id': self.uid, 'audio_file_id': self.audio_file_id}
            if self.caption:
                obj['caption'] = self.caption
            if self.parse_mode:
                obj['parse_mode'] = self.parse_mode
            if self.caption_entities:
                obj['caption_entities'] = self.caption_entities
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content
            return obj


class InputMessageContent:
    """
    This object represents the content of a message to be sent as a result of an inline query. 
    Telegram clients currently support the following 5 types:

        InputContactMessageContent
        InputLocationMessageContent
        InputTextMessageContent
        InputVenueMessageContent
        InputInvoiceMessageContent

   """

    def __init__(self):
        self.Text = self.__InputTextMessageContent
        self.Location = self.__InputLocationMessageContent
        self.Venue = self.__InputVenueMessageContent
        self.Contact = self.__InputContactMessageContent
        self.Invoice = self.__InputInvoiceMessageContent

    class __InputTextMessageContent(JsonSerializable):
        def __init__(self, message_text, parse_mode=None, entities=None, disable_web_page_preview=False):
            """
            Represents the content of a text message to be sent as the result of an inline query
            :param str message_text: Text of the message to be sent, 1-4096 characters
            :param str or None parse_mode: Optional. Mode for parsing entities in the message text
            :param list[MessageEntity] or None entities: Optional. List of special entities that appear in message text,
                                                         which can be specified instead of parse_mode
            :param bool disable_web_page_preview: Optional. Disables link previews for links in to send message
            """
            self.message_text = message_text
            self.parse_mode = parse_mode
            self.entities = entities
            self.disable_web_page_preview = disable_web_page_preview

        def to_dict(self):
            obj = {'message_text': self.message_text}
            if self.parse_mode:
                obj['parse_mode'] = self.parse_mode
            if self.entities:
                obj['entities'] = self.entities
            if self.disable_web_page_preview:
                obj['disable_web_page_preview'] = self.disable_web_page_preview
            return obj

    class __InputLocationMessageContent(JsonSerializable):
        def __init__(self, latitude, longitude, horizontal_accuracy=None, live_period=None, heading=None,
                     proximity_alert_radius=None):
            """
            Represents the content of a location message to be sent as the result of an inline query
            :param int latitude: Latitude of the location in degrees
            :param int longitude: Longitude of the location in degrees
            :param int or None horizontal_accuracy: Optional. The radius of uncertainty for the location,
                                                    measured in meters; 0-1500
            :param int or None live_period: Optional. Period in seconds for which the location can be updated,
                                            should be between 60 and 86400
            :param int or None heading: Optional. For live locations, a direction in which the user is moving,
                                       in degrees. Must be between 1 and 360 if specified
            :param int or None proximity_alert_radius: Optional. For live locations, a maximum distance for proximity
                                                       alerts about approaching another chat member, in meters.
                                                       Must be between 1 and 100000 if specified
            """
            self.latitude = latitude
            self.longitude = longitude
            self.horizontal_accuracy = horizontal_accuracy
            self.live_period = live_period
            self.heading = heading
            self.proximity_alert_radius = proximity_alert_radius

        def to_dict(self):
            obj = {'latitude': self.latitude, 'longitude': self.longitude}
            if self.horizontal_accuracy:
                obj['horizontal_accuracy'] = self.horizontal_accuracy
            if self.live_period:
                obj['live_period'] = self.live_period
            if self.heading:
                obj['heading'] = self.heading
            if self.proximity_alert_radius:
                obj['proximity_alert_radius'] = self.proximity_alert_radius
            return obj

    class __InputVenueMessageContent(JsonSerializable):
        def __init__(self, latitude, longitude, title, address, foursquare_id=None, foursquare_type=None,
                     google_place_id=None, google_place_type=None):
            """
            Represents the content of a venue message to be sent as the result of an inline query
            :param int latitude: Latitude of the venue in degrees
            :param int longitude: Longitude of the venue in degrees
            :param str title: Name of the venue
            :param str address: Address of the venue
            :param str or None foursquare_id: Optional. Foursquare identifier of the venue, if known
            :param str or None foursquare_type: Optional. Foursquare type of the venue, if known.
                                                For example, “arts_entertainment/default”, “arts_entertainment/aquarium”
                                                or “food/icecream”
            :param str or None google_place_id: Optional. Google Places identifier of the venue
            :param str or None google_place_type: Optional. Google Places type of the venue
            """
            self.latitude = latitude
            self.longitude = longitude
            self.title = title
            self.address = address
            self.foursquare_id = foursquare_id
            self.foursquare_type = foursquare_type
            self.google_place_id = google_place_id
            self.google_place_type = google_place_type

        def to_dict(self):
            obj = {'latitude': self.latitude, 'longitude': self.longitude, 'title': self.title, 'address': self.address}
            if self.foursquare_id:
                obj['foursquare_id'] = self.foursquare_id
            if self.foursquare_type:
                obj['foursquare_type'] = self.foursquare_type
            if self.google_place_id:
                obj['google_place_id'] = self.google_place_type
            if self.google_place_type:
                obj['google_place_type'] = self.google_place_type
            return obj

    class __InputContactMessageContent(JsonSerializable):
        def __init__(self, phone_number, first_name, last_name=None, vcard=None):
            """
            Represents a result of an inline query that was chosen by the user and sent to their chat partner
            :param str phone_number: Contact's phone number
            :param str first_name: Contact's first name
            :param str or None last_name: Optional. Contact's last name
            :param str or None vcard: Optional. Additional data about the contact in the form of a vCard, 0-2048 bytes
            """
            self.phone_number = phone_number
            self.first_name = first_name
            self.last_name = last_name
            self.vcard = vcard

        def to_dict(self):
            obj = {'phone_number': self.phone_number, 'first_name': self.first_name}
            if self.last_name:
                obj['last_name'] = self.last_name
            if self.vcard:
                obj['vcard'] = self.vcard
            return obj

    class __InputInvoiceMessageContent(JsonSerializable):
        def __init__(self, title, description, payload, provider_token, currency, prices, max_tip_amount=None,
                     suggested_tip_amounts=None, provider_data=None, photo_url=None, photo_size=None, photo_width=None,
                     photo_height=None, need_name=False, need_phone_number=False, need_email=False,
                     need_shipping_address=False, send_phone_number_to_provider=False, send_email_to_provider=False,
                     is_flexible=False):
            """
            Represents the content of an invoice message to be sent as the result of an inline query
            :param str title: Product name, 1-32 characters
            :param str description: Product description, 1-255 characters
            :param str payload: Bot-defined invoice payload, 1-128 bytes. This will not be displayed to the user,
                                use for your internal processes
            :param str provider_token: Payment provider token, obtained via Bot father
            :param str currency: Three-letter ISO 4217 currency code
            :param list[LabeledPrice] prices: Price breakdown, a JSON-serialized list of components
            :param int or None max_tip_amount: Optional. The maximum accepted amount for tips in the smallest units of
                                               the currency (integer, not float/double)
            :param list[int] or None suggested_tip_amounts: Optional. A JSON-serialized array of proposed amounts of
                                                            tip in the smallest units of the currency (integer, not
                                                            float/double)
            :param str or None provider_data: Optional. A JSON-serialized object for data about the invoice,
                                              which will be shared with the payment provider
            :param str or None photo_url: Optional. URL of the product photo for the invoice
            :param int or None photo_size: Optional. Photo size
            :param int or None photo_width: Optional. Photo width
            :param int or None photo_height: Optional. Photo height
            :param bool need_name: Optional. Pass True, if you require the user's full name to complete the order
            :param bool need_phone_number: Optional. Pass True, if you require the user's phone number to complete the
                                           order
            :param bool need_email: Optional. Pass True, if you require the user's email address to complete the order
            :param bool need_shipping_address: Optional. Pass True, if you require the user's shipping address to
                                               complete the order
            :param bool send_phone_number_to_provider: Optional. Pass True, if user's phone number should be sent to
                                                       provider
            :param bool send_email_to_provider: Optional. Pass True, if user's email address should be sent to provider
            :param bool is_flexible: Optional. Pass True, if the final price depends on the shipping method
            """
            self.title = title
            self.description = description
            self.payload = payload
            self.provider_token = provider_token
            self.currency = currency
            self.prices = prices
            self.max_tip_amount = max_tip_amount
            self.suggested_tip_amounts = suggested_tip_amounts
            self.provider_data = provider_data
            self.photo_url = photo_url
            self.photo_size = photo_size
            self.photo_width = photo_width
            self.photo_height = photo_height
            self.need_name = need_name
            self.need_phone_number = need_phone_number
            self.need_email = need_email
            self.need_shipping_address = need_shipping_address
            self.send_phone_number_to_provider = send_phone_number_to_provider
            self.send_email_to_provider = send_email_to_provider
            self.is_flexible = is_flexible

        def to_dict(self):
            obj = {
                'title': self.title,
                'description': self.description,
                'payload': self.payload,
                'provider_token': self.provider_token,
                'currency': self.currency,
                'prices': self.prices
            }
            if self.max_tip_amount:
                obj['max_tip_amount'] = self.max_tip_amount
            if self.suggested_tip_amounts:
                obj['suggested_tip_amounts'] = self.suggested_tip_amounts
            if self.provider_data:
                obj['provider_data'] = self.provider_data
            if self.photo_url:
                obj['photo_url'] = self.photo_url
            if self.photo_size:
                obj['photo_size'] = self.photo_size
            if self.photo_width:
                obj['photo_width'] = self.photo_width
            if self.photo_height:
                obj['photo_height'] = self.photo_height
            if self.need_name:
                obj['need_name'] = self.need_name
            if self.need_phone_number:
                obj['need_phone_number'] = self.need_phone_number
            if self.need_email:
                obj['need_email'] = self.need_email
            if self.need_shipping_address:
                obj['need_shipping_address'] = self.need_shipping_address
            if self.send_phone_number_to_provider:
                obj['send_phone_number_to_provider'] = self.send_phone_number_to_provider
            if self.send_email_to_provider:
                obj['send_email_to_provider'] = self.send_email_to_provider
            if self.is_flexible:
                obj['is_flexible'] = self.is_flexible
            return obj


class ChosenInlineResult(JsonDeserializable):
    """
    Represents a result of an inline query that was chosen by the user and sent to their chat partner
    """

    def __init__(self, result_id, from_user, query, location, inline_message_id):
        self.result_id = result_id
        self.from_user = from_user
        self.query = query
        self.location = location
        self.inline_message_id = inline_message_id

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        result_id = obj['result_id']
        from_user = User.de_json(obj['from'])
        query = obj['query']
        location = None
        if 'location' in obj:
            location = Location.de_json(obj['location'])
        inline_message_id = obj['inline_message_id']
        return cls(result_id, from_user, query, location, inline_message_id)


class SentWebAppMessage(JsonDeserializable):
    """
    Contains information about an inline message sent by a Web App on behalf a user
    """

    def __init__(self, inline_message_id):
        """
        Initialize the SentWebAppMessage object
        :param str or None inline_message_id: Optional, Identifier of the sent inline message
        """
        self.inline_message_id = inline_message_id

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        inline_message_id = None
        if 'inline_message_id' in obj:
            inline_message_id = obj['inline_message_id']
        return cls(inline_message_id)


class LabeledPrice(JsonSerializable):
    def __init__(self, label, amount):
        """
        This object represents a portion of the price for goods or services
        :param str label: Portion label
        :param int amount: Price of the product in the smallest units of the currency integer, not float/double
        :rtype: dict
        """
        self.label = label
        self.amount = amount

    def to_dict(self):
        return {'label': self.label, 'amount': self.amount}


class Invoice(JsonDeserializable):
    def __init__(self, title, description, start_parameter, currency, total_amount):
        """
        This object contains basic information about an invoice
        """
        self.title = title
        self.description = description
        self.start_parameter = start_parameter
        self.currency = currency
        self.total_amount = total_amount

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        title = obj['title']
        description = obj['description']
        start_parameter = obj['start_parameter']
        currency = obj['currency']
        total_amount = obj['total_amount']
        return cls(title, description, start_parameter, currency, total_amount)


class ShippingAddress(JsonDeserializable):
    def __init__(self, country_code, state, city, street_line1, street_line2, post_code):
        """
        This object represents a shipping address
        """
        self.country_code = country_code
        self.state = state
        self.city = city
        self.street_line1 = street_line1
        self.street_line2 = street_line2
        self.post_code = post_code

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        country_code = obj['country_code']
        state = obj['state']
        city = obj['city']
        street_line1 = obj['street_line1']
        street_line2 = obj['street_line2']
        post_code = obj['post_code']
        return cls(country_code, state, city, street_line1, street_line2, post_code)


class OrderInfo(JsonDeserializable):
    def __init__(self, name, phone_number, email, shipping_address):
        """
        This object represents information about an order
        """
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.shipping_address = shipping_address

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        name = None
        if 'name' in obj:
            name = obj['name']
        phone_number = None
        if 'phone_number' in obj:
            phone_number = obj['phone_number']
        email = None
        if 'email' in obj:
            email = obj['email']
        shipping_address = None
        if 'shipping_address' in obj:
            shipping_address = ShippingAddress.de_json(obj['shipping_address'])
        return cls(name, phone_number, email, shipping_address)


class ShippingOption(JsonSerializable):
    def __init__(self, uid, title, prices):
        """
        This object represents one shipping option
        :param str uid: Shipping option identifier
        :param str title: Option title
        :param list[LabeledPrice] prices: List of price portions
        :rtype: dict
        """
        self.uid = uid
        self.title = title
        self.prices = prices

    def to_dict(self):
        return {'id': self.uid, 'title': self.title, 'prices': self.prices}


class SuccessfulPayment(JsonDeserializable):
    def __init__(self, currency, total_amount, invoice_payload, shipping_option_id, order_info,
                 telegram_payment_charge_id, provider_payment_charge_id):
        """
        This object contains basic information about a successful payment
        """
        self.currency = currency
        self.total_amount = total_amount
        self.invoice_payload = invoice_payload
        self.shipping_option_id = shipping_option_id
        self.order_info = order_info
        self.telegram_payment_charge_id = telegram_payment_charge_id
        self.provider_payment_charge_id = provider_payment_charge_id

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        currency = obj['currency']
        total_amount = obj['total_amount']
        invoice_payload = obj['invoice_payload']
        shipping_option_id = None
        if 'shipping_option_id' in obj:
            shipping_option_id = obj['shipping_option_id']
        order_info = None
        if 'order_info' in obj:
            order_info = OrderInfo.de_json(obj['order_info'])
        telegram_payment_charge_id = obj['telegram_payment_charge_id']
        provider_payment_charge_id = obj['provider_payment_charge_id']
        return cls(currency, total_amount, invoice_payload, shipping_option_id, order_info,
                   telegram_payment_charge_id, provider_payment_charge_id)


class ShippingQuery(JsonDeserializable):
    def __init__(self, uid, from_user, invoice_payload, shipping_address):
        """
        This object contains information about an incoming shipping query
        """
        self.uid = uid
        self.from_user = from_user
        self.invoice_payload = invoice_payload
        self.shipping_address = shipping_address

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        uid = obj['id']
        from_user = User.de_json(obj['from'])
        invoice_payload = obj['invoice_payload']
        shipping_address = ShippingAddress.de_json(obj['shipping_address'])
        return cls(uid, from_user, invoice_payload, shipping_address)


class PreCheckoutQuery(JsonDeserializable):
    def __init__(self, uid, from_user, currency, total_amount, invoice_payload, shipping_option_id, order_info):
        """
        This object contains information about an incoming pre-checkout query
        """
        self.uid = uid
        self.from_user = from_user
        self.currency = currency
        self.total_amount = total_amount
        self.invoice_payload = invoice_payload
        self.shipping_option_id = shipping_option_id
        self.order_info = order_info

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        uid = obj['id']
        from_user = User.de_json(obj['from'])
        currency = obj['currency']
        total_amount = obj['total_amount']
        invoice_payload = obj['invoice_payload']
        shipping_option_id = None
        if 'shipping_option_id' in obj:
            shipping_option_id = obj['shipping_option_id']
        order_info = None
        if 'order_info' in obj:
            order_info = OrderInfo.de_json(obj['order_info'])
        return cls(uid, from_user, currency, total_amount, invoice_payload, shipping_option_id, order_info)


class PassportData(JsonDeserializable):
    def __init__(self, data, credentials):
        """
        Contains information about Telegram Passport data shared with the bot by the user
        """
        self.data = data
        self.credentials = credentials

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        data = obj['EncryptedPassportElement']
        credentials = obj['EncryptedCredentials']
        return cls(data, credentials)


class PassportFile(JsonDeserializable):
    def __init__(self, file_id, file_unique_id, file_size, file_date):
        """
        This object represents a file uploaded to Telegram Passport
        """
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.file_size = file_size
        self.file_date = file_date

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        file_id = obj['file_id']
        file_unique_id = obj['file_unique_id']
        file_size = obj['file_size']
        file_date = obj['file_date']
        return cls(file_id, file_unique_id, file_size, file_date)


class EncryptedPassportElement(JsonDeserializable):
    def __init__(self, ttype, data, phone_number, files, front_side, reverse_side, selfie, translation, hashes):
        """
        Contains information about documents or other Telegram Passport elements shared with the bot by the user
        """
        self.ttype = ttype
        self.data = data
        self.phone_number = phone_number
        self.files = files
        self.front_side = front_side
        self.reverse_side = reverse_side
        self.selfie = selfie
        self.translation = translation
        self.hashes = hashes

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        ttype = obj['type']
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
        hashes = obj['hash']
        return cls(ttype, data, phone_number, files, front_side, reverse_side, selfie, translation, hashes)

    @classmethod
    def parse_files(cls, obj):
        files = []
        for x in obj:
            file = PassportFile.de_json(x)
            files.append(file)
        return files

    @classmethod
    def parse_translation(cls, obj):
        translations = []
        for x in obj:
            translation = PassportFile.de_json(x)
            translations.append(translation)
        return translations


class EncryptedCredentials(JsonDeserializable):
    def __init__(self, data, hashes, secret):
        """
        Contains data required for decrypting and authenticating EncryptedPassportElement.
        See the Telegram Passport Documentation for a complete description of the data decryption and
        authentication processes.
        """
        self.data = data
        self.hashes = hashes
        self.secret = secret

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        data = obj['data']
        hashes = obj['hash']
        secret = obj['secret']
        return cls(data, hashes, secret)


class PassportElementError(JsonDeserializable):
    """
    This object represents an error in the Telegram Passport element
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

    def __init__(self):
        self.DataField = self.__PassportElementErrorDataField
        self.FrontSide = self.__PassportElementErrorFrontSide
        self.ReverseSide = self.__PassportElementErrorReverseSide
        self.Selfie = self.__PassportElementErrorSelfie
        self.File = self.__PassportElementErrorFile
        self.Files = self.__PassportElementErrorFiles
        self.TranslationFile = self.__PassportElementErrorFile
        self.TranslationFiles = self.__PassportElementErrorFiles
        self.Unspecified = self.__PassportElementErrorUnspecified

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        source = None
        if 'source' in obj:
            source = obj['source']

        if source == 'data':
            return cls.__PassportElementErrorDataField.de_json(obj_type)
        elif source == 'front_side':
            return cls.__PassportElementErrorFrontSide.de_json(obj_type)
        elif source == 'reverse_side':
            return cls.__PassportElementErrorReverseSide.de_json(obj_type)
        elif source == 'selfie':
            return cls.__PassportElementErrorSelfie.de_json(obj_type)
        elif source == 'file_hash':
            return cls.__PassportElementErrorFile.de_json(obj_type)
        elif source == 'file_hashes':
            return cls.__PassportElementErrorFiles.de_json(obj_type)
        elif source == 'translation_files':
            return cls.__PassportElementErrorTranslationFile.de_json(obj_type)
        elif source == 'translation_files':
            return cls.__PassportElementErrorTranslationFiles.de_json(obj_type)
        elif source == 'unspecified':
            return cls.__PassportElementErrorUnspecified.de_json(obj_type)
        else:
            return None

    class __PassportElementErrorDataField(JsonDeserializable):
        def __init__(self, source, ttype, field_name, data_hash, message):
            """
            Represents an issue in one of the data fields that was provided by the user
            """
            self.source = source
            self.ttype = ttype
            self.field_name = field_name
            self.data_hash = data_hash
            self.message = message

        @classmethod
        def de_json(cls, obj_type):
            obj = cls.check_type(obj_type)
            source = obj['source']  # Error source, must be data
            ttype = obj['type']
            field_name = obj['field_name']
            data_hash = obj['data_hash']
            message = obj['message']
            return cls(source, ttype, field_name, data_hash, message)

    class __PassportElementErrorFrontSide(JsonDeserializable):
        def __init__(self, source, ttype, file_hash, message):
            """
            Represents an issue with the front side of a document
            """
            self.source = source
            self.ttype = ttype
            self.file_hash = file_hash
            self.message = message

        @classmethod
        def de_json(cls, obj_type):
            obj = cls.check_type(obj_type)
            source = obj['source']  # Error source, must be front_side
            ttype = obj['type']
            file_hash = obj['file_hash']
            message = obj['message']
            return cls(source, ttype, file_hash, message)

    class __PassportElementErrorFile(JsonDeserializable):
        def __init__(self, source, ttype, file_hash, message):
            """
            Represents an issue with a document scan
            """
            self.source = source
            self.ttype = ttype
            self.file_hash = file_hash
            self.message = message

        @classmethod
        def de_json(cls, obj_type):
            obj = cls.check_type(obj_type)
            source = obj['source']  # Error source, must be filed
            ttype = obj['type']
            file_hash = obj['file_hash']
            message = obj['message']
            return cls(source, ttype, file_hash, message)

    class __PassportElementErrorFiles(JsonDeserializable):
        def __init__(self, source, ttype, file_hashes, message):
            """
            Represents an issue with a list of scans
            """
            self.source = source
            self.ttype = ttype
            self.file_hashes = file_hashes
            self.message = message

        @classmethod
        def de_json(cls, obj_type):
            obj = cls.check_type(obj_type)
            source = obj['source']  # Error source, must be files
            ttype = obj['type']
            file_hashes = obj['file_hashes']
            message = obj['message']
            return cls(source, ttype, file_hashes, message)

    class __PassportElementErrorReverseSide(JsonDeserializable):
        def __init__(self, source, ttype, file_hash, message):
            """
            Represents an issue with the reverse side of a document
            """
            self.source = source
            self.ttype = ttype
            self.file_hash = file_hash
            self.message = message

        @classmethod
        def de_json(cls, obj_type):
            obj = cls.check_type(obj_type)
            source = obj['source']  # Error source, must be reverse_side
            ttype = obj['type']
            file_hash = obj['file_hash']
            message = obj['message']
            return cls(source, ttype, file_hash, message)

    class __PassportElementErrorSelfie(JsonDeserializable):
        def __init__(self, source, ttype, file_hash, message):
            """
            Represents an issue with the selfie with a document
            """
            self.source = source
            self.ttype = ttype
            self.file_hash = file_hash
            self.message = message

        @classmethod
        def de_json(cls, obj_type):
            obj = cls.check_type(obj_type)
            source = obj['source']  # Error source, must be selfie
            ttype = obj['type']
            file_hash = obj['file_hash']
            message = obj['message']
            return cls(source, ttype, file_hash, message)

    class __PassportElementErrorTranslationFile(JsonDeserializable):
        def __init__(self, source, ttype, file_hash, message):
            """
            Represents an issue with one of the files that constitute the translation of a document
            """
            self.source = source
            self.ttype = ttype
            self.file_hash = file_hash
            self.message = message

        @classmethod
        def de_json(cls, obj_type):
            obj = cls.check_type(obj_type)
            source = obj['source']  # Error source, must be translation_file
            ttype = obj['type']
            file_hash = obj['file_hash']
            message = obj['message']
            return cls(source, ttype, file_hash, message)

    class __PassportElementErrorTranslationFiles(JsonDeserializable):
        def __init__(self, source, ttype, file_hashes, message):
            """
            Represents an issue with the translated version of a document
            """
            self.source = source
            self.ttype = ttype
            self.file_hashes = file_hashes
            self.message = message

        @classmethod
        def de_json(cls, obj_type):
            obj = cls.check_type(obj_type)
            source = obj['source']  # Error source, must be translation_files
            ttype = obj['type']
            file_hashes = obj['file_hashes']
            message = obj['message']
            return cls(source, ttype, file_hashes, message)

    class __PassportElementErrorUnspecified(JsonDeserializable):
        def __init__(self, source, ttype, element_hash, message):
            """
            Represents an issue in an unspecified place
            """
            self.source = source
            self.ttype = ttype
            self.element_hash = element_hash
            self.message = message

        @classmethod
        def de_json(cls, obj_type):
            obj = cls.check_type(obj_type)
            source = obj['source']  # Error source, must be unspecified
            ttype = obj['type']
            element_hash = obj['element_hash']
            message = obj['message']
            return cls(source, ttype, element_hash, message)


class Game(JsonDeserializable):
    def __init__(self, title, description, photo, text, text_entities, animation):
        """
        This object represents a game
        """
        self.title = title
        self.description = description
        self.photo = photo
        self.text = text
        self.text_entities = text_entities
        self.animation = animation

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
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
    def parse_photo(cls, obj):
        photos = []
        for x in obj:
            photos.append(PhotoSize.de_json(x))
        return photos

    @classmethod
    def parse_entities(cls, obj):
        entities = []
        for x in obj:
            entities.append(MessageEntity.de_json(x))
        return entities


class CallbackGame:
    """
    A placeholder, currently holds no information
    """
    pass


class GameHighScore(JsonDeserializable):
    def __init__(self, position, user, score):
        """
        This object represents one row of the high scores' table for a game
        """
        self.position = position
        self.user = user
        self.score = score

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        position = obj['position']
        user = User.de_json(obj['user'])
        score = obj['score']
        return cls(position, user, score)
