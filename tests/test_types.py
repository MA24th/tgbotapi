# -*- coding: utf-8 -*-

"""
test_types.py
~~~~~~~~~~~~~
This submodule provides a tests for tgbotapi types objects
:copyright: (c) 2022 by Mustafa Asaad.
:license: GPLv2, see LICENSE for more details.
"""

import unittest
from tgbotapi import types


@unittest.SkipTest
class TestUpdate(unittest.TestCase):
    with open("schema/Update.json") as f:
        data = f.read()

    # object = types.Update.de_json(data)

    def test_update(self):
        update = self.object
        self.assertEqual(update.update_id, 523905383)
        # update.message -> test_update_message
        # update.edited_message -> test_update_edited_message
        # update.channel_post -> test_update_channel_post
        # update.edited_channel_post -> test_update_edited_channel_post
        # update.inline_query -> test_update_inline_query
        # update.chosen_inline_result -> test_update_chosen_inline_result
        # update.callback_query -> test_update_callback_query
        # update.shipping_query -> test_update_shipping_query
        # update.pre_checkout_query -> test_update_pre_checkout_query
        # update.poll -> test_update_poll
        # update.poll_answer -> test_update_poll_answer
        # update.my_chat_member -> test_update_my_chat_member
        # update.chat_member -> test_update_chat_member
        # update.chat_join_request -> test_update_chat_join_request

    def test_update_message(self):
        msg = self.object.message
        self.assertEqual(msg.message_id, 'id')

    def test_update_edited_message(self):
        msg = self.object.edited_message
        self.assertEqual(msg.message_id, 'id')

    def test_update_channel_post(self):
        post = self.object.channel_post
        self.assertEqual(post.message_id, 'id')

    def test_update_edited_channel_post(self):
        post = self.object.edited_channel_post
        self.assertEqual(post.message_id, 'id')

    def test_update_inline_query(self):
        query = self.object.inline_query
        self.assertEqual(query.uid, "id")

    def test_update_chosen_inline_result(self):
        result = self.object.inline_query
        self.assertEqual(result.result_id, "result_id")

    def test_update_callback_query(self):
        query = self.object.callback_query
        self.assertEqual(query.uid, "id")

    def test_update_shipping_query(self):
        query = self.object.shipping_query
        self.assertEqual(query.uid, "id")

    def test_update_pre_checkout_query(self):
        query = self.object.pre_checkout_query
        self.assertEqual(query.uid, "id")

    def test_update_poll(self):
        poll = self.object.poll
        self.assertEqual(poll.uid, "id")

    def test_update_poll_answer(self):
        answer = self.object.poll_answer
        self.assertEqual(answer.poll_id, "poll id")

    def test_update_my_chat_member(self):
        member = self.object.my_chat_member
        self.assertEqual(member.date, 1234567890)

    def test_update_chat_member(self):
        member = self.object.chat_member
        self.assertEqual(member.date, 1234567890)

    def test_update_chat_join_request(self):
        request = self.object.chat_join_request
        # request.chat
        self.assertEqual(request.chat.uid, 383324787)
        self.assertEqual(request.chat.ttype, "private")
        self.assertEqual(request.chat.title, "GuardBot")
        self.assertEqual(request.chat.username, "MA24th")
        self.assertEqual(request.chat.first_name, "Mustafa")
        self.assertEqual(request.chat.last_name, "Asaad")
        # request.chat.photo
        self.assertEqual(request.chat.photo.small_file_id, "ChatPhoto small file id")
        self.assertEqual(request.chat.photo.small_file_unique_id, "ChatPhoto small file unique id")
        self.assertEqual(request.chat.photo.big_file_id, "ChatPhoto big file id")
        self.assertEqual(request.chat.photo, "ChatPhoto big file unique id")
        self.assertEqual(request.chat.bio, "Keep Focusing")
        self.assertEqual(request.chat.has_private_forwards, True)
        self.assertEqual(request.chat.description, "this is the best description of description")
        self.assertEqual(request.chat.invite_link, "Chat invite link")
        # request.chat.pinned_messages
        self.assertEqual(request.chat.pinned_messages, None)
        # request.chat.permissions
        self.assertEqual(request.chat.permissions.can_send_messages, True)
        self.assertEqual(request.chat.permissions.can_send_media_messages, False)
        self.assertEqual(request.chat.permissions.can_send_polls, True)
        self.assertEqual(request.chat.permissions.can_send_other_messages, False)
        self.assertEqual(request.chat.permissions.can_add_web_page_previews, False)
        self.assertEqual(request.chat.permissions.can_change_info, False)
        self.assertEqual(request.chat.permissions.can_invite_users, True)
        self.assertEqual(request.chat.permissions.can_pin_messages, True)
        self.assertEqual(request.chat.slow_mode_delay, 0)
        self.assertEqual(request.chat.message_auto_delete_time, 10)
        self.assertEqual(request.chat.has_protected_content, False)
        self.assertEqual(request.chat.sticker_set_name, "Chat sticker set name")
        self.assertEqual(request.chat.can_set_sticker_set, True)
        self.assertEqual(request.chat.linked_chat_id, 12345678)
        # request.chat.location
        self.assertEqual(request.chat.location.location.longitude, 33.29)
        self.assertEqual(request.chat.location.location.latitude, 40.50)
        self.assertEqual(request.chat.location.location.horizontal_accuracy, 100)
        self.assertEqual(request.chat.location.location.heading, 30)
        self.assertEqual(request.chat.location.location.proximity_alert_radius, 20)
        self.assertEqual(request.chat.location.address, "Chat location address")
        # request.from
        self.assertEqual(request.from_user.uid, 952435061)
        self.assertEqual(request.from_user.is_bot, True)
        self.assertEqual(request.from_user.first_name, "GuardBot")
        self.assertEqual(request.from_user.last_name, None)
        self.assertEqual(request.from_user.username, "guardbot")
        self.assertEqual(request.from_user.language_code, "en")
        self.assertEqual(request.from_user.can_join_groups, True)
        self.assertEqual(request.from_user.can_read_all_group_messages, True)
        self.assertEqual(request.from_user.supports_inline_queries, True)
        self.assertEqual(request.date, 1234567890)
        self.assertEqual(request.bio, "bio")
        # request.invite_link
        self.assertEqual(request.invite_link.invite_linke, "invite_link")
        self.assertEqual(request.invite_link.creator.uid, 952435061)
        self.assertEqual(request.invite_link.creator.is_bot, True)
        self.assertEqual(request.invite_link.creator.first_name, "GuardBot")
        self.assertEqual(request.invite_link.creator.last_name, None)
        self.assertEqual(request.invite_link.creator.username, "guardbot")
        self.assertEqual(request.invite_link.creator.language_code, "en")
        self.assertEqual(request.invite_link.creator.can_join_groups, True)
        self.assertEqual(request.invite_link.creator.can_read_all_group_messages, True)
        self.assertEqual(request.invite_link.creator.supports_inline_queries, True)
        self.assertEqual(request.invite_link.creats_join_request, True)
        self.assertEqual(request.invite_link.is_primary, True)
        self.assertEqual(request.invite_link.is_revoked, False)
        self.assertEqual(request.invite_link.name, "name")
        self.assertEqual(request.invite_link.expire_date, 1234567890)
        self.assertEqual(request.invite_link.member_limit, 12)
        self.assertEqual(request.invite_link.pending_join_request_count, 2)


