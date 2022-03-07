from .utils import *
import json

""" 
    Telegram Available types
    All types used in the Bot API responses are represented as JSON-objects.
"""


class Update(JsonDeserializable):
    """ 
    This object represents an incoming update
    """

    def __init__(self, update_id, message, edited_message, channel_post, edited_channel_post, inline_query,
                 chosen_inline_result, callback_query, shipping_query, pre_checkout_query, poll, poll_answer,
                 my_chat_member, chat_member):
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
            pre_checkout_query = PreCheckoutQuery.de_json(
                obj['pre_checkout_query'])
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
        return cls(update_id, message, edited_message, channel_post, edited_channel_post, inline_query,
                   chosen_inline_result, callback_query, shipping_query, pre_checkout_query, poll, poll_answer,
                   my_chat_member, chat_member)


class WebhookInfo(JsonDeserializable):
    """
    Contains information about the current status of a webhook
    """

    def __init__(self, url, has_custom_certificate, pending_update_count, ip_address, last_error_date,
                 last_error_message, max_connections, allowed_updates):
        self.url = url
        self.has_custom_certificate = has_custom_certificate
        self.pending_update_count = pending_update_count
        self.ip_address = ip_address
        self.last_error_date = last_error_date
        self.last_error_message = last_error_message
        self.max_connections = max_connections
        self.allowed_updates = allowed_updates

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        url = obj['url']
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
        max_connections = None
        if 'max_connections' in obj:
            max_connections = obj['max_connections']
        allowed_updates = None
        if 'allowed_updates' in obj:
            allowed_updates = obj['allowed_updates']
        return cls(url, has_custom_certificate, pending_update_count, ip_address, last_error_date, last_error_message,
                   max_connections, allowed_updates)


class User(JsonDeserializable):
    """
    This object represents a Telegram user or bot
    """

    def __init__(self, uid, is_bot, first_name, last_name, username, language_code, can_join_groups,
                 can_read_all_group_messages, supports_inline_queries):

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
        can_join_groups = None
        if 'can_join_groups' in obj:
            can_join_groups = obj['can_join_groups']
        can_read_all_group_messages = None
        if 'can_read_all_group_messages' in obj:
            can_read_all_group_messages = obj['can_read_all_group_messages']
        supports_inline_queries = None
        if 'supports_inline_queries' in obj:
            supports_inline_queries = obj['supports_inline_queries']
        return cls(uid, is_bot, first_name, last_name, username, language_code, can_join_groups,
                   can_read_all_group_messages, supports_inline_queries)


class Chat(JsonDeserializable):
    """
    This object represents a chat
    """

    def __init__(self, uid, ttype, title, username, first_name, last_name, photo, bio, has_private_forwards,
                 description, invite_link, pinned_message, permissions, slow_mode_delay, message_auto_delete_time,
                 has_protected_content, sticker_set_name, can_set_sticker_set, linked_chat_id, location):

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
        has_private_forwards = None
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
        has_protected_content = None
        if 'has_protected_content' in obj:
            has_protected_content = obj['has_protected_content']
        sticker_set_name = None
        if 'sticker_set_name' in obj:
            sticker_set_name = obj['sticker_set_name']
        can_set_sticker_set = None
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
    """This object represents a message"""

    def __init__(self, message_id, from_user, sender_chat, date, chat, options):
        self.message_id = message_id
        self.from_user = from_user
        self.sender_chat = sender_chat
        self.date = date
        self.chat = chat
        self.forward_from_chat = None
        self.forward_from_message_id = None
        self.forward_from = None
        self.forward_date = None
        self.reply_to_message = None
        self.via_bot = None
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
        self.message_auto_delete_timer_changed = None
        self.migrate_to_chat_id = None
        self.migrate_from_chat_id = None
        self.pinned_message = None
        self.invoice = None
        self.successful_payment = None
        self.connected_website = None
        self.proximity_alert_triggered = None
        self.voice_chat_scheduled = None
        self.voice_chat_started = None
        self.voice_chat_ended = None
        self.voice_chat_participants_invited = None
        self.reply_markup = None
        for key in options:
            setattr(self, key, options[key])

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        message_id = obj['message_id']
        from_user = None
        if 'from' in obj:
            from_user = User.de_json(obj['from'])
        sender_chat = None
        if 'sender_chat' in obj:
            sender_chat = Chat.de_json(obj['sender_chat'])
        date = obj['date']
        chat = Chat.de_json(obj['chat'])
        opts = {}
        if 'forward_from' in obj:
            opts['forward_from'] = User.de_json(obj['forward_from'])
        if 'forward_from_chat' in obj:
            opts['forward_from_chat'] = Chat.de_json(obj['forward_from_chat'])
        if 'forward_from_message_id' in obj:
            opts['forward_from_message_id'] = obj['forward_from_message_id']
        if 'forward_sender_name' in obj:
            opts['forward_sender_name'] = obj['forward_sender_name']
        if 'forward_signature' in obj:
            opts['forward_signature'] = obj['forward_signature']
        if 'forward_date' in obj:
            opts['forward_date'] = obj['forward_date']
        if 'reply_to_message' in obj:
            opts['reply_to_message'] = Message.de_json(obj['reply_to_message'])
        if 'via_bot' in obj:
            opts['via_bot'] = User.de_json(obj['via_bot'])
        if 'edit_date' in obj:
            opts['edit_date'] = obj['edit_date']
        if 'media_group_id' in obj:
            opts['media_group_id'] = obj['media_group_id']
        if 'author_signature' in obj:
            opts['author_signature'] = obj['author_signature']
        if 'text' in obj:
            opts['text'] = obj['text']
        if 'entities' in obj:
            opts['entities'] = Message.parse_entities(obj['entities'])
        if 'caption_entities' in obj:
            opts['caption_entities'] = Message.parse_entities(
                obj['caption_entities'])
        if 'audio' in obj:
            opts['audio'] = Audio.de_json(obj['audio'])
        if 'document' in obj:
            opts['document'] = Document.de_json(obj['document'])
        if 'animation' in obj:
            opts['animation'] = Animation.de_json(obj['animation'])
        if 'game' in obj:
            opts['game'] = Game.de_json(obj['game'])
        if 'photo' in obj:
            opts['photo'] = Message.parse_photo(obj['photo'])
        if 'sticker' in obj:
            opts['sticker'] = Sticker.de_json(obj['sticker'])
        if 'video' in obj:
            opts['video'] = Video.de_json(obj['video'])
        if 'voice' in obj:
            opts['voice'] = Audio.de_json(obj['voice'])
        if 'video_note' in obj:
            opts['video_note'] = VideoNote.de_json(obj['video_note'])
        if 'caption' in obj:
            opts['caption'] = obj['caption']
        if 'contact' in obj:
            opts['contact'] = Contact.de_json(json.dumps(obj['contact']))
        if 'location' in obj:
            opts['location'] = Location.de_json(obj['location'])
        if 'venue' in obj:
            opts['venue'] = Venue.de_json(obj['venue'])
        if 'poll' in obj:
            opts['poll'] = Poll.de_json(obj['poll'])
        if 'dice' in obj:
            opts['dice'] = Dice.de_json(obj['dice'])
        if 'new_chat_members' in obj:
            opts['new_chat_members'] = Message.parse_users(obj['new_chat_members'])
        if 'left_chat_member' in obj:
            opts['left_chat_member'] = User.de_json(obj['left_chat_member'])
        if 'new_chat_title' in obj:
            opts['new_chat_title'] = obj['new_chat_title']
        if 'new_chat_photo' in obj:
            opts['new_chat_photo'] = Message.parse_photo(obj['new_chat_photo'])
        if 'delete_chat_photo' in obj:
            opts['delete_chat_photo'] = obj['delete_chat_photo']
        if 'group_chat_created' in obj:
            opts['group_chat_created'] = obj['group_chat_created']
        if 'supergroup_chat_created' in obj:
            opts['supergroup_chat_created'] = obj['supergroup_chat_created']
        if 'channel_chat_created' in obj:
            opts['channel_chat_created'] = obj['channel_chat_created']
        if 'message_auto_delete_timer_changed' in obj:
            opts['message_auto_delete_timer_changed'] = MessageAutoDeleteTimerChanged.de_json(
                obj['message_auto_delete_timer_changed'])
        if 'migrate_to_chat_id' in obj:
            opts['migrate_to_chat_id'] = obj['migrate_to_chat_id']
        if 'migrate_from_chat_id' in obj:
            opts['migrate_from_chat_id'] = obj['migrate_from_chat_id']
        if 'pinned_message' in obj:
            opts['pinned_message'] = Message.de_json(obj['pinned_message'])
        if 'invoice' in obj:
            opts['invoice'] = Invoice.de_json(obj['invoice'])
        if 'successful_payment' in obj:
            opts['successful_payment'] = SuccessfulPayment.de_json(obj['successful_payment'])
        if 'connected_website' in obj:
            opts['connected_website'] = obj['connected_website']
        if 'passport_data' in obj:
            opts['passport_data'] = obj['passport_data']
        if 'proximity_alert_triggered' in obj:
            opts['proximity_alert_triggered'] = ProximityAlertTriggered.de_json(
                obj['proximity_alert_triggered'])
        if 'voice_chat_scheduled' in obj:
            opts['voice_chat_scheduled'] = VoiceChatScheduled.de_json(obj['voice_chat_scheduled'])
        if 'voice_chat_started' in obj:
            opts['voice_chat_started'] = VoiceChatStarted.de_json(obj['voice_chat_started'])
        if 'voice_chat_ended' in obj:
            opts['voice_chat_ended'] = VoiceChatEnded.de_json(obj['voice_chat_ended'])
        if 'voice_chat_participants_invited' in obj:
            opts['voice_chat_participants_invited'] = VoiceChatParticipantsInvited.de_json(
                obj['voice_chat_participants_invited'])
        if 'reply_markup' in obj:
            opts['reply_markup'] = InlineKeyboardMarkup(obj['reply_markup'])
        return cls(message_id, from_user, sender_chat, date, chat, opts)

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


