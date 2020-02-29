import pytest
from tgbotapi import types


def test_Update():
    dic = {
        "update_id": 938203,
        "message": {
            "message_id": 241,
            "from": {
                "is_bot": False,
                "id": 383324787,
                "first_name": "Mustafa",
                "last_name": "Asaad",
                "username": "MA24th"
            },
            "chat": {
                "id": 383324787,
                "first_name": "Mustafa",
                "last_name": "Asaad",
                "username": "MA24th",
                "type": "private"
            },
            "date": 1441447009,
            "text": "/start"
        }}
    obj = types.Update.de_json(dic)
    assert obj.update_id == 938203
    assert obj.message.message_id == 241
    assert obj.message.from_user.is_bot == False
    assert obj.message.from_user.id == 383324787
    assert obj.message.from_user.first_name == 'Mustafa'
    assert obj.message.from_user.last_name == 'Asaad'
    assert obj.message.from_user.username == 'MA24th'
    assert obj.message.chat.id == 383324787
    assert obj.message.chat.first_name == 'Mustafa'
    assert obj.message.chat.last_name == 'Asaad'
    assert obj.message.chat.username == 'MA24th'
    assert obj.message.chat.type == 'private'
    assert obj.message.date == 1441447009
    assert obj.message.text == '/start'
    assert obj.edited_message == None
    assert obj.channel_post == None
    assert obj.edited_channel_post == None
    assert obj.inline_query == None
    assert obj.chosen_inline_result == None
    assert obj.callback_query == None
    assert obj.shipping_query == None
    assert obj.pre_checkout_query == None
    assert obj.poll == None
    assert obj.poll_anwser == None


def test_WebhookInfo():
    dic = {
        'url': 'weburl',
        'has_custom_certificate': None,
        'pending_update_count': 1,
        'last_error_date': 155555,
        'last_error_message': 'abc',
        'max_connections': 44,
        'allowed_updates': 'au'
    }
    obj = types.WebhookInfo.de_json(dic)
    assert obj.url == 'weburl'
    assert obj.has_custom_certificate == None
    assert obj.pending_update_count == 1
    assert obj.last_error_date == 155555
    assert obj.last_error_message == 'abc'
    assert obj.max_connections == 44
    assert obj.allowed_updates == 'au'


def test_User():
    dic = {
        "id": 952435061,
        "is_bot": True,
        "first_name": "GuardBot",
        "last_name": None,
        "username": "@gu9rdbot",
        "language_code": 'en',
        "can_join_groups": True,
        "can_read_all_group_messages": False,
        "supports_inline_queries": True
    }
    user = types.User.de_json(dic)
    assert user.id == 952435061
    assert user.first_name == 'GuardBot'
    assert user.last_name == None
    assert user.is_bot == True
    assert user.username == '@gu9rdbot'
    assert user.language_code == 'en'
    assert user.can_join_groups == True
    assert user.can_read_all_group_messages == False
    assert user.supports_inline_queries == True


def test_Chat():
    dic = {
        "id": -1001184458459,
        "type": "channel",
        "title": "GRID9",
        "username": "grid9x",
        "first_name": None,
        "last_name": None,
        "photo": {
            'small_file_id': 111,
            'small_file_unique_id': 222,
            'big_file_id': 333,
            'big_file_unique_id': 444},
        "description": 'group description',
        "invite_link": None,
        "pinned_message": {
            "message_id": 26,
            "chat": {"id": -1001184458459, "title": "GRID9", "username": "grid9x",
                     "type": "channel"}, "date": 1581868153, "text": "/start"},
        "permissions": {
            'can_send_messages': True,
            'can_send_media_messages': True,
            'can_send_polls': False,
            'can_send_other_messages': True,
            'can_add_web_page_previews': False,
            'can_change_info': False,
            'can_invite_users': True,
            'can_pin_messages': True
        },
        "slow_mode_delay": 5,
        "sticker_set_name": 'channelstickers',
        "can_set_sticker_set": False
    }
    obj = types.Chat.de_json(dic)
    assert obj.id == -1001184458459
    assert obj.type == 'channel'
    assert obj.title == 'GRID9'
    assert obj.first_name == None
    assert obj.last_name == None
    assert obj.photo.small_file_id == 111
    assert obj.photo.small_file_unique_id == 222
    assert obj.photo.big_file_id == 333
    assert obj.photo.big_file_unique_id == 444
    assert obj.description == 'group description'
    assert obj.invite_link == None
    assert obj.pinned_message.message_id == 26
    assert obj.pinned_message.chat.id == -1001184458459
    assert obj.pinned_message.chat.title == 'GRID9'
    assert obj.pinned_message.chat.username == 'grid9x'
    assert obj.pinned_message.chat.type == 'channel'
    assert obj.pinned_message.chat.first_name == None
    assert obj.pinned_message.chat.last_name == None
    assert obj.pinned_message.chat.photo == None
    assert obj.pinned_message.chat.description == None
    assert obj.pinned_message.chat.invite_link == None
    assert obj.pinned_message.chat.pinned_message == None
    assert obj.pinned_message.chat.permissions == None
    assert obj.pinned_message.chat.slow_mode_delay == None
    assert obj.pinned_message.chat.sticker_set_name == None
    assert obj.pinned_message.chat.can_set_sticker_set == None
    assert obj.pinned_message.date == 1581868153
    assert obj.pinned_message.text == '/start'
    assert obj.permissions.can_send_messages == True
    assert obj.permissions.can_send_media_messages == True
    assert obj.permissions.can_send_polls == False
    assert obj.permissions.can_send_other_messages == True
    assert obj.permissions.can_add_web_page_previews == False
    assert obj.permissions.can_change_info == False
    assert obj.permissions.can_invite_users == True
    assert obj.permissions.can_pin_messages == True
    assert obj.slow_mode_delay == 5
    assert obj.sticker_set_name == 'channelstickers'
    assert obj.can_set_sticker_set == False


