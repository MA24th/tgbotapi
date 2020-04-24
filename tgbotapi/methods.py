import json
import requests
from .types import JsonSerializable, InputMedia
from .utilities import per_thread, logger, is_string

""" Telegram Available methods
    All methods in the Bot API are case-insensitive. We support GET and POST HTTP methods. 
    Use either URL query string or application/json or application/x-www-form-urlencoded,
    Or multipart/form-data for passing parameters in Bot API requests.
    On successful call, a JSON-object containing the result will be returned.
"""


def _get_req_session(reset=False):
    return per_thread('req_session', lambda: requests.session(), reset)


def _make_request(method, api_url, api_method, files, params, proxies):
    """
    Makes a request to the Telegram API.
    :param str method: HTTP method ['get', 'post'].
    :param str api_url: telegram api url for api_method.
    :param str api_method: Name of the API method to be called. (E.g. 'getUpdates').
    :param any or None files: files content's a data.
    :param dict or None params: Should be a dictionary with key-value pairs.
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :return dict result: a JSON dictionary.
    """
    logger.debug("Request: method={0} url={1} params={2} files={3}".format(method, api_url, params, files))
    timeout = 9999
    if params:
        if 'timeout' in params:
            timeout = params['timeout'] + 10

    result = _get_req_session().request(method, api_url, params, data=None, headers=None,
                                        cookies=None, files=files, auth=None, timeout=timeout, allow_redirects=True,
                                        proxies=proxies, verify=None, stream=None, cert=None)
    logger.debug("The server returned: '{0}'".format(result.text.encode('utf8')))
    return _check_result(api_method, result)['result']


def _check_result(api_method, result):
    """
    Checks whether `result` is a valid API response.
    A result is considered invalid if:
        - The server returned an HTTP response code other than 200.
        - The content of the result is invalid JSON.
        - The method call was unsuccessful (The JSON 'ok' field equals False).

    :raises ApiException: if one of the above listed cases is applicable.
    :param str api_method: The name of the method called.
    :param any result: The returned result of the method request.
    :return any result_json: a JSON dictionary.
    """
    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text.encode('utf8'))
        raise ApiException(msg, api_method, result)

    try:
        result_json = result.json()
    except Exception:
        msg = 'The server returned an invalid JSON response. Response body:\n[{0}]' \
            .format(result.text.encode('utf8'))
        raise ApiException(msg, api_method, result)

    if not result_json['ok']:
        msg = 'Error code: {0} Description: {1}' \
            .format(result_json['error_code'], result_json['description'])
        raise ApiException(msg, api_method, result)
    return result_json


def get_updates(token, proxies, offset=None, limit=None, timeout=0, allowed_updates=None):
    """
    Use this method to receive incoming updates using long polling.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int offset: Identifier of the first update to be returned.
    :param int limit: Limits the number of updates to be retrieved.
    :param int timeout: Timeout in seconds for long polling, Defaults to 0.
    :param list allowed_updates: An Array of String.
    :return: An Array of Update objects.
    """
    method = r'get'
    api_method = r'getUpdates'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {}
    if offset:
        params['offset'] = offset
    if limit:
        params['limit'] = limit
    if timeout:
        params['timeout'] = timeout
    if allowed_updates:
        params['allowed_updates'] = json.dumps(allowed_updates)
    return _make_request(method, api_url, api_method, files, params, proxies)


def set_webhook(token, proxies, url=None, certificate=None, max_connections=None, allowed_updates=None):
    """
    Use this method to specify a url and receive incoming updates via an outgoing webhook.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param str url: HTTPS url to send updates to. Use an empty string to remove webhook integration.
    :param any certificate: Upload your public key [InputFile] certificate so that the root certificate in use can be checked.
    :param int max_connections: Maximum allowed number of simultaneous HTTPS connections to the webhook for update delivery, 1-100. Defaults to 40.
    :param list allowed_updates: A JSON-serialized list of the update types you want your bot to receive.
    :return: True On success.
    """
    method = r'post'
    api_method = r'setWebhook'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'url': url if url else ""}
    if certificate:
        files = {'certificate': certificate}
    if max_connections:
        params['max_connections'] = max_connections
    if allowed_updates:
        params['allowed_updates'] = json.dumps(allowed_updates)
    return _make_request(method, api_url, api_method, files, params, proxies)


def delete_webhook(token, proxies):
    """
    Use this method to remove webhook integration if you decide to switch back to getUpdates. 
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :return: True on success.
    """
    method = r'post'
    api_method = r'deleteWebhook'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = None
    return _make_request(method, api_url, api_method, files, params, proxies)


def get_webhook_info(token, proxies):
    """
    Use this method to get current webhook status. 
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :return: a WebhookInfo object, otherwise an object with the url field empty.
    """
    method = r'get'
    api_method = r'getWebhookInfo'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = None
    return _make_request(method, api_url, api_method, files, params, proxies)


def get_me(token, proxies):
    """
    A simple method for testing your bot's auth token. 
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :return: a User object.
    """
    method = r'get'
    api_method = r'getMe'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = None
    return _make_request(method, api_url, api_method, files, params, proxies)