class MessageEntity(JsonDeserializable):
    """
    This object represents one special entity in a text message. For example, hashtags, usernames, URLs, etc
    """

    def __init__(self, ttype, offset, length, url=None, user=None, language=None):
        self.ttype = ttype
        self.offset = offset
        self.length = length
        self.url = url
        self.user = user
        self.language = language

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
    """
    This object represents one size of a photo or a file / sticker thumbnail
    """

    def __init__(self, file_id, file_unique_id, width, height, file_size=None):
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
        file_size = obj['file_size']
        return cls(file_id, file_unique_id, width, height, file_size)


class Audio(JsonDeserializable):
    """
    This object represents an audio file to be treated as music by the Telegram clients
    """

    def __init__(self, file_id, file_unique_id, duration, performer, title, file_name, mime_type, file_size, thumb):
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
    """
    This object represents a general file
    """

    def __init__(self, file_id, file_unique_id, thumb=None, file_name=None, mime_type=None, file_size=None):
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
        if 'thumb' in obj and 'file_id' in obj['thumb']:
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
    """
    This object represents a video file
    """

    def __init__(self, file_id, file_unique_id, width, height, duration, thumb, file_name, mime_type, file_size):
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


class Animation(JsonDeserializable):
    """
    This object represents an animation file (GIF or H.264/MPEG-4 AVC video without sound)
    """

    def __init__(self, file_id, file_unique_id, width, height, duration, thumb, file_name, mime_type, file_size):
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


class Voice(JsonDeserializable):
    """
    This object represents a voice note
    """

    def __init__(self, file_id, file_unique_id, duration, mime_type=None, file_size=None):
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


class VideoNote(JsonDeserializable):
    """
    This object represents a video message
    """

    def __init__(self, file_id, file_unique_id, length, duration, thumb=None, file_size=None):
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


class Contact(JsonDeserializable):
    """
    This object represents a phone contact
    """

    def __init__(self, phone_number, first_name, last_name=None, user_id=None, vcard=None):
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


class Location(JsonDeserializable):
    """
    This object represents a point on the map
    """

    def __init__(self, longitude, latitude, horizontal_accuracy, live_period, heading, proximity_alert_radius):
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
    """
    This object represents a venue
    """

    def __init__(self, location, title, address, foursquare_id, foursquare_type, google_place_id, google_place_type):
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


class ProximityAlertTriggered(JsonDeserializable):
    """
    This object represents the content of a service message,
    sent whenever a user in the chat triggers a proximity alert set by another user
    """

    def __init__(self, traveler, watcher, distance):
        self.traveler = traveler
        self.watcher = watcher
        self.distance = distance

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        traveler = User.de_json(obj['tarveler'])
        watcher = User.de_json(obj['watcher'])
        distance = obj['distance']
        return cls(traveler, watcher, distance)


class PollOption(JsonDeserializable):
    """
    This object contains information about one answer option in a poll
    """

    def __init__(self, text, voter_count):
        self.text = text
        self.voter_count = voter_count

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        text = obj['text']
        voter_count = obj['voter_count']
        return cls(text, voter_count)


class PollAnswer(JsonDeserializable):
    """
    This object represents an answer of a user in a non-anonymous poll
    """

    def __init__(self, poll_id, user, option_ids):
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
    """
    This object contains information about a poll
    """

    def __init__(self, uid, question, options, total_voter_count, is_closed, is_anonymous, ttype,
                 allows_multiple_answers, correct_option_id, explanation, explanation_entities, open_period,
                 close_date):
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
        allows_multiple_answers = obj['allows_multiple_answers']
        correct_option_id = None
        if 'correct_option_id' in obj:
            correct_option_id = obj['correct_option_id']
        explanation = None
        if 'explanation' in obj:
            explanation = obj['explanation']
        explanation_entities = None
        if 'explanation_entities' in obj:
            explanation_entities = Poll.parse_explanation_entities(
                obj['explanation_entities'])
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