def test_Message():
    dic = {
        'message_id': 23,
        'from': {
            "id": 383324787,
            "is_bot": False,
            "first_name": "Mustafa",
            "last_name": "Asaad",
            "username": "MA24th",
            "language_code": "en"},
        'date': 15553332,
        'chat': {
            "id": -1001184458459,
            "type": "channel",
            "title": "GRID9",
            "username": "grid9x",
            "first_name": None,
            "last_name": None,
            "photo": {
                'small_file_id': 111,
                'small_file_unique_id': 222,
                'big_file_id': 333,
                'big_file_unique_id': 444},
            "description": 'group description',
            "invite_link": None,
            "pinned_message": {
                "message_id": 26,
                "chat": {
                    "id": -1001184458459,
                    "title": "GRID9",
                    "username": "grid9x",
                    "type": "channel"
                },
                "date": 1581868153,
                "text": "/start"},
            "permissions": {
                'can_send_messages': True,
                'can_send_media_messages': True,
                'can_send_polls': False,
                'can_send_other_messages': True,
                'can_add_web_page_previews': False,
                'can_change_info': False,
                'can_invite_users': True,
                'can_pin_messages': True
            },
            "slow_mode_delay": 5,
            "sticker_set_name": 'channelstickers',
            "can_set_sticker_set": False
        },
    }
    obj = types.Message.de_json(dic)
    assert obj.message_id == 23
    assert obj.from_user.id == 383324787
    assert obj.from_user.is_bot == False
    assert obj.from_user.first_name == 'Mustafa'
    assert obj.from_user.last_name == 'Asaad'
    assert obj.from_user.language_code == 'en'
    assert obj.date == 15553332
    assert obj.chat.id == -1001184458459
    assert obj.chat.type == 'channel'
    assert obj.chat.title == 'GRID9'
    assert obj.chat.username == 'grid9x'
    assert obj.chat.first_name == None
    assert obj.chat.last_name == None
    assert obj.chat.photo.small_file_id == 111
    assert obj.chat.photo.small_file_unique_id == 222
    assert obj.chat.photo.big_file_id == 333
    assert obj.chat.photo.big_file_unique_id == 444
    assert obj.chat.description == 'group description'
    assert obj.chat.invite_link == None
    assert obj.chat.pinned_message.message_id == 26
    assert obj.chat.pinned_message.chat.id == -1001184458459
    assert obj.chat.pinned_message.chat.type == 'channel'
    assert obj.chat.pinned_message.chat.title == 'GRID9'
    assert obj.chat.pinned_message.chat.username == 'grid9x'
    assert obj.chat.pinned_message.date == 1581868153
    assert obj.chat.pinned_message.text == '/start'
    assert obj.chat.permissions.can_send_messages == True
    assert obj.chat.permissions.can_send_media_messages == True
    assert obj.chat.permissions.can_send_polls == False
    assert obj.chat.permissions.can_send_other_messages == True
    assert obj.chat.permissions.can_add_web_page_previews == False
    assert obj.chat.permissions.can_change_info == False
    assert obj.chat.permissions.can_invite_users == True
    assert obj.chat.permissions.can_pin_messages == True
    assert obj.chat.slow_mode_delay == 5
    assert obj.chat.sticker_set_name == 'channelstickers'
    assert obj.chat.can_set_sticker_set == False


def test_MessageEntity():
    dic = {
        'type': 'any',
        'offset': 2323,
        'length': 44,
        'url': 'any_url',
        'language': 'en'
    }
    obj = types.MessageEntity.de_json(dic)
    assert obj.type == 'any'
    assert obj.offset == 2323
    assert obj.length == 44
    assert obj.url == 'any_url'
    assert obj.user == None
    assert obj.language == 'en'


def test_PhotoSize():
    dic = {
        'file_id': 1111,
        'file_unique_id': 1122,
        'width': 40,
        'height': 40,
        'file_size': 32
    }
    obj = types.PhotoSize.de_json(dic)
    assert obj.file_id == 1111
    assert obj.file_unique_id == 1122
    assert obj.width == 40
    assert obj.height == 40
    assert obj.file_size == 32


def test_Audio():
    dic = {
        'file_id': 1,
        'file_unique_id': 11,
        'duration': 32,
        'performer': 'abc',
        'title': 'test',
        'mime_type': 'type',
        'file_size': 44,
        'thumb': {
            'file_id': 33,
            'file_unique_id': 22,
            'width': 30,
            'height': 22
        }
    }
    obj = types.Audio.de_json(dic)
    assert obj.file_id == 1
    assert obj.file_unique_id == 11
    assert obj.duration == 32
    assert obj.performer == 'abc'
    assert obj.title == 'test'
    assert obj.mime_type == 'type'
    assert obj.file_size == 44
    assert obj.thumb.file_id == 33
    assert obj.thumb.file_unique_id == 22
    assert obj.thumb.width == 30
    assert obj.thumb.height == 22


def test_Document():
    dic = {
        'file_id': 'BQADBQADMwIAAsYifgZ_CEh0u682xwI',
        'file_unique_id': 'CEh0u682xwI',
        'thumb': {
            'file_id': 'AAQFABPJLB0sAAQq17w-li3bzoIfAAIC',
            'file_unique_id': 'CEh0u682xwI',
            'file_size': 1822,
            'width': 90,
            'height': 60
        },
        'file_name': 'Text File',
        'mime_type': 'sticker',
        'file_size': 446
    }
    obj = types.Document.de_json(dic)
    assert obj.file_id == 'BQADBQADMwIAAsYifgZ_CEh0u682xwI'
    assert obj.file_unique_id == 'CEh0u682xwI'
    assert obj.thumb.file_id == 'AAQFABPJLB0sAAQq17w-li3bzoIfAAIC'
    assert obj.thumb.file_unique_id == 'CEh0u682xwI'
    assert obj.thumb.file_size == 1822
    assert obj.thumb.width == 90
    assert obj.thumb.height == 60
    assert obj.file_name == 'Text File'
    assert obj.mime_type == 'sticker'
    assert obj.file_size == 446


