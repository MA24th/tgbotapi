import json
import requests
from . import types
from .utilities import per_thread, logger, is_string
try:
    from requests.packages.urllib3 import fields

    format_header_param = fields.format_header_param
except ImportError:
    format_header_param = None

API_URL = None
READ_TIMEOUT = 9999
CONNECT_TIMEOUT = 3.5
proxy = None
FILE_URL = None


def _get_req_session(reset=False):
    return per_thread('req_session', lambda: requests.session(), reset)


def _make_request(token, method_name, method='get', params=None, files=None):
    """
    Makes a request to the Telegram API.
    :param token: [String, Required]: The bot's API token. (Created with @BotFather)
    :param method_name: [String, Required]: Name of the API method to be called. (E.g. 'getUpdates')
    :param method: [HTTP method, Optional] Defaults to 'get'.
    :param params: [Dict ,Optional]: Should be a dictionary with key-value pairs.
    :param files: [Optional] files content's a data.
    :returns: a JSON dictionary.
    """
    if API_URL is None:
        request_url = "https://api.telegram.org/bot{0}/{1}".format(
            token, method_name)
    else:
        request_url = API_URL.format(token, method_name)

    logger.debug("Request: method={0} url={1} params={2} files={3}".format(
        method, request_url, params, files))
    read_timeout = READ_TIMEOUT
    connect_timeout = CONNECT_TIMEOUT
    if files and format_header_param:
        fields.format_header_param = _no_encode(format_header_param)
    if params:
        if 'timeout' in params:
            read_timeout = params['timeout'] + 10
        if 'connect-timeout' in params:
            connect_timeout = params['connect-timeout'] + 10
    result = _get_req_session().request(method, request_url, params=params, files=files,
                                        timeout=(connect_timeout, read_timeout), proxies=proxy)
    logger.debug("The server returned: '{0}'".format(
        result.text.encode('utf8')))
    return _check_result(method_name, result)['result']


def _check_result(method_name, result):
    """
    Checks whether `result` is a valid API response.
    A result is considered invalid if:
        - The server returned an HTTP response code other than 200
        - The content of the result is invalid JSON.
        - The method call was unsuccessful (The JSON 'ok' field equals False)

    :raises ApiException: if one of the above listed cases is applicable
    :param method_name: [String, Required]: The name of the method called
    :param result: [Dict, Required]: The returned result of the method request
    :returns: a JSON dictionary.
    """
    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text.encode('utf8'))
        raise ApiException(msg, method_name, result)

    try:
        result_json = result.json()
    except:
        msg = 'The server returned an invalid JSON response. Response body:\n[{0}]' \
            .format(result.text.encode('utf8'))
        raise ApiException(msg, method_name, result)

    if not result_json['ok']:
        msg = 'Error code: {0} Description: {1}' \
            .format(result_json['error_code'], result_json['description'])
        raise ApiException(msg, method_name, result)
    return result_json


def get_updates(token, offset=None, limit=None, timeout=None, allowed_updates=None):
    """
    Use this method to receive incoming updates using long polling.
    :param offset [Integer, Optional]:
    :param limit [Integer, Optional]:
    :param timeout [timeout, Optional]:
    :param allowed_updates [Array of String, Optional]:
    :returns: An Array of Update objects.
    """
    method_url = r'getUpdates'
    payload = {}
    if offset:
        payload['offset'] = offset
    if limit:
        payload['limit'] = limit
    if timeout:
        payload['timeout'] = timeout
    if allowed_updates:
        payload['allowed_updates'] = json.dumps(allowed_updates)
    return _make_request(token, method_url, params=payload)


def set_webhook(token, url=None, certificate=None, max_connections=None, allowed_updates=None):
    """
    Use this method to specify a url and receive incoming updates via an outgoing webhook.
    :param url [String, Required]:
    :param certificate [InputFile, Optional]:
    :param max_connections [Integer, Optional]:
    :param allowed_updates [Array of String, Optional]
    :returns: True On success.
    """
    method_url = r'setWebhook'
    payload = {
        'url': url if url else "",
    }
    files = None
    if certificate:
        files = {'certificate': certificate}
    if max_connections:
        payload['max_connections'] = max_connections
    if allowed_updates:
        payload['allowed_updates'] = json.dumps(allowed_updates)
    return _make_request(token, method_url, params=payload, files=files)


def delete_webhook(token):
    """
    Use this method to remove webhook integration if you decide to switch back to getUpdates. 
    :param requires no parameters:
    :returns: True on success. 
    """
    method_url = r'deleteWebhook'
    return _make_request(token, method_url)


def get_webhook_info(token):
    """
    Use this method to get current webhook status. 
    :param requires no parameters:
    :returns: a WebhookInfo object, otherwise an object with the url field empty.
    """
    method_url = r'getWebhookInfo'
    payload = {}
    return _make_request(token, method_url, params=payload)


def get_me(token):
    """
    A simple method for testing your bot's auth token. 
    :param requires no parameters: 
    :returns: a User object.
    """
    method_url = r'getMe'
    return _make_request(token, method_url)


def send_message(token, chat_id, text, parse_mode=None, disable_web_page_preview=None, disable_notification=None,  reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send text messages. On success, the sent Message is returned.
    :param chat_id [Integer or String, Requierd]:
    :param text [String, Required]:
    :param parse_mode [String, Optional]:
    :param disable_web_page_preview [Boolean, Optional]:
    :param disable_notification [Boolean, Optional]:
    :param reply_to_message_id [Integer, Optional]:
    :param reply_markup [InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply, Optional]:
    :returns: a Message object.
    """
    method_url = r'sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    if parse_mode:
        payload['parse_mode'] = parse_mode
    if disable_web_page_preview:
        payload['disable_web_page_preview'] = disable_web_page_preview
    if disable_notification:
        payload['disable_notification'] = disable_notification
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload, method='post')


def forward_message(token, chat_id, from_chat_id, message_id, disable_notification=None):
    """
    Use this method to forward messages of any kind.
    :param chat_id [Integer or String, Requierd]:
    :param from_chat_id [Integer or String, Required]:
    :param disable_notification [Boolean, Optional]:
    :param message_id [Integer, Required]:
    :returns: a Message object.
    """
    method_url = r'forwardMessage'
    payload = {'chat_id': chat_id,
               'from_chat_id': from_chat_id, 'message_id': message_id}
    if disable_notification:
        payload['disable_notification'] = disable_notification
    return _make_request(token, method_url, params=payload)


def send_photo(token, chat_id, photo, caption=None, parse_mode=None, disable_notification=None, reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send photos. 
    :param chat_id [Integer or String, Requierd]:
    :param photo [InputFile or String, Required]:
    :param caption [String, Optional]:
    :param parse_mode [String, Optional]:
    :param disable_notification [Boolean, Optional]:
    :param reply_to_message_id [Integer, Optional]:
    :param reply_markup [InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply, Optional]:
    :returns: a Message object.
    """
    method_url = r'sendPhoto'
    payload = {'chat_id': chat_id}
    files = None
    if not is_string(photo):
        files = {'photo': photo}
    else:
        payload['photo'] = photo
    if caption:
        payload['caption'] = caption
    if parse_mode:
        payload['parse_mode'] = parse_mode
    if disable_notification:
        payload['disable_notification'] = disable_notification
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload, files=files, method='post')