class Dice(JsonDeserializable):
    """
    This object represents a dice with random value
    """

    def __init__(self, value, emoji):
        self.value = value
        self.emoji = emoji

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        emoji = obj['emoji']
        value = obj['value']
        return cls(emoji, value)


class MessageAutoDeleteTimerChanged(JsonDeserializable):
    """
    This object represents a service message about a change in auto-delete timer settings
    """

    def __init__(self, message_auto_delete_time):
        self.message_auto_delete_time = message_auto_delete_time

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        message_auto_delete_time = obj['message_auto_delete_time']
        return cls(message_auto_delete_time)


class VoiceChatScheduled(JsonDeserializable):
    """
    This object represents a service message about a voice chat scheduled in the chat
    """

    def __init__(self, start_date):
        self.start_date = start_date

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        start_date = obj['start_date']
        return cls(start_date)


class VoiceChatStarted(JsonDeserializable):
    """
    This object represents a service message about a voice chat started in the chat
    """

    def __init__(self, field):
        self.field = field

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        field = None
        if obj:
            field = obj
        return cls(field)


class VoiceChatEnded(JsonDeserializable):
    """
    This object represents a service message about a voice chat ended in the chat
    """

    def __init__(self, duration):
        self.duration = duration

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        duration = obj['duration']
        return cls(duration)


class VoiceChatParticipantsInvited(JsonDeserializable):
    """
    This object represents a service message about new members invited to a voice chat
    """

    def __init__(self, users):
        self.users = users

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        users = None
        if 'users' in obj:
            users = VoiceChatParticipantsInvited.parse_users(obj['users'])
        return cls(users)

    @classmethod
    def parse_users(cls, obj):
        users = []
        for x in obj:
            users.append(User.de_json(x))
        return users


class UserProfilePhotos(JsonDeserializable):
    """
    This object represents one size of a photo or a file / sticker thumbnail
    """

    def __init__(self, total_count, photos):
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
    """ 
    This object represents a file ready to be downloaded.
    """

    def __init__(self, file_id, file_unique_id, file_size, file_path):
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


class ReplyKeyboardMarkup(JsonSerializable):
    """
    This object represents a custom keyboard with reply options (see Introduction to bots for details and examples)
    """

    def __init__(self, resize_keyboard=None, one_time_keyboard=None, selective=None, row_width=3):
        self.keyboard = []
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard
        self.selective = selective
        self.row_width = row_width

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
                row.append(button.to_dict())
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
                btn_array.append(button.to_dict())
        self.keyboard.append(btn_array)
        return self

    def to_dict(self):
        """
        Converts this object to its json representation following the Telegram API guidelines described here:
        https://core.telegram.org/bots/api#replykeyboardmarkup
        :return:
        """
        obj = {'keyboard': self.keyboard}
        if self.one_time_keyboard:
            obj['one_time_keyboard'] = True
        if self.resize_keyboard:
            obj['resize_keyboard'] = True
        if self.selective:
            obj['selective'] = True
        return obj

    def to_json(self):
        return json.dumps(self.to_dict())


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

    def to_dict(self):
        obj = {'text': self.text}
        if self.request_contact:
            obj['request_contact'] = self.request_contact
        if self.request_location:
            obj['request_location'] = self.request_location
        if self.request_poll:
            obj['request_poll'] = KeyboardButtonPollType(
                self.request_poll)
        return obj

    def to_json(self):
        return json.dumps(self.to_dict())


class KeyboardButtonPollType(JsonDeserializable):
    """
    This object represents ttype of poll,
    which is allowed to be created and sent when the corresponding button is pressed
    """

    def __init__(self, ttype):
        self.ttype = ttype

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        ttype = obj['type']
        return cls(ttype)


class ReplyKeyboardRemove(JsonSerializable):
    """ 
    Upon receiving a message with this object, 
    Telegram clients will remove the current custom keyboard and display the default letter-keyboard,
    By default, custom keyboards are displayed until a new keyboard is sent by a bot,
    An exception is made for one-time keyboards that are hidden immediately after the user presses a button
    (see ReplyKeyboardMarkup).
    """

    def __init__(self, selective=None):
        self.selective = selective

    def to_json(self):
        obj = {'remove_keyboard': True}
        if self.selective:
            obj['selective'] = True
        return json.dumps(obj)


class InlineKeyboardMarkup(Dictionaryable, JsonSerializable):
    """
    This object represents an inline keyboard that appears right next to the message it belongs to
    """

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
            row.append(button.to_dict())
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
            btn_array.append(button.to_dict())
        self.keyboard.append(btn_array)
        return self

    def to_json(self):
        """
        Converts this object to its json representation following the Telegram API guidelines described here:
        https://core.telegram.org/bots/api#inlinekeyboardmarkup
        :return:
        """
        obj = {'inline_keyboard': self.keyboard}
        return json.dumps(obj)

    def to_dict(self):
        obj = {'inline_keyboard': self.keyboard}
        return obj


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

    def to_dict(self):
        obj = {'text': self.text}
        if self.url:
            obj['url'] = self.url
        if self.callback_data:
            obj['callback_data'] = self.callback_data
        if self.switch_inline_query is not None:
            obj['switch_inline_query'] = self.switch_inline_query
        if self.switch_inline_query_current_chat is not None:
            obj['switch_inline_query_current_chat'] = self.switch_inline_query_current_chat
        if self.callback_game is not None:
            obj['callback_game'] = self.callback_game
        if self.pay is not None:
            obj['pay'] = self.pay
        if self.login_url is not None:
            obj['login_url'] = self.login_url
        return obj

    def to_json(self):
        return json.dumps(self.to_dict())


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

    def to_dict(self):
        obj = {'url': self.url}
        if self.forward_text:
            obj['forward_text'] = self.forward_text
        if self.bot_username:
            obj['bot_username'] = self.bot_username
        if self.request_write_access:
            obj['request_write_access'] = self.request_write_access
        return obj

    def to_json(self):
        return json.dumps(self.to_dict())


class CallbackQuery(JsonDeserializable):
    """
    This object represents an incoming callback query from a callback button in an inline keyboard
    """

    def __init__(self, uid, from_user, data, chat_instance, message=None, inline_message_id=None, game_short_name=None):
        self.game_short_name = game_short_name
        self.chat_instance = chat_instance
        self.uid = uid
        self.from_user = from_user
        self.message = message
        self.data = data
        self.inline_message_id = inline_message_id

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
        obj = {'force_reply': True}
        if self.selective:
            obj['selective'] = True
        return json.dumps(obj)