def test_Video():
    dic = {
        'file_id': 1,
        'file_unique_id': 2,
        'width': 40,
        'height': 40,
        'duration': 3,
        'thumb': {
            'file_id': 33,
            'file_unique_id': 37,
            'width': 40,
            'height': 40,
            'file_size': 32
        },
        'mime_type': 'mime',
        'file_size': 42
    }
    obj = types.Video.de_json(dic)
    assert obj.file_id == 1
    assert obj.file_unique_id == 2
    assert obj.width == 40
    assert obj.height == 40
    assert obj.duration == 3
    assert obj.thumb.file_id == 33
    assert obj.thumb.file_unique_id == 37
    assert obj.thumb.width == 40
    assert obj.thumb.height == 40
    assert obj.thumb.file_size == 32
    assert obj.mime_type == 'mime'
    assert obj.file_size == 42


def test_Animation():
    dic = {
        "file_id": 1,
        "file_unique_id": 221,
        "width": 60,
        "height": 60,
        "duration": 53,
        "thumb": {
            "file_id": 12,
            "file_unique_id": 22,
            "width": 40,
            "height": 40},
        "file_name": "filename",
        "mime_type": "type",
        "file_size": 64
    }
    obj = types.Animation.de_json(dic)
    assert obj.file_id == 1
    assert obj.file_unique_id == 221
    assert obj.width == 60
    assert obj.height == 60
    assert obj.duration == 53
    assert obj.thumb.file_id == 12
    assert obj.thumb.file_unique_id == 22
    assert obj.thumb.width == 40
    assert obj.thumb.height == 40
    assert obj.file_name == 'filename'
    assert obj.mime_type == 'type'
    assert obj.file_size == 64


def test_Voice():
    dic = {
        "duration": 0,
        "mime_type": "audio/ogg",
        "file_id": "AwcccccccDH1JaB7w_gyFjYQxVAg",
        "file_unique_id": "CEh0u682xwI",
        "file_size": 10481
    }
    obj = types.Voice.de_json(dic)
    assert obj.duration == 0
    assert obj.mime_type == 'audio/ogg'
    assert obj.file_id == 'AwcccccccDH1JaB7w_gyFjYQxVAg'
    assert obj.file_unique_id == 'CEh0u682xwI'
    assert obj.file_size == 10481


def test_VideoNote():
    dic = {
        'file_id': 1,
        'file_unique_id': 2,
        'length': 34,
        'duration': 3,
        'thumb': {
            'file_id': 33,
            'file_unique_id': 37,
            'width': 40,
            'height': 40,
            'file_size': 32
        },
        'file_size': 42
    }
    obj = types.VideoNote.de_json(dic)
    assert obj.file_id == 1
    assert obj.file_unique_id == 2
    assert obj.length == 34
    assert obj.duration == 3
    assert obj.thumb.file_id == 33
    assert obj.thumb.file_unique_id == 37
    assert obj.thumb.width == 40
    assert obj.thumb.height == 40
    assert obj.thumb.file_size == 32
    assert obj.file_size == 42


def test_Contact():
    json_string = {
        'phone_number': '009647815214015',
        'first_name': 'Mustafa',
        'last_name': 'Asaad',
        'user_id': 383324787,
        'vcard': 'vcard'
    }
    contact = types.Contact.de_json(json_string)
    assert contact.phone_number == '009647815214015'
    assert contact.first_name == 'Mustafa'
    assert contact.last_name == 'Asaad'
    assert contact.user_id == 383324787
    assert contact.vcard == 'vcard'


def test_Location():
    dic = {'longitude': 29, 'latitude': 44}
    obj = types.Location.de_json(dic)
    assert obj.longitude == 29
    assert obj.latitude == 44


def test_Venue():
    dic = {
        'location': {
            'latitude': 44,
            'longitude': 29
        },
        'title': 'venue',
        'address': 'any',
        'foursquare_id': 22,
        'foursquare_type': 'any',

    }
    obj = types.Venue.de_json(dic)
    assert obj.location.latitude == 44
    assert obj.location.longitude == 29
    assert obj.title == 'venue'
    assert obj.address == 'any'
    assert obj.foursquare_id == 22
    assert obj.foursquare_type == 'any'


def test_PollOption():
    dic = {
        'text': 'abc',
        'voter_count': 25
    }
    obj = types.PollOption.de_json(dic)
    assert obj.text == 'abc'
    assert obj.voter_count == 25


def test_PollAnswer():
    dic = {
        'poll_id': 2,
        'user': {
            "is_bot": False,
            "id": 383324787,
            "first_name": "Mustafa",
            "last_name": "Asaad",
            "username": "MA24th"
        },
        'option_ids': 44
    }
    obj = types.PollAnswer.de_json(dic)
    assert obj.poll_id == 2
    assert obj.user.is_bot == False
    assert obj.user.id == 383324787
    assert obj.user.first_name == 'Mustafa'
    assert obj.user.last_name == 'Asaad'
    assert obj.user.username == 'MA24th'
    assert obj.option_ids == 44


def test_Poll():
    dic = {
        'id': 444,
        'question': 'is abc?',
        'options': [
            {'text': 'a', 'voter_count': 1},
            {'text': 'b', 'voter_count': 5}
        ],
        'is_closed': False,
        'is_anonymous': True,
        'type': 'gif',
        'allows_multiple_answers': False,
        'correct_option_id': 1
    }
    obj = types.Poll.de_json(dic)
    assert obj.poll_id == 444
    assert obj.question == 'is abc?'
    assert obj.options[0].text == 'a'
    assert obj.options[1].voter_count == 5
    assert obj.is_closed == False
    assert obj.is_anonymous == True
    assert obj.type == 'gif'
    assert obj.allows_multiple_answers == False
    assert obj.correct_option_id == 1