class TestWebhookInfo(unittest.TestCase):
    with open("schema/WebhookInfo.json") as f:
        data = f.read()

    object = types.WebhookInfo.de_json(data)

    def test_webhook_info(self):
        self.assertEqual(self.object.url, "WebhookInfo url")
        self.assertEqual(self.object.has_custom_certificate, False)
        self.assertEqual(self.object.pending_update_count, 2)
        self.assertEqual(self.object.ip_address, "192.168.0.1")
        self.assertEqual(self.object.last_error_date, 1234567890)
        self.assertEqual(self.object.last_error_message, "connection timeout")
        self.assertEqual(self.object.max_connections, 40)
        self.assertEqual(self.object.allowed_updates, ["message"])


class TestUser(unittest.TestCase):
    with open("schema/User.json") as f:
        data = f.read()

    object = types.User.de_json(data)

    def test_user(self):
        user = self.object
        self.assertEqual(user.uid, 987654321)
        self.assertEqual(user.is_bot, True)
        self.assertEqual(user.first_name, "GuardBot")
        self.assertEqual(user.last_name, None)
        self.assertEqual(user.username, "guardbot")
        self.assertEqual(user.language_code, "en")
        self.assertEqual(user.can_join_groups, True)
        self.assertEqual(user.can_read_all_group_messages, True)
        self.assertEqual(user.supports_inline_queries, True)