class ChatPhoto(JsonDeserializable):
    """
    This object represents a chat photo
    """

    def __init__(self, small_file_id, small_file_unique_id, big_file_id, big_file_unique_id):
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
    """
    Represents an invitation link for a chat
    """

    def __init__(self, invite_link, creator, creates_join_request, is_primary, is_revoked, name, expire_date,
                 member_limit, pending_join_request_count):
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
        creates_join_request = obj['creates_join_request']
        is_primary = obj['is_primary']
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


class ChatMember(JsonDeserializable):
    """
    This object contains information about one member of a chat
    """

    def __init__(self, status, user, is_anonymous, can_manage_chat, custom_title, until_date, can_be_edited,
                 can_change_info, can_post_messages, can_edit_messages, can_delete_messages, can_manage_voice_chats,
                 can_invite_users, can_restrict_members, is_member, can_pin_messages, can_promote_members,
                 can_send_messages, can_send_media_messages, can_send_polls, can_send_other_messages,
                 can_add_web_page_previews):

        self.status = status
        self.user = user
        self.is_anonymous = is_anonymous
        self.can_manage_chat = can_manage_chat
        self.custom_title = custom_title
        self.until_date = until_date
        self.can_be_edited = can_be_edited
        self.can_change_info = can_change_info
        self.can_post_messages = can_post_messages
        self.can_edit_messages = can_edit_messages
        self.can_delete_messages = can_delete_messages
        self.can_manage_voice_chats = can_manage_voice_chats
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

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        status = obj['status']
        user = User.de_json(obj['user'])
        is_anonymous = None
        if 'is_anonymous' in obj:
            is_anonymous = obj['is_anonymous']
        can_manage_chat = None
        if 'can_manage_chat' in obj:
            can_manage_chat = obj['can_manage_chat']
        custom_title = None
        if 'custom_title' in obj:
            custom_title = obj['custom_title']
        until_date = None
        if 'until_date' in obj:
            until_date = obj['until_date']
        can_be_edited = None
        if 'can_be_edited' in obj:
            can_be_edited = obj['can_be_edited']
        can_post_messages = None
        if 'can_post_messages' in obj:
            can_post_messages = obj['can_post_messages']
        can_edit_messages = None
        if 'can_edit_messages' in obj:
            can_edit_messages = obj['can_edit_messages']
        can_delete_messages = None
        if 'can_delete_messages' in obj:
            can_delete_messages = obj['can_delete_messages']
        can_manage_voice_chats = None
        if 'can_manage_voice_chats' in obj:
            can_manage_voice_chats = obj['can_manage_voice_chats']
        can_restrict_members = None
        if 'can_restrict_members' in obj:
            can_restrict_members = obj['can_restrict_members']
        can_promote_members = None
        if 'can_promote_members' in obj:
            can_promote_members = obj['can_promote_members']
        can_change_info = None
        if 'can_change_info' in obj:
            can_change_info = obj['can_change_info']
        can_invite_users = None
        if 'can_invite_users' in obj:
            can_invite_users = obj['can_invite_users']
        can_pin_messages = None
        if 'can_pin_messages' in obj:
            can_pin_messages = obj['can_pin_messages']
        is_member = None
        if 'is_member' in obj:
            is_member = obj['is_member']
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
            can_send_other_messages = obj['can_send_other_messages']
        can_add_web_page_previews = None
        if 'can_add_web_page_previews' in obj:
            can_add_web_page_previews = obj['can_add_web_page_previews']
        return cls(status, user, is_anonymous, can_manage_chat, custom_title, until_date, can_be_edited,
                   can_change_info, can_post_messages, can_edit_messages, can_delete_messages, can_manage_voice_chats,
                   can_invite_users, can_restrict_members, is_member, can_pin_messages, can_promote_members,
                   can_send_messages, can_send_media_messages, can_send_other_messages, can_add_web_page_previews,
                   can_send_polls)


class ChatMemberUpdated(JsonDeserializable):
    """
    This object represents changes in the status of a chat member
    """

    def __init__(self, chat, from_user, date, old_chat_member, new_chat_member, invite_link):
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


class ChatPermissions(JsonDeserializable):
    """
    Describes actions that a non-administrator user is allowed to take in a chat
    """

    def __init__(self, can_send_messages=None, can_send_media_messages=None, can_send_polls=None,
                 can_send_other_messages=None, can_add_web_page_previews=None, can_change_info=None,
                 can_invite_users=None, can_pin_messages=None):
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
            can_send_other_messages = obj['can_send_other_messages']
        can_add_web_page_previews = None
        if 'can_add_web_page_previews' in obj:
            can_add_web_page_previews = obj['can_add_web_page_previews']
        can_change_info = None
        if 'can_change_info' in obj:
            can_change_info = obj['can_change_info']
        can_invite_users = None
        if 'can_invite_users' in obj:
            can_invite_users = obj['can_invite_users']
        can_pin_messages = None
        if 'can_pin_messages' in obj:
            can_pin_messages = obj['can_pin_messages']
        return cls(can_send_messages, can_send_media_messages, can_send_polls, can_send_other_messages,
                   can_add_web_page_previews, can_change_info, can_invite_users, can_pin_messages)


class ChatLocation(JsonDeserializable):
    """
    Represents a location to which a chat is connected
    """

    def __init__(self, location, address):
        self.location = location
        self.address = address

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        location = Location.de_json(obj['location'])
        address = obj['address']
        return cls(location, address)


class BotCommand(JsonDeserializable):
    """
    This object represents a bot command
    """

    def __init__(self, command, description):
        self.command = command
        self.description = description

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        command = obj['command']
        description = obj['description']
        return cls(command, description)


class ResponseParameters(JsonDeserializable):
    """
    Contains information about why a request was unsuccessful
    """

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

    def __init__(self, migrate_to_chat_id, retry_after):
        self.migrate_to_chat_id = migrate_to_chat_id
        self.retry_after = retry_after