def test_UserProfilePhotos():
    dic = {
        "total_count": 1,
        "photos": [
            [
                {
                    "file_id": "AgADAgADqacxG6wpRwABvEB6fpeIcKS4HAIkAATZH_SpyZjzIwdVAAIC",
                    "file_unique_id": "CEh0u682xwI",
                    "file_size": 6150,  "width": 160, "height": 160
                },
                {
                    "file_id": "AgADAgADqacxG6wpRwABvEB6fpeIcKS4HAIkAATOiTNi_YoJMghVAAIC",
                    "file_unique_id": "CEh0u682xwI",
                    "file_size": 13363, "width": 320, "height": 320
                },
                {
                    "file_id": "AgADAgADqacxG6wpRwABvEB6fpeIcKS4HAIkAAQW4DyFv0-lhglVAAIC",
                    "file_unique_id": "CEh0u682xwI",
                    "file_size": 28347, "width": 640, "height": 640
                },
                {
                    "file_id": "AgADAgADqacxG6wpRwABvEB6fpeIcKS4HAIkAAT50RvJCg0GQApVAAIC",
                    "file_unique_id": "CEh0u682xwI",
                    "file_size": 33953, "width": 800, "height": 800
                }]]}
    obj = types.UserProfilePhotos.de_json(dic)
    assert obj.total_count == 1
    assert obj.photos[0][0].file_id == 'AgADAgADqacxG6wpRwABvEB6fpeIcKS4HAIkAATZH_SpyZjzIwdVAAIC'
    assert obj.photos[0][1].file_unique_id == 'CEh0u682xwI'
    assert obj.photos[0][2].file_size == 28347
    assert obj.photos[0][3].width == 800


def test_File():
    dic = {
        'file_id': 1123,
        'file_unique_id': 3211,
        'file_size': 23,
        'file_path': 'filepath'
    }
    obj = types.File.de_json(dic)
    assert obj.file_id == 1123
    assert obj.file_unique_id == 3211
    assert obj.file_size == 23
    assert obj.file_path == 'filepath'


def test_ReplyKeyboardMarkup():
    dic = r'{"keyboard": []}'
    obj = types.ReplyKeyboardMarkup().to_json()
    assert obj == dic


def test_KeyboardButton():
    dic = r'{"text": "any", "request_contact": "any"}'
    obj = types.KeyboardButton(text='any', request_contact='any',
                               request_location=None, request_poll=None).to_json()
    assert obj == dic


def test_keyboardButtonPollType():
    dic = {
        'type': 'any'
    }
    obj = types.KeyboardButtonPollType.de_json(dic)
    assert obj.poll_type == 'any'


def test_ReplyKeyboardRemove():
    dic = r'{"remove_keyboard": true}'
    obj = types.ReplyKeyboardRemove(selective=None).to_json()
    assert obj == dic


def test_InlineKeyboardMarkup():
    Markup = types.InlineKeyboardMarkup(row_width=2)
    Button = types.InlineKeyboardButton
    Markup.add(Button(text='bt1'))
    Markup.add(Button(text='bt2'))
    Markup.add(Button(text='bt3'))
    obj = Markup.to_json()
    assert obj == r'{"inline_keyboard": [[{"text": "bt1"}], [{"text": "bt2"}], [{"text": "bt3"}]]}'


def test_InlineKeyboardButton():
    obj = types.InlineKeyboardButton(text='text', url='url', callback_data='callback_data', switch_inline_query='switch_inline_query',
                                     switch_inline_query_current_chat='switch_inline_query_current_chat', callback_game='callback_game', pay='pay', login_url='login_url').to_json()
    assert obj == r'{"text": "text", "url": "url", "callback_data": "callback_data", "switch_inline_query": "switch_inline_query", "switch_inline_query_current_chat": "switch_inline_query_current_chat", "callback_game": "callback_game", "pay": "pay", "login_url": "login_url"}'


def test_LoginUrl():
    dic = r'{"url": "any", "forward_text": "ftext", "bot_username": "gu9rdbot", "request_write_access": true}'
    obj = types.LoginUrl(url='any', forward_text='ftext',
                         bot_username='gu9rdbot', request_write_access=True).to_json()
    assert obj == dic


def test_CallbackQuery():
    dic = {
        "id": 1122,
        "from": {
            "id": 383324787,
            "is_bot": False,
            "first_name": "Mustafa",
            "last_name": "Asaad",
            "username": "MA24th",
            "language_code": "en"},
        "message": {
            "message_id": 412,
            "from": {
                "id": 383324787,
                "is_bot": False,
                "first_name": "Mustafa",
                "last_name": "Asaad",
                "username": "MA24th",
                "language_code": "en"},
            "chat": {
                "id": -1001405936102,
                "title": "GRID9",
                "type": "supergroup"},
            "date": 1581869200,
            "text": "/start"
        },
        'inline_message_id': 2234,
        'chat_instance': 'any',
        'data': 'any',
        'game_short_name': 'any'
    }
    obj = types.CallbackQuery.de_json(dic)
    assert obj.id == 1122
    assert obj.from_user.id == 383324787
    assert obj.from_user.is_bot == False
    assert obj.from_user.first_name == 'Mustafa'
    assert obj.from_user.last_name == 'Asaad'
    assert obj.from_user.username == 'MA24th'
    assert obj.from_user.language_code == 'en'
    assert obj.message.message_id == 412
    assert obj.message.from_user.id == 383324787
    assert obj.message.from_user.is_bot == False
    assert obj.message.from_user.first_name == 'Mustafa'
    assert obj.message.from_user.last_name == 'Asaad'
    assert obj.message.from_user.username == 'MA24th'
    assert obj.message.from_user.language_code == 'en'
    assert obj.message.chat.id == -1001405936102
    assert obj.message.chat.title == 'GRID9'
    assert obj.message.chat.type == 'supergroup'
    assert obj.message.date == 1581869200
    assert obj.message.text == '/start'
    assert obj.inline_message_id == 2234
    assert obj.chat_instance == 'any'
    assert obj.data == 'any'
    assert obj.game_short_name == 'any'