def send_message(token, proxies, chat_id, text, parse_mode=None, disable_web_page_preview=False,
                 disable_notification=False, reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send text messages. On success, the sent Message is returned.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param str text: Text of the message to be sent, 1-4096 characters after entities parsing.
    :param str parse_mode: Send Markdown or HTML.
    :param bool disable_web_page_preview: Disables link previews for links in this message.
    :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
    :param int reply_to_message_id: If the message is a reply, ID of the original message.
    :param dict reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
    :return: a Message object.
    """
    method = r'post'
    api_method = r'sendMessage'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'text': text}
    if parse_mode:
        params['parse_mode'] = parse_mode
    if disable_web_page_preview:
        params['disable_web_page_preview'] = disable_web_page_preview
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        params['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(method, api_url, api_method, files, params, proxies)


def forward_message(token, proxies, chat_id, from_chat_id, message_id, disable_notification=False):
    """
    Use this method to forward messages of any kind.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param int or str from_chat_id: Unique identifier for the chat where the original message was sent.
    :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
    :param int message_id: Message identifier in the chat specified in from_chat_id.
    :return: a Message object.
    """
    method = r'post'
    api_method = r'forwardMessage'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'from_chat_id': from_chat_id, 'message_id': message_id}
    if disable_notification:
        params['disable_notification'] = disable_notification
    return _make_request(method, api_url, api_method, files, params, proxies)


def send_photo(token, proxies, chat_id, photo, caption=None, parse_mode=None, disable_notification=False,
               reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send photos.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param any photo: Photo [file_id or InputFile] to send.
    :param str caption: Photo caption, 0-1024 characters after entities parsing
    :param str parse_mode: Send Markdown or HTML.
    :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
    :param int reply_to_message_id: If the message is a reply, ID of the original message.
    :param dict reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
    :return: a Message object.
    """
    method = r'post'
    api_method = r'sendPhoto'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id}
    if not is_string(photo):
        files = {'photo': photo}
    else:
        params['photo'] = photo
    if caption:
        params['caption'] = caption
    if parse_mode:
        params['parse_mode'] = parse_mode
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        params['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(method, api_url, api_method, files, params, proxies)


def send_audio(token, proxies, chat_id, audio, caption=None, parse_mode=None, duration=None, performer=None, title=None,
               thumb=None, disable_notification=False, reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send audio files.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param any audio: Audio [file_id or InputFile] to send.
    :param str caption: Photo caption, 0-1024 characters after entities parsing
    :param str parse_mode: Send Markdown or HTML.
    :param int duration: Duration of the audio in seconds.
    :param str performer: Performer.
    :param str title: Track Name.
    :param any thumb: Thumbnail [file_id or InputFile] of the file sent.
    :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
    :param int reply_to_message_id: If the message is a reply, ID of the original message.
    :param dict reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
    :return: a Message object.
    """
    method = r'post'
    api_method = r'sendAudio'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id}
    if not is_string(audio):
        files = {'audio': audio}
    else:
        params['audio'] = audio
    if caption:
        params['caption'] = caption
    if parse_mode:
        params['parse_mode'] = parse_mode
    if duration:
        params['duration'] = duration
    if performer:
        params['performer'] = performer
    if title:
        params['title'] = title
    if thumb:
        params['thumb'] = thumb
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        params['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(method, api_url, api_method, files, params, proxies)


def send_document(token, proxies, chat_id, document, thumb=None, caption=None, parse_mode=None, disable_notification=False,
                  reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send general files.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param any document: File [file_id or InputFile] to send.
    :param any thumb: Thumbnail [file_id or InputFile] of the file sent.
    :param str caption: Document caption, 0-1024 characters after entities parsing
    :param str parse_mode: Send Markdown or HTML.
    :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
    :param int reply_to_message_id: If the message is a reply, ID of the original message.
    :param dict reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
    :return: a Message object.
    """
    method = r'post'
    api_method = r'sendDocument'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id}
    if not is_string(document):
        files = {'document': document}
    else:
        params['document'] = document
    if thumb:
        params['thumb'] = thumb
    if caption:
        params['caption'] = caption
    if parse_mode:
        params['parse_mode'] = parse_mode
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        params['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(method, api_url, api_method, files, params, proxies)


def send_video(token, proxies, chat_id, video, duration=None, width=None, height=None, thumb=None, caption=None, parse_mode=None,
               supports_streaming=None, disable_notification=False, reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send video files.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param any video: Video [file_id or InputFile] to send.
    :param int duration: Duration of the video in seconds.
    :param int width: Video width.
    :param int height: Video height.
    :param any thumb: Thumbnail [file_id or InputFile] of the file sent.
    :param str caption: Video caption, 0-1024 characters after entities parsing.
    :param str parse_mode: Send Markdown or HTML.
    :param bool supports_streaming: Pass True, if the uploaded video is suitable for streaming.
    :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
    :param int reply_to_message_id: If the message is a reply, ID of the original message.
    :param dict reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
    :return: a Message object.
    """
    method = r'post'
    api_method = r'sendVideo'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id}
    if not is_string(video):
        files = {'video': video}
    else:
        params['video'] = video
    if duration:
        params['duration'] = duration
    if width:
        params['width'] = width
    if height:
        params['height'] = height
    if thumb:
        params['thumb'] = thumb
    if caption:
        params['caption'] = caption
    if parse_mode:
        params['parse_mode'] = parse_mode
    if supports_streaming:
        params['supports_streaming'] = supports_streaming
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        params['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(method, api_url, api_method, files, params, proxies)


def send_animation(token, proxies, chat_id, animation, duration=None, width=None, height=None, thumb=None, caption=None,
                   parse_mode=None, disable_notification=False, reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send animation files.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param any animation: Animation [file_id or InputFile] to send.
    :param int duration: Duration of the animation in seconds.
    :param int width: Animation width.
    :param int height: Animation height.
    :param any thumb: Thumbnail [file_id or InputFile] of the file sent.
    :param str caption: Video caption, 0-1024 characters after entities parsing.
    :param str parse_mode: Send Markdown or HTML.
    :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
    :param int reply_to_message_id: If the message is a reply, ID of the original message.
    :param dict reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
    :return: a Message object.
    """
    method = r'post'
    api_method = r'sendAnimation'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id}
    if not is_string(animation):
        files = {'animation': animation}
    else:
        params['animation'] = animation
    if duration:
        params['duration'] = duration
    if width:
        params['width'] = width
    if height:
        params['height'] = height
    if thumb:
        params['thumb'] = thumb
    if caption:
        params['caption'] = caption
    if parse_mode:
        params['parse_mode'] = parse_mode
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        params['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(method, api_url, api_method, files, params, proxies)


def send_voice(token, proxies, chat_id, voice, caption=None, parse_mode=None, duration=None, disable_notification=False,
               reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send audio files.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param any voice: Audio [file_id or InputFile] to send.
    :param str caption: Video caption, 0-1024 characters after entities parsing.
    :param str parse_mode: Send Markdown or HTML.
    :param int duration: Duration of the voice in seconds.
    :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
    :param int reply_to_message_id: If the message is a reply, ID of the original message.
    :param dict reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
    :return: a Message object.
    """
    method = r'post'
    api_method = r'sendVoice'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    params = {'chat_id': chat_id}
    files = None
    if not is_string(voice):
        files = {'voice': voice}
    else:
        params['voice'] = voice
    if caption:
        params['caption'] = caption
    if parse_mode:
        params['parse_mode'] = parse_mode
    if duration:
        params['duration'] = duration
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        params['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(method, api_url, api_method, files, params, proxies)


def send_video_note(token, proxies, chat_id, video_note, duration=None, length=None, thumb=None, disable_notification=False,
                    reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send video messages.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param any video_note: Video note [file_id or InputFile] to send.
    :param int duration: Duration of the VideoNote in seconds.
    :param int length: Video width and height, i.e. diameter of the video message.
    :param any thumb: Thumbnail [file_id or InputFile] of the file sent.
    :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
    :param int reply_to_message_id: If the message is a reply, ID of the original message.
    :param dict reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
    :return: a Message object.
    """
    method = r'post'
    api_method = r'sendVideoNote'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    params = {'chat_id': chat_id}
    files = None
    if not is_string(video_note):
        files = {'video_note': video_note}
    else:
        params['video_note'] = video_note
    if duration:
        params['duration'] = duration
    if length:
        params['length'] = length
    if thumb:
        params['thumb'] = thumb
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        params['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(method, api_url, api_method, files, params, proxies)


def send_media_group(token, proxies, chat_id, media, disable_notification=False, reply_to_message_id=None):
    """
    Use this method to send a group of photos or videos as an album.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param list media: A JSON-serialized array of [InputMediaPhoto or InputMediaVideo] to be sent, must include 2–10 items
    :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
    :param int reply_to_message_id: If the message is a reply, ID of the original message.
    :return: a Messages object.
    """
    method = r'post'
    api_method = r'sendMediaGroup'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    media_json, files = _convert_input_media_array(media)
    params = {'chat_id': chat_id, 'media': media_json}
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    return _make_request(method, api_url, api_method, files, params, proxies)


def send_location(token, proxies, chat_id, latitude, longitude, live_period=None, disable_notification=False,
                  reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send point on the map.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param float latitude: Latitude of the location.
    :param float longitude: Longitude of the location.
    :param int live_period: Period in seconds for which the location will be updated, should be between 60 and 86400.
    :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
    :param int reply_to_message_id: If the message is a reply, ID of the original message.
    :param dict reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
    :return: a Message object.
    """
    method = r'post'
    api_method = r'sendLocation'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id,
              'latitude': latitude, 'longitude': longitude}
    if live_period:
        params['live_period'] = live_period
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        params['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(method, api_url, api_method, files, params, proxies)


def edit_message_live_location(token, proxies, latitude, longitude, chat_id=None, message_id=None,
                               inline_message_id=None, reply_markup=None):
    """
    Use this method to edit live location messages.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Required if inline_message_id is not specified, Unique identifier for the target chat.
    :param int message_id: Required if inline_message_id is not specified, Identifier of the message to edit.
    :param str inline_message_id: Required if chat_id and message_id are not specified, Identifier of the inline message.
    :param float latitude: Latitude of the location.
    :param float longitude: Longitude of the location.
    :param any reply_markup: A JSON-serialized object for an InlineKeyboardMarkup.
    :return: a Message object, otherwise True.
    """
    method = r'post'
    api_method = r'editMessageLiveLocation'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'latitude': latitude, 'longitude': longitude}
    if chat_id:
        params['chat_id'] = chat_id
    if message_id:
        params['message_id'] = message_id
    if inline_message_id:
        params['inline_message_id'] = inline_message_id
    if reply_markup:
        params['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(method, api_url, api_method, files, params, proxies)


def stop_message_live_location(token, proxies, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
    """
    Use this method to stop updating a live location message before live_period expires.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Required if inline_message_id is not specified, Unique identifier for the target chat.
    :param int message_id: Required if inline_message_id is not specified, Identifier of the message to edit.
    :param str inline_message_id: Required if chat_id and message_id are not specified, Identifier of the inline message.
    :param any reply_markup: A JSON-serialized object for an InlineKeyboardMarkup.
    :return: a Message object, otherwise True.
    """
    method = r'post'
    api_method = r'stopMessageLiveLocation'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {}
    if chat_id:
        params['chat_id'] = chat_id
    if message_id:
        params['message_id'] = message_id
    if inline_message_id:
        params['inline_message_id'] = inline_message_id
    if reply_markup:
        params['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(method, api_url, api_method, files, params, proxies)


def send_venue(token, proxies, chat_id, latitude, longitude, title, address, foursquare_id=None, foursquare_type=None,
               disable_notification=False, reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send information about a venue.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param float latitude: Latitude of the location.
    :param float longitude: Longitude of the location.
    :param str title: Name of the venue.
    :param str address: Address of the venue.
    :param str foursquare_id: Foursquare identifier of the venue.
    :param str foursquare_type: Foursquare type of the venue, if known.
    :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
    :param int reply_to_message_id: If the message is a reply, ID of the original message.
    :param dict reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
    :return: a Message object.
    """
    method = r'post'
    api_method = r'sendVenue'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude, 'title': title, 'address': address}
    if foursquare_id:
        params['foursquare_id'] = foursquare_id
    if foursquare_type:
        params['foursquare_type'] = foursquare_type
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        params['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(method, api_url, api_method, files, params, proxies)


def send_contact(token, proxies, chat_id, phone_number, first_name, last_name=None, vcard=None, disable_notification=False,
                 reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send information about a venue.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param str phone_number: Contact's phone number.
    :param str first_name: Contact's first name.
    :param str last_name: Contact's last name.
    :param str vcard: Additional data about the contact in the form of a vCard, 0-2048 bytes.
    :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
    :param int reply_to_message_id: If the message is a reply, ID of the original message.
    :param dict reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
    :return: a Message object.
    """
    method = r'post'
    api_method = r'sendContact'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id,
              'phone_number': phone_number, 'first_name': first_name}
    if last_name:
        params['last_name'] = last_name
    if vcard:
        params['vcard'] = vcard
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        params['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(method, api_url, api_method, files, params, proxies)


def send_poll(token, proxies, chat_id, question, options, is_anonymous=True, type='regular', allows_multiple_answers=False,
              correct_option_id=None, explanation=None, explanation_parse_mode=None, open_period=None, close_date=None,
              is_closed=True, disable_notifications=False, reply_to_message_id=None,
              reply_markup=None):
    """
    Use this method to send information about a venue.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param str question: Poll question, 1-255 characters.
    :param list options: A JSON-serialized list of answer options, 2-10 strings 1-100 characters each.
    :param bool is_anonymous: True, if the poll needs to be anonymous, defaults to True.
    :param str type: Poll type, “quiz” or “regular”, defaults to “regular”.
    :param bool allows_multiple_answers: True, if the poll allows multiple answers, ignored for polls in quiz mode, defaults to False.
    :param int correct_option_id: 0-based identifier of the correct answer option, required for polls in quiz mode.
    :param str or None explanation: Text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style poll.
    :param str or None explanation_parse_mode: Mode for parsing entities in the explanation.
    :param int or None open_period: Amount of time in seconds the poll will be active after creation, 5-600. Can't be used together with close_date.
    :param int or None close_date: Point in time (Unix timestamp) when the poll will be automatically closed. Must be at least 5 and no more than 600 seconds in the future. Can't be used together with open_period.
    :param bool is_closed: Pass True, if the poll needs to be immediately closed. This can be useful for poll preview.
    :param bool disable_notifications: Sends the message silently. Users will receive a notification with no sound.
    :param int reply_to_message_id: If the message is a reply, ID of the original message.
    :param any reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
    :return: a Message object.
    """
    method = r'post'
    api_method = r'sendPoll'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'question': question, 'options': _convert_list_json_serializable(options)}
    if is_anonymous:
        params['is_anonymous'] = is_anonymous
    if type:
        params['type'] = type
    if allows_multiple_answers:
        params['allows_multiple_answers'] = allows_multiple_answers
    if correct_option_id:
        params['correct_option_id'] = correct_option_id
    if explanation:
        params['explanation'] = explanation
    if explanation_parse_mode:
        params['explanation_parse_mode'] = explanation_parse_mode
    if open_period:
        params['open_period'] = open_period
    if close_date:
        params['close_date'] = close_date
    if is_closed:
        params['is_closed'] = is_closed
    if disable_notifications:
        params['disable_notification'] = disable_notifications
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        params['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(method, api_url, api_method, files, params, proxies)


def send_dice(token, proxies, chat_id, emoji='🎲', disable_notification=False, reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send a dice.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param str emoji: Emoji on which the dice throw animation is based. Currently, must be one of “🎲” or “🎯”, Defaults to “🎲” .
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
    :param int or None reply_to_message_id: If the message is a reply, ID of the original message.
    :param list[dict] or None reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
    :return: a Message object.
    """
    method = r'post'
    api_method = r'sendDice'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'emoji': emoji}
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        params['reply_markup'] = reply_markup
    return _make_request(method, api_url, api_method, files, params, proxies)


def send_chat_action(token, proxies, chat_id, action):
    """
    Use this method when you need to tell the user that something is happening on the bot's side.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param str action: Type of action to broadcast.
    :return: True On success.
    """
    method = r'post'
    api_method = r'sendChatAction'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'action': action}
    return _make_request(method, api_url, api_method, files, params, proxies)


def get_user_profile_photos(token, proxies, user_id, offset=None, limit=100):
    """
    Use this method to get a list of profile pictures for a user.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str user_id: Unique identifier of the target user.
    :param int offset: Sequential number of the first photo to be returned. By default, all photos are returned.
    :param int limit: Limits the number of photos to be retrieved. Values between 1—100 are accepted. Defaults to 100.
    :return: a UserProfilePhoto object.
    """
    method = r'post'
    api_method = r'getUserProfilePhotos'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'user_id': user_id}
    if offset:
        params['offset'] = offset
    if limit:
        params['limit'] = limit
    return _make_request(method, api_url, api_method, files, params, proxies)


def get_file(token, proxies, file_id):
    """
    Use this method to get basic info about a file and prepare it for downloading.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str file_id: File identifier to get info about
    :return: a File object.
    """
    method = r'post'
    api_method = r'getFile'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'file_id': file_id}
    return _make_request(method, api_url, api_method, files, params, proxies)


def download_file(token, proxies, file_path):
    """
    Use this method to download file with specified file_path.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param file_path: File path, User https://api.telegram.org/file/bot<token>/<file_path> to get the file.
    :return: any, On success.
    """
    api_url = "https://api.telegram.org/file/bot{0}/{1}".format(token, file_path)
    result = _get_req_session().get(api_url, proxies)
    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text)
        raise ApiException(msg, 'Download file', result)
    return result.content


def kick_chat_member(token, proxies, chat_id, user_id, until_date=None):
    """
    Use this method to kick a user from a group, a supergroup or a channel.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param int or str user_id: Unique identifier of the target user.
    :param int until_date: Date when the user will be unbanned, unix time.
    :return: True On success.
    """
    method = r'post'
    api_method = 'kickChatMember'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'user_id': user_id}
    if until_date:
        params['until_date'] = until_date
    return _make_request(method, api_url, api_method, files, params, proxies)


def unban_chat_member(token, proxies, chat_id, user_id):
    """
    Use this method to unban a previously kicked user in a supergroup or channel.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param int or str user_id: Unique identifier of the target user.
    :return: True On success.
    """
    method = r'post'
    api_method = 'unbanChatMember'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'user_id': user_id}
    return _make_request(method, api_url, api_method, files, params, proxies)


