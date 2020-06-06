from tgbotapi import types


def test_update():
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
    assert obj.message.from_user.is_bot is False
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
    assert obj.edited_message is None
    assert obj.channel_post is None
    assert obj.edited_channel_post is None
    assert obj.inline_query is None
    assert obj.chosen_inline_result is None
    assert obj.callback_query is None
    assert obj.shipping_query is None
    assert obj.pre_checkout_query is None
    assert obj.poll is None
    assert obj.poll_answer is None


def test_webhook_info():
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
    assert None == obj.has_custom_certificate
    assert obj.pending_update_count == 1
    assert obj.last_error_date == 155555
    assert obj.last_error_message == 'abc'
    assert obj.max_connections == 44
    assert obj.allowed_updates == 'au'


def test_user():
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
    assert user.last_name is None
    assert user.is_bot is True
    assert user.username == '@gu9rdbot'
    assert user.language_code == 'en'
    assert user.can_join_groups is True
    assert user.can_read_all_group_messages is False
    assert user.supports_inline_queries is True


def test_chat():
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
    assert obj.first_name is None
    assert obj.last_name is None
    assert obj.photo.small_file_id == 111
    assert obj.photo.small_file_unique_id == 222
    assert obj.photo.big_file_id == 333
    assert obj.photo.big_file_unique_id == 444
    assert obj.description == 'group description'
    assert obj.invite_link is None
    assert obj.pinned_message.message_id == 26
    assert obj.pinned_message.chat.id == -1001184458459
    assert obj.pinned_message.chat.title == 'GRID9'
    assert obj.pinned_message.chat.username == 'grid9x'
    assert obj.pinned_message.chat.type == 'channel'
    assert obj.pinned_message.chat.first_name is None
    assert obj.pinned_message.chat.last_name is None
    assert obj.pinned_message.chat.photo is None
    assert obj.pinned_message.chat.description is None
    assert obj.pinned_message.chat.invite_link is None
    assert obj.pinned_message.chat.pinned_message is None
    assert obj.pinned_message.chat.permissions is None
    assert obj.pinned_message.chat.slow_mode_delay is None
    assert obj.pinned_message.chat.sticker_set_name is None
    assert obj.pinned_message.chat.can_set_sticker_set is None
    assert obj.pinned_message.date == 1581868153
    assert obj.pinned_message.text == '/start'
    assert obj.permissions.can_send_messages is True
    assert obj.permissions.can_send_media_messages is True
    assert obj.permissions.can_send_polls is False
    assert obj.permissions.can_send_other_messages is True
    assert obj.permissions.can_add_web_page_previews is False
    assert obj.permissions.can_change_info is False
    assert obj.permissions.can_invite_users is True
    assert obj.permissions.can_pin_messages is True
    assert obj.slow_mode_delay == 5
    assert obj.sticker_set_name == 'channelstickers'
    assert obj.can_set_sticker_set is False


def test_message():
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
    assert obj.from_user.is_bot is False
    assert obj.from_user.first_name == 'Mustafa'
    assert obj.from_user.last_name == 'Asaad'
    assert obj.from_user.language_code == 'en'
    assert obj.date == 15553332
    assert obj.chat.id == -1001184458459
    assert obj.chat.type == 'channel'
    assert obj.chat.title == 'GRID9'
    assert obj.chat.username == 'grid9x'
    assert obj.chat.first_name is None
    assert obj.chat.last_name is None
    assert obj.chat.photo.small_file_id == 111
    assert obj.chat.photo.small_file_unique_id == 222
    assert obj.chat.photo.big_file_id == 333
    assert obj.chat.photo.big_file_unique_id == 444
    assert obj.chat.description == 'group description'
    assert obj.chat.invite_link is None
    assert obj.chat.pinned_message.message_id == 26
    assert obj.chat.pinned_message.chat.id == -1001184458459
    assert obj.chat.pinned_message.chat.type == 'channel'
    assert obj.chat.pinned_message.chat.title == 'GRID9'
    assert obj.chat.pinned_message.chat.username == 'grid9x'
    assert obj.chat.pinned_message.date == 1581868153
    assert obj.chat.pinned_message.text == '/start'
    assert obj.chat.permissions.can_send_messages is True
    assert obj.chat.permissions.can_send_media_messages is True
    assert obj.chat.permissions.can_send_polls is False
    assert obj.chat.permissions.can_send_other_messages is True
    assert obj.chat.permissions.can_add_web_page_previews is False
    assert obj.chat.permissions.can_change_info is False
    assert obj.chat.permissions.can_invite_users is True
    assert obj.chat.permissions.can_pin_messages is True
    assert obj.chat.slow_mode_delay == 5
    assert obj.chat.sticker_set_name == 'channelstickers'
    assert obj.chat.can_set_sticker_set is False