def send_audio(token, chat_id, audio, caption=None, parse_mode=None, duration=None, performer=None, title=None, thumb=None, disable_notification=None, reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send audio files.
    :param chat_id [Integer or String, Required]:
    :param audio [InputFile or String, Required]:
    :param caption [String, Optional]:
    :param parse_mode [String, Optional]:
    :param duration [Integer, Optional]:
    :param performer [String, Optional]:
    :param title [String, Optional]:
    :param thumb [InputFile or String, Optional]:
    :param disable_notification [Boolean, Optional]:
    :param reply_to_message_id [Integer, Optional]:
    :param reply_markup [InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply, Optional]:
    :returns: a Message object.
    """
    method_url = r'sendAudio'
    payload = {'chat_id': chat_id}
    files = None
    if not is_string(audio):
        files = {'audio': audio}
    else:
        payload['audio'] = audio
    if caption:
        payload['caption'] = caption
    if parse_mode:
        payload['parse_mode'] = parse_mode
    if duration:
        payload['duration'] = duration
    if performer:
        payload['performer'] = performer
    if title:
        payload['title'] = title
    if thumb:
        payload['thumb'] = thumb
    if disable_notification:
        payload['disable_notification'] = disable_notification
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload, files=files, method='post')


def send_Document(token, chat_id, document, thumb=None, caption=None, parse_mode=None, disable_notification=None, reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send general files.
    :param chat_id [Integer or String, Required]:
    :param document [InputFile or String, Required]:
    :param thumb [InputFile or String, Optional]:
    :param caption [String 0-1024 characters, Optional]:
    :param parse_mode [String, Optional]:
    :param disable_notification [Boolean, Optional]:
    :param reply_to_message_id [Integer, Optional]:
    :param reply_markup [InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply, Optional]
    :returns: a Message object.
    """
    method_url = r'sendDocument'
    payload = {'chat_id': chat_id}
    files = None
    if not is_string(document):
        files = {'document': document}
    else:
        payload['document'] = document
    if thumb:
        payload['thumb'] = thumb
    if caption:
        payload['caption'] = caption
    if parse_mode:
        payload['parse_mode'] = parse_mode
    if disable_notification:
        payload['disable_notification'] = disable_notification
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload, files=files, method='post')


def send_video(token, chat_id, video, duration=None, width=None, height=None, thumb=None, caption=None, parse_mode=None, supports_streaming=None, disable_notification=None, reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send video files.
    :param chat_id [Integer or String, Required]:
    :param video [InputFile or String, Required]:
    :param duration [Integer, Optional]:
    :param width [Integer, Optional]:
    :param height [Integer, Optional]:
    :param thumb [InputFile or String, Optional]:
    :param caption [String 0-1024 characters, Optional]:
    :param parse_mode [String, Optional]:
    :param supports_streaming [Boolean, Optional]:
    :param disable_notification [Boolean, Optional]:
    :param reply_to_message_id [Integer, Optional]:
    :param reply_markup [InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply, Optional]
    :returns: a Message object.
    """    
    method_url = r'sendVideo'
    payload = {'chat_id': chat_id}
    files = None
    if not is_string(video):
        files = {'video': video}
    else:
        payload['video'] = video
    if duration:
        payload['duration'] = duration
    if width:
        payload['width'] = width
    if height:
        payload['height'] = height
    if thumb:
        payload['thumb'] = thumb
    if caption:
        payload['caption'] = caption
    if parse_mode:
        payload['parse_mode'] = parse_mode
    if supports_streaming:
        payload['supports_streaming'] = supports_streaming
    if disable_notification:
        payload['disable_notification'] = disable_notification
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload, files=files, method='post')


def send_animation(token, chat_id, animation, duration=None, width=None, height=None, thumb=None, caption=None, parse_mode=None, disable_notification=None, reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send animation files.
    :param chat_id [Integer or String, Required]:
    :param animation [InputFile or String, Required]:
    :param duration [Integer, Optional]:
    :param width [Integer, Optional]:
    :param height [Integer, Optional]:
    :param thumb [InputFile or String, Optional]:
    :param caption [String 0-1024 characters, Optional]:
    :param parse_mode [String, Optional]:
    :param disable_notification [Boolean, Optional]:
    :param reply_to_message_id [Integer, Optional]:
    :param reply_markup [InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply, Optional]
    :returns: a Message object.
    """ 
    method_url = r'sendAnimation'
    payload = {'chat_id': chat_id}
    files = None
    if not is_string(animation):
        files = {'animation': animation}
    else:
        payload['animation'] = animation
    if duration:
        payload['duration'] = duration
    if width:
        payload['width'] = width
    if height:
        payload['height'] = height
    if thumb:
        payload['thumb'] = thumb
    if caption:
        payload['caption'] = caption
    if parse_mode:
        payload['parse_mode'] = parse_mode
    if disable_notification:
        payload['disable_notification'] = disable_notification
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload, files=files, method='post')


def send_voice(token, chat_id, voice, caption=None, parse_mode=None, duration=None, disable_notification=None, reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send audio files.
    :param chat_id [Integer or String, Required]:
    :param voice [InputFile or String, Required]:
    :param caption [String 0-1024 characters, Optional]:
    :param parse_mode [String, Optional]:
    :param duration [Integer, Optional]:
    :param disable_notification [Boolean, Optional]:
    :param reply_to_message_id [Integer, Optional]:
    :param reply_markup [InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply, Optional]
    :returns: a Message object.
    """ 
    method_url = r'sendVoice'
    payload = {'chat_id': chat_id}
    files = None
    if not is_string(voice):
        files = {'voice': voice}
    else:
        payload['voice'] = voice
    if caption:
        payload['caption'] = caption
    if parse_mode:
        payload['parse_mode'] = parse_mode
    if duration:
        payload['duration'] = duration
    if disable_notification:
        payload['disable_notification'] = disable_notification
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload, files=files, method='post')


def send_video_note(token, chat_id, video_note, duration=None, length=None, thumb=None, disable_notification=None, reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send video messages.
    :param chat_id [Integer or String, Required]:
    :param video_note [InputFile or String, Required]:
    :param duration [Integer, Optional]:
    :param length [Integer, Optional]:
    :param thumb [InputFile or String, Optional]:
    :param disable_notification [Boolean, Optional]:
    :param reply_to_message_id [Integer, Optional]:
    :param reply_markup [InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply, Optional]
    :returns: a Message object.
    """  
    method_url = r'sendVideoNote'
    payload = {'chat_id': chat_id}
    files = None
    if not is_string(video_note):
        files = {'video_note': video_note}
    else:
        payload['video_note'] = video_note
    if duration:
        payload['duration'] = duration
    if length:
        payload['length'] = length
    if thumb:
        payload['thumb'] = thumb
    if disable_notification:
        payload['disable_notification'] = disable_notification
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload, files=files, method='post')