def restrict_chat_member(token, proxies, chat_id, user_id, permissions, until_date=None):
    """
    Use this method to restrict a user in a supergroup.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param int or str user_id: Unique identifier of the target user.
    :param dict permissions: New user permissions must be ChatPermissions object.
    :param int until_date: 	Date when restrictions will be lifted for the user, unix time.
    :return: True On success.
    """
    method = r'post'
    api_method = 'restrictChatMember'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'user_id': user_id, 'permissions': permissions}
    if until_date:
        params['until_date'] = until_date
    return _make_request(method, api_url, api_method, files, params, proxies)


def promote_chat_member(token, proxies, chat_id, user_id, can_change_info=None, can_post_messages=None,
                        can_edit_messages=None, can_delete_messages=None, can_invite_users=None,
                        can_restrict_members=None, can_pin_messages=None, can_promote_members=None):
    """
    Use this method to promote or demote a user in a supergroup or a channel.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param int or str user_id: Unique identifier of the target user.
    :param bool can_change_info: Pass True, if the administrator can change chat title, photo and other settings.
    :param bool can_post_messages: Pass True, if the administrator can create channel posts, channels only.
    :param bool can_edit_messages: Pass True, if the administrator can edit messages of other users and can pin messages, channels only.
    :param bool can_delete_messages: Pass True, if the administrator can delete messages of other users.
    :param bool can_invite_users: Pass True, if the administrator can invite new users to the chat.
    :param bool can_restrict_members: Pass True, if the administrator can restrict, ban or unban chat members.
    :param bool can_pin_messages: Pass True, if the administrator can pin messages, supergroups only.
    :param bool can_promote_members: Pass True, if the administrator can add new administrators with a subset of his own privileges or demote administrators that he has promoted, directly or indirectly (promoted by administrators that were appointed by him).
    :return: True On success.
    """
    method = r'post'
    api_method = 'promoteChatMember'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'user_id': user_id}
    if can_change_info:
        params['can_change_info'] = can_change_info
    if can_post_messages:
        params['can_post_messages'] = can_post_messages
    if can_edit_messages:
        params['can_edit_messages'] = can_edit_messages
    if can_delete_messages:
        params['can_delete_messages'] = can_delete_messages
    if can_invite_users:
        params['can_invite_users'] = can_invite_users
    if can_restrict_members:
        params['can_restrict_members'] = can_restrict_members
    if can_pin_messages:
        params['can_pin_messages'] = can_pin_messages
    if can_promote_members:
        params['can_promote_members'] = can_promote_members
    return _make_request(method, api_url, api_method, files, params, proxies)