class TestChat(unittest.TestCase):
    with open("schema/Chat.json") as f:
        data = f.read()

    object = types.Chat.de_json(data)

    def test_chat(self):
        chat = self.object
        self.assertEqual(chat.uid, 383324787)
        self.assertEqual(chat.ttype, "private")
        self.assertEqual(chat.title, "GuardBot")
        self.assertEqual(chat.username, "MA24th")
        self.assertEqual(chat.first_name, "Mustafa")
        self.assertEqual(chat.last_name, "Asaad")
        # chat.photo -> test_chat_photo
        self.assertEqual(chat.bio, "Keep Focusing")
        self.assertEqual(chat.has_private_forwards, True)
        self.assertEqual(chat.description, "this is the best description of description")
        self.assertEqual(chat.invite_link, "Chat invite link")
        # chat.pinned_messages -> test_chat_pinned_messages
        # chat.permissions -> test_chat_permissions
        self.assertEqual(chat.slow_mode_delay, 0)
        self.assertEqual(chat.message_auto_delete_time, 10)
        self.assertEqual(chat.has_protected_content, False)
        self.assertEqual(chat.sticker_set_name, "Chat sticker set name")
        self.assertEqual(chat.can_set_sticker_set, True)
        self.assertEqual(chat.linked_chat_id, 12345678)
        # chat.location -> test_chat_location

    def test_chat_photo(self):
        photo = self.object.photo
        self.assertEqual(photo.small_file_id, "ChatPhoto small file id")
        self.assertEqual(photo.small_file_unique_id, "ChatPhoto small file unique id")
        self.assertEqual(photo.big_file_id, "ChatPhoto big file id")
        self.assertEqual(photo.big_file_unique_id, "ChatPhoto big file unique id")

    def test_chat_pinned_message(self):
        pass

    def test_chat_permissions(self):
        permissions = self.object.permissions
        self.assertEqual(permissions.can_send_messages, True)
        self.assertEqual(permissions.can_send_media_messages, False)
        self.assertEqual(permissions.can_send_polls, True)
        self.assertEqual(permissions.can_send_other_messages, False)
        self.assertEqual(permissions.can_add_web_page_previews, False)
        self.assertEqual(permissions.can_change_info, False)
        self.assertEqual(permissions.can_invite_users, True)
        self.assertEqual(permissions.can_pin_messages, True)

    def test_chat_location(self):
        location = self.object.location
        self.assertEqual(location.location.longitude, 33.29)
        self.assertEqual(location.location.latitude, 40.50)
        self.assertEqual(location.location.horizontal_accuracy, 100)
        self.assertEqual(location.location.heading, 30)
        self.assertEqual(location.location.proximity_alert_radius, 20)
        self.assertEqual(location.address, "Chat location address")


@unittest.SkipTest
class TestMessage(unittest.TestCase):
    with open("schema/Message.json") as f:
        data = f.read()

    # object = types.Message.de_json(data)

    def test_message(self):
        msg = self.object
        self.assertEqual(msg.message_id, 1234567890)
        # msg.from  -> test_msg_from
        # msg.sender_chat  -> test_msg_sender_chat
        self.assertEqual(msg.date, 1234567890)
        # msg.chat  -> test_msg_chat
        # msg.forward_from  -> test_msg_forward_from
        # msg.forward_from_chat  -> test_msg_forward_from_chat
        self.assertEqual(msg.forward_from_message_id, 1234567890)
        self.assertEqual(msg.forward_signature, "Musty")
        self.assertEqual(msg.forward_sender_name, "Me")
        self.assertEqual(msg.forward_date, 123456789)
        self.assertEqual(msg.is_automatic_forward, True)
        # msg.reply_to_message  -> test_msg_reply_to_message
        # msg.via_bot  -> test_msg_via_bot
        self.assertEqual(msg.edit_date, 1234567890)
        self.assertEqual(msg.has_protected_content, True)
        self.assertEqual(msg.media_group_id, "abc")
        self.assertEqual(msg.author_signature, "Musty")
        self.assertEqual(msg.test, "hello")
        # msg.entities  -> test_msg_entities
        # msg.animation  -> test_msg_animation
        # msg.audio  -> test_msg_audio
        # msg.document  -> test_msg_document
        # msg.photo  -> test_msg_photo
        # msg.sticker  -> test_msg_sticker
        # msg.video  -> test_msg_video
        # msg.video_note  -> test_msg_video_note
        # msg.voice  -> test_msg_voice
        self.assertEqual(msg.caption, "Message caption")
        # msg.caption_entities  -> test_msg_caption_entities
        # msg.contact  -> test_msg_contact
        # msg.dice  -> test_msg_dice
        # msg.game  -> test_msg_game
        # msg.poll  -> test_msg_poll
        # msg.venue  -> test_msg_venue
        # msg.location  -> test_msg_location
        # msg.new_chat_members  -> test_msg_new_chat_members
        # msg.left_chat_member  -> test_msg_left_chat_member
        self.assertEqual(msg.new_chat_title, "Message new chat title")
        # msg.new_chat_photo  -> test_msg_new_chat_photo
        self.assertEqual(msg.delete_chat_photo, True)
        self.assertEqual(msg.group_chat_created, True)
        self.assertEqual(msg.supergroup_chat_created, False)
        self.assertEqual(msg.channel_chat_created, False)
        # msg.message_auto_delete_timer_changed -> test_msg_message_auto_delete_timer_changed
        self.assertEqual(msg.migrate_to_chat_id, 1234567890)
        self.assertEqual(msg.migrate_from_chat_id, 1234567890)
        # msg.pinned_message -> test_msg_pinned_message
        # msg.invoice -> test_msg_invoice
        # msg.successful_payment -> test_msg_successful_payment
        self.assertEqual(msg.connected_website, "google.com")
        # msg.passport_data -> test_msg_passport_data
        # msg.proximity_alert_triggered -> test_msg_proximity_alert_triggered
        # msg.voice_chat_scheduled -> test_msg_voice_chat_scheduled
        # msg.voice_chat_started -> test_msg_voice_chat_started
        # msg.voice_chat_ended -> test_msg_voice_chat_ended
        # msg.voice_chat_participants_invited -> test_msg_voice_chat_participants_invited
        # msg.reply_markup -> test_msg_reply_markup

    def test_msg_from(self):
        pass

    def test_msg_sender_chat(self):
        pass

    def test_msg_chat(self):
        pass

    def test_msg_forward_from(self):
        pass

    def test_msg_forward_from_chat(self):
        pass

    def test_msg_reply_to_message(self):
        pass

    def test_msg_via_bot(self):
        pass

    def test_msg_entities(self):
        pass

    def test_msg_animation(self):
        pass

    def test_msg_audio(self):
        pass

    def test_msg_document(self):
        pass

    def test_msg_photo(self):
        pass

    def test_msg_sticker(self):
        pass

    def test_msg_video(self):
        pass

    def test_msg_video_note(self):
        pass

    def test_msg_voice(self):
        pass

    def test_msg_caption_entities(self):
        pass

    def test_msg_contact(self):
        pass

    def test_msg_dice(self):
        pass

    def test_msg_game(self):
        pass

    def test_msg_poll(self):
        pass

    def test_msg_venue(self):
        pass

    def test_msg_location(self):
        pass

    def test_msg_new_chat_member(self):
        pass

    def test_msg_left_chat_member(self):
        pass

    def test_msg_new_chat_photo(self):
        pass

    def test_msg_message_auto_delete_timer_changed(self):
        pass

    def test_msg_pinned_message(self):
        pass

    def test_msg_invoice(self):
        pass

    def test_msg_successful_payment(self):
        pass

    def test_msg_passport_data(self):
        pass

    def test_msg_proximity_alert_triggered(self):
        pass

    def test_msg_voice_chat_scheduled(self):
        pass

    def test_msg_voice_chat_started(self):
        pass

    def test_msg_voice_chat_ended(self):
        pass

    def test_msg_voice_chat_participants_invited(self):
        pass

    def test_msg_reply_markup(self):
        pass