def test_ForceReply():
    dic = r'{"force_reply": true, "selective": true}'
    obj = types.ForceReply(selective='okay').to_json()
    assert obj == dic


def test_ChatPhoto():
    dic = {
        'small_file_id': 111,
        'small_file_unique_id': 222,
        'big_file_id': 333,
        'big_file_unique_id': 444
    }
    obj = types.ChatPhoto.de_json(dic)
    assert obj.small_file_id == 111
    assert obj.small_file_unique_id == 222
    assert obj.big_file_id == 333
    assert obj.big_file_unique_id == 444


def test_ChatMember():
    dic = {
        'user': {
            "id": 383324787,
            "is_bot": False,
            "first_name": "Mustafa",
            "last_name": "Asaad",
            "username": "MA24th",
            "language_code": "en"
        },
        'status': 'creator',
        'custom_title': 'DevOps Lion',
        'until_date': None,
        'can_be_edited': False,
        'can_post_messages': True,
        'can_edit_messages': True,
        'can_delete_messages': True,
        'can_restrict_members': True,
        'can_promote_members': True,
        'can_change_info': True,
        'can_invite_users': True,
        'can_pin_messages': True,
        'is_member': True,
        'can_send_messages': True,
        'can_send_media_messages': True,
        'can_send_polls': True,
        'can_send_other_messages': True,
        'can_add_web_page_previews': True
    }
    obj = types.ChatMember.de_json(dic)
    assert obj.user.id == 383324787
    assert obj.user.is_bot == False
    assert obj.user.first_name == 'Mustafa'
    assert obj.user.last_name == 'Asaad'
    assert obj.user.username == 'MA24th'
    assert obj.user.language_code == 'en'
    assert obj.status == 'creator'
    assert obj.custom_title == 'DevOps Lion'
    assert obj.until_date == None
    assert obj.can_be_edited == False
    assert obj.can_post_messages == True
    assert obj.can_edit_messages == True
    assert obj.can_delete_messages == True
    assert obj.can_restrict_members == True
    assert obj.can_promote_members == True
    assert obj.can_change_info == True
    assert obj.can_invite_users == True
    assert obj.can_pin_messages == True
    assert obj.is_member == True
    assert obj.can_send_messages == True
    assert obj.can_send_media_messages == True
    assert obj.can_send_polls == True
    assert obj.can_send_other_messages == True


def test_ChatPermissions():
    dic = {
        'can_send_messages': True,
        'can_send_media_messages': True,
        'can_send_polls': False,
        'can_send_other_messages': True,
        'can_add_web_page_previews': False,
        'can_change_info': False,
        'can_invite_users': True,
        'can_pin_messages': False
    }
    obj = types.ChatPermissions.de_json(dic)
    assert obj.can_send_messages == True
    assert obj.can_send_media_messages == True
    assert obj.can_send_polls == False
    assert obj.can_send_other_messages == True
    assert obj.can_add_web_page_previews == False
    assert obj.can_change_info == False
    assert obj.can_invite_users == True
    assert obj.can_pin_messages == False


def test_ResponseParameters():
    dic = {
        'migrate_to_chat_id': 2342,
        'retry_after': 3232
    }
    obj = types.ResponseParameters.de_json(dic)
    assert obj.migrate_to_chat_id == 2342
    assert obj.retry_after == 3232


def test_InputMedia():
    dic = r'{"type": "any", "media": "any", "caption": "any", "parse_mode": "Markdown"}'
    obj = types.InputMedia(type='any', media='any',
                           caption='any', parse_mode='Markdown').to_json()
    assert obj == dic


def test_InputMediaAnimation():
    dic = r'{"type": "animation", "media": "any", "caption": "any", "parse_mode": "Markdown", "width": 40, "height": 40, "duration": 5}'
    obj = types.InputMediaAnimation(media='any', thumb=None, caption='any',
                                    parse_mode='Markdown', width=40, height=40, duration=5).to_json()
    assert obj == dic


def test_InputMediaDocument():
    dic = r'{"type": "document", "media": "any", "caption": "any", "parse_mode": "Markdown", "thumb": "any"}'
    obj = types.InputMediaDocument(
        media='any', thumb='any', caption='any', parse_mode='Markdown').to_json()
    assert obj == dic


def test_InputMediaAudio():
    dic = r'{"type": "audio", "media": "any", "caption": "any", "parse_mode": "Markdown", "duration": 6, "title": "any"}'
    obj = types.InputMediaAudio(media='any', thumb=None, caption='any',
                                parse_mode='Markdown', duration=6, performer=None, title='any').to_json()
    assert obj == dic


def test_InputMediaPhoto():
    dic = r'{"type": "photo", "media": "any", "caption": "any", "parse_mode": "Markdown"}'
    obj = types.InputMediaPhoto(
        media='any', caption='any', parse_mode='Markdown').to_json()
    assert obj == dic


def test_InputMediaVideo():
    dic = r'{"type": "video", "media": "any", "caption": "any", "parse_mode": "Markdown", "thumb": "any", "width": 40, "height": 40, "duration": 4}'
    obj = types.InputMediaVideo(media='any', thumb='any', caption='any', parse_mode='Markdown',
                                width=40, height=40, duration=4, supports_streaming=None).to_json()
    assert obj == dic