def test_message_entity():
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
    assert obj.user is None
    assert obj.language == 'en'


def test_photo_size():
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


def test_audio():
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
            'height': 22,
            'file_size': 12
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
    assert obj.thumb.file_size == 12


def test_document():
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


def test_video():
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


def test_animation():
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
            "height": 40,
            "file_size": 32},
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
    assert obj.thumb.file_size == 32
    assert obj.file_name == 'filename'
    assert obj.mime_type == 'type'
    assert obj.file_size == 64


def test_voice():
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


def test_video_note():
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


def test_contact():
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


def test_location():
    dic = {'longitude': 29, 'latitude': 44}
    obj = types.Location.de_json(dic)
    assert obj.longitude == 29
    assert obj.latitude == 44


def test_venue():
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


def test_poll_option():
    dic = {
        'text': 'abc',
        'voter_count': 25
    }
    obj = types.PollOption.de_json(dic)
    assert obj.text == 'abc'
    assert obj.voter_count == 25


def test_poll_answer():
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
    assert obj.user.is_bot is False
    assert obj.user.id == 383324787
    assert obj.user.first_name == 'Mustafa'
    assert obj.user.last_name == 'Asaad'
    assert obj.user.username == 'MA24th'
    assert obj.option_ids == 44


def test_poll():
    dic = {
        'id': 444,
        'question': 'is abc?',
        'options': [
            {'text': 'a', 'voter_count': 1},
            {'text': 'b', 'voter_count': 5}
        ],
        'total_voter_count': 1003,
        'is_closed': False,
        'is_anonymous': True,
        'type': 'gif',
        'allows_multiple_answers': False,
        'correct_option_id': 1
    }
    obj = types.Poll.de_json(dic)
    assert obj.id == 444
    assert obj.question == 'is abc?'
    assert obj.options[0].text == 'a'
    assert obj.options[1].voter_count == 5
    assert obj.total_voter_count == 1003
    assert obj.is_closed is False
    assert obj.is_anonymous is True
    assert obj.type == 'gif'
    assert obj.allows_multiple_answers is False
    assert obj.correct_option_id == 1