def set_chat_administrator_custom_title(token, proxies, chat_id, user_id, custom_title):
    """
    Use this method to set a custom title for an administrator in a supergroup promoted by the bot. 
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param int or str user_id: Unique identifier of the target user.
    :param str custom_title: New custom title for the administrator; 0-16 characters.
    :return: True on success.
    """
    method = r'post'
    api_method = r'setChatAdministratorCustomTitle'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'user_id': user_id, 'custom_title': custom_title}
    return _make_request(method, api_url, api_method, files, params, proxies)


def set_chat_permissions(token, proxies, chat_id, permissions):
    """
    Use this method to set default chat permissions for all members. 
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param dict permissions: New default chat permissions must be a ChatPermissions object
    :return: True on success.
    """
    method = r'post'
    api_method = r'setChatPermissions'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'permissions': permissions}
    return _make_request(method, api_url, api_method, files, params, proxies)


def export_chat_invite_link(token, proxies, chat_id):
    """
    Use this method to generate a new invite link for a chat. 
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :return: new link as String on success.
    """
    method = r'get'
    api_method = r'exportChatInviteLink'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id}
    return _make_request(method, api_url, api_method, files, params, proxies)


def set_chat_photo(token, proxies, chat_id, photo):
    """
    Use this method to set a new profile photo for the chat.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param any photo: Use this method to set a new profile photo for the chat.
    :return: True on success.
    """
    method = r'post'
    api_method = r'setChatPhoto'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id}
    if not is_string(photo):
        files = {'photo': photo}
    else:
        params['photo'] = photo
    return _make_request(method, api_url, api_method, files, params, proxies)


