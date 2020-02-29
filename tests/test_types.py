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