def test_ChosenInlineResult():
    dic = {
        'result_id': 123456,
        'from': {
            "id": 383324787,
            "is_bot": False,
            "first_name": "Mustafa",
            "last_name": "Asaad",
            "username": "MA24th",
            "language_code": "en"
        },
        'query': 'abc',
        'location': {
            'latitude': 44,
            'longitude': 29
        },
        'inline_message_id': 1233
    }
    obj = types.ChosenInlineResult.de_json(dic)
    assert obj.result_id == 123456
    assert obj.from_user.id == 383324787
    assert obj.from_user.is_bot == False
    assert obj.from_user.first_name == 'Mustafa'
    assert obj.from_user.last_name == 'Asaad'
    assert obj.from_user.username == 'MA24th'
    assert obj.from_user.language_code == 'en'
    assert obj.query == 'abc'
    assert obj.location.latitude == 44
    assert obj.location.longitude == 29
    assert obj.inline_message_id == 1233


def test_EncryptedCredentials():
    dic = {
        'data': 'SpyZjzIwdVAAIC',
        'hash': 'AgADAgADqacxG6wpRwABvEB6fpeIcKS4HAIkAATZH',
        'secret': 'secretpwd'
    }
    obj = types.EncryptedCredentials.de_json(dic)
    assert obj.data == 'SpyZjzIwdVAAIC'
    assert obj.hash == 'AgADAgADqacxG6wpRwABvEB6fpeIcKS4HAIkAATZH'
    assert obj.secret == 'secretpwd'


def test_EncryptedPassportElement():
    dic = {
        'type': 'passport',
        'data': 'SpyZjzIwdVAAIC',
        'phone_number': '009647815214015',
        'files': [
            {
                'file_id': 1123,
                'file_unique_id': 3211,
                'file_size': 32,
                'file_date': 155383
            }
        ],
        'front_side': {
            'file_id': 1123,
            'file_unique_id': 3211,
            'file_size': 32,
            'file_date': 155383
        },
        'reverse_side': {
            'file_id': 1123,
            'file_unique_id': 3211,
            'file_size': 32,
            'file_date': 155383
        },
        'selfie': {
            'file_id': 1123,
            'file_unique_id': 3211,
            'file_size': 32,
            'file_date': 155383
        },
        'translation': [
            {
                'file_id': 1123,
                'file_unique_id': 3211,
                'file_size': 32,
                'file_date': 155383
            }
        ],
        'hash': 'AgADAgADqacxG6wpRwABvEB6fpeIcKS4HAIkAATZH'
    }
    obj = types.EncryptedPassportElement.de_json(dic)
    assert obj.type == 'passport'
    assert obj.data == 'SpyZjzIwdVAAIC'
    assert obj.phone_number == '009647815214015'
    assert obj.files[0].file_id == 1123
    assert obj.files[0].file_unique_id == 3211
    assert obj.files[0].file_size == 32
    assert obj.files[0].file_date == 155383
    assert obj.front_side.file_id == 1123
    assert obj.front_side.file_unique_id == 3211
    assert obj.front_side.file_size == 32
    assert obj.front_side.file_date == 155383
    assert obj.reverse_side.file_id == 1123
    assert obj.reverse_side.file_unique_id == 3211
    assert obj.reverse_side.file_size == 32
    assert obj.reverse_side.file_date == 155383
    assert obj.selfie.file_id == 1123
    assert obj.selfie.file_unique_id == 3211
    assert obj.selfie.file_size == 32
    assert obj.selfie.file_date == 155383
    assert obj.translation[0].file_id == 1123
    assert obj.translation[0].file_unique_id == 3211
    assert obj.translation[0].file_size == 32
    assert obj.translation[0].file_date == 155383
    assert obj.hash == 'AgADAgADqacxG6wpRwABvEB6fpeIcKS4HAIkAATZH'


def test_Game():
    dic = {
        'title': 'GameTitle',
        'description': 'GameDescription',
        'photo': [{
            'file_id': 111,
            'file_unique_id': 222,
            'width': 40,
            'height': 40,
            'file_size': 32
        }],
        'text': 'some text',
        'text_entities': [
            {
                'type': 'any',
                'offset': 'all',
                'length': 22,
                'url': 'some url',
                'user': {
                    "id": 383324787,
                    "is_bot": False,
                    "first_name": "Mustafa",
                    "last_name": "Asaad",
                    "username": "MA24th",
                    "language_code": "en"
                },
                'language': 'en'
            },
        ],
        'animation': {
            "file_id": 1,
            "file_unique_id": 221,
            "width": 60,
            "height": 60,
            "duration": 53,
            "thumb": {
                "file_id": 12,
                "file_unique_id": 22,
                "width": 40,
                "height": 40
            },
            "file_name": "filename",
            "mime_type": "type",
            "file_size": 64
        }

    }
    obj = types.Game.de_json(dic)
    assert obj.title == 'GameTitle'
    assert obj.description == 'GameDescription'
    assert obj.photo[0].file_id == 111
    assert obj.photo[0].file_unique_id == 222
    assert obj.photo[0].width == 40
    assert obj.photo[0].height == 40
    assert obj.photo[0].file_size == 32
    assert obj.text == 'some text'
    assert obj.text_entities[0].type == 'any'
    assert obj.text_entities[0].offset == 'all'
    assert obj.text_entities[0].length == 22
    assert obj.text_entities[0].url == 'some url'
    assert obj.text_entities[0].user.id == 383324787
    assert obj.text_entities[0].user.is_bot == False
    assert obj.text_entities[0].user.first_name == 'Mustafa'
    assert obj.text_entities[0].user.last_name == 'Asaad'
    assert obj.text_entities[0].user.username == 'MA24th'
    assert obj.text_entities[0].user.language_code == 'en'
    assert obj.text_entities[0].language == 'en'
    assert obj.animation.file_id == 1
    assert obj.animation.file_unique_id == 221
    assert obj.animation.width == 60
    assert obj.animation.height == 60
    assert obj.animation.duration == 53
    assert obj.animation.thumb.file_id == 12
    assert obj.animation.thumb.file_unique_id == 22
    assert obj.animation.thumb.width == 40
    assert obj.animation.thumb.height == 40
    assert obj.animation.file_name == 'filename'
    assert obj.animation.mime_type == 'type'
    assert obj.animation.file_size == 64