def delete_chat_photo(token, proxies, chat_id):
    """
    Use this method to delete a chat photo.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :return: True on success.
    """
    method = r'post'
    api_method = r'deleteChatPhoto'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id}
    return _make_request(method, api_url, api_method, files, params, proxies)


def set_chat_title(token, proxies, chat_id, title):
    """
    Use this method to change the title of a chat.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param str title: New chat title, 1-255 characters.
    :return: True on success.
    """
    method = r'post'
    api_method = r'setChatTitle'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'title': title}
    return _make_request(method, api_url, api_method, files, params, proxies)


def set_chat_description(token, proxies, chat_id, description=None):
    """
    Use this method to change the description of a group, a supergroup or a channel.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param str description: New chat description, 0-255 characters.
    :return: True on success.
    """
    method = r'post'
    api_method = r'setChatDescription'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id}
    if description:
        params['description'] = description
    return _make_request(method, api_url, api_method, files, params, proxies)


def pin_chat_message(token, proxies, chat_id, message_id, disable_notification=False):
    """
    Use this method to pin a message in a group, a supergroup, or a channel.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param int message_id: Identifier of a message to pin.
    :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
    :return: True on success.
    """
    method = r'post'
    api_method = r'pinChatMessage'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'message_id': message_id}
    if disable_notification:
        params['disable_notification'] = disable_notification
    return _make_request(method, api_url, api_method, files, params, proxies)


def unpin_chat_message(token, proxies, chat_id):
    """
    Use this method to unpin a message in a group, a supergroup, or a channel.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :return: True on success.
    """
    method = r'post'
    api_method = r'unpinChatMessage'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id}
    return _make_request(method, api_url, api_method, files, params, proxies)


def leave_chat(token, proxies, chat_id):
    """
    Use this method for your bot to leave a group, supergroup or channel.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :return: True on success.
    """
    method = r'post'
    api_method = r'leaveChat'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id}
    return _make_request(method, api_url, api_method, files, params, proxies)


def get_chat(token, proxies, chat_id):
    """
    Use this method to get up to date information about the chat.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :return: a Chat object.
    """
    method = r'get'
    api_method = r'getChat'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id}
    return _make_request(method, api_url, api_method, files, params, proxies)


def get_chat_administrators(token, proxies, chat_id):
    """
    Use this method to get a list of administrators in a chat.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :return: an Array of ChatMember object.
    """
    method = r'get'
    api_method = r'getChatAdministrators'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id}
    return _make_request(method, api_url, api_method, files, params, proxies)


def get_chat_members_count(token, proxies, chat_id):
    """
    Use this method to get the number of members in a chat.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :return: Integer On success.
    """
    method = r'get'
    api_method = r'getChatMembersCount'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id}
    return _make_request(method, api_url, api_method, files, params, proxies)


def get_chat_member(token, proxies, chat_id, user_id):
    """
    Use this method to get information about a member of a chat.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param int user_id: Unique identifier of the target user.
    :return: a ChatMember object On success.
    """
    method = r'get'
    api_method = r'getChatMember'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'user_id': user_id}
    return _make_request(method, api_url, api_method, files, params, proxies)


def set_chat_sticker_set(token, proxies, chat_id, sticker_set_name):
    """
    Use this method to set a new group sticker set for a supergroup.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param str sticker_set_name: Name of the sticker set to be set as the group sticker set.
    :return: True On success.
    """
    method = r'post'
    api_method = r'setChatStickerSet'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'sticker_set_name': sticker_set_name}
    return _make_request(method, api_url, api_method, files, params, proxies)


def delete_chat_sticker_set(token, proxies, chat_id):
    """
    Use this method to delete a group sticker set from a supergroup.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :return: True On success.
    """
    method = r'post'
    api_method = r'deleteChatStickerSet'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id}
    return _make_request(method, api_url, api_method, files, params, proxies)


def answer_callback_query(token, proxies, callback_query_id, text=None, show_alert=False, url=None, cache_time=None):
    """
    Use this method to send answers to callback queries sent from inline keyboards.     
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param str callback_query_id: Unique identifier for the query to be answered.
    :param str text: Text of the notification. If not specified, nothing will be shown to the user, 0-200 characters.
    :param bool show_alert: If true, an alert will be shown by the client instead of a notification at the top of the chat screen. Defaults to false.
    :param str url: URL that will be opened by the user's client.
    :param int cache_time: The maximum amount of time in seconds that the result of the callback query may be cached client-side.
    :return: True On success.
    """
    method = r'post'
    api_method = r'answerCallbackQuery'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'callback_query_id': callback_query_id}
    if text:
        params['text'] = text
    if show_alert:
        params['show_alert'] = show_alert
    if url:
        params['url'] = url
    if cache_time is not None:
        params['cache_time'] = cache_time
    return _make_request(method, api_url, api_method, files, params, proxies)


def set_my_commands(token, proxies, commands):
    """
    Use this method to change the list of the bot's commands.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param list commands: A JSON-serialized list of bot commands to be set as the list of the bot's commands. At most 100 commands can be specified.
    :return: True On success.
    """
    method = r'post'
    api_method = r'setMyCommands'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'commands': commands}
    return _make_request(method, api_url, api_method, files, params, proxies)