def test_user_profile_photos():
    dic = {
        "total_count": 1,
        "photos": [
            [
                {
                    "file_id": "AgADAgADqacxG6wpRwABvEB6fpeIcKS4HAIkAATZH_SpyZjzIwdVAAIC",
                    "file_unique_id": "CEh0u682xwI",
                    "file_size": 6150, "width": 160, "height": 160
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


def test_file():
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


def test_reply_keyboard_markup():
    dic = r'{"keyboard": []}'
    obj = types.ReplyKeyboardMarkup().to_json()
    assert obj == dic


def test_keyboard_button():
    dic = r'{"text": "any", "request_contact": "any"}'
    obj = types.KeyboardButton(text='any', request_contact='any',
                               request_location=None, request_poll=None).to_json()
    assert obj == dic


def test_keyboard_button_poll_type():
    dic = {
        'type': 'any'
    }
    obj = types.KeyboardButtonPollType.de_json(dic)
    assert obj.type == 'any'


def test_reply_keyboard_remove():
    dic = r'{"remove_keyboard": true}'
    obj = types.ReplyKeyboardRemove(selective=None).to_json()
    assert obj == dic


def test_inline_keyboard_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    button = types.InlineKeyboardButton
    markup.add(button(text='bt1'))
    markup.add(button(text='bt2'))
    markup.add(button(text='bt3'))
    obj = markup.to_json()
    assert obj == r'{"inline_keyboard": [[{"text": "bt1"}], [{"text": "bt2"}], [{"text": "bt3"}]]}'


def test_inline_keyboard_button():
    obj = types.InlineKeyboardButton(text='text', url='url', callback_data='callback_data',
                                     switch_inline_query='switch_inline_query',
                                     switch_inline_query_current_chat='switch_inline_query_current_chat',
                                     callback_game='callback_game', pay='pay', login_url='login_url').to_json()
    assert obj == r'{"text": "text", "url": "url", "callback_data": "callback_data", "switch_inline_query": "switch_inline_query", "switch_inline_query_current_chat": "switch_inline_query_current_chat", "callback_game": "callback_game", "pay": "pay", "login_url": "login_url"}'


def test_login_url():
    dic = r'{"url": "any", "forward_text": "ftext", "bot_username": "gu9rdbot", "request_write_access": true}'
    obj = types.LoginUrl(url='any', forward_text='ftext',
                         bot_username='gu9rdbot', request_write_access=True).to_json()
    assert obj == dic


def test_call_back_query():
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
    assert obj.from_user.is_bot is False
    assert obj.from_user.first_name == 'Mustafa'
    assert obj.from_user.last_name == 'Asaad'
    assert obj.from_user.username == 'MA24th'
    assert obj.from_user.language_code == 'en'
    assert obj.message.message_id == 412
    assert obj.message.from_user.id == 383324787
    assert obj.message.from_user.is_bot is False
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


def test_force_reply():
    dic = r'{"force_reply": true, "selective": true}'
    obj = types.ForceReply(selective='okay').to_json()
    assert obj == dic


def test_chat_photo():
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


def test_chat_member():
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
    assert obj.user.is_bot is False
    assert obj.user.first_name == 'Mustafa'
    assert obj.user.last_name == 'Asaad'
    assert obj.user.username == 'MA24th'
    assert obj.user.language_code == 'en'
    assert obj.status == 'creator'
    assert obj.custom_title == 'DevOps Lion'
    assert obj.until_date is None
    assert obj.can_be_edited is False
    assert obj.can_post_messages is True
    assert obj.can_edit_messages is True
    assert obj.can_delete_messages is True
    assert obj.can_restrict_members is True
    assert obj.can_promote_members is True
    assert obj.can_change_info is True
    assert obj.can_invite_users is True
    assert obj.can_pin_messages is True
    assert obj.is_member is True
    assert obj.can_send_messages is True
    assert obj.can_send_media_messages is True
    assert obj.can_send_polls is True
    assert obj.can_send_other_messages is True


def test_chat_permissions():
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
    assert obj.can_send_messages is True
    assert obj.can_send_media_messages is True
    assert obj.can_send_polls is False
    assert obj.can_send_other_messages is True
    assert obj.can_add_web_page_previews is False
    assert obj.can_change_info is False
    assert obj.can_invite_users is True
    assert obj.can_pin_messages is False


def test_bot_commands():
    dic = {
        'command': 'command name',
        'description': 'command description'
    }
    obj = types.BotCommand.de_json(dic)
    assert obj.command == 'command name'
    assert obj.description == 'command description'


def test_response_parameters():
    dic = {
        'migrate_to_chat_id': 2342,
        'retry_after': 3232
    }
    obj = types.ResponseParameters.de_json(dic)
    assert obj.migrate_to_chat_id == 2342
    assert obj.retry_after == 3232


# def test_input_media():
#     dic = r'{"type": "any", "media": "any", "caption": "any", "parse_mode": "Markdown"}'
#     obj = types.InputMedia(type='any', media='any', caption='any', parse_mode='Markdown').to_json()
#     assert obj == dic

def test_input_media_photo():
    dic = r'{"type": "photo", "media": "any", "caption": "any", "parse_mode": "Markdown"}'
    obj = types.InputMedia().Photo(type='photo', media='any', caption='any', parse_mode='Markdown').to_json()
    assert obj == dic


def test_input_media_video():
    dic = r'{"type": "video", "media": "any", "thumb": "any", "caption": "any", "parse_mode": "Markdown", "width": 40, ' \
          r'"height": 40, "duration": 4, "supports_streaming": false}'
    obj = types.InputMedia().Video(type='video', media='any', thumb='any', caption='any', parse_mode='Markdown',
                                   width=40, height=40, duration=4).to_json()
    assert obj == dic


def test_input_media_animation():
    dic = r'{"type": "animation", "media": "any", "thumb": "any", "caption": "abc", "parse_mode": "Markdown", "width": 12, "height": 12, "duration": 5}'
    obj = types.InputMedia().Animation(type='animation', media='any', thumb='any', caption='abc', parse_mode='Markdown',
                                       width=12, height=12, duration=5).to_json()
    assert obj == dic


def test_input_media_document():
    dic = r'{"type": "document", "media": "any", "thumb": "any", "caption": "any", "parse_mode": "Markdown"}'
    obj = types.InputMedia().Document(type='document', media='any', thumb='any', caption='any',
                                      parse_mode='Markdown').to_json()
    assert obj == dic


def test_input_media_audio():
    dic = r'{"type": "audio", "media": "any", "caption": "any", "parse_mode": "Markdown", "duration": 6, "title": "any"}'
    obj = types.InputMedia().Audio(type="audio", media='any', thumb=None, caption='any', parse_mode='Markdown',
                                   duration=6, performer=None, title='any').to_json()
    assert obj == dic


def test_input_file():
    pass


def test_sticker():
    dic = {
        'file_id': 222,
        'file_unique_id': 2323,
        'width': 30,
        'height': 20,
        'is_animated': True,
        'emoji': '🐣',
        'set_name': 'st',
        'file_size': 32
    }
    obj = types.Sticker.de_json(dic)
    assert obj.file_id == 222
    assert obj.file_unique_id == 2323
    assert obj.width == 30
    assert obj.height == 20
    assert obj.is_animated is True
    assert obj.thumb is None
    assert obj.emoji == '🐣'
    assert obj.set_name == 'st'
    assert obj.mask_position is None
    assert obj.file_size == 32


def test_sticker_set():
    dic = {
        'name': 'stt',
        'title': 'sst',
        'contains_masks': False,
        'stickers': [
            {'file_id': 222, 'file_unique_id': 2323, 'width': 30, 'height': 20, 'is_animated': True, 'emoji': '🐣',
             'set_name': 'st', 'file_size': 32}],
        'thumb': {
            'file_id': 1111,
            'file_unique_id': 1122,
            'width': 40,
            'height': 40,
            'file_size': 32
        }
    }
    obj = types.StickerSet.de_json(dic)
    assert obj.name == 'stt'
    assert obj.title == 'sst'
    assert obj.contains_masks is False
    assert obj.stickers[0].file_id == 222
    assert obj.stickers[0].file_unique_id == 2323
    assert obj.stickers[0].width == 30
    assert obj.thumb.file_id == 1111
    assert obj.thumb.file_unique_id == 1122
    assert obj.thumb.width == 40
    assert obj.thumb.height == 40
    assert obj.thumb.file_size == 32


def test_mask_position():
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


def test_inline_query():
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
    assert obj.from_user.is_bot is False
    assert obj.from_user.first_name == 'Mustafa'
    assert obj.from_user.last_name == 'Asaad'
    assert obj.from_user.username == 'MA24th'
    assert obj.from_user.language_code == 'en'
    assert obj.location.latitude == 44
    assert obj.location.longitude == 29
    assert obj.query == 'abc'
    assert obj.offset == 'all'


def test_inline_query_result():
    pass


def test_inline_query_result_article():
    dic = r'{"type": "article", "id": 24, "title": "article", "input_message_content": "any"}'
    obj = types.InlineQueryResult().Article(id=24, title='article', input_message_content='any').to_json()
    assert obj == dic


def test_inline_query_result_audio():
    dic = r'{"type": "audio", "id": 24, "audio_url": "url", "title": "audio"}'
    obj = types.InlineQueryResult().Audio(id=24, audio_url='url', title='audio').to_json()
    assert obj == dic


def test_inline_query_result_cached_audio():
    dic = r'{"type": "audio", "id": 24, "audio_file_id": 12}'
    obj = types.InlineQueryResult().CachedAudio(type='audio', id=24, audio_file_id=12).to_json()
    assert obj == dic


def test_inline_query_result_cached_document():
    dic = r'{"type": "document", "id": 24, "document_file_id": 12}'
    obj = types.InlineQueryResult().CachedDocument(
        type='document', id=24, document_file_id=12).to_json()
    assert obj == dic


def test_inline_query_result_cached_gif():
    dic = r'{"type": "gif", "id": 24, "gif_file_id": 12, "title": "giftitle", "caption": "gifcaption", "parse_mode": "Markdown", "input_message_content": "any"}'
    obj = types.InlineQueryResult().CachedGif(type='gif', id=24, gif_file_id=12, title='giftitle', caption='gifcaption',
                                              parse_mode='Markdown', reply_markup=None,
                                              input_message_content='any').to_json()
    assert obj == dic


def test_inline_query_result_cached_mpeg4gif():
    dic = r'{"type": "mpeg4gif", "id": 24, "mpeg4_file_id": 12}'
    obj = types.InlineQueryResult().CachedMpeg4Gif(
        type='mpeg4gif', id=24, mpeg4_file_id=12).to_json()
    assert obj == dic


def test_inline_query_result_cached_photo():
    dic = r'{"type": "photo", "id": 122, "photo_url": "photourl", "thumb_url": "thumburl", "title": "tiltle", "description": "description", "caption": "caption", "parse_mode": "Markdown", "input_message_content": "any"}'
    obj = types.InlineQueryResult().CachedPhoto(type='photo', id=122, photo_url='photourl', thumb_url='thumburl',
                                                photo_width=30, photo_height=30, title='tiltle',
                                                description='description', caption='caption', parse_mode='Markdown',
                                                reply_markup=None, input_message_content='any').to_json()
    assert obj == dic


def test_inline_query_result_cached_sticker():
    dic = r'{"type": "sticker", "id": 24, "sticker_file_id": 12}'
    obj = types.InlineQueryResult().CachedSticker(
        type='sticker', id=24, sticker_file_id=12).to_json()
    assert obj == dic


def test_inline_query_result_cached_video():
    dic = r'{"type": "video", "id": 24, "video_file_id": 12}'
    obj = types.InlineQueryResult().CachedVideo(
        type='video', id=24, video_file_id=12).to_json()
    assert obj == dic


def test_inline_query_result_cached_voice():
    dic = r'{"type": "voice", "id": 24, "voice_file_id": 12}'
    obj = types.InlineQueryResult().CachedVoice(
        type='voice', id=24, voice_file_id=12).to_json()
    assert obj == dic


def test_inline_query_result_contact():
    dic = r'{"type": "contact", "id": 383324787, "phone_number": "009647815214015", "first_name": "Mustafa"}'
    obj = types.InlineQueryResult().Contact(
        id=383324787, phone_number='009647815214015', first_name='Mustafa').to_json()
    assert obj == dic


def test_inline_query_result_game():
    dic = r'{"type": "game", "id": 24, "game_short_name": "gamename"}'
    obj = types.InlineQueryResult().Game(
        id=24, game_short_name='gamename').to_json()
    assert obj == dic


def test_inline_query_result_document():
    dic = r'{"type": "document", "id": 24, "title": "title", "document_url": "durl", "mime_type": "any"}'
    obj = types.InlineQueryResult().Document(
        id=24, title='title', document_url='durl', mime_type='any').to_json()
    assert obj == dic


def test_inline_query_result_gif():
    dic = r'{"type": "gif", "id": 24, "gif_url": "gurl", "thumb_url": "any"}'
    obj = types.InlineQueryResult().Gif(
        id=24, gif_url='gurl', thumb_url='any').to_json()
    assert obj == dic


def test_inline_query_result_location():
    dic = r'{"type": "location", "id": 24, "title": "Baghdad", "latitude": 39, "longitude": 44}'
    obj = types.InlineQueryResult().Location(
        id=24, title='Baghdad', latitude=39, longitude=44).to_json()
    assert obj == dic


def test_inline_query_result_mpeg4gif():
    dic = r'{"type": "mpeg4_gif", "id": 24, "mpeg4_url": "mpurl", "thumb_url": "thurl"}'
    obj = types.InlineQueryResult().Mpeg4Gif(
        id=24, mpeg4_url='mpurl', thumb_url='thurl').to_json()
    assert obj == dic


def test_inline_query_result_photo():
    dic = r'{"type": "photo", "id": 24, "photo_url": "phurl", "thumb_url": "thurl"}'
    obj = types.InlineQueryResult().Photo(
        id=24, photo_url='phurl', thumb_url='thurl').to_json()
    assert obj == dic


def test_inline_query_result_venue():
    dic = r'{"type": "venue", "id": 24, "title": "any", "latitude": 29, "longitude": 44, "address": "any"}'
    obj = types.InlineQueryResult().Venue(
        id=24, title='any', latitude=29, longitude=44, address='any').to_json()
    assert obj == dic


def test_inline_query_result_video():
    dic = r'{"type": "video", "id": 24, "video_url": "vurl", "mime_type": "mtype", "thumb_url": "thurl", "title": "any"}'
    obj = types.InlineQueryResult().Video(
        id=24, video_url='vurl', mime_type='mtype', thumb_url='thurl', title='any').to_json()
    assert obj == dic


def test_inline_query_result_voice():
    dic = r'{"type": "voice", "id": 24, "voice_url": "vurl", "title": "any"}'
    obj = types.InlineQueryResult().Voice(
        id=24, voice_url='vurl', title='any').to_json()
    assert obj == dic


def test_input_message_content():
    pass


def test_input_contact_message_content():
    dic = {
        'phone_number': '009647815214015',
        'first_name': 'Mustafa',
        'last_name': 'Asaad'
    }
    obj = types.InputMessageContent().Contact(phone_number='009647815214015', first_name='Mustafa',
                                              last_name='Asaad').to_dict()
    assert obj == dic


def test_input_location_message_content():
    dic = {
        'latitude': 29,
        'live_period': 15,
        'longitude': 44
    }
    obj = types.InputMessageContent().Location(latitude=29, longitude=44, live_period=15).to_dict()
    assert obj == dic


def test_input_text_message_content():
    dic = {
        'message_text': 'any',
        'parse_mode': 'Markdown',
        'disable_web_page_preview': True
    }
    obj = types.InputMessageContent().Text(message_text='any', parse_mode='Markdown',
                                           disable_web_page_preview=True).to_dict()
    assert obj == dic


def test_input_venue_message_content():
    dic = {
        'latitude': 29,
        'longitude': 44,
        'title': 'any',
        'address': 'ad',
        'foursquare_id': 55,
        'foursquare_type': 'any'
    }
    obj = types.InputMessageContent().Venue(
        latitude=29, longitude=44, title='any', address='ad', foursquare_id=55, foursquare_type='any').to_dict()
    assert obj == dic


def test_chosen_inline_result():
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
    assert obj.from_user.is_bot is False
    assert obj.from_user.first_name == 'Mustafa'
    assert obj.from_user.last_name == 'Asaad'
    assert obj.from_user.username == 'MA24th'
    assert obj.from_user.language_code == 'en'
    assert obj.query == 'abc'
    assert obj.location.latitude == 44
    assert obj.location.longitude == 29
    assert obj.inline_message_id == 1233


def test_labeled_price():
    dic = r'{"label": "apple", "amount": 2}'
    obj = types.LabeledPrice(label='apple', amount=2).to_json()
    assert obj == dic


def test_invoice():
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


def test_shipping_address():
    dic = {
        'country_code': 'iq',
        'state': 'Diyala',
        'city': 'Khalis',
        'street_line1': 'Kh 32006 44 st',
        'street_line2': None,
        'post_code': 32006
    }
    obj = types.ShippingAddress.de_json(dic)
    assert obj.country_code == 'iq'
    assert obj.state == 'Diyala'
    assert obj.city == 'Khalis'
    assert obj.street_line1 == 'Kh 32006 44 st'
    assert obj.street_line2 is None
    assert obj.post_code == 32006


def test_order_info():
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


def test_shipping_option():
    dic = r'{"id": 23, "title": "apple", "prices": []}'
    obj = types.ShippingOption(id=23, title='apple').to_json()
    assert obj == dic


def test_successful_payment():
    dic = {
        'currency': 'IQD',
        'total_amount': 25000,
        'invoice_payload': 'trans',
        'telegram_payment_charge_id': 2232,
        'provider_payment_charge_id': 2333
    }
    obj = types.SuccessfulPayment.de_json(dic)
    assert obj.currency == 'IQD'
    assert obj.total_amount == 25000
    assert obj.invoice_payload == 'trans'
    assert obj.shipping_option_id is None
    assert obj.order_info is None
    assert obj.telegram_payment_charge_id == 2232
    assert obj.provider_payment_charge_id == 2333


def test_shipping_query():
    dic = {
        'id': 22,
        'from': {
            "id": 383324787,
            "is_bot": False,
            "first_name": "Mustafa",
            "last_name": "Asaad",
            "username": "MA24th",
            "language_code": "en"},
        'invoice_payload': 'abc',
        'shipping_address': {
            'country_code': 'iq',
            'state': 'Diyala',
            'city': 'Khalis',
            'street_line1': 'Kh 32006 44 st',
            'street_line2': None,
            'post_code': 32006}
    }
    obj = types.ShippingQuery.de_json(dic)
    assert obj.id == 22
    assert obj.from_user.id == 383324787
    assert obj.from_user.is_bot is False
    assert obj.from_user.first_name == 'Mustafa'
    assert obj.from_user.last_name == 'Asaad'
    assert obj.from_user.username == 'MA24th'
    assert obj.from_user.language_code == 'en'
    assert obj.invoice_payload == 'abc'
    assert obj.shipping_address.country_code == 'iq'
    assert obj.shipping_address.post_code == 32006


def test_pre_checkout_query():
    dic = {
        'id': 888,
        'from': {
            "id": 383324787,
            "is_bot": False,
            "first_name": "Mustafa",
            "last_name": "Asaad",
            "username": "MA24th",
            "language_code": "en"},
        'currency': 'IQD',
        'total_amount': 25000,
        'invoice_payload': 'abc'
    }
    obj = types.PreCheckoutQuery.de_json(dic)
    assert obj.id == 888
    assert obj.from_user.id == 383324787
    assert obj.from_user.username == 'MA24th'
    assert obj.currency == 'IQD'
    assert obj.total_amount == 25000
    assert obj.invoice_payload == 'abc'
    assert obj.shipping_option_id is None
    assert obj.order_info is None


def test_passport_data():
    dic = {
        'EncryptedPassportElement': '12u8kadf',
        'EncryptedCredentials': 'djladjf:dkjfaklj'
    }
    obj = types.PassportData.de_json(dic)
    assert obj.data == '12u8kadf'
    assert obj.credentials == "djladjf:dkjfaklj"


def test_passport_file():
    dic = {
        'file_id': 44,
        'file_unique_id': 25,
        'file_size': 32,
        'file_date': 155555
    }
    obj = types.PassportFile.de_json(dic)
    assert obj.file_id == 44
    assert obj.file_unique_id == 25
    assert obj.file_size == 32
    assert obj.file_date == 155555


def test_encrypted_passport_element():
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


def test_encrypted_credentials():
    dic = {
        'data': 'SpyZjzIwdVAAIC',
        'hash': 'AgADAgADqacxG6wpRwABvEB6fpeIcKS4HAIkAATZH',
        'secret': 'secretpwd'
    }
    obj = types.EncryptedCredentials.de_json(dic)
    assert obj.data == 'SpyZjzIwdVAAIC'
    assert obj.hash == 'AgADAgADqacxG6wpRwABvEB6fpeIcKS4HAIkAATZH'
    assert obj.secret == 'secretpwd'


def test_passport_element_error():
    dic = {
        'source': 'unspecified',
        'type': 'any',
        'element_hash': 'any',
        'message': None,
    }
    obj = types.PassportElementError.de_json(dic)
    assert obj.source == 'unspecified'
    assert obj.type == 'any'
    assert obj.element_hash == 'any'
    assert obj.message is None


def test_passport_element_error_data_field():
    dic = {
        'source': 'data',
        'type': 'any',
        'field_name': 'abc',
        'data_hash': 'any',
        'message': None
    }
    obj = types.PassportElementErrorDataField.de_json(dic)
    assert obj.source == 'data'
    assert obj.type == 'any'
    assert obj.field_name == 'abc'
    assert obj.data_hash == 'any'
    assert obj.message is None


def test_passport_element_error_front_side():
    dic = {
        'source': 'front_side',
        'type': 'any',
        'file_hash': 'abc',
        'message': None
    }
    obj = types.PassportElementErrorFrontSide.de_json(dic)
    assert obj.source == 'front_side'
    assert obj.type == 'any'
    assert obj.file_hash == 'abc'
    assert obj.message is None


def test_passport_element_error_file():
    dic = {
        'source': 'file',
        'type': 'any',
        'file_hash': 'abc',
        'message': None
    }
    obj = types.PassportElementErrorFile.de_json(dic)
    assert obj.source == 'file'
    assert obj.type == 'any'
    assert obj.file_hash == 'abc'
    assert obj.message is None


def test_passport_element_error_files():
    dic = {
        'source': 'files',
        'type': 'any',
        'file_hashes': 'abc',
        'message': None
    }
    obj = types.PassportElementErrorFiles.de_json(dic)
    assert obj.source == 'files'
    assert obj.type == 'any'
    assert obj.file_hashes == 'abc'
    assert obj.message is None


def test_passport_element_error_reverse_side():
    dic = {
        'source': 'reverse_side',
        'type': 'any',
        'file_hash': 'abc',
        'message': None
    }
    obj = types.PassportElementErrorReverseSide.de_json(dic)
    assert obj.source == 'reverse_side'
    assert obj.type == 'any'
    assert obj.file_hash == 'abc'
    assert obj.message is None


def test_passport_element_error_selfie():
    dic = {
        'source': 'selfie',
        'type': 'any',
        'file_hash': 'abc',
        'message': None
    }
    obj = types.PassportElementErrorSelfie.de_json(dic)
    assert obj.source == 'selfie'
    assert obj.type == 'any'
    assert obj.file_hash == 'abc'
    assert obj.message is None


def test_passport_element_error_translation_file():
    dic = {
        'source': 'translation_file',
        'type': 'any',
        'file_hash': 'abc',
        'message': None
    }
    obj = types.PassportElementErrorTranslationFile.de_json(dic)
    assert obj.source == 'translation_file'
    assert obj.type == 'any'
    assert obj.file_hash == 'abc'
    assert obj.message is None


def test_passport_element_error_translation_files():
    dic = {
        'source': 'translation_files',
        'type': 'any',
        'file_hashes': 'abc',
        'message': None
    }
    obj = types.PassportElementErrorTranslationFiles.de_json(dic)
    assert obj.source == 'translation_files'
    assert obj.type == 'any'
    assert obj.file_hashes == 'abc'
    assert obj.message is None


def test_passport_element_error_unspecified():
    dic = {
        'source': 'unspecified',
        'type': 'any',
        'element_hash': 'abc',
        'message': None
    }
    obj = types.PassportElementErrorUnspecified.de_json(dic)
    assert obj.source == 'unspecified'
    assert obj.type == 'any'
    assert obj.element_hash == 'abc'
    assert obj.message is None


def test_game():
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
                "height": 40,
                "file_size": 32
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
    assert obj.text_entities[0].user.is_bot is False
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
    assert obj.animation.thumb.file_size == 32
    assert obj.animation.file_name == 'filename'
    assert obj.animation.mime_type == 'type'
    assert obj.animation.file_size == 64


def test_call_back_game():
    pass


def test_game_high_score():
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
    assert obj.user.is_bot is False
    assert obj.user.first_name == 'Mustafa'
    assert obj.user.last_name == 'Asaad'
    assert obj.user.username == 'MA24th'
    assert obj.user.language_code == 'en'