def send_media_group(token, chat_id, media, disable_notification=None, reply_to_message_id=None):
    """
    Use this method to send a group of photos or videos as an album.
    :param chat_id [Integer or String, Required]:
    :param media [Array of InputMediaPhoto and InputMediaVideo, Required]:
    :param disable_notification [Boolean, Optional]:
    :param reply_to_message_id [Integer, Optional]:
    :returns: a Messages object.
    """
    method_url = r'sendMediaGroup'
    media_json, files = _convert_input_media_array(media)
    payload = {'chat_id': chat_id, 'media': media_json}
    if disable_notification:
        payload['disable_notification'] = disable_notification
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    return _make_request(token, method_url, params=payload, method='post' if files else 'get', files=files if files else None)


def send_location(token, chat_id, latitude, longitude, live_period=None, disable_notification=None, reply_to_message_id=None, reply_markup=None,):
    """
    Use this method to send point on the map.
    :param chat_id [Integer or String, Required]:
    :param latitude [Float, Required]:
    :param longitude [Float, Required]:
    :param live_period [Integer, Optional]:
    :param disable_notification [Boolean, Optional]:
    :param reply_to_message_id [Integer, Optional]:
    :param reply_markup [InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply, Optional]
    :returns: a Message object.
    """  
    method_url = r'sendLocation'
    payload = {'chat_id': chat_id,
               'latitude': latitude, 'longitude': longitude}
    if live_period:
        payload['live_period'] = live_period
    if disable_notification:
        payload['disable_notification'] = disable_notification
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload)


def edit_message_live_location(token,  latitude, longitude, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
    """
    Use this method to edit live location messages.
    :param chat_id [Integer or String, Optional, Required if inline_message_id is not specified]:
    :param message_id [Integer, Optional, Required if inline_message_id is not specified]:
    :param inline_message_id [String, Optional, Required if chat_id and message_id are not specified]:
    :param latitude [Float, Required]:
    :param longitude [Float, Required]:
    :param reply_markup [InlineKeyboardMarkup, Optional]
    :returns: a Message object, otherwise True.
    """
    method_url = r'editMessageLiveLocation'
    payload = {'latitude': latitude, 'longitude': longitude}
    if chat_id:
        payload['chat_id'] = chat_id
    if message_id:
        payload['message_id'] = message_id
    if inline_message_id:
        payload['inline_message_id'] = inline_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload)


def stop_message_live_location(token, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
    """
    Use this method to stop updating a live location message before live_period expires.
    :param chat_id [Integer or String, Optional, Required if inline_message_id is not specified]:
    :param message_id [Integer, Optional, Required if inline_message_id is not specified]:
    :param inline_message_id [String, Optional, Required if chat_id and message_id are not specified]:
    :param reply_markup [InlineKeyboardMarkup, Optional]
    :returns: a Message object, otherwise True.
    """
    method_url = r'stopMessageLiveLocation'
    payload = {}
    if chat_id:
        payload['chat_id'] = chat_id
    if message_id:
        payload['message_id'] = message_id
    if inline_message_id:
        payload['inline_message_id'] = inline_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload)


def send_venue(token, chat_id, latitude, longitude, title, address, foursquare_id=None, foursquare_type=None, disable_notification=None, reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send information about a venue.
    :param chat_id [Integer or String, Required]:
    :param latitude [Float, Required]:
    :param longitude [Float, Required]:
    :param title [String, Required]:
    :param address [String, Required]:
    :param foursquare_id [String, Optional]:
    :param foursquare_type [String, Optional]:
    :param disable_notification [Boolean, Optional]:
    :param reply_to_message_id [Integer, Optional]:
    :param reply_markup [InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply, Optional]
    :returns: a Message object.
    """  
    method_url = r'sendVenue'
    payload = {'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude, 'title': title, 'address': address}
    if foursquare_id:
        payload['foursquare_id'] = foursquare_id
    if foursquare_type:
        payload['foursquare_type'] = foursquare_type
    if disable_notification:
        payload['disable_notification'] = disable_notification
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload)


def send_contact(token, chat_id, phone_number, first_name, last_name=None, vcard=None, disable_notification=None, reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send information about a venue.
    :param chat_id [Integer or String, Required]:
    :param phone_number [String, Required]:
    :param first_name [String, Required]:
    :param last_name [String, Optional]:
    :param vcard [String, Optional]:
    :param disable_notification [Boolean, Optional]:
    :param reply_to_message_id [Integer, Optional]:
    :param reply_markup [InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply, Optional]
    :returns: a Message object.
    """
    method_url = r'sendContact'
    payload = {'chat_id': chat_id,
               'phone_number': phone_number, 'first_name': first_name}
    if last_name:
        payload['last_name'] = last_name
    if vcard:
        payload['vcard'] = vcard
    if disable_notification:
        payload['disable_notification'] = disable_notification
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload)