def get_my_commands(token, proxies):
    """
    Use this method to get the current list of the bot's commands.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :return: Array of BotCommand On success.
    """
    method = r'get'
    api_method = r'getMyCommands'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = None
    return _make_request(method, api_url, api_method, files, params, proxies)


# Updating messages
def edit_message_text(token, proxies, text, chat_id=None, message_id=None, inline_message_id=None, parse_mode=None,
                      disable_web_page_preview=False, reply_markup=None):
    """
    Use this method to edit text and game messages.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat.
    :param int message_id: Required if inline_message_id is not specified. Identifier of the message to edit.
    :param str inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
    :param str text: Text of the message to be sent, 1-4096 characters after entities parsing.
    :param str parse_mode: Send Markdown or HTML.
    :param bool disable_web_page_preview: Disables link previews for links in this message
    :param any reply_markup: A JSON-serialized object for an InlineKeyboardMarkup.
    :return: a Message object On success, otherwise True.
    """
    method = r'post'
    api_method = r'editMessageText'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'text': text}
    if chat_id:
        params['chat_id'] = chat_id
    if message_id:
        params['message_id'] = message_id
    if inline_message_id:
        params['inline_message_id'] = inline_message_id
    if parse_mode:
        params['parse_mode'] = parse_mode
    if disable_web_page_preview:
        params['disable_web_page_preview'] = disable_web_page_preview
    if reply_markup:
        params['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(method, api_url, api_method, files, params, proxies)


def edit_message_caption(token, proxies, caption, chat_id=None, message_id=None, inline_message_id=None, parse_mode=None,
                         reply_markup=None):
    """
    Use this method to edit captions of messages.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat.
    :param int message_id: Required if inline_message_id is not specified. Identifier of the message to edit.
    :param str inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
    :param str caption: New caption of the message, 0-1024 characters after entities parsing.
    :param str parse_mode: Send Markdown or HTML.
    :param any reply_markup: A JSON-serialized object for an InlineKeyboardMarkup.
    :return: a Message object On success, otherwise True.
    """
    method = r'post'
    api_method = r'editMessageCaption'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'caption': caption}
    if chat_id:
        params['chat_id'] = chat_id
    if message_id:
        params['message_id'] = message_id
    if inline_message_id:
        params['inline_message_id'] = inline_message_id
    if parse_mode:
        params['parse_mode'] = parse_mode
    if reply_markup:
        params['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(method, api_url, api_method, files, params, proxies)


def edit_message_media(token, proxies, media, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
    """
    Use this method to edit animation, audio, document, photo, or video messages.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat.
    :param int message_id: Required if inline_message_id is not specified. Identifier of the message to edit.
    :param str inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
    :param any media: A JSON-serialized object for a new media content of the message must be InputMedia.
    :param any reply_markup: A JSON-serialized object for an InlineKeyboardMarkup.:
    :return: a Message object On success, otherwise True.
    """
    method = r'post'
    api_method = r'editMessageMedia'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    media_json, files = _convert_input_media(media)
    params = {'media': media_json}
    if chat_id:
        params['chat_id'] = chat_id
    if message_id:
        params['message_id'] = message_id
    if inline_message_id:
        params['inline_message_id'] = inline_message_id
    if reply_markup:
        params['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(method, api_url, api_method, files, params, proxies)


def edit_message_reply_markup(token, proxies, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
    """
    Use this method to edit only the reply markup of messages.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat.
    :param int message_id: Required if inline_message_id is not specified. Identifier of the message to edit.
    :param str inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
    :param any reply_markup: A JSON-serialized object for an InlineKeyboardMarkup.
    :return: a Message object On success, otherwise True.
    """
    method = r'post'
    api_method = r'editMessageReplyMarkup'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {}
    if chat_id:
        params['chat_id'] = chat_id
    if message_id:
        params['message_id'] = message_id
    if inline_message_id:
        params['inline_message_id'] = inline_message_id
    if reply_markup:
        params['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(method, api_url, api_method, files, params, proxies)


def stop_poll(token, proxies, chat_id, message_id, reply_markup=None):
    """
    Use this method to stop a poll which was sent by the bot.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param int message_id: Identifier of the original message with the poll.
    :param any reply_markup: A JSON-serialized object for an InlineKeyboardMarkup.
    :return: a Poll object On success.
    """
    method = r'post'
    api_method = r'stopPoll'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'message_id': message_id}
    if reply_markup:
        params['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(method, api_url, api_method, files, params, proxies)


def delete_message(token, proxies, chat_id, message_id):
    """
    Use this method to delete a message, including service messages, with the following limitations:
        - A message can only be deleted if it was sent less than 48 hours ago.
        - A dice message in a private chat can only be deleted if it was sent more than 24 hours ago.
        - Bots can delete outgoing messages in private chats, groups, and supergroups.
        - Bots can delete incoming messages in private chats.
        - Bots granted can_post_messages permissions can delete outgoing messages in channels.
        - If the bot is an administrator of a group, it can delete any message there.
        - If the bot has can_delete_messages permission in a supergroup or a channel, it can delete any message there.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param int message_id: Identifier of the message to delete
    :return: True On success.
    """
    method = r'post'
    api_method = r'deleteMessage'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'message_id': message_id}
    return _make_request(method, api_url, api_method, files, params, proxies)


def send_sticker(token, proxies, chat_id, sticker, disable_notification=False, reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send static .WEBP or animated .TGS stickers.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param any sticker: Sticker [file_id or InputFile] to send.
    :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
    :param int reply_to_message_id: If the message is a reply, ID of the original message.
    :param dict reply_markup: InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
    :return: a Message object On success.
    """
    method = r'post'
    api_method = r'sendSticker'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id}
    if not is_string(sticker):
        files = {'sticker': sticker}
    else:
        params['sticker'] = sticker
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        params['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(method, api_url, api_method, files, params, proxies)


def get_sticker_set(token, proxies, name):
    """
    Use this method to get a sticker set.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param str name:  Name of the sticker set.
    :return: a StickerSet object On success.
    """
    method = r'post'
    api_method = r'getStickerSet'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'name': name}
    return _make_request(method, api_url, api_method, files, params, proxies)


def upload_sticker_file(token, proxies, user_id, png_sticker):
    """
    Use this method to upload a .PNG file with a sticker.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int user_id: Unique identifier of the target user.
    :param any png_sticker: Png image with the sticker,
    :return: a File object On success.
    """
    method = r'post'
    api_method = r'uploadStickerFile'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = {'png_sticker': png_sticker}
    params = {'user_id': user_id}
    return _make_request(method, api_url, api_method, files, params, proxies)


def create_new_sticker_set(token, proxies, user_id, name, title, png_sticker, tgs_sticker, emojis, contains_masks=None,
                           mask_position=False):
    """
    Use this method to create a new sticker set owned by a user. 
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int user_id: Unique identifier of the target user.
    :param str name: Short name of sticker set.
    :param str title: New chat title, 1-255 characters.
    :param any png_sticker: PNG image [file_id or InputFile] with the sticker.
    :param any tgs_sticker: TGS animation [InputFile] with the sticker.
    :param str emojis: One or more emoji corresponding to the sticker.
    :param bool contains_masks: Pass True, if a set of mask stickers should be created.
    :param any mask_position: A JSON-serialized object for position where the mask should be placed on faces.
    :return: True On success.
    """
    method = r'post'
    api_method = r'createNewStickerSet'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'user_id': user_id, 'name': name, 'title': title, 'emojis': emojis}
    if not is_string(png_sticker):
        files = {'png_sticker': png_sticker}
    else:
        params['png_sticker'] = png_sticker
    if not is_string(tgs_sticker):
        files = {'tgs_sticker', tgs_sticker}
    if contains_masks:
        params['contains_masks'] = contains_masks
    if mask_position:
        params['mask_position'] = mask_position.to_json()
    return _make_request(method, api_url, api_method, files, params, proxies)


def add_sticker_to_set(token, proxies, user_id, name, png_sticker, emojis, tgs_sticker=None, mask_position=False):
    """
    Use this method to add a new sticker to a set created by the bot.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int user_id: Unique identifier of the target user.
    :param str name: Short name of sticker set.
    :param any png_sticker: PNG image [file_id or InputFile] with the sticker.
    :param any tgs_sticker: TGS animation [InputFile] with the sticker.
    :param str emojis: One or more emoji corresponding to the sticker.
    :param any mask_position: A JSON-serialized object for position where the mask should be placed on faces.
    :return: True on success.
    """
    method = r'post'
    api_method = r'addStickerToSet'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'user_id': user_id, 'name': name, 'emojis': emojis}
    if not is_string(png_sticker):
        files = {'png_sticker': png_sticker}
    else:
        params['png_sticker'] = png_sticker
    if not is_string(tgs_sticker):
        files = {'tgs_sticker': tgs_sticker}
    if mask_position:
        params['mask_position'] = mask_position.to_json()
    return _make_request(method, api_url, api_method, files, params, proxies)


def set_sticker_position_in_set(token, proxies, sticker, position):
    """
    Use this method to move a sticker in a set created by the bot to a specific position. 
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param str sticker: File identifier of the sticker.
    :param int position: New sticker position in the set, zero-based.
    :return: True on success.
    """
    method = r'post'
    api_method = r'setStickerPositionInSet'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'sticker': sticker, 'position': position}
    return _make_request(method, api_url, api_method, files, params, proxies)


def delete_sticker_from_set(token, proxies, sticker):
    """
    Use this method to delete a sticker from a set created by the bot.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param str sticker: File identifier of the sticker.
    :return: True on success.
    """
    method = r'post'
    api_method = r'deleteStickerFromSet'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'sticker': sticker}
    return _make_request(method, api_url, api_method, files, params, proxies)


def set_sticker_set_thumb(token, proxies, name, user_id, thumb=None):
    """
    Use this method to set the thumbnail of a sticker set.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param str name: Short name of sticker set.
    :param int user_id: Unique identifier of the target user.
    :param any thumb: Thumbnail [file_id or InputFile] of the file sent.
    :return: True on success
    """
    method = r'post'
    api_method = r'setStickerSetThumb'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'name': name, 'user_id': user_id}
    if thumb:
        params['thumb'] = thumb
    return _make_request(method, api_url, api_method, files, params, proxies)


def answer_inline_query(token, proxies, inline_query_id, results, cache_time=300, is_personal=False, next_offset=None,
                        switch_pm_text=None, switch_pm_parameter=None):
    """
    Use this method to send answers to an inline query.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param str inline_query_id: Unique identifier for the answered query.
    :param any results: A JSON-serialized array of [InlineQueryResult] results for the inline query.
    :param int cache_time: The maximum amount of time in seconds that the result of the inline query may be cached on the server. Defaults to 300.
    :param bool is_personal: Pass True, if results may be cached on the server side only for the user that sent the query.
    :param str next_offset: Pass the offset that a client should send in the next query with the same text to receive more results.
    :param str switch_pm_text: If passed, clients will display a button with specified text that switches the user to a private chat with the bot and sends the bot a start message with the parameter switch_pm_parameter.
    :param str switch_pm_parameter: 	Deep-linking parameter for the /start message sent to the bot when user presses the switch button. 1-64 characters, only A-Z, a-z, 0-9, _ and - are allowed.
    :return: True on success
    """
    method = r'post'
    api_method = r'answerInlineQuery'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'inline_query_id': inline_query_id, 'results': _convert_list_json_serializable(results)}
    if cache_time is not None:
        params['cache_time'] = cache_time
    if is_personal:
        params['is_personal'] = is_personal
    if next_offset is not None:
        params['next_offset'] = next_offset
    if switch_pm_text:
        params['switch_pm_text'] = switch_pm_text
    if switch_pm_parameter:
        params['switch_pm_parameter'] = switch_pm_parameter
    return _make_request(method, api_url, api_method, files, params, proxies)


# Payments (https://core.telegram.org/bots/api#payments)
def send_invoice(token, proxies, chat_id, title, description, payload, provider_token, start_parameter, currency, prices,
                 provider_data=None, photo_url=None, photo_size=None, photo_width=None, photo_height=None,
                 need_name=False, need_phone_number=False, need_email=False, need_shipping_address=False,
                 send_phone_number_to_provider=False, send_email_to_provider=False, is_flexible=False,
                 disable_notification=False, reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send invoices. On success, the sent Message is returned.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param str title: New chat title, 1-255 characters.
    :param str description: Product description, 1-255 characters
    :param str payload: Bot-defined invoice payload, 1-128 bytes.
    :param str provider_token: Payments provider token, obtained via Botfather.
    :param str start_parameter: Unique deep-linking parameter that can be used to generate this invoice when used as a start parameter.
    :param str currency: Three-letter ISO 4217 currency code.
    :param list prices: Price breakdown, a JSON-serialized list of components.
    :param str provider_data: JSON-encoded data about the invoice, which will be shared with the payment provider.
    :param str photo_url: URL of the product photo for the invoice.
    :param photo_size: Photo Size.
    :param photo_width: Photo Width.
    :param photo_height: Photo Height.
    :param need_name: Pass True, if you require the user's full name to complete the order
    :param need_phone_number: Pass True, if you require the user's phone number to complete the order.
    :param need_email: Pass True, if you require the user's email address to complete the order
    :param need_shipping_address: Pass True, if you require the user's shipping address to complete the order.
    :param send_phone_number_to_provider: Pass True, if user's phone number should be sent to provider.
    :param send_email_to_provider: Pass True, if user's email address should be sent to provider.
    :param is_flexible: Pass True, if the final price depends on the shipping method.
    :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
    :param int reply_to_message_id: If the message is a reply, ID of the original message.
    :param any reply_markup: A JSON-serialized object for an InlineKeyboardMarkup.
    :return: a Message object.
    """
    method = r'post'
    api_method = r'sendInvoice'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'title': title, 'description': description, 'payload': payload,
              'provider_token': provider_token, 'start_parameter': start_parameter, 'currency': currency,
              'prices': _convert_list_json_serializable(prices)}
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
    return _make_request(method, api_url, api_method, files, params, proxies)


def answer_shipping_query(token, proxies, shipping_query_id, ok, shipping_options=None, error_message=None):
    """
    Use this method to reply to shipping queries,
    If you sent an invoice requesting a shipping address and the parameter is_flexible was specified,
    the Bot API will send an Update with a shipping_query field to the bot.
    :param str token: Bot's token (you don't need to fill this)
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param str shipping_query_id: Unique identifier for the query to be answered
    :param bool ok: Specify True if delivery to the specified address is possible and False if there are any problems.
    :param list shipping_options: Required if ok is True. A JSON-serialized array of available shipping options.
    :param str error_message: Required if ok is False. Error message in human readable form that explains why it is impossible to complete the order.
    :return: True, On success.
    """
    method = r'post'
    api_method = 'answerShippingQuery'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'shipping_query_id': shipping_query_id, 'ok': ok}
    if shipping_options:
        params['shipping_options'] = _convert_list_json_serializable(
            shipping_options)
    if error_message:
        params['error_message'] = error_message
    return _make_request(method, api_url, api_method, files, params, proxies)


def answer_pre_checkout_query(token, proxies, pre_checkout_query_id, ok, error_message=None):
    """
    Use this method to respond to such pre-checkout queries. 
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param str pre_checkout_query_id: Unique identifier for the query to be answered.
    :param bool ok: Specify True if delivery to the specified address is possible and False if there are any problems.
    :param str error_message: Required if ok is False. Error message in human readable form that explains why it is impossible to complete the order.
    :return: True On success.
    """
    method = r'post'
    api_method = r'answerPreCheckoutQuery'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'pre_checkout_query_id': pre_checkout_query_id, 'ok': ok}
    if error_message:
        params['error_message'] = error_message
    return _make_request(method, api_url, api_method, files, params, proxies)


def set_passport_data_errors(token, proxies, user_id, errors):
    """
    Use this if the data submitted by the user doesn't satisfy the standards your service requires for any reason.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int user_id: Unique identifier of the target user.
    :param list errors: A JSON-serialized array of [PassportElementError] describing the errors.
    :return: True On success.
    """
    method = r'post'
    api_method = r'setPassportDataErrors'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'user_id': user_id, 'errors': errors}
    return _make_request(method, api_url, api_method, files, params, proxies)


def send_game(token, proxies, chat_id, game_short_name, disable_notification=False, reply_to_message_id=None, reply_markup=None):
    """
    Use this method to send a game.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int or str chat_id: Unique identifier for the target chat or username of the target channel.
    :param str game_short_name: Short name of the game, serves as the unique identifier for the game.
    :param bool disable_notification: Sends the message silently. Users will receive a notification with no sound.
    :param int reply_to_message_id: If the message is a reply, ID of the original message.
    :param any reply_markup: A JSON-serialized object for an InlineKeyboardMarkup.
    :return: a Message object On success.
    """
    method = r'post'
    api_method = r'sendGame'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'game_short_name': game_short_name}
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        params['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(method, api_url, api_method, files, params, proxies)


# https://core.telegram.org/bots/api#setgamescore
def set_game_score(token, proxies, user_id, score, force=False, disable_edit_message=False, chat_id=None, message_id=None,
                   inline_message_id=None):
    """
    Use this method to set the score of the specified user in a game.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int user_id: Unique identifier of the target user.
    :param int score: New score, must be non-negative.
    :param bool force: Pass True, if the high score is allowed to decrease.
    :param bool disable_edit_message: Pass True, if the game message should not be automatically edited to include the current scoreboard.
    :param int or str chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat.
    :param int message_id: Required if inline_message_id is not specified. Identifier of the message to edit.
    :param str inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
    :return: On success a Message object, otherwise returns True.
    """
    method = r'post'
    api_method = r'setGameScore'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'user_id': user_id, 'score': score}
    if force:
        params['force'] = force
    if chat_id:
        params['chat_id'] = chat_id
    if message_id:
        params['message_id'] = message_id
    if inline_message_id:
        params['inline_message_id'] = inline_message_id
    if disable_edit_message:
        params['disable_edit_message'] = disable_edit_message
    return _make_request(method, api_url, api_method, files, params, proxies)