class InputMedia:
    """ 
    This object represents the content of a media message to be sent,
    It should be one of:
        InputMediaPhoto
        InputMediaVideo
        InputMediaAnimation
        InputMediaAudio
        InputMediaDocument
    """

    def __init__(self):
        self.Photo = self.__InputMediaPhoto
        self.Video = self.__InputMediaVideo
        self.Animation = self.__InputMediaAnimation
        self.Audio = self.__InputMediaAudio
        self.Document = self.__InputMediaDocument

    class __InputMediaPhoto(JsonSerializable):
        def __init__(self, ttype, media, caption=None, parse_mode=None, caption_entities=None):
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

        def to_json(self):
            return json.dumps(self.to_dict())

    class __InputMediaVideo(JsonSerializable):
        def __init__(self, ttype, media, thumb=None, caption=None, parse_mode=None, caption_entities=None, width=None,
                     height=None, duration=None, supports_streaming=False):
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
            obj['supports_streaming'] = self.supports_streaming
            return obj

        def to_json(self):
            return json.dumps(self.to_dict())

    class __InputMediaAnimation(JsonSerializable):
        def __init__(self, ttype, media, thumb=None, caption=None, parse_mode=None, caption_entities=None, width=None,
                     height=None, duration=None):
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

        def to_json(self):
            return json.dumps(self.to_dict())

    class __InputMediaAudio(JsonSerializable):
        def __init__(self, ttype, media, thumb=None, caption=None, parse_mode=None, caption_entities=None, width=None,
                     height=None, duration=None, performer=None, title=None):
            self.ttype = ttype
            self.media = media
            self.thumb = thumb
            self.caption = caption
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities
            self.width = width
            self.height = height
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
            if self.width:
                obj['width'] = self.width
            if self.height:
                obj['height'] = self.height
            if self.duration:
                obj['duration'] = self.duration
            if self.performer:
                obj['performer'] = self.performer
            if self.title:
                obj['title'] = self.title
            return obj

        def to_json(self):
            return json.dumps(self.to_dict())

    class __InputMediaDocument(JsonSerializable):
        def __init__(self, ttype, media, thumb=None, caption=None, parse_mode=None, caption_entities=None,
                     disable_content_type_detection=True):
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

        def to_json(self):
            return json.dumps(self.to_dict())


# InputFile
""" This object represents the contents of a file to be uploaded. 
    Must be posted using multipart/form-data in the usual way that files are uploaded via the browser.
"""


class Sticker(JsonDeserializable):
    """
    This object represents a sticker
    """

    def __init__(self, file_id, file_unique_id, width, height, thumb, emoji, set_name, mask_position, file_size,
                 is_animated):
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

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
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
        return cls(file_id, file_unique_id, width, height, thumb, emoji, set_name, mask_position, file_size,
                   is_animated)


class StickerSet(JsonDeserializable):
    """
    This object represents a sticker set
    """

    def __init__(self, name, title, contains_masks, stickers, thumb):
        self.name = name
        self.title = title
        self.contains_masks = contains_masks
        self.stickers = stickers
        self.thumb = thumb

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        name = obj['name']
        title = obj['title']
        contains_masks = obj['contains_masks']
        stickers = StickerSet.parse_stickers(obj['stickers'])
        thumb = PhotoSize.de_json(obj['thumb'])
        return cls(name, title, contains_masks, stickers, thumb)

    @classmethod
    def parse_stickers(cls, obj):
        stickers = []
        for sticker in obj:
            stickers.append(Sticker.de_json(sticker))
        return stickers


class MaskPosition(JsonDeserializable, JsonSerializable):
    """
    This object describes the position on faces where a mask should be placed by default
    """

    def __init__(self, point, x_shift, y_shift, scale):
        self.point = point
        self.x_shift = x_shift
        self.y_shift = y_shift
        self.scale = scale

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        point = obj['point']
        x_shift = obj['x_shift']
        y_shift = obj['y_shift']
        scale = obj['scale']
        return cls(point, x_shift, y_shift, scale)

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {'point': self.point, 'x_shift': self.x_shift, 'y_shift': self.y_shift, 'scale': self.scale}