def send_poll(token, chat_id, question, options, is_anonymous=None, type=None, allows_multiple_answers=None, correct_option_id=None, is_closed=None, disable_notifications=False, reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send information about a venue.
    :param chat_id [Integer or String, Required]:
    :param question [String, Required]:
    :param options [Array of String, Required]:
    :param is_anonymous [Boolean, Optional]:
    :param type [String, Optional]:
    :param allows_multiple_answers [Boolean, Optional]:
    :param correct_option_id [Integer, Optional]:
    :param is_closed [Boolean, Optional]:
    :param disable_notification [Boolean, Optional]:
    :param reply_to_message_id [Integer, Optional]:
    :param reply_markup [InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply, Optional]
    :returns: a Message object.
    """
    method_url = r'sendPoll'
    payload = {'chat_id': chat_id, 'question': question, 'options': _convert_list_json_serializable(options)}
    if is_anonymous:
        payload['is_anonymous'] = is_anonymous
    if type:
        payload['type'] = type    
    if allows_multiple_answers:
        payload['allows_multiple_answers'] = allows_multiple_answers
    if correct_option_id:
        payload['correct_option_id'] = correct_option_id
    if type:
        payload['type'] = type  
    if disable_notifications:
        payload['disable_notification'] = disable_notifications
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload)


def send_dice(token, chat_id, disable_notification=None, reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send a dice.
    :param chat_id [Integer or String, Requierd]:
    :param disable_notification [Boolean, Optional]:
    :param reply_to_message_id [Integer, Optional]:
    :param reply_markup [InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply, Optional]:
    :returns: a Message object.
    """
    method_url = r'sendDice'
    payload = {'chat_id': chat_id}
    if disable_notification:
        payload['disable_notification'] = disable_notification
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = reply_markup
    return _make_request(token, method_url, params=payload)


def send_chat_action(token, chat_id, action):
    """
    Use this method when you need to tell the user that something is happening on the bot's side.
    :param chat_id [Integer or String, Requierd]:
    :param action [String, Required]:
    :returns: True On success.
    """
    method_url = r'sendChatAction'
    payload = {'chat_id': chat_id, 'action': action}
    return _make_request(token, method_url, params=payload)


def get_user_profile_photos(token, user_id, offset=None, limit=None):
    """
    Use this method when you need to tell the user that something is happening on the bot's side.
    :param user_id [Integer or String, Requierd]:
    :param offset [Integer, Optional]:
    :param limit [Integer, Optional]:
    :returns: a UserProfilePhoto object.
    """
    method_url = r'getUserProfilePhotos'
    payload = {'user_id': user_id}
    if offset:
        payload['offset'] = offset
    if limit:
        payload['limit'] = limit
    return _make_request(token, method_url, params=payload)


def get_file(token, file_id):
    """
    Use this method when you need to tell the user that something is happening on the bot's side.
    :param file_id [Integer or String, Requierd]:
    :returns: a File object.
    """
    method_url = r'getFile'
    payload = {'file_id': file_id}
    return _make_request(token, method_url, params=payload)


def kick_chat_member(token, chat_id, user_id, until_date=None):
    """
    Use this method when you need to tell the user that something is happening on the bot's side.
    :param chat_id [Integer or String, Requierd]:
    :param user_id [Integer, Requierd]:
    :param until_date [Integer, Optional]:
    :returns: True On success.
    """
    method_url = 'kickChatMember'
    payload = {'chat_id': chat_id, 'user_id': user_id}
    if until_date:
        payload['until_date'] = until_date
    return _make_request(token, method_url, params=payload, method='post')


def unban_chat_member(token, chat_id, user_id):
    """
    Use this method when you need to tell the user that something is happening on the bot's side.
    :param chat_id [Integer or String, Requierd]: Unique identifier for the target chat or username of the target channel (in the format @channelusername).
    :param user_id [Integer, Requierd]:
    :returns: True On success.
    """
    method_url = 'unbanChatMember'
    payload = {'chat_id': chat_id, 'user_id': user_id}
    return _make_request(token, method_url, params=payload, method='post')


def restrict_chat_member(token, chat_id, user_id, permissions, until_date=None):
    """
    Use this method to restrict a user in a supergroup.
    :param chat_id [Integer or String, Requierd]: Unique identifier for the target chat or username of the target channel (in the format @channelusername).
    :param user_id [Integer, Requierd]:
    :param permissions [ChatPermissions, Required]:
    :param until_date [Integer, Optional]
    :returns: True On success.
    """
    method_url = 'restrictChatMember'
    payload = {'chat_id': chat_id, 'user_id': user_id, 'permissions':permissions}
    if until_date:
        payload['until_date'] = until_date
    return _make_request(token, method_url, params=payload, method='post')


def promote_chat_member(token, chat_id, user_id, can_change_info=None, can_post_messages=None, can_edit_messages=None, can_delete_messages=None, can_invite_users=None, can_restrict_members=None, can_pin_messages=None, can_promote_members=None):
    """
    Use this method to promote or demote a user in a supergroup or a channel.
    :param token [String, Required]: 
    :param chat_id [Integer or String, Requierd]:
    :param user_id [Integer, Requierd]: ]
    :param can_change_info [Boolean, Optional]: 
    :param can_post_messages [Boolean, Optional]: 
    :param can_edit_messages [Boolean, Optional]: 
    :param can_delete_messages [Boolean, Optional]: 
    :param can_invite_users [Boolean, Optional]: 
    :param can_restrict_members [Boolean, Optional]: 
    :param can_pin_messages [Boolean, Optional]: 
    :param can_promote_members [Boolean, Optional]: 
    :returns: True On success.
    """
    method_url = 'promoteChatMember'
    payload = {'chat_id': chat_id, 'user_id': user_id}
    if can_change_info:
        payload['can_change_info'] = can_change_info
    if can_post_messages:
        payload['can_post_messages'] = can_post_messages
    if can_edit_messages:
        payload['can_edit_messages'] = can_edit_messages
    if can_delete_messages:
        payload['can_delete_messages'] = can_delete_messages
    if can_invite_users:
        payload['can_invite_users'] = can_invite_users
    if can_restrict_members:
        payload['can_restrict_members'] = can_restrict_members
    if can_pin_messages:
        payload['can_pin_messages'] = can_pin_messages
    if can_promote_members:
        payload['can_promote_members'] = can_promote_members
    return _make_request(token, method_url, params=payload, method='post')


def set_chat_adminstrator_custom_title(token, chat_id, user_id, custom_title):
    """
    Use this method to set a custom title for an administrator in a supergroup promoted by the bot. 
    :param token [Integer, Required]:
    :param chat_id [String or Integer, Required]:
    :param user_id [Integer, Required]:
    :param custom_title [String, Required]:
    :returns: True on success.
    """
    method_url = r'setChatAdministratorCustomTitle'
    payload = {'chat_id': chat_id, 'user_id': user_id, 'custom_title': custom_title}
    return _make_request(token, method_url, params=payload, method='post')


def set_chat_permissions(token, chat_id, permissions):
    """
    Use this method to set default chat permissions for all members. 
    :param token [String, Required]:
    :param chat_id [String or Integer, Required]:
    :param permissions	[ChatPermissions, Required]:
    :returns: True on success.
    """
    method_url = r'setChatPermissions'
    payload = {'chat_id': chat_id, 'permissions': permissions}
    return _make_request(token, method_url, params=payload, method='post')

def export_chat_invite_link(token, chat_id):
    """
    Use this method to generate a new invite link for a chat. 
    :param token [String, Required]:
    :param chat_id [String or Integer, Required]:
    :returns: new link as String on success.
    """
    method_url = r'exportChatInviteLink'
    payload = {'chat_id': chat_id}
    return _make_request(token, method_url, params=payload, method='post')


def set_chat_photo(token, chat_id, photo):
    """
    Use this method to set a new profile photo for the chat.
    :param token [String, Required]:
    :param chat_id [String or Integer, Required]:
    :param photo [InputFile, Required]:
    :returns: True on success.
    """
    method_url = r'setChatPhoto'
    payload = {'chat_id': chat_id}
    files = None
    if not is_string(photo):
        files = {'photo': photo}
    else:
        payload['photo'] = photo
    return _make_request(token, method_url, params=payload, files=files, method='post')


def delete_chat_photo(token, chat_id):
    """
    Use this method to delete a chat photo.
    :param token [String, Required]:
    :param chat_id [String or Integer, Required]:
    :returns: True on success.
    """
    method_url = r'deleteChatPhoto'
    payload = {'chat_id': chat_id}
    return _make_request(token, method_url, params=payload, method='post')


def set_chat_title(token, chat_id, title):
    """
    Use this method to change the title of a chat.
    :param token [String, Required]:
    :param chat_id [String or Integer, Required]:
    :param title [String, Required]:
    :returns: True on success.
    """
    method_url = r'setChatTitle'
    payload = {'chat_id': chat_id, 'title': title}
    return _make_request(token, method_url, params=payload, method='post')


def set_chat_description(token, chat_id, description=None):
    """
    Use this method to change the description of a group, a supergroup or a channel.
    :param token [String, Required]:
    :param chat_id [String or Integer, Required]:
    :param description [String, Optional]:
    :returns: True on success.
    """
    method_url = r'setChatDescription'
    payload = {'chat_id': chat_id}
    if description:
        payload['description'] = description
    return _make_request(token, method_url, params=payload, method='post')


def pin_chat_message(token, chat_id, message_id, disable_notification=False):
    """
    Use this method to pin a message in a group, a supergroup, or a channel.
    :param token [String, Required]:
    :param chat_id [String or Integer, Required]:
    :param message_id [Integer, Required]:
    :param disable_notification [Boolean, Optional]:
    :returns: True on success.
    """
    method_url = r'pinChatMessage'
    payload = {'chat_id': chat_id, 'message_id': message_id}
    if disable_notification:
        payload['disable_notification'] = disable_notification
    return _make_request(token, method_url, params=payload, method='post')


def unpin_chat_message(token, chat_id):
    """
    Use this method to unpin a message in a group, a supergroup, or a channel.
    :param token [String, Required]:
    :param chat_id [String or Integer, Required]:
    :returns: True on success.
    """
    method_url = r'unpinChatMessage'
    payload = {'chat_id': chat_id}
    return _make_request(token, method_url, params=payload, method='post')


def leave_chat(token, chat_id):
    """
    Use this method for your bot to leave a group, supergroup or channel.
    :param token [String, Required]:
    :param chat_id [String or Integer, Required]:
    :returns: True on success.
    """
    method_url = r'leaveChat'
    payload = {'chat_id': chat_id}
    return _make_request(token, method_url, params=payload)


def get_chat(token, chat_id):
    """
    Use this method to get up to date information about the chat.
    :param token [String, Required]:
    :param chat_id [String or Integer, Required]:
    :returns: a Chat object.
    """
    method_url = r'getChat'
    payload = {'chat_id': chat_id}
    return _make_request(token, method_url, params=payload)


def get_chat_administrators(token, chat_id):
    """
    Use this method to get a list of administrators in a chat.
    :param token [String, Required]:
    :param chat_id [String or Integer, Required]:
    :returns: an Array of ChatMember object.
    """
    method_url = r'getChatAdministrators'
    payload = {'chat_id': chat_id}
    return _make_request(token, method_url, params=payload)


def get_chat_members_count(token, chat_id):
    """
    Use this method to get the number of members in a chat.
    :param token [String, Required]:
    :param chat_id [String or Integer, Required]:
    :returns: Integer On success.
    """
    method_url = r'getChatMembersCount'
    payload = {'chat_id': chat_id}
    return _make_request(token, method_url, params=payload)


def get_chat_member(token, chat_id, user_id):
    """
    Use this method to get information about a member of a chat.
    :param token [String, Required]:
    :param chat_id [String or Integer, Required]:
    :param chat_id [Integer, Required]:
    :returns: a ChatMember object On success.
    """
    method_url = r'getChatMember'
    payload = {'chat_id': chat_id, 'user_id': user_id}
    return _make_request(token, method_url, params=payload)


def set_chat_sticker_set(token, chat_id, sticker_set_name):
    """
    Use this method to set a new group sticker set for a supergroup.
    :param token [String, Required]:
    :param chat_id [String or Integer, Required]:
    :param sticker_set_name [String, Required]:
    :returns: True On success.
    """
    method_url = r'setChatStickerSet'
    payload = {'chat_id': chat_id, 'sticker_set_name': sticker_set_name}
    return _make_request(token, method_url, params=payload)


def delete_chat_sticker_set(token, chat_id):
    """
    Use this method to delete a group sticker set from a supergroup.
    :param token [String, Required]:
    :param chat_id [String or Integer, Required]:
    :returns: True On success.
    """
    method_url = r'deleteChatStickerSet'
    payload = {'chat_id': chat_id}
    return _make_request(token, method_url, params=payload)


def answer_callback_query(token, callback_query_id, text=None, show_alert=None, url=None, cache_time=None):
    """
    Use this method to send answers to callback queries sent from inline keyboards.     
    :param token [String, Required]:
    :param callback_query_id [String, Optional]: 
    :param text [String, Optional]:
    :param show_alert [Boolean, Optional]:
    :param url [String, Optional]:
    :param cache_time [Integer, Optional]:
    :returns: True On success.
    """
    method_url = r'answerCallbackQuery'
    payload = {'callback_query_id': callback_query_id}
    if text:
        payload['text'] = text
    if show_alert:
        payload['show_alert'] = show_alert
    if url:
        payload['url'] = url
    if cache_time is not None:
        payload['cache_time'] = cache_time
    return _make_request(token, method_url, params=payload, method='post')


def set_my_commands(token, commands):
    """
    Use this method to change the list of the bot's commands. 
    :param commands [Array of BotCommand, Required]:
    :returns: True On success.
    """
    method_url = r'setMyCommands'
    payload = {'commands': commands}
    return _make_request(token, method_url, params=payload)


def get_my_commands(token):
    """
    Use this method to get the current list of the bot's commands. 
    :param [Requires no parameters]:
    :returns: Array of BotCommand On success.
    """
    method_url = r'getMyCommands'
    return _make_request(token, method_url)

# Updating messages


def edit_message_text(token, text, chat_id=None, message_id=None, inline_message_id=None, parse_mode=None, disable_web_page_preview=None, reply_markup=None):
    """
    Use this method to edit text and game messages.
    :param token [String, Required]:
    :param chat_id [Integer or String, Optional, Required if inline_message_id is not specified]:
    :param message_id [Integer, Optional, Required if inline_message_id is not specified]:
    :param inline_message_id [String, Optional, Required if chat_id and message_id are not specified]:
    :param text [String, Required]:
    :param parse_mode [String, Optional]:
    :param disable_web_page_preview [Boolean, Optional]:
    :param reply_markup [InlineKeyboardMarkup, Optional]:
    :returns: a Message object On success, otherwise True.
    """
    method_url = r'editMessageText'
    payload = {'text': text}
    if chat_id:
        payload['chat_id'] = chat_id
    if message_id:
        payload['message_id'] = message_id
    if inline_message_id:
        payload['inline_message_id'] = inline_message_id
    if parse_mode:
        payload['parse_mode'] = parse_mode
    if disable_web_page_preview:
        payload['disable_web_page_preview'] = disable_web_page_preview
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload, method='post')