def test_GameHighScore():
    dic = {
        'position': 'player1',
        'user': {
                    "id": 383324787,
                    "is_bot": False,
                    "first_name": "Mustafa",
                    "last_name": "Asaad",
                    "username": "MA24th",
                    "language_code": "en"
        },
        'score': 223
    }
    obj = types.GameHighScore.de_json(dic)
    assert obj.position == 'player1'
    assert obj.user.id == 383324787
    assert obj.user.is_bot == False
    assert obj.user.first_name == 'Mustafa'
    assert obj.user.last_name == 'Asaad'
    assert obj.user.username == 'MA24th'
    assert obj.user.language_code == 'en'


def test_InlineQuery():
    dic = {
        'id': 122,
        'from': {
            "id": 383324787,
            "is_bot": False,
            "first_name": "Mustafa",
            "last_name": "Asaad",
            "username": "MA24th",
            "language_code": "en"
        },
        'location': {
            'latitude': 44,
            'longitude': 29
        },
        'query': 'abc',
        'offset': 'all'
    }
    obj = types.InlineQuery.de_json(dic)
    assert obj.id == 122
    assert obj.from_user.id == 383324787
    assert obj.from_user.is_bot == False
    assert obj.from_user.first_name == 'Mustafa'
    assert obj.from_user.last_name == 'Asaad'
    assert obj.from_user.username == 'MA24th'
    assert obj.from_user.language_code == 'en'
    assert obj.location.latitude == 44
    assert obj.location.longitude == 29
    assert obj.query == 'abc'
    assert obj.offset == 'all'


def test_InlineQueryResult():
    pass


def test_InlineQueryResultArticle():
    dic = r'{"type": "article", "id": 24, "title": "article", "input_message_content": "any"}'
    obj = types.InlineQueryResultArticle(
        id=24, title='article', input_message_content='any').to_json()
    assert obj == dic


def test_InlineQueryResultAudio():
    dic = r'{"type": "audio", "id": 24, "audio_url": "url", "title": "audio"}'
    obj = types.InlineQueryResultAudio(
        id=24, audio_url='url', title='audio').to_json()
    assert obj == dic


def test_InlineQueryResultCachedAudio():
    dic = r'{"type": "audio", "id": 24, "audio_file_id": 12}'
    obj = types.InlineQueryResultCachedAudio(
        type='audio', id=24, audio_file_id=12).to_json()
    assert obj == dic


def test_InlineQueryResultCachedDocument():
    dic = r'{"type": "document", "id": 24, "document_file_id": 12}'
    obj = types.InlineQueryResultCachedDocument(
        type='document', id=24, document_file_id=12).to_json()
    assert obj == dic


def test_InlineQueryResultCachedGif():
    dic = r'{"type": "gif", "id": 24, "gif_file_id": 12, "title": "giftitle", "caption": "gifcaption", "parse_mode": "Markdown", "input_message_content": "any"}'
    obj = types.InlineQueryResultCachedGif(type='gif', id=24, gif_file_id=12, title='giftitle',
                                           caption='gifcaption', parse_mode='Markdown', reply_markup=None, input_message_content='any').to_json()
    assert obj == dic


def test_InlineQueryResultCachedMpeg4Gif():
    dic = r'{"type": "mpeg4gif", "id": 24, "mpeg4_file_id": 12}'
    obj = types.InlineQueryResultCachedMpeg4Gif(
        type='mpeg4gif', id=24, mpeg4_file_id=12).to_json()
    assert obj == dic


def test_InlineQueryResultCachedPhoto():
    dic = r'{"type": "photo", "id": 122, "photo_url": "photourl", "thumb_url": "thumburl", "title": "tiltle", "description": "description", "caption": "caption", "parse_mode": "Markdown", "input_message_content": "any"}'
    obj = types.InlineQueryResultCachedPhoto(type='photo', id=122, photo_url='photourl', thumb_url='thumburl', photo_width=30, photo_height=30,
                                             title='tiltle', description='description', caption='caption', parse_mode='Markdown', reply_markup=None, input_message_content='any').to_json()
    assert obj == dic


def test_InlineQueryResultCachedSticker():
    dic = r'{"type": "sticker", "id": 24, "sticker_file_id": 12}'
    obj = types.InlineQueryResultCachedSticker(
        type='sticker', id=24, sticker_file_id=12).to_json()
    assert obj == dic


def test_InlineQueryResultCachedVideo():
    dic = r'{"type": "video", "id": 24, "video_file_id": 12}'
    obj = types.InlineQueryResultCachedVideo(
        type='video', id=24, video_file_id=12).to_json()
    assert obj == dic


def test_InlineQueryResultCachedVoice():
    dic = r'{"type": "voice", "id": 24, "voice_file_id": 12}'
    obj = types.InlineQueryResultCachedVoice(
        type='voice', id=24, voice_file_id=12).to_json()
    assert obj == dic


def test_InlineQueryResultContact():
    dic = r'{"type": "contact", "id": 383324787, "phone_number": "009647815214015", "first_name": "Mustafa"}'
    obj = types.InlineQueryResultContact(
        id=383324787, phone_number='009647815214015', first_name='Mustafa').to_json()
    assert obj == dic


def test_InlineQueryResultGame():
    dic = r'{"type": "game", "id": 24, "game_short_name": "gamename"}'
    obj = types.InlineQueryResultGame(
        id=24, game_short_name='gamename').to_json()
    assert obj == dic


def test_InlineQueryResultDocument():
    dic = r'{"type": "document", "id": 24, "title": "title", "document_url": "durl", "mime_type": "any"}'
    obj = types.InlineQueryResultDocument(
        id=24, title='title', document_url='durl', mime_type='any').to_json()
    assert obj == dic