class InlineQuery(JsonDeserializable):
    """
    This object represents an incoming inline query,
    When the user sends an empty query,
    your bot could return some default or trending results.
    """

    def __init__(self, uid, from_user, query, offset, chat_type, location):
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
        """
        Represents a link to an article or web page
        """

        def __init__(self, uid, title, input_message_content, reply_markup=None, url=None,
                     hide_url=None, description=None, thumb_url=None, thumb_width=None, thumb_height=None):
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

        def to_json(self):
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
            return json.dumps(obj)

    class __InlineQueryResultAudio(JsonSerializable):
        """
        Represents a link to an MP3 audio file
        """

        def __init__(self, uid, audio_url, title, caption=None, parse_mode=None, caption_entities=None, performer=None,
                     audio_duration=None, reply_markup=None, input_message_content=None):
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

        def to_json(self):
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
                obj['input_message_content'] = self.input_message_content.to_dict()
            return json.dumps(obj)

    class __InlineQueryResultCachedAudio(JsonSerializable):
        """
        Represents a link to an MP3 audio file stored on the Telegram servers
        """

        def __init__(self, ttype, uid, audio_file_id, title=None, description=None, caption=None, parse_mode=None,
                     caption_entities=None, reply_markup=None, input_message_content=None):
            self.ttype = ttype
            self.uid = uid
            self.audio_file_id = audio_file_id
            self.title = title
            self.description = description
            self.caption = caption
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities
            self.reply_markup = reply_markup
            self.input_message_content = input_message_content

        def to_dict(self):
            obj = {'type': self.ttype, 'id': self.uid,
                   'audio_file_id': self.audio_file_id}
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

        def to_json(self):
            return json.dumps(self.to_dict())

    class __InlineQueryResultCachedDocument(JsonSerializable):
        """
        Represents a link to a file stored on the Telegram servers
        """

        def __init__(self, ttype, uid, document_file_id, title=None, description=None, caption=None, parse_mode=None,
                     caption_entities=None, reply_markup=None, input_message_content=None):
            self.ttype = ttype
            self.uid = uid
            self.document_file_id = document_file_id
            self.title = title
            self.description = description
            self.caption = caption
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities
            self.reply_markup = reply_markup
            self.input_message_content = input_message_content

        def to_dict(self):
            obj = {'type': self.ttype, 'id': self.uid,
                   'document_file_id': self.document_file_id}
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

        def to_json(self):
            return json.dumps(self.to_dict())

    class __InlineQueryResultCachedGif(JsonSerializable):
        """
        Represents a link to an animated GIF file stored on the Telegram servers
        """

        def __init__(self, ttype, uid, gif_file_id, title=None, caption=None, parse_mode=None, caption_entities=None,
                     reply_markup=None, input_message_content=None):
            self.ttype = ttype
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

        def to_json(self):
            return json.dumps(self.to_dict())

    class __InlineQueryResultCachedMpeg4Gif(JsonSerializable):
        """
        Represents a link to a video animation (H.264/MPEG-4 AVC video without sound) stored on the Telegram servers
        """

        def __init__(self, ttype, uid, mpeg4_file_id, title=None, caption=None, parse_mode=None, caption_entities=None,
                     reply_markup=None, input_message_content=None):
            self.ttype = ttype
            self.uid = uid
            self.mpeg4_file_id = mpeg4_file_id
            self.title = title
            self.caption = caption
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities
            self.reply_markup = reply_markup
            self.input_message_content = input_message_content

        def to_dict(self):
            obj = {'type': self.ttype, 'id': self.uid,
                   'mpeg4_file_id': self.mpeg4_file_id}
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

        def to_json(self):
            return json.dumps(self.to_dict())

    class __InlineQueryResultCachedPhoto(JsonSerializable):
        """
        Represents a link to a photo. By default, this photo will be sent by the user with optional caption
        """

        def __init__(self, ttype, uid, photo_url, thumb_url, photo_width=None, photo_height=None, title=None,
                     description=None, caption=None, parse_mode=None, caption_entities=None, reply_markup=None,
                     input_message_content=None):
            self.ttype = ttype
            self.uid = uid
            self.photo_url = photo_url
            self.thumb_url = thumb_url
            self.photo_width = photo_width
            self.photo_height = photo_height
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

        def to_json(self):
            return json.dumps(self.to_dict())

    class __InlineQueryResultCachedSticker(JsonSerializable):
        """
        Represents a link to a sticker stored on the Telegram servers
        """

        def __init__(self, ttype, uid, sticker_file_id, reply_markup=None, input_message_content=None):
            self.ttype = ttype
            self.uid = uid
            self.sticker_file_id = sticker_file_id
            self.reply_markup = reply_markup
            self.input_message_content = input_message_content

        def to_dict(self):
            obj = {'type': self.ttype, 'id': self.uid,
                   'sticker_file_id': self.sticker_file_id}
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content
            return obj

        def to_json(self):
            return json.dumps(self.to_dict())

    class __InlineQueryResultCachedVideo(JsonSerializable):
        """
        Represents a link to a video file stored on the Telegram servers
        """

        def __init__(self, ttype, uid, video_file_id, title=None, description=None, caption=None, parse_mode=None,
                     caption_entities=None, reply_markup=None, input_message_content=None):
            self.ttype = ttype
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
            obj = {'type': self.ttype, 'id': self.uid,
                   'video_file_id': self.video_file_id}
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

        def to_json(self):
            return json.dumps(self.to_dict())

    class __InlineQueryResultCachedVoice(JsonSerializable):
        """
        Represents a link to a voice message stored on the Telegram servers
        """

        def __init__(self, ttype, uid, voice_file_id, title=None, description=None, caption=None, parse_mode=None,
                     caption_entities=None, reply_markup=None, input_message_content=None):
            self.ttype = ttype
            self.uid = uid
            self.voice_file_id = voice_file_id
            self.title = title
            self.description = description
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

        def to_json(self):
            return json.dumps(self.to_dict())

    class __InlineQueryResultContact(JsonSerializable):
        """
        Represents a contact with a phone number
        """

        def __init__(self, uid, phone_number, first_name, last_name=None, reply_markup=None,
                     input_message_content=None, thumb_url=None, thumb_width=None, thumb_height=None):
            self.ttype = 'contact'
            self.uid = uid
            self.phone_number = phone_number
            self.first_name = first_name
            self.last_name = last_name
            self.reply_markup = reply_markup
            self.input_message_content = input_message_content
            self.thumb_url = thumb_url
            self.thumb_width = thumb_width
            self.thumb_height = thumb_height

        def to_json(self):
            obj = {'type': self.ttype, 'id': self.uid,
                   'phone_number': self.phone_number, 'first_name': self.first_name}
            if self.last_name:
                obj['last_name'] = self.last_name
            if self.thumb_url:
                obj['thumb_url'] = self.thumb_url
            if self.thumb_width:
                obj['thumb_width'] = self.thumb_width
            if self.thumb_height:
                obj['thumb_height'] = self.thumb_height
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content
            return json.dumps(obj)

    class __InlineQueryResultGame(JsonSerializable):
        """
        Represents a Game
        """

        def __init__(self, uid, game_short_name, reply_markup=None):
            self.ttype = 'game'
            self.uid = uid
            self.game_short_name = game_short_name
            self.reply_markup = reply_markup

        def to_json(self):
            obj = {'type': self.ttype, 'id': self.uid,
                   'game_short_name': self.game_short_name}
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup.to_dict()
            return json.dumps(obj)

    class __InlineQueryResultDocument(JsonSerializable):
        """
        Represents a link to a file
        """

        def __init__(self, uid, title, document_url, mime_type, caption=None, parse_mode=None, caption_entities=None,
                     description=None, reply_markup=None, input_message_content=None, thumb_url=None, thumb_width=None,
                     thumb_height=None):
            self.ttype = 'document'
            self.uid = uid
            self.title = title
            self.document_url = document_url
            self.mime_type = mime_type
            self.caption = caption
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities
            self.description = description
            self.reply_markup = reply_markup
            self.input_message_content = input_message_content
            self.thumb_url = thumb_url
            self.thumb_width = thumb_width
            self.thumb_height = thumb_height

        def to_json(self):
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
            if self.thumb_url:
                obj['thumb_url'] = self.thumb_url
            if self.thumb_width:
                obj['thumb_width'] = self.thumb_width
            if self.thumb_height:
                obj['thumb_height'] = self.thumb_height
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup.to_dict()
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content.to_dict()
            return json.dumps(obj)

    class __InlineQueryResultGif(JsonSerializable):
        """
        Represents a link to an animated GIF file
        """

        def __init__(self, uid, gif_url, gif_width=None, gif_height=None, gif_duration=None, thumb_url=None,
                     thumb_mime_type=None, title=None, caption=None, parse_mode=None, caption_entities=None,
                     reply_markup=None, input_message_content=None):
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

        def to_json(self):
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
                obj['input_message_content'] = self.input_message_content.to_dict()
            return json.dumps(obj)

    class __InlineQueryResultLocation(JsonSerializable):
        """
        Represents a location on a map
        """

        def __init__(self, uid, title, latitude, longitude, horizontal_accuracy=None, live_period=None, heading=None,
                     proximity_alert_radius=None, reply_markup=None, input_message_content=None, thumb_url=None,
                     thumb_width=None, thumb_height=None):
            self.ttype = 'location'
            self.uid = uid
            self.title = title
            self.latitude = latitude
            self.longitude = longitude
            self.horizontal_accuracy = horizontal_accuracy
            self.live_period = live_period
            self.heading = heading
            self.proximity_alert_radius = proximity_alert_radius
            self.reply_markup = reply_markup
            self.input_message_content = input_message_content
            self.thumb_url = thumb_url
            self.thumb_width = thumb_width
            self.thumb_height = thumb_height

        def to_json(self):
            obj = {'type': self.ttype, 'id': self.uid, 'title': self.title,
                   'latitude': self.latitude, 'longitude': self.longitude}
            if self.horizontal_accuracy:
                obj['horizontal_accuracy'] = self.horizontal_accuracy
            if self.live_period:
                obj['live_period'] = self.live_period
            if self.heading:
                obj['heading'] = self.heading
            if self.proximity_alert_radius:
                obj['proximity_alert_radius'] = self.proximity_alert_radius
            if self.thumb_url:
                obj['thumb_url'] = self.thumb_url
            if self.thumb_width:
                obj['thumb_width'] = self.thumb_width
            if self.thumb_height:
                obj['thumb_height'] = self.thumb_height
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup.to_dict()
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content.to_dict()
            return json.dumps(obj)

    class __InlineQueryResultMpeg4Gif(JsonSerializable):
        """
        Represents a link to a video animation (H.264/MPEG-4 AVC video without sound)
        """

        def __init__(self, uid, mpeg4_url, mpeg4_width=None, mpeg4_height=None, mpeg4_duration=None, thumb_url=None,
                     thumb_mime_type=None, title=None, caption=None, parse_mode=None, caption_entities=None,
                     reply_markup=None, input_message_content=None):
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

        def to_json(self):
            obj = {'type': self.ttype, 'id': self.uid,
                   'mpeg4_url': self.mpeg4_url, 'thumb_url': self.thumb_url}
            if self.mpeg4_width:
                obj['mpeg4_width'] = self.mpeg4_width
            if self.mpeg4_height:
                obj['mpeg4_height'] = self.mpeg4_height
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
                obj['input_message_content'] = self.input_message_content.to_dict()
            if self.mpeg4_duration:
                obj['mpeg4_duration '] = self.mpeg4_duration
            return json.dumps(obj)

    class __InlineQueryResultPhoto(JsonSerializable):
        """
        Represents a link to a photo
        """

        def __init__(self, uid, photo_url, thumb_url, photo_width=None, photo_height=None, title=None, description=None,
                     caption=None, parse_mode=None, caption_entities=None, reply_markup=None,
                     input_message_content=None):
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

        def to_json(self):
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
                obj['reply_markup'] = self.reply_markup.to_dict()
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content.to_dict()
            return json.dumps(obj)

    class __InlineQueryResultVenue(JsonSerializable):
        """
        Represents a venue
        """

        def __init__(self, uid, latitude, longitude, title, address, foursquare_id=None, foursquare_type=None,
                     google_place_id=None, google_place_type=None, reply_markup=None, input_message_content=None,
                     thumb_url=None, thumb_width=None, thumb_height=None):
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

        def to_json(self):
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
            if self.thumb_url:
                obj['thumb_url'] = self.thumb_url
            if self.thumb_width:
                obj['thumb_width'] = self.thumb_width
            if self.thumb_height:
                obj['thumb_height'] = self.thumb_height
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup.to_dict()
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content.to_dict()
            return json.dumps(obj)

    class __InlineQueryResultVideo(JsonSerializable):
        """
        Represents a link to a page containing an embedded video player or a video file
        """

        def __init__(self, uid, video_url, mime_type, thumb_url, title,
                     caption=None, parse_mode=None, caption_entities=None, video_width=None, video_height=None,
                     video_duration=None, description=None, reply_markup=None, input_message_content=None):
            self.ttype = 'video'
            self.uid = uid
            self.video_url = video_url
            self.mime_type = mime_type
            self.video_width = video_width
            self.video_height = video_height
            self.video_duration = video_duration
            self.thumb_url = thumb_url
            self.title = title
            self.caption = caption
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities
            self.description = description
            self.input_message_content = input_message_content
            self.reply_markup = reply_markup

        def to_json(self):
            obj = {'type': self.ttype, 'id': self.uid, 'video_url': self.video_url, 'mime_type': self.mime_type,
                   'thumb_url': self.thumb_url, 'title': self.title}
            if self.video_width:
                obj['video_width'] = self.video_width
            if self.video_height:
                obj['video_height'] = self.video_height
            if self.video_duration:
                obj['video_duration'] = self.video_duration
            if self.description:
                obj['description'] = self.description
            if self.caption:
                obj['caption'] = self.caption
            if self.parse_mode:
                obj['parse_mode'] = self.parse_mode
            if self.caption_entities:
                obj['caption_entities'] = self.caption_entities
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup.to_dict()
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content.to_dict()
            return json.dumps(obj)

    class __InlineQueryResultVoice(JsonSerializable):
        """
        Represents a link to a voice recording in an .ogg container encoded with OPUS
        """

        def __init__(self, uid, voice_url, title, caption=None, parse_mode=None, caption_entities=None, performer=None,
                     voice_duration=None, reply_markup=None, input_message_content=None):
            self.ttype = 'voice'
            self.uid = uid
            self.voice_url = voice_url
            self.title = title
            self.caption = caption
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities
            self.performer = performer
            self.voice_duration = voice_duration
            self.reply_markup = reply_markup
            self.input_message_content = input_message_content

        def to_json(self):
            obj = {'type': self.ttype, 'id': self.uid,
                   'voice_url': self.voice_url, 'title': self.title}
            if self.caption:
                obj['caption'] = self.caption
            if self.parse_mode:
                obj['parse_mode'] = self.parse_mode
            if self.caption_entities:
                obj['caption_entities'] = self.caption_entities
            if self.performer:
                obj['performer'] = self.performer
            if self.voice_duration:
                obj['voice_duration'] = self.voice_duration
            if self.reply_markup:
                obj['reply_markup'] = self.reply_markup.to_dict()
            if self.input_message_content:
                obj['input_message_content'] = self.input_message_content.to_dict()
            return json.dumps(obj)


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

    class __InputTextMessageContent(Dictionaryable):
        """
        Represents the content of a text message to be sent as the result of an inline query.
        """

        def __init__(self, message_text, parse_mode=None, caption_entities=None, disable_web_page_preview=None):
            self.message_text = message_text
            self.parse_mode = parse_mode
            self.caption_entities = caption_entities
            self.disable_web_page_preview = disable_web_page_preview

        def to_dict(self):
            obj = {'message_text': self.message_text}
            if self.parse_mode:
                obj['parse_mode'] = self.parse_mode
            if self.caption_entities:
                obj['caption_entities'] = self.caption_entities
            if self.disable_web_page_preview:
                obj['disable_web_page_preview'] = self.disable_web_page_preview
            return obj

    class __InputLocationMessageContent(Dictionaryable):
        """
        Represents the content of a location message to be sent as the result of an inline query
        """

        def __init__(self, latitude, longitude, horizontal_accuracy=None, live_period=None, heading=None,
                     proximity_alert_radius=None):
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

    class __InputVenueMessageContent(Dictionaryable):
        """
        Represents the content of a venue message to be sent as the result of an inline query
        """

        def __init__(self, latitude, longitude, title, address, foursquare_id=None, foursquare_type=None,
                     google_place_id=None, google_place_type=None):
            self.latitude = latitude
            self.longitude = longitude
            self.title = title
            self.address = address
            self.foursquare_id = foursquare_id
            self.foursquare_type = foursquare_type
            self.google_place_id = google_place_id
            self.google_place_type = google_place_type

        def to_dict(self):
            obj = {'latitude': self.latitude, 'longitude': self.longitude, 'title': self.title,
                   'address': self.address}
            if self.foursquare_id:
                obj['foursquare_id'] = self.foursquare_id
            if self.foursquare_type:
                obj['foursquare_type'] = self.foursquare_type
            if self.google_place_id:
                obj['google_place_id'] = self.google_place_type
            if self.google_place_type:
                obj['google_place_type'] = self.google_place_type
            return obj

    class __InputContactMessageContent(Dictionaryable):
        """
        Represents a result of an inline query that was chosen by the user and sent to their chat partner
        """

        def __init__(self, phone_number, first_name, last_name=None):
            self.phone_number = phone_number
            self.first_name = first_name
            self.last_name = last_name

        def to_dict(self):
            obj = {'phone_number': self.phone_number,
                   'first_name': self.first_name}
            if self.last_name:
                obj['last_name'] = self.last_name
            return obj

    class __InputInvoiceMessageContent(Dictionaryable):
        """
        Represents the content of an invoice message to be sent as the result of an inline query
        """

        def __init__(self, title, description, payload, provider_token, currency, prices, max_tip_amount,
                     suggested_tip_amounts, provider_data, photo_url, photo_size, photo_width, photo_height, need_name,
                     need_phone_number, need_email, need_shipping_address, send_phone_number_to_provider,
                     send_email_to_provider, is_flexible):
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

    def __init__(self, result_id, from_user, query, location=None, inline_message_id=None):
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