def edit_message_caption(token, caption, chat_id=None, message_id=None, inline_message_id=None, parse_mode=None, reply_markup=None):
    """
    Use this method to edit captions of messages.
    :param token [String, Required]:
    :param chat_id [Integer or String, Optional, Required if inline_message_id is not specified]:
    :param message_id [Integer, Optional, Required if inline_message_id is not specified]:
    :param inline_message_id [String, Optional, Required if chat_id and message_id are not specified]:
    :param caption [String, Required]:
    :param parse_mode [String, Optional]:
    :param reply_markup [InlineKeyboardMarkup, Optional]:
    :returns: a Message object On success, otherwise True.
    """
    method_url = r'editMessageCaption'
    payload = {'caption': caption}
    if chat_id:
        payload['chat_id'] = chat_id
    if message_id:
        payload['message_id'] = message_id
    if inline_message_id:
        payload['inline_message_id'] = inline_message_id
    if parse_mode:
        payload['parse_mode'] = parse_mode
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload, method='post')


def edit_message_media(token, media, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
    """
    Use this method to edit animation, audio, document, photo, or video messages.
    :param token [String, Required]:
    :param chat_id [Integer or String, Optional, Required if inline_message_id is not specified]:
    :param message_id [Integer, Optional, Required if inline_message_id is not specified]:
    :param inline_message_id [String, Optional, Required if chat_id and message_id are not specified]:
    :param media [InputMedia, Required]:
    :param reply_markup [InlineKeyboardMarkup, Optional]:
    :returns: a Message object On success, otherwise True.
    """
    method_url = r'editMessageMedia'
    media_json, file = _convert_input_media(media)
    payload = {'media': media_json}
    if chat_id:
        payload['chat_id'] = chat_id
    if message_id:
        payload['message_id'] = message_id
    if inline_message_id:
        payload['inline_message_id'] = inline_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload, files=file, method='post' if file else 'get')