def test_InlineQueryResultGif():
    dic = r'{"type": "gif", "id": 24, "gif_url": "gurl", "thumb_url": "any"}'
    obj = types.InlineQueryResultGif(
        id=24, gif_url='gurl', thumb_url='any').to_json()
    assert obj == dic


def test_InlineQueryResultLocation():
    dic = r'{"type": "location", "id": 24, "title": "Baghdad", "latitude": 39, "longitude": 44}'
    obj = types.InlineQueryResultLocation(
        id=24, title='Baghdad', latitude=39, longitude=44).to_json()
    assert obj == dic


def test_InlineQueryResultMpeg4Gif():
    dic = r'{"type": "mpeg4_gif", "id": 24, "mpeg4_url": "mpurl", "thumb_url": "thurl"}'
    obj = types.InlineQueryResultMpeg4Gif(
        id=24, mpeg4_url='mpurl', thumb_url='thurl').to_json()
    assert obj == dic


def test_InlineQueryResultPhoto():
    dic = r'{"type": "photo", "id": 24, "photo_url": "phurl", "thumb_url": "thurl"}'
    obj = types.InlineQueryResultPhoto(
        id=24, photo_url='phurl', thumb_url='thurl').to_json()
    assert obj == dic


def test_InlineQueryResultVenue():
    dic = r'{"type": "venue", "id": 24, "title": "any", "latitude": 29, "longitude": 44, "address": "any"}'
    obj = types.InlineQueryResultVenue(
        id=24, title='any', latitude=29, longitude=44, address='any').to_json()
    assert obj == dic


def test_InlineQueryResultVideo():
    dic = r'{"type": "video", "id": 24, "video_url": "vurl", "mime_type": "mtype", "thumb_url": "thurl", "title": "any"}'
    obj = types.InlineQueryResultVideo(
        id=24, video_url='vurl', mime_type='mtype', thumb_url='thurl', title='any').to_json()
    assert obj == dic


def test_InlineQueryResultVoice():
    dic = r'{"type": "voice", "id": 24, "voice_url": "vurl", "title": "any"}'
    obj = types.InlineQueryResultVoice(
        id=24, voice_url='vurl', title='any').to_json()
    assert obj == dic


def InputMessageContent():
    pass


def test_InputContactMessageContent():
    dic = {
        'phone_number': '009647815214015',
        'first_name': 'Mustafa',
        'last_name': 'Asaad'
    }
    obj = types.InputContactMessageContent(
        phone_number='009647815214015', first_name='Mustafa', last_name='Asaad').to_dic()
    assert obj == dic


def test_InputLocationMessageContent():
    dic = {
        'latitude': 29,
        'live_period': 15,
        'longitude': 44
    }
    obj = types.InputLocationMessageContent(
        latitude=29, longitude=44, live_period=15).to_dic()
    assert obj == dic


def test_InputTextMessageContent():
    dic = {
        'message_text': 'any',
        'parse_mode': 'Markdown',
        'disable_web_page_preview': True
    }
    obj = types.InputTextMessageContent(
        message_text='any', parse_mode='Markdown', disable_web_page_preview=True).to_dic()
    assert obj == dic


def test_InputVenueMessageContent():
    dic = {
        'latitude': 29,
        'longitude': 44,
        'title': 'any',
        'address': 'ad',
        'foursquare_id': 55,
        'foursquare_type': 'any'
    }
    obj = types.InputVenueMessageContent(
        latitude=29, longitude=44, title='any', address='ad', foursquare_id=55, foursquare_type='any').to_dic()
    assert obj == dic


def test_Invoice():
    dic = {
        'title': 'any',
        'description': 'dany',
        'start_parameter': 'a',
        'currency': 'usd',
        'total_amount': 20
    }
    obj = types.Invoice.de_json(dic)
    assert obj.title == 'any'
    assert obj.description == 'dany'
    assert obj.start_parameter == 'a'
    assert obj.currency == 'usd'
    assert obj.total_amount == 20


def test_LabeledPrice():
    dic = r'{"label": "apple", "amount": 2}'
    obj = types.LabeledPrice(label='apple', amount=2).to_json()
    assert obj == dic


def test_MaskPosition():
    dic = {
        'point': 22,
        'x_shift': 330,
        'y_shift': 55,
        'scale': 40
    }
    obj = types.MaskPosition.de_json(dic)
    assert obj.point == 22
    assert obj.x_shift == 330
    assert obj.y_shift == 55
    assert obj.scale == 40


def test_OrderInfo():
    dic = {
        'name': 'namey',
        'phone_number': '11223344',
        'email': 'ma24th@yahoo.com',
        'shipping_address': {
            'country_code': 'iq',
            'state': 'Diyala',
            'city': 'Khalis',
            'street_line1': 'KH 32th',
            'street_line2': 'KH 32th',
            'post_code': 32006
        }
    }
    obj = types.OrderInfo.de_json(dic)
    assert obj.name == 'namey'
    assert obj.phone_number == '11223344'
    assert obj.email == 'ma24th@yahoo.com'
    assert obj.shipping_address.country_code == 'iq'
    assert obj.shipping_address.state == 'Diyala'
    assert obj.shipping_address.city == 'Khalis'
    assert obj.shipping_address.street_line1 == 'KH 32th'
    assert obj.shipping_address.street_line2 == 'KH 32th'
    assert obj.shipping_address.post_code == 32006


def test_PassportData():
    dic = {
        'EncryptedPassportElement': '12u8kadf',
        'EncryptedCredentials': 'djladjf:dkjfaklj'
    }
    obj = types.PassportData.de_json(dic)
    assert obj.data == '12u8kadf'
    assert obj.credentials == "djladjf:dkjfaklj"


def test_ShippingOption():
    dic = r'{"id": 23, "title": "apple", "prices": []}'
    obj = types.ShippingOption(id=23, title='apple').to_json()
    assert obj == dic