# https://core.telegram.org/bots/api#getgamehighscores
def get_game_high_scores(token, proxies, user_id, chat_id=None, message_id=None, inline_message_id=None):
    """
    Use this method to get data for high score tables.
    :param str token: The bot's API token. (Created with @BotFather).
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :param int user_id: Unique identifier of the target user.
    :param int or str chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat.
    :param int message_id: Required if inline_message_id is not specified. Identifier of the message to edit.
    :param str inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
    :return: an Array of GameHighScore objects.
    """
    method = r'get'
    api_method = r'getGameHighScores'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'user_id': user_id}
    if chat_id:
        params['chat_id'] = chat_id
    if message_id:
        params['message_id'] = message_id
    if inline_message_id:
        params['inline_message_id'] = inline_message_id
    return _make_request(method, api_url, api_method, files, params, proxies)


def _convert_list_json_serializable(results):
    ret = ''
    for r in results:
        if isinstance(r, JsonSerializable):
            ret = ret + r.to_json() + ','
    if len(ret) > 0:
        ret = ret[:-1]
    return '[' + ret + ']'


def _convert_markup(markup):
    if isinstance(markup, JsonSerializable):
        return markup.to_json()
    return markup


def _convert_input_media(media):
    if isinstance(media, InputMedia):
        return media.convert_input_media()
    return None, None


def _convert_input_media_array(array):
    media = []
    files = {}
    for input_media in array:
        if isinstance(input_media, InputMedia):
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