def edit_message_reply_markup(token, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
    """
    Use this method to edit only the reply markup of messages.
    :param token [String, Required]:
    :param chat_id [Integer or String, Optional, Required if inline_message_id is not specified]:
    :param message_id [Integer, Optional, Required if inline_message_id is not specified]:
    :param inline_message_id [String, Optional, Required if chat_id and message_id are not specified]:
    :param reply_markup [InlineKeyboardMarkup, Optional]:
    :returns: a Message object On success, otherwise True.
    """
    method_url = r'editMessageReplyMarkup'
    payload = {}
    if chat_id:
        payload['chat_id'] = chat_id
    if message_id:
        payload['message_id'] = message_id
    if inline_message_id:
        payload['inline_message_id'] = inline_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload, method='post')


def stop_poll(token, chat_id, message_id, reply_markup=None):
    """
    Use this method to stop a poll which was sent by the bot.
    :param token [String, Required]:
    :param chat_id [Integer or String, Required]:
    :param message_id [Integer, Required]:
    :param reply_markup [InlineKeyboardMarkup, Optional]:
    :returns: a Poll object On success.
    """
    method_url = r'stopPoll'
    payload = {'chat_id': chat_id, 'message_id': message_id}
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload)


def delete_message(token, chat_id, message_id):
    """
    Use this method to delete a message.
    :param token [String, Required]:
    :param chat_id [Integer or String, Required]:
    :param message_id [Integer, Required]:
    :returns: True On success.
    """
    method_url = r'deleteMessage'
    payload = {'chat_id': chat_id, 'message_id': message_id}
    return _make_request(token, method_url, params=payload, method='post')


def send_sticker(token, chat_id, sticker, reply_to_message_id=None, reply_markup=None, disable_notification=None):
    """
    Use this method to send static .WEBP or animated .TGS stickers.
    :param token [String, Required]:
    :param chat_id [Integer or String, Required]:
    :param sticker [InputFile or String, Required]:
    :param disable_notification [Boolean, Optional]:
    :param reply_to_message_id [Integer, Optional]:
    :param reply_markup [InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply, Optional]
    :returns: a Message object On success.
    """
    method_url = r'sendSticker'
    payload = {'chat_id': chat_id}
    files = None
    if not is_string(sticker):
        files = {'sticker': sticker}
    else:
        payload['sticker'] = sticker
    if disable_notification:
        payload['disable_notification'] = disable_notification
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload, files=files, method='post')


def get_sticker_set(token, name):
    method_url = r'getStickerSet'
    """
    Use this method to send static .WEBP or animated .TGS stickers.
    :param token [String, Required]:
    :param name [String, Required]:
    :returns: a StickerSet object On success.
    """    
    return _make_request(token, method_url, params={'name': name})


def upload_sticker_file(token, user_id, png_sticker):
    """
    Use this method to upload a .PNG file with a sticker.
    :param token [String, Required]:
    :param user_id [Integer, Required]:
    :param png_sticker [InputFile, Required]:
    :returns: a File object On success.
    """    
    method_url = r'uploadStickerFile'
    payload = {'user_id': user_id}
    files = {'png_sticker': png_sticker}
    return _make_request(token, method_url, params=payload, files=files, method='post')


def create_new_sticker_set(token, user_id, name, title, png_sticker, tgs_sticker, emojis, contains_masks=None, mask_position=None):
    """
    Use this method to create a new sticker set owned by a user. 
    :param token [String, Required]:
    :param user_id [Integer, Required]:
    :param name [String, Required]:
    :param title [String, Required]:
    :param png_sticker [InputFile or String, Optional]:
    :param tgs_sticker [InputFile, Optional]:
    :param emojis [String, Required]:
    :param contains_masks [Boolean, Optional]:
    :param mask_position [MaskPostion, Optional]
    :returns: True On success.
    """
    method_url = r'createNewStickerSet'
    payload = {'user_id': user_id, 'name': name,
               'title': title, 'emojis': emojis}
    files = None
    if not is_string(png_sticker):
        files = {'png_sticker': png_sticker}
    else:
        payload['png_sticker'] = png_sticker
    if not is_string(tgs_sticker):
        files = {'tgs_sticker', tgs_sticker}
    if contains_masks:
        payload['contains_masks'] = contains_masks
    if mask_position:
        payload['mask_position'] = mask_position.to_json()
    return _make_request(token, method_url, params=payload, files=files, method='post')