class LabeledPrice(JsonSerializable):
    """
    This object represents a portion of the price for goods or services
    """

    def __init__(self, label, amount):
        self.label = label
        self.amount = amount

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {'label': self.label, 'amount': self.amount}


class Invoice(JsonDeserializable):
    """
    This object contains basic information about an invoice
    """

    def __init__(self, title, description, start_parameter, currency, total_amount):
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
    """
    This object represents a shipping address
    """

    def __init__(self, country_code, state, city, street_line1, street_line2, post_code):
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
    """
    This object represents information about an order
    """

    def __init__(self, name, phone_number, email, shipping_address):
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
    """
    This object represents one shipping option
    """

    def __init__(self, uid, title):
        self.uid = uid
        self.title = title
        self.prices = []

    def add_price(self, *args):
        for price in args:
            self.prices.append(price)
        return self

    def to_json(self):
        price_list = []
        for p in self.prices:
            price_list.append(p.to_dict())
        obj = json.dumps(
            {'id': self.uid, 'title': self.title, 'prices': price_list})
        return obj


class SuccessfulPayment(JsonDeserializable):
    """
    This object contains basic information about a successful payment
    """

    def __init__(self, currency, total_amount, invoice_payload, shipping_option_id, order_info,
                 telegram_payment_charge_id, provider_payment_charge_id):
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
    """
    This object contains information about an incoming shipping query
    """

    def __init__(self, uid, from_user, invoice_payload, shipping_address):
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
    """
    This object contains information about an incoming pre-checkout query
    """

    def __init__(self, uid, from_user, currency, total_amount, invoice_payload, shipping_option_id, order_info):
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
    """
    Contains information about Telegram Passport data shared with the bot by the user
    """

    def __init__(self, data, credentials):
        self.data = data
        self.credentials = credentials

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        data = obj['EncryptedPassportElement']
        credentials = obj['EncryptedCredentials']
        return cls(data, credentials)