class TestMessageId(unittest.TestCase):
    with open("schema/MessageId.json") as f:
        data = f.read()

    object = types.MessageId.de_json(data)

    def test_message_id(self):
        self.assertEqual(self.object.message_id, 1234567890, "Integer, Unique message identifier")


class TestMessageEntity(unittest.TestCase):
    with open("schema/MessageEntity.json") as f:
        data = f.read()

    object = types.MessageEntity.de_json(data)

    def test_message_entity(self):
        entity = self.object
        self.assertEqual(entity.ttype, "MessageEntity type")
        self.assertEqual(entity.offset, 0)
        self.assertEqual(entity.length, 7)
        self.assertEqual(entity.url, "MessageEntity url")
        # message_entity.user -> test_message_entity_user
        self.assertEqual(entity.language, "en")

    def test_message_entity_user(self):
        user = self.object.user
        self.assertEqual(user.uid, 987654321)
        self.assertEqual(user.is_bot, True)
        self.assertEqual(user.first_name, "GuardBot")
        self.assertEqual(user.last_name, None)
        self.assertEqual(user.username, "guardbot")
        self.assertEqual(user.language_code, "en")
        self.assertEqual(user.can_join_groups, True)
        self.assertEqual(user.can_read_all_group_messages, True)
        self.assertEqual(user.supports_inline_queries, True)


class TestPhotoSize(unittest.TestCase):
    with open("schema/PhotoSize.json") as f:
        data = f.read()

    object = types.PhotoSize.de_json(data)

    def test_photo_size(self):
        photo = self.object
        self.assertEqual(photo.file_id, "PhotoSize file id")
        self.assertEqual(photo.file_unique_id, "PhotoSize file unique id")
        self.assertEqual(photo.width, 180)
        self.assertEqual(photo.height, 200)
        self.assertEqual(photo.file_size, 640)


class TestAnimation(unittest.TestCase):
    with open("schema/Animation.json") as f:
        data = f.read()

    object = types.Animation.de_json(data)

    def test_animation(self):
        animation = self.object
        self.assertEqual(animation.file_id, "Animation file id")
        self.assertEqual(animation.file_unique_id, "Animation file unique id")
        self.assertEqual(animation.width, 180)
        self.assertEqual(animation.height, 200)
        self.assertEqual(animation.duration, 120)
        # animation.thumb -> test_animation_thumb
        self.assertEqual(animation.file_name, "Animation file name")
        self.assertEqual(animation.mime_type, "Animation mime type")
        self.assertEqual(animation.file_size, 640)

    def test_animation_thumb(self):
        thumb = self.object.thumb
        self.assertEqual(thumb.file_id, "PhotoSize file id")
        self.assertEqual(thumb.file_unique_id, "PhotoSize file unique id")
        self.assertEqual(thumb.width, 180)
        self.assertEqual(thumb.height, 200)
        self.assertEqual(thumb.file_size, 640)