def add_sticker_to_set(token, user_id, name, png_sticker, emojis, tgs_sticker=None, mask_position=None):
    """
    Use this method to add a new sticker to a set created by the bot.
    :param token [String, Required]:
    :param user_id [Integer, Required]:
    :param name [String, Required]:
    :param png_sticker [InputFile or String, Required]:
    :param tgs_sticker [InputFile, Optional]:
    :param emojis [String, Required]:
    :param mask_position [MaskPostion, Optional]
    :returns: True on success.
    """
    method_url = r'addStickerToSet'
    payload = {'user_id': user_id, 'name': name, 'emojis': emojis}
    files = None
    if not is_string(png_sticker):
        files = {'png_sticker': png_sticker}
    else:
        payload['png_sticker'] = png_sticker
    if not is_string(tgs_sticker):
        files = {'tgs_sticker': tgs_sticker}
    if mask_position:
        payload['mask_position'] = mask_position.to_json()
    return _make_request(token, method_url, params=payload, files=files, method='post')


def set_sticker_position_in_set(token, sticker, position):
    """
    Use this method to move a sticker in a set created by the bot to a specific position. 
    :param token [String, Required]:
    :param sticker [String, Required]:
    :param position [Integr, Required]:
    :returns: True on success.
    """
    method_url = r'setStickerPositionInSet'
    payload = {'sticker': sticker, 'position': position}
    return _make_request(token, method_url, params=payload, method='post')


def delete_sticker_from_set(token, sticker):
    """
    Use this method to delete a sticker from a set created by the bot.
    :param token [String, Required]:
    :param sticker [String, Required]:
    :returns: True on success.
    """
    method_url = r'deleteStickerFromSet'
    payload = {'sticker': sticker}
    return _make_request(token, method_url, params=payload, method='post')


def set_sticker_set_thumb(token, name, user_id, thumb=None):
    """
    Use this method to set the thumbnail of a sticker set.
    :param token [String, Required]:
    :param name [String, Required]:
    :param user_id [Integer, Required]:
    :param thumb [InputFile or String, Optional]:
    :returns: True on success
    """
    method_url = r'setStickerSetThumb'
    payload = {'name': name, 'user_id': user_id}
    if thumb:
        payload['thumb'] = thumb
    return _make_request(token, method_url, params=payload)


def answer_inline_query(token, inline_query_id, results, cache_time=None, is_personal=None, next_offset=None, switch_pm_text=None, switch_pm_parameter=None):
    """
    Use this method to send answers to an inline query.
    :param token [String, Required]:
    :param inline_query_id [String, Required]:
    :param results [Array of InlineQueryResultger, Required]:
    :param cache_time [Integer, Optional]:
    :param is_personal [Boolean, Optional]:
    :param next_offset [String, Optional]:
    :param switch_pm_text [String, Optional]:
    :param switch_pm_parameter [String, Optional]:
    :returns: True on success
    """
    method_url = r'answerInlineQuery'
    payload = {'inline_query_id': inline_query_id, 'results': _convert_list_json_serializable(results)}
    if cache_time is not None:
        payload['cache_time'] = cache_time
    if is_personal:
        payload['is_personal'] = is_personal
    if next_offset is not None:
        payload['next_offset'] = next_offset
    if switch_pm_text:
        payload['switch_pm_text'] = switch_pm_text
    if switch_pm_parameter:
        payload['switch_pm_parameter'] = switch_pm_parameter
    return _make_request(token, method_url, params=payload, method='post')


# Payments (https://core.telegram.org/bots/api#payments)