class PassportFile(JsonDeserializable):
    """
    This object represents a file uploaded to Telegram Passport
    """

    def __init__(self, file_id, file_unique_id, file_size, file_date):
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
    """
    Contains information about documents or other Telegram Passport elements shared with the bot by the user
    """

    def __init__(self, ttype, data, phone_number, files, front_side, reverse_side, selfie, translation, hashes):
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
    """
    Contains data required for decrypting and authenticating EncryptedPassportElement.
    See the Telegram Passport Documentation for a complete description of the data decryption and
    authentication processes.
    """

    def __init__(self, data, hashes, secret):
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
        pass

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        source = None
        if 'source' in obj:
            source = obj['source']

        if source == 'data':
            return PassportElementErrorDataField.de_json(obj_type)
        elif source == 'front_side':
            return PassportElementErrorFrontSide.de_json(obj_type)
        elif source == 'reverse_side':
            return PassportElementErrorReverseSide.de_json(obj_type)
        elif source == 'selfie':
            return PassportElementErrorSelfie.de_json(obj_type)
        elif source == 'file_hash':
            return PassportElementErrorFile.de_json(obj_type)
        elif source == 'file_hashes':
            return PassportElementErrorFiles.de_json(obj_type)
        elif source == 'translation_files':
            return PassportElementErrorTranslationFile.de_json(obj_type)
        elif source == 'translation_files':
            return PassportElementErrorTranslationFiles.de_json(obj_type)
        elif source == 'unspecified':
            return PassportElementErrorUnspecified.de_json(obj_type)
        else:
            return None


class PassportElementErrorDataField(JsonDeserializable):
    """
    Represents an issue in one of the data fields that was provided by the user
    """

    def __init__(self, source, ttype, field_name, data_hash, message):
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


class PassportElementErrorFrontSide(JsonDeserializable):
    """
    Represents an issue with the front side of a document
    """

    def __init__(self, source, ttype, file_hash, message):
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


class PassportElementErrorFile(JsonDeserializable):
    """
    Represents an issue with a document scan
    """

    def __init__(self, source, ttype, file_hash, message):
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


class PassportElementErrorFiles(JsonDeserializable):
    """
    Represents an issue with a list of scans
    """

    def __init__(self, source, ttype, file_hashes, message):
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


class PassportElementErrorReverseSide(JsonDeserializable):
    """
    Represents an issue with the reverse side of a document
    """

    def __init__(self, source, ttype, file_hash, message):
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


class PassportElementErrorSelfie(JsonDeserializable):
    """
    Represents an issue with the selfie with a document
    """

    def __init__(self, source, ttype, file_hash, message):
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


class PassportElementErrorTranslationFile(JsonDeserializable):
    """
    Represents an issue with one of the files that constitute the translation of a document
    """

    def __init__(self, source, ttype, file_hash, message):
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


class PassportElementErrorTranslationFiles(JsonDeserializable):
    """
    Represents an issue with the translated version of a document
    """

    def __init__(self, source, ttype, file_hashes, message):
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


class PassportElementErrorUnspecified(JsonDeserializable):
    """
    Represents an issue in an unspecified place
    """

    def __init__(self, source, ttype, element_hash, message):
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
    """
    This object represents a game
    """

    def __init__(self, title, description, photo, text=None, text_entities=None, animation=None):
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
    A placeholder, currently holds no information. Use BotFather to set up your game
    """
    pass


class GameHighScore(JsonDeserializable):
    """
    This object represents one row of the high scores' table for a game
    """

    def __init__(self, position, user, score):
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