class TestAudio(unittest.TestCase):
    with open("schema/Audio.json") as f:
        data = f.read()

    object = types.Audio.de_json(data)

    def test_audio(self):
        audio = self.object
        self.assertEqual(audio.file_id, "Audio file id")
        self.assertEqual(audio.file_unique_id, "Audio file unique id")
        self.assertEqual(audio.duration, 120)
        self.assertEqual(audio.performer, "Audio performer")
        self.assertEqual(audio.file_name, "Audio file name")
        self.assertEqual(audio.mime_type, "Audio mime type")
        self.assertEqual(audio.file_size, 640)
        # audio.thumb -> test_audio_thumb

    def test_audio_thumb(self):
        thumb = self.object.thumb
        self.assertEqual(thumb.file_id, "PhotoSize file id")
        self.assertEqual(thumb.file_unique_id, "PhotoSize file unique id")
        self.assertEqual(thumb.width, 180)
        self.assertEqual(thumb.height, 200)
        self.assertEqual(thumb.file_size, 640)


class TestDocument(unittest.TestCase):
    with open("schema/Document.json") as f:
        data = f.read()

    object = types.Document.de_json(data)

    def test_document(self):
        document = self.object
        self.assertEqual(document.file_id, "Document file id")
        self.assertEqual(document.file_unique_id, "Document file unique id")
        # document.thumb -> test_document_thumb
        self.assertEqual(document.file_name, "Document file name")
        self.assertEqual(document.mime_type, "Document mime type")
        self.assertEqual(document.file_size, 640)

    def test_document_thumb(self):
        thumb = self.object.thumb
        self.assertEqual(thumb.file_id, "PhotoSize file id")
        self.assertEqual(thumb.file_unique_id, "PhotoSize file unique id")
        self.assertEqual(thumb.width, 180)
        self.assertEqual(thumb.height, 200)
        self.assertEqual(thumb.file_size, 640)


class TestVideo(unittest.TestCase):
    with open("schema/Video.json") as f:
        data = f.read()

    object = types.Video.de_json(data)

    def test_video(self):
        video = self.object
        self.assertEqual(video.file_id, "Video file id")
        self.assertEqual(video.file_unique_id, "Video file unique id")
        self.assertEqual(video.width, 180)
        self.assertEqual(video.height, 200)
        self.assertEqual(video.duration, 120)
        # video.thumb -> test_video_thumb
        self.assertEqual(video.file_name, "Video file name")
        self.assertEqual(video.mime_type, "Video mime type")
        self.assertEqual(video.file_size, 640)

    def test_video_thumb(self):
        thumb = self.object.thumb
        self.assertEqual(thumb.file_id, "PhotoSize file id")
        self.assertEqual(thumb.file_unique_id, "PhotoSize file unique id")
        self.assertEqual(thumb.width, 180)
        self.assertEqual(thumb.height, 200)
        self.assertEqual(thumb.file_size, 640)


class TestVideoNote(unittest.TestCase):
    with open("schema/VideoNote.json") as f:
        data = f.read()

    object = types.VideoNote.de_json(data)

    def test_video_note(self):
        video_note = self.object
        self.assertEqual(video_note.file_id, "VideoNote file id")
        self.assertEqual(video_note.file_unique_id, "VideoNote file unique id")
        self.assertEqual(video_note.length, 90)
        self.assertEqual(video_note.duration, 120)
        # video_note.thumb -> test_video_note_thumb
        self.assertEqual(video_note.file_size, 640)

    def test_video_note_thumb(self):
        thumb = self.object.thumb
        self.assertEqual(thumb.file_id, "PhotoSize file id")
        self.assertEqual(thumb.file_unique_id, "PhotoSize file unique id")
        self.assertEqual(thumb.width, 180)
        self.assertEqual(thumb.height, 200)
        self.assertEqual(thumb.file_size, 640)


class TestVoice(unittest.TestCase):
    with open("schema/Voice.json") as f:
        data = f.read()

    object = types.Voice.de_json(data)

    def test_voice(self):
        voice = self.object
        self.assertEqual(voice.file_id, "Voice file id")
        self.assertEqual(voice.file_unique_id, "Voice file unique id")
        self.assertEqual(voice.duration, 120)
        self.assertEqual(voice.mime_type, "Voice mime type")
        self.assertEqual(voice.file_size, 640)


class TestContact(unittest.TestCase):
    with open("schema/Contact.json") as f:
        data = f.read()

    object = types.Contact.de_json(data)

    def test_contact(self):
        contact = self.object
        self.assertEqual(contact.phone_number, "Contact phone number")
        self.assertEqual(contact.first_name, "Contact first name")
        self.assertEqual(contact.last_name, "Contact last name")
        self.assertEqual(contact.user_id, 1234567890)
        self.assertEqual(contact.vcard, "Contact vcard")


class TestDice(unittest.TestCase):
    with open("schema/Dice.json") as f:
        data = f.read()

    object = types.Dice.de_json(data)

    def test_dice(self):
        dice = self.object
        self.assertEqual(dice.emoji, "Dice emoji")
        self.assertEqual(dice.value, 64)


class TestPollOption(unittest.TestCase):
    with open("schema/PollOption.json") as f:
        data = f.read()

    object = types.PollOption.de_json(data)

    def test_poll_option(self):
        option = self.object
        self.assertEqual(option.text, "PollOption text")
        self.assertEqual(option.voter_count, 12)