def send_invoice(token, chat_id, title, description, payload, provider_token, start_parameter, currency, prices, provider_data=None, photo_url=None, photo_size=None, photo_width=None, photo_height=None, need_name=None, need_phone_number=None, need_email=None, need_shipping_address=None, send_phone_number_to_provider=None,  send_email_to_provider=None, is_flexible=None, disable_notification=None, reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send invoices. On success, the sent Message is returned.
    :param token [String, Required]:
    :param chat_id [Integer, Required]:
    :param title [String, Required]:
    :param description [String, Required]:
    :param payload [String, Required]:
    :param provider_token [String, Required]:
    :param start_parameter [String, Required]:
    :param currency [String, Required]:
    :param prices [Array of LabeledPrice, Required]:
    :param provider_data [String, Optional]:
    :param photo_url [String, Optional]:
    :param photo_size [Integer, Optional]:
    :param photo_width [Integer, Optional]: Photo width
    :param photo_height [Integer, Optional]: Photo height
    :param need_name [Boolean, Optional]:
    :param need_phone_number [Boolean, Optional]:
    :param need_email [Boolean, Optional]:
    :param need_shipping_address [Boolean, Optional]:
    :param send_phone_number_to_provider [Boolean, Optional]:
    :param send_email_to_provider [Boolean, Optional]: 
    :param is_flexible [Boolean, Optional]:
    :param disable_notification [Boolean, Optional]:
    :param reply_to_message_id [Integer, Optional]:
    :param reply_markup [InlineKeyboardMarkup, Optional]:
    :returns: a Message object.
    """
    method_url = r'sendInvoice'
    params = {'chat_id': chat_id, 'title': title, 'description': description, 'payload': payload, 'provider_token': provider_token, 'start_parameter': start_parameter, 'currency': currency, 'prices': _convert_list_json_serializable(prices)}
    if provider_data:
        params['provider_data'] = provider_data
    if photo_url:
        params['photo_url'] = photo_url
    if photo_size:
        params['photo_size'] = photo_size
    if photo_width:
        params['photo_width'] = photo_width
    if photo_height:
        params['photo_height'] = photo_height
    if need_name:
        params['need_name'] = need_name
    if need_phone_number:
        params['need_phone_number'] = need_phone_number
    if need_email:
        params['need_email'] = need_email
    if need_shipping_address:
        params['need_shipping_address'] = need_shipping_address
    if send_phone_number_to_provider:
        params['send_phone_number_to_provider'] = send_phone_number_to_provider
    if send_email_to_provider:
        params['send_email_to_provider'] = send_email_to_provider
    if is_flexible:
        params['is_flexible'] = is_flexible
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        params['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=params)


def answer_shipping_query(token, shipping_query_id, ok, shipping_options=None, error_message=None):
    """
    If you sent an invoice requesting a shipping address and the parameter is_flexible was specified, the Bot API will send an Update with a shipping_query field to the bot. Use this method to reply to shipping queries. On success, True is returned.
    :param token: Bot's token (you don't need to fill this)
    :param shipping_query_id: Unique identifier for the query to be answered
    :param ok: Specify True if delivery to the specified address is possible and False if there are any problems (for example, if delivery to the specified address is not possible)
    :param shipping_options: Required if ok is True. A JSON-serialized array of available shipping options.
    :param error_message: Required if ok is False. Error message in human readable form that explains why it is impossible to complete the order (e.g. "Sorry, delivery to your desired address is unavailable'). Telegram will display this message to the user.
    :returns:
    """
    method_url = 'answerShippingQuery'
    payload = {'shipping_query_id': shipping_query_id, 'ok': ok}
    if shipping_options:
        payload['shipping_options'] = _convert_list_json_serializable(
            shipping_options)
    if error_message:
        payload['error_message'] = error_message
    return _make_request(token, method_url, params=payload)


def answer_pre_checkout_query(token, pre_checkout_query_id, ok, error_message=None):
    """
    Use this method to respond to such pre-checkout queries. 
    :param token [String, Required]:
    :param pre_checkout_query_id [String, Required]:
    :param ok [Boolean, Required]:
    :param error_message [String, Optional, Required if ok is False]:
    :returns: True On success.
    """
    method_url = r'answerPreCheckoutQuery'
    payload = {'pre_checkout_query_id': pre_checkout_query_id, 'ok': ok}
    if error_message:
        payload['error_message'] = error_message
    return _make_request(token, method_url, params=payload)


def set_passport_data_errors(token, user_id, erros):
    """
    Use this if the data submitted by the user doesn't satisfy the standards your service requires for any reason.
    :param token [String, Required]:
    :param user_id [Integer, Required]:
    :param errors [Array of PassportElementError, Required]:
    :returns: True On success.
    """
    method_url = r'setPassportDataErrors'
    params = {'user_id': user_id, 'errors': erros}
    return _make_request(token, method_url, params)


def send_game(token, chat_id, game_short_name, disable_notification=None, reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send a game.
    :param token [String, Required]:
    :param chat_id [Integer, Required]:
    :param game_short_name [String, Required]:
    :param disable_notification [Boolean, Optional]:
    :param reply_to_message_id [Integer, Optional]:
    :param reply_markup [InlineKeyboardMarkup, Optional]:
    :returns: a Message object On success.
    """
    method_url = r'sendGame'
    payload = {'chat_id': chat_id, 'game_short_name': game_short_name}
    if disable_notification:
        payload['disable_notification'] = disable_notification
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(token, method_url, params=payload)


# https://core.telegram.org/bots/api#setgamescore
def set_game_score(token, user_id, score, force=None, disable_edit_message=None, chat_id=None, message_id=None, inline_message_id=None):
    """
    Use this method to set the score of the specified user in a game.
    :param token [String, Required]:
    :param user_id [Integer, Required]:
    :param score [Integer, Required]: 
    :param force [Boolean, Optional]: 
    :param disable_edit_message [Boolean, Optional]: 
    :param chat_id [Optional, required if inline_message_id is not specified]:
    :param message_id [Integer, Optional, required if inline_message_id is not specified]:
    :param inline_message_id [Integer, Optional, required if chat_id and message_id are not specified]:
    :returns: On success a Message object, otherwise returns True.
    """
    method_url = r'setGameScore'
    payload = {'user_id': user_id, 'score': score}
    if force:
        payload['force'] = force
    if chat_id:
        payload['chat_id'] = chat_id
    if message_id:
        payload['message_id'] = message_id
    if inline_message_id:
        payload['inline_message_id'] = inline_message_id
    if disable_edit_message:
        payload['disable_edit_message'] = disable_edit_message
    return _make_request(token, method_url, params=payload)


# https://core.telegram.org/bots/api#getgamehighscores
def get_game_high_scores(token, user_id, chat_id=None, message_id=None, inline_message_id=None):
    """
    Use this method to get data for high score tables.
    :param token [String, Required]:
    :param user_id [Integer, Required]: 
    :param chat_id [String or Integer, Optional]:
    :param message_id [Integer, Optional]:
    :param inline_message_id [Integer, Optional]:
    :returns: an Array of GameHighScore objects.
    """
    method_url = r'getGameHighScores'
    payload = {'user_id': user_id}
    if chat_id:
        payload['chat_id'] = chat_id
    if message_id:
        payload['message_id'] = message_id
    if inline_message_id:
        payload['inline_message_id'] = inline_message_id
    return _make_request(token, method_url, params=payload)


# CUSTOM FUNCTIONS (NOT PROVIDED BY TELEGRAM BOT API)
def get_file_url(token, file_id):
    if FILE_URL is None:
        return "https://api.telegram.org/file/bot{0}/{1}".format(token, get_file(token, file_id)['file_path'])
    else:
        return FILE_URL.format(token, get_file(token, file_id)['file_path'])


def download_file(token, file_path):
    if FILE_URL is None:
        url = "https://api.telegram.org/file/bot{0}/{1}".format(
            token, file_path)
    else:
        url = FILE_URL.format(token, file_path)

    result = _get_req_session().get(url, proxies=proxy)
    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text)
        raise ApiException(msg, 'Download file', result)
    return result.content


def _convert_list_json_serializable(results):
    ret = ''
    for r in results:
        if isinstance(r, types.JsonSerializable):
            ret = ret + r.to_json() + ','
    if len(ret) > 0:
        ret = ret[:-1]
    return '[' + ret + ']'


def _convert_markup(markup):
    if isinstance(markup, types.JsonSerializable):
        return markup.to_json()
    return markup


def _convert_input_media(media):
    if isinstance(media, types.InputMedia):
        return media._convert_input_media()
    return None, None


def _convert_input_media_array(array):
    media = []
    files = {}
    for input_media in array:
        if isinstance(input_media, types.InputMedia):
            media_dict = input_media.to_dic()
            if media_dict['media'].startswith('attach://'):
                key = media_dict['media'].replace('attach://', '')
                files[key] = input_media.media
            media.append(media_dict)
    return json.dumps(media), files


def _no_encode(func):
    def wrapper(key, val):
        if key == 'filename':
            return u'{0}={1}'.format(key, val)
        else:
            return func(key, val)

    return wrapper


class ApiException(Exception):
    """
    This class represents an Exception thrown when a call to the Telegram API fails.
    In addition to an informative message, it has a `function_name` and a `result` attribute, which respectively
    contain the name of the failed function and the returned result that made the function to be considered  as
    failed.
    """

    def __init__(self, msg, function_name, result):
        super(ApiException, self).__init__(
            "A request to the Telegram API was unsuccessful. {0}".format(msg))
        self.function_name = function_name
        self.result = result