class TestPollAnswer(unittest.TestCase):
    with open("schema/PollAnswer.json") as f:
        data = f.read()

    object = types.PollAnswer.de_json(data)

    def test_poll_answer(self):
        answer = self.object
        self.assertEqual(answer.poll_id, "PollAnswer poll id")
        # answer.user -> test_poll_answer_user
        self.assertEqual(answer.option_ids, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_poll_answer_user(self):
        user = self.object.user
        self.assertEqual(user.uid, 987654321)
        self.assertEqual(user.is_bot, True)
        self.assertEqual(user.first_name, "GuardBot")
        self.assertEqual(user.last_name, None)
        self.assertEqual(user.username, "guardbot")
        self.assertEqual(user.language_code, "en")
        self.assertEqual(user.can_join_groups, True)
        self.assertEqual(user.can_read_all_group_messages, True)
        self.assertEqual(user.supports_inline_queries, True)


class TestPoll(unittest.TestCase):
    with open("schema/Poll.json") as f:
        data = f.read()

    object = types.Poll.de_json(data)

    def test_poll(self):
        poll = self.object
        self.assertEqual(poll.uid, "Poll id")
        self.assertEqual(poll.question, "Poll question")
        # poll.options -> test_poll_options
        self.assertEqual(poll.total_voter_count, 12)
        self.assertEqual(poll.is_closed, True)
        self.assertEqual(poll.is_anonymous, False)
        self.assertEqual(poll.ttype, "Poll type")
        self.assertEqual(poll.allows_multiple_answers, False)
        self.assertEqual(poll.correct_option_id, 1)
        self.assertEqual(poll.explanation, "Poll explanation")
        # poll.explanation_entities -> test_poll_explanation_entities
        self.assertEqual(poll.open_period, 120)
        self.assertEqual(poll.close_date, 1234567890)

    def test_poll_options(self):
        option = self.object.options[0]
        self.assertEqual(option.text, "PollOption text")
        self.assertEqual(option.voter_count, 12)

    def test_poll_explanation_entities(self):
        entity = self.object.explanation_entities[0]
        self.assertEqual(entity.ttype, "MessageEntity type")
        self.assertEqual(entity.offset, 0)
        self.assertEqual(entity.length, 7)
        self.assertEqual(entity.url, "MessageEntity url")
        self.assertEqual(entity.language, "en")
        self.assertEqual(entity.user.uid, 987654321)
        self.assertEqual(entity.user.is_bot, True)
        self.assertEqual(entity.user.first_name, "GuardBot")
        self.assertEqual(entity.user.last_name, None)
        self.assertEqual(entity.user.username, "guardbot")
        self.assertEqual(entity.user.language_code, "en")
        self.assertEqual(entity.user.can_join_groups, True)
        self.assertEqual(entity.user.can_read_all_group_messages, True)
        self.assertEqual(entity.user.supports_inline_queries, True)


class TestLocation(unittest.TestCase):
    with open("schema/Location.json") as f:
        data = f.read()

    object = types.Location.de_json(data)

    def test_location(self):
        location = self.object
        self.assertEqual(location.longitude, 33.29)
        self.assertEqual(location.latitude, 40.50)
        self.assertEqual(location.live_period, 60)
        self.assertEqual(location.heading, 30)
        self.assertEqual(location.proximity_alert_radius, 20)


class TestVenue(unittest.TestCase):
    with open("schema/Venue.json") as f:
        data = f.read()

    object = types.Venue.de_json(data)

    def test_venue(self):
        venue = self.object
        # venue.location -> test_venue_location
        self.assertEqual(venue.title, "Venue title")
        self.assertEqual(venue.address, "Venue address")
        self.assertEqual(venue.foursquare_id, "Venue foursquare id")
        self.assertEqual(venue.foursquare_type, "Venue foursquare type")
        self.assertEqual(venue.google_place_id, "Venue google place id")
        self.assertEqual(venue.google_place_type, "Venue google place type")

    def test_venue_location(self):
        location = self.object.location
        self.assertEqual(location.longitude, 33.29)
        self.assertEqual(location.latitude, 40.50)
        self.assertEqual(location.live_period, 60)
        self.assertEqual(location.heading, 30)
        self.assertEqual(location.proximity_alert_radius, 20)


class TestProximityAlertTriggered(unittest.TestCase):
    with open("schema/ProximityAlertTriggered.json") as f:
        data = f.read()

    object = types.ProximityAlertTriggered.de_json(data)

    def test_proximity_alert_triggered(self):
        alert = self.object
        # alert.traveler -> test_alert_traveler
        # alert.watcher -> test_alert_watcher
        self.assertEqual(alert.distance, 200)

    def test_alert_traveler(self):
        traveler = self.object.traveler
        self.assertEqual(traveler.uid, 987654321)
        self.assertEqual(traveler.is_bot, True)
        self.assertEqual(traveler.first_name, "GuardBot")
        self.assertEqual(traveler.last_name, None)
        self.assertEqual(traveler.username, "guardbot")
        self.assertEqual(traveler.language_code, "en")
        self.assertEqual(traveler.can_join_groups, True)
        self.assertEqual(traveler.can_read_all_group_messages, True)
        self.assertEqual(traveler.supports_inline_queries, True)

    def test_alert_watcher(self):
        watcher = self.object.watcher
        self.assertEqual(watcher.uid, 987654321)
        self.assertEqual(watcher.is_bot, False)
        self.assertEqual(watcher.first_name, "Mustafa")
        self.assertEqual(watcher.last_name, None)
        self.assertEqual(watcher.username, "MA24th")
        self.assertEqual(watcher.language_code, "en")
        self.assertEqual(watcher.can_join_groups, True)
        self.assertEqual(watcher.can_read_all_group_messages, True)
        self.assertEqual(watcher.supports_inline_queries, True)


class TestMessageAutoDeleteTimerChanged(unittest.TestCase):
    with open("schema/MessageAutoDeleteTimerChanged.json") as f:
        data = f.read()

    object = types.MessageAutoDeleteTimerChanged.de_json(data)

    def test_message_auto_delete_timer_changed(self):
        changed = self.object
        self.assertEqual(changed.message_auto_delete_time, 0)


class TestVoiceChatScheduled(unittest.TestCase):
    with open("schema/VoiceChatScheduled.json") as f:
        data = f.read()

    object = types.VoiceChatScheduled.de_json(data)

    def test_voice_chat_scheduled(self):
        scheduled = self.object
        self.assertEqual(scheduled.start_date, 1234567890)


class TestVoiceChatEnded(unittest.TestCase):
    with open("schema/VoiceChatEnded.json") as f:
        data = f.read()

    object = types.VoiceChatEnded.de_json(data)

    def test_voice_chat_ended(self):
        ended = self.object
        self.assertEqual(ended.duration, 0)


class TestVoiceChatParticipantsInvited(unittest.TestCase):
    with open("schema/VoiceChatParticipantsInvited.json") as f:
        data = f.read()

    object = types.VoiceChatParticipantsInvited.de_json(data)

    def test_voice_chat_participants_invited(self):
        invited = self.object.users[0]
        self.assertEqual(invited.uid, 987654321)
        self.assertEqual(invited.is_bot, True)
        self.assertEqual(invited.first_name, "GuardBot")
        self.assertEqual(invited.last_name, None)
        self.assertEqual(invited.username, "guardbot")
        self.assertEqual(invited.language_code, "en")
        self.assertEqual(invited.can_join_groups, True)
        self.assertEqual(invited.can_read_all_group_messages, True)
        self.assertEqual(invited.supports_inline_queries, True)


class TestUserProfilePhotos(unittest.TestCase):
    with open("schema/UserProfilePhotos.json") as f:
        data = f.read()

    object = types.UserProfilePhotos.de_json(data)

    def test_user_profile_photos(self):
        profile = self.object
        self.assertEqual(profile.total_count, 1)
        # profile.photos -> test_profile_photos

    def test_profile_photos(self):
        photo = self.object.photos[0][0]
        self.assertEqual(photo.file_id, "PhotoSize file id")
        self.assertEqual(photo.file_unique_id, "PhotoSize file unique id")
        self.assertEqual(photo.width, 180)
        self.assertEqual(photo.height, 200)
        self.assertEqual(photo.file_size, 640)


class TestFile(unittest.TestCase):
    with open("schema/File.json") as f:
        data = f.read()

    object = types.File.de_json(data)

    def test_file(self):
        file = self.object
        self.assertEqual(file.file_id, "File file id")
        self.assertEqual(file.file_unique_id, "File file unique id")
        self.assertEqual(file.file_size, 16)
        self.assertEqual(file.file_path, "File file path")


class TestReplyKeyboardMarkup(unittest.TestCase):
    with open("schema/ReplyKeyboardMarkup.json") as f:
        data = f.read()

    object = types.ReplyKeyboardMarkup.de_json(data)

    def test_reply_keyboard_markup(self):
        markup = self.object
        # markup.keyboard -> test_markup_keyboard
        self.assertEqual(markup.resize_keyboard, True)
        self.assertEqual(markup.one_time_keyboard, True)
        self.assertEqual(markup.input_field_placeholder, "input field place holder")
        self.assertEqual(markup.selective, True)

    def test_markup_keyboard(self):
        keyboard = self.object.keyboard[0][0]
        self.assertEqual(keyboard.text, "KeyboardButton text")
        self.assertEqual(keyboard.request_contact, False)
        self.assertEqual(keyboard.request_location, True)
        self.assertEqual(keyboard.request_poll.ttype, "KeyboardButtonPollType type")


class TestKeyboardButton(unittest.TestCase):
    with open("schema/KeyboardButton.json") as f:
        data = f.read()

    object = types.KeyboardButton.de_json(data)

    def test_keyboard_button(self):
        keyboard = self.object
        self.assertEqual(keyboard.text, "KeyboardButton text")
        self.assertEqual(keyboard.request_contact, False)
        self.assertEqual(keyboard.request_location, True)
        # keyboard.request_poll -> test_keyboard_request_poll

    def test_keyboard_request_poll(self):
        request_poll = self.object.request_poll
        self.assertEqual(request_poll.ttype, "KeyboardButtonPollType type")


class TestReplyKeyboardRemove(unittest.TestCase):
    with open("schema/ReplyKeyboardRemove.json") as f:
        data = f.read()

    object = types.ReplyKeyboardRemove(remove_keyboard=True, selective=False).to_json()

    def test_reply_keyboard_remove(self):
        self.assertEqual(self.object, self.data)


class TestInlineKeyboardMarkup(unittest.TestCase):
    with open("schema/InlineKeyboardMarkup.json") as f:
        data = f.read()

    object = types.InlineKeyboardMarkup.de_json(data)

    def test_inline_keyboard_markup(self):
        # object.inline_keyboard = test_inline_keyboard
        pass

    def test_inline_keyboard(self):
        button = self.object.inline_keyboard[0][0]
        self.assertEqual(button.text, "InlineKeyboardButton text")
        self.assertEqual(button.url, "InlineKeyboardButton url")
        self.assertEqual(button.login_url.url, "LoginUrl url")
        self.assertEqual(button.login_url.forward_text, "LoginUrl forward text")
        self.assertEqual(button.login_url.bot_username, "LoginUrl bot username")
        self.assertEqual(button.login_url.request_write_access, True)
        self.assertEqual(button.callback_data, "InlineKeyboardButton callback data")
        self.assertEqual(button.switch_inline_query, "InlineKeyboardButton switch inline query")
        self.assertEqual(button.switch_inline_query_current_chat, "InlineKeyboardButton siq current chat")
        self.assertEqual(button.callback_game, None)
        self.assertEqual(button.pay, True)


class TestInlineKeyboardButton(unittest.TestCase):
    with open("schema/InlineKeyboardButton.json") as f:
        data = f.read()

    object = types.InlineKeyboardButton.de_json(data)

    def test_inline_keyboard_button(self):
        button = self.object
        self.assertEqual(button.text, "InlineKeyboardButton text")
        self.assertEqual(button.url, "InlineKeyboardButton url")
        # button.login_url -> test_button_login_url
        self.assertEqual(button.callback_data, "InlineKeyboardButton callback data")
        self.assertEqual(button.switch_inline_query, "InlineKeyboardButton switch inline query")
        self.assertEqual(button.switch_inline_query_current_chat, "InlineKeyboardButton siq current chat")
        self.assertEqual(button.callback_game, None)
        self.assertEqual(button.pay, True)

    def test_button_login_url(self):
        login_url = self.object.login_url
        self.assertEqual(login_url.url, "LoginUrl url")
        self.assertEqual(login_url.forward_text, "LoginUrl forward text")
        self.assertEqual(login_url.bot_username, "LoginUrl bot username")
        self.assertEqual(login_url.request_write_access, True)


class TestLoginUrl(unittest.TestCase):
    with open("schema/LoginUrl.json") as f:
        data = f.read()

    object = types.LoginUrl.de_json(data)

    def test_login_url(self):
        login_url = self.object
        self.assertEqual(login_url.url, "LoginUrl url")
        self.assertEqual(login_url.forward_text, "LoginUrl forward text")
        self.assertEqual(login_url.bot_username, "LoginUrl bot username")
        self.assertEqual(login_url.request_write_access, True)


class TestCallbackQuery(unittest.TestCase):
    with open("schema/CallbackQuery.json") as f:
        data = f.read()

    object = types.CallbackQuery.de_json(data)

    def test_callback_query(self):
        query = self.object
        self.assertEqual(query.uid, "CallbackQuery id")
        # query.form_user -> test_query_form_user
        # query.message -> test_query_message
        self.assertEqual(query.inline_message_id, "CallbackQuery inline message id")
        self.assertEqual(query.chat_instance, "CallbackQuery chat instance")
        self.assertEqual(query.game_short_name, "CallbackQuery game short name")

    def test_query_form_user(self):
        user = self.object.from_user
        self.assertEqual(user.uid, 987654321)
        self.assertEqual(user.is_bot, True)
        self.assertEqual(user.first_name, "GuardBot")
        self.assertEqual(user.last_name, None)
        self.assertEqual(user.username, "guardbot")
        self.assertEqual(user.language_code, "en")
        self.assertEqual(user.can_join_groups, True)
        self.assertEqual(user.can_read_all_group_messages, True)
        self.assertEqual(user.supports_inline_queries, True)

    def test_query_message(self):
        msg = self.object.message
        self.assertEqual(msg, None)


class TestForceReply(unittest.TestCase):
    with open("schema/ForceReply.json") as f:
        data = f.read()

    object = types.ForceReply(force_reply=True, input_field_placeholder='abc', selective=True)

    def test_force_reply(self):
        force_reply = str(self.object)
        self.assertEqual(force_reply, self.data)
