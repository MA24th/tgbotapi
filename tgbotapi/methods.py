import json
import requests
from .types import JsonSerializable
from .utils import *

""" Telegram Available methods
    All methods in the Bot API are case-insensitive. We support GET and POST HTTP methods. 
    Use either URL query string or application/json or application/x-www-form-urlencoded,
    Or multipart/form-data for passing parameters in Bot API requests.
    On successful call, a JSON-object containing the result will be returned.
"""


class ApiException(Exception):
    """
    This class represents an Exception thrown when a call to the Telegram API fails.
    In addition to an informative message, it has a `function_name` and a `result` attribute, which respectively
    contain the name of the failed function and the returned result that made the function to be considered  as
    failed.
    """

    def __init__(self, msg, function_name, result):
        super(ApiException, self).__init__("A request to the Telegram API was unsuccessful. {0}".format(msg))
        self.function_name = function_name
        self.result = result


def _convert_markup(markup):
    if isinstance(markup, JsonSerializable):
        return markup.to_json()
    return markup


def _get_req_session(reset=False):
    return per_thread('req_session', lambda: requests.session(), reset)


def _make_request(method, api_url, api_method, files, params, proxies):
    """
    Makes a request to the Telegram API.
    :param str method: HTTP method ['get', 'post'].
    :param str api_url: telegram api url for api_method.
    :param str api_method: Name of the API method to be called. (E.g. 'getUpdates').
    :param any files: files content's a data.
    :param dict or None params: Should be a dictionary with key-value pairs.
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy.
    :return: JSON DICT FORMAT
    :rtype: dict
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
    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]'.format(result.status_code, result.reason,
                                                                               result.text.encode('utf8'))
        raise ApiException(msg, api_method, result)

    try:

        result_json = result.json()
    except Exception:
        msg = 'The server returned an invalid JSON response. Response body:\n[{0}]'.format(result.text.encode('utf8'))
        raise ApiException(msg, api_method, result)

    if not result_json['ok']:
        msg = 'Error code: {0} Description: {1}'.format(result_json['error_code'], result_json['description'])
        raise ApiException(msg, api_method, result)
    return result_json['result']


def get_updates(token, proxies, offset, limit, timeout, allowed_updates):
    """
    Use this method to receive incoming updates using long polling.
    :type token: str
    :type proxies: dict or None
    :type offset: int or None
    :type limit: int or None
    :type timeout: int or None
    :type allowed_updates: list[str] or None
    :rtype: dict
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


def set_webhook(token, proxies, url, certificate, max_connections, allowed_updates):
    """
    Use this method to specify a url and receive incoming updates via an outgoing webhook.
    :type token: str
    :type proxies: dict or None
    :type url: str
    :type certificate: any
    :type max_connections: int
    :type allowed_updates: list or None
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :rtype: dict
    """
    method = r'get'
    api_method = r'getMe'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = None
    return _make_request(method, api_url, api_method, files, params, proxies)


def send_message(token, proxies, chat_id, text, parse_mode, disable_web_page_preview, disable_notification,
                 reply_to_message_id, reply_markup):
    """
    Use this method to send text messages. On success, the sent Message is returned.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type text: str
    :type parse_mode: str or None
    :type disable_web_page_preview: bool
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type reply_markup: dict or None
    :rtype: dict
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


def forward_message(token, proxies, chat_id, from_chat_id, message_id, disable_notification):
    """
    Use this method to forward messages of any kind.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type from_chat_id: int or str
    :type disable_notification: bool
    :type message_id: int
    :rtype: dict
    """
    method = r'post'
    api_method = r'forwardMessage'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'from_chat_id': from_chat_id, 'message_id': message_id}
    if disable_notification:
        params['disable_notification'] = disable_notification
    return _make_request(method, api_url, api_method, files, params, proxies)


def send_photo(token, proxies, chat_id, photo, caption, parse_mode, disable_notification, reply_to_message_id,
               reply_markup):
    """
    Use this method to send photos.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type photo: any
    :type caption: str or None
    :type parse_mode: str or None
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type reply_markup: dict or None
    :rtype: dict
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


def send_audio(token, proxies, chat_id, audio, caption, parse_mode, duration, performer, title, thumb,
               disable_notification, reply_to_message_id, reply_markup):
    """
    Use this method to send audio files.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type audio: any
    :type caption: str or None
    :type parse_mode: str or None
    :type duration: int or None
    :type performer: str or None
    :type title: str or None
    :type thumb: any
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type reply_markup: dict or None
    :rtype: dict
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


def send_document(token, proxies, chat_id, document, thumb, caption, parse_mode, disable_notification,
                  reply_to_message_id, reply_markup):
    """
    Use this method to send general files.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type document: any
    :type thumb: any or None
    :type caption: str or None
    :type parse_mode: str or None
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type reply_markup: dict or None
    :rtype: dict
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


def send_video(token, proxies, chat_id, video, duration, width, height, thumb, caption, parse_mode, supports_streaming,
               disable_notification, reply_to_message_id, reply_markup):
    """
    Use this method to send video files.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type video: any
    :type duration: int or None
    :type width: int or None
    :type height: int or None
    :type thumb: any
    :type caption: str or None
    :type parse_mode: str or None
    :type supports_streaming: bool
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type reply_markup: dict or None
    :rtype: dict
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


def send_animation(token, proxies, chat_id, animation, duration, width, height, thumb, caption, parse_mode,
                   disable_notification, reply_to_message_id, reply_markup):
    """
    Use this method to send animation files.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type animation: any
    :type duration: int or None
    :type width: int or None
    :type height: int or None
    :type thumb: any or None
    :type caption: str or None
    :type parse_mode: str or None
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type reply_markup: dict or None
    :rtype: dict
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


def send_voice(token, proxies, chat_id, voice, caption, parse_mode, duration, disable_notification, reply_to_message_id,
               reply_markup):
    """
    Use this method to send audio files.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type voice: any or None
    :type caption: str or None
    :type parse_mode: str or None
    :type duration: int or None
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type reply_markup: dict or None
    :rtype: dict
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


def send_video_note(token, proxies, chat_id, video_note, duration, length, thumb, disable_notification,
                    reply_to_message_id, reply_markup):
    """
    Use this method to send video messages.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type video_note: any or None
    :type duration: int or None
    :type length: int or None
    :type thumb: any or None
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type reply_markup: dict or None
    :rtype: dict
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


def send_media_group(token, proxies, chat_id, media, disable_notification, reply_to_message_id):
    """
    Use this method to send a group of photos or videos as an album.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type media: list
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'sendMediaGroup'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id}
    if not is_string(media):
        files = {'media': media}
    else:
        params['media'] = media
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    return _make_request(method, api_url, api_method, files, params, proxies)


def send_location(token, proxies, chat_id, latitude, longitude, live_period, disable_notification, reply_to_message_id,
                  reply_markup):
    """
    Use this method to send point on the map.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type latitude: float
    :type longitude: float
    :type live_period: int or None
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type reply_markup: dict or None
    :rtype: dict
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


def edit_message_live_location(token, proxies, latitude, longitude, chat_id, message_id, inline_message_id,
                               reply_markup):
    """
    Use this method to edit live location messages.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type message_id: int or None
    :type inline_message_id: int or None
    :type latitude: float
    :type longitude: float
    :type reply_markup: dict
    :rtype: dict
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


def stop_message_live_location(token, proxies, chat_id, message_id, inline_message_id, reply_markup):
    """
    Use this method to stop updating a live location message before live_period expires.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type message_id: int or None
    :type inline_message_id: int or None
    :type reply_markup: dict or None
    :rtype: dict
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


def send_venue(token, proxies, chat_id, latitude, longitude, title, address, foursquare_id, foursquare_type,
               disable_notification, reply_to_message_id, reply_markup):
    """
    Use this method to send information about a venue.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type latitude: float
    :type longitude: float
    :type title: str or None
    :type address: str
    :type foursquare_id: str or None
    :type foursquare_type: str or None
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type reply_markup: dict or None
    :rtype: dict
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


def send_contact(token, proxies, chat_id, phone_number, first_name, last_name, vcard, disable_notification,
                 reply_to_message_id, reply_markup):
    """
    Use this method to send phone contacts.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or
    :type phone_number: str
    :type first_name: str
    :type last_name: str or None
    :type vcard: str or None
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type reply_markup: dict or None
    :rtype: dict
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


def send_poll(token, proxies, chat_id, question, options, is_anonymous, type, allows_multiple_answers,
              correct_option_id,
              explanation, explanation_parse_mode, open_period, close_date, is_closed, disable_notifications,
              reply_to_message_id, reply_markup):
    """
    Use this method to send a native poll.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type question: str
    :type options: list
    :type is_anonymous: bool
    :type type: str or None
    :type allows_multiple_answers: bool
    :type correct_option_id: int or None
    :type explanation: str or None
    :type explanation_parse_mode: str or None
    :type open_period: int or None
    :type close_date: int or None
    :type is_closed: bool
    :type disable_notifications: bool
    :type reply_to_message_id: int or None
    :type reply_markup: dict or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'sendPoll'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'question': question, 'options': options}
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


def send_dice(token, proxies, chat_id, emoji, disable_notification, reply_to_message_id, reply_markup):
    """
    Use this method to send a dice.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type emoji: str or None
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type reply_markup: dict or None
    :rtype: dict
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
        params['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(method, api_url, api_method, files, params, proxies)


def send_chat_action(token, proxies, chat_id, action):
    """
    Use this method when you need to tell the user that something is happening on the bot's side.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type action: str
    :rtype: dict
    """
    method = r'post'
    api_method = r'sendChatAction'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'action': action}
    return _make_request(method, api_url, api_method, files, params, proxies)


def get_user_profile_photos(token, proxies, user_id, offset, limit):
    """
    Use this method to get a list of profile pictures for a user.
    :type token: str
    :type proxies: dict or None
    :type user_id: int or str
    :type offset: int or None
    :type limit: int or None
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :type file_id: str
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :type file_path: str
    :rtype: any
    """
    api_url = "https://api.telegram.org/file/bot{0}/{1}".format(token, file_path)
    result = _get_req_session().get(api_url, proxies)
    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text)
        raise ApiException(msg, 'Download file', result)
    return result.content


def kick_chat_member(token, proxies, chat_id, user_id, until_date):
    """
    Use this method to kick a user from a group, a supergroup or a channel.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type user_id: int
    :type user_id: int
    :type until_date: int or None
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type user_id: int
    :rtype: dict
    """
    method = r'post'
    api_method = 'unbanChatMember'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'user_id': user_id}
    return _make_request(method, api_url, api_method, files, params, proxies)


def restrict_chat_member(token, proxies, chat_id, user_id, permissions, until_date):
    """
    Use this method to restrict a user in a supergroup.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type user_id: int
    :type permissions: dict
    :type until_date: int or None
    :rtype: dict
    """
    method = r'post'
    api_method = 'restrictChatMember'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'user_id': user_id, 'permissions': permissions}
    if until_date:
        params['until_date'] = until_date
    return _make_request(method, api_url, api_method, files, params, proxies)


def promote_chat_member(token, proxies, chat_id, user_id, can_change_info, can_post_messages, can_edit_messages,
                        can_delete_messages, can_invite_users, can_restrict_members, can_pin_messages,
                        can_promote_members):
    """
    Use this method to promote or demote a user in a supergroup or a channel.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type user_id: int
    :type can_change_info: bool
    :type can_post_messages: bool
    :type can_edit_messages: bool
    :type can_delete_messages: bool
    :type can_invite_users: bool
    :type can_restrict_members: bool
    :type can_pin_messages: bool
    :type can_promote_members: bool
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type user_id: int
    :type custom_title: str\
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type permissions: dict
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type photo: any
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type title: str
    :rtype: dict
    """
    method = r'post'
    api_method = r'setChatTitle'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'title': title}
    return _make_request(method, api_url, api_method, files, params, proxies)


def set_chat_description(token, proxies, chat_id, description):
    """
    Use this method to change the description of a group, a supergroup or a channel.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type description: str or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'setChatDescription'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id}
    if description:
        params['description'] = description
    return _make_request(method, api_url, api_method, files, params, proxies)


def pin_chat_message(token, proxies, chat_id, message_id, disable_notification):
    """
    Use this method to pin a message in a group, a supergroup, or a channel.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type message_id: int
    :type disable_notification: bool
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :return: an Array of ChatMember object.
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type user_id: int
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type sticker_set_name: str
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :rtype: dict
    """
    method = r'post'
    api_method = r'deleteChatStickerSet'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id}
    return _make_request(method, api_url, api_method, files, params, proxies)


def answer_callback_query(token, proxies, callback_query_id, text, show_alert, url, cache_time):
    """
    Use this method to send answers to callback queries sent from inline keyboards.
    :type token: str
    :type proxies: dict or None
    :type callback_query_id: str
    :type text: str or None
    :type show_alert: bool
    :type url: str or None
    :type cache_time: int or None
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :type commands: list[dict]
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :rtype: dict
    """
    method = r'get'
    api_method = r'getMyCommands'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = None
    return _make_request(method, api_url, api_method, files, params, proxies)


def edit_message_text(token, proxies, text, chat_id, message_id, inline_message_id, parse_mode,
                      disable_web_page_preview,
                      reply_markup):
    """
    Use this method to edit text and game messages.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type message_id: int or None
    :type inline_message_id: str or None
    :type text: str
    :type parse_mode: str or None
    :type disable_web_page_preview: bool
    :type reply_markup: dict or None
    :rtype: dict
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


def edit_message_caption(token, proxies, caption, chat_id, message_id, inline_message_id, parse_mode, reply_markup):
    """
    Use this method to edit captions of messages.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type message_id: int or None
    :type inline_message_id: str or None
    :type caption: str or None
    :type parse_mode: str or None
    :type reply_markup: dict or None
    :rtype: dict
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


def edit_message_media(token, proxies, media, chat_id, message_id, inline_message_id, reply_markup):
    """
    Use this method to edit animation, audio, document, photo, or video messages.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type message_id: int or None
    :type inline_message_id: str or None
    :type media: dict
    :type reply_markup: dict or None:
    :rtype: dict
    """
    method = r'post'
    api_method = r'editMessageMedia'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {}
    if not is_string(media):
        files = {'media': media}
    else:
        params = {'media': media}
    if chat_id:
        params['chat_id'] = chat_id
    if message_id:
        params['message_id'] = message_id
    if inline_message_id:
        params['inline_message_id'] = inline_message_id
    if reply_markup:
        params['reply_markup'] = _convert_markup(reply_markup)
    return _make_request(method, api_url, api_method, files, params, proxies)


def edit_message_reply_markup(token, proxies, chat_id, message_id, inline_message_id, reply_markup):
    """
    Use this method to edit only the reply markup of messages.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type message_id: int or None
    :type inline_message_id: str or None
    :type reply_markup: dict or None
    :rtype: dict
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


def stop_poll(token, proxies, chat_id, message_id, reply_markup):
    """
    Use this method to stop a poll which was sent by the bot.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type message_id: int or None
    :type reply_markup: dict or None
    :rtype: dict
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
    Use this method to delete a message, including service messages.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type message_id: int or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'deleteMessage'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'message_id': message_id}
    return _make_request(method, api_url, api_method, files, params, proxies)


def send_sticker(token, proxies, chat_id, sticker, disable_notification, reply_to_message_id,
                 reply_markup):
    """
    Use this method to send static .WEBP or animated .TGS stickers.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type sticker: any
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type reply_markup: dict or None
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :type name: str
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :type user_id: int
    :type png_sticker: any
    :rtype: dict
    """
    method = r'post'
    api_method = r'uploadStickerFile'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = {'png_sticker': png_sticker}
    params = {'user_id': user_id}
    return _make_request(method, api_url, api_method, files, params, proxies)


def create_new_sticker_set(token, proxies, user_id, name, title, png_sticker, tgs_sticker, emojis, contains_masks,
                           mask_position):
    """
    Use this method to create a new sticker set owned by a user.
    :type token: str
    :type proxies: dict or None
    :type user_id: int
    :type name: str
    :type title: str
    :type png_sticker: any or None
    :type tgs_sticker: any or None
    :type emojis: str
    :type contains_masks: bool
    :type mask_position: dict
    :rtype: dict
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
        params['mask_position'] = mask_position
    return _make_request(method, api_url, api_method, files, params, proxies)


def add_sticker_to_set(token, proxies, user_id, name, png_sticker, emojis, tgs_sticker, mask_position):
    """
    Use this method to add a new sticker to a set created by the bot.
    :type token: str
    :type proxies: dict or None
    :type user_id: int
    :type name: str
    :type png_sticker: any or None
    :type tgs_sticker: any or None
    :type emojis: str
    :type mask_position: dict
    :rtype: dict
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
        params['mask_position'] = mask_position
    return _make_request(method, api_url, api_method, files, params, proxies)


def set_sticker_position_in_set(token, proxies, sticker, position):
    """
    Use this method to move a sticker in a set created by the bot to a specific position.
    :type token: str
    :type proxies: dict or None
    :type sticker: str
    :type position: int
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :type sticker: str
    :rtype: dict
    """
    method = r'post'
    api_method = r'deleteStickerFromSet'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'sticker': sticker}
    return _make_request(method, api_url, api_method, files, params, proxies)


def set_sticker_set_thumb(token, proxies, name, user_id, thumb):
    """
    Use this method to set the thumbnail of a sticker set.
    :type token: str
    :type proxies: dict or None
    :type name: str
    :type user_id: int
    :type thumb: any or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'setStickerSetThumb'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'name': name, 'user_id': user_id}
    if thumb:
        params['thumb'] = thumb
    return _make_request(method, api_url, api_method, files, params, proxies)


def answer_inline_query(token, proxies, inline_query_id, results, cache_time, is_personal, next_offset, switch_pm_text,
                        switch_pm_parameter):
    """
    Use this method to send answers to an inline query.
    :type token: str
    :type proxies: dict or None
    :type inline_query_id: str
    :type results: list[dict]
    :type cache_time: int or None
    :type is_personal: bool
    :type next_offset: str or None
    :type switch_pm_text: str or None
    :type switch_pm_parameter: str or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'answerInlineQuery'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'inline_query_id': inline_query_id, 'results': results}
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


def send_invoice(token, proxies, chat_id, title, description, payload, provider_token, start_parameter, currency,
                 prices,
                 provider_data, photo_url, photo_size, photo_width, photo_height, need_name, need_phone_number,
                 need_email, need_shipping_address, send_phone_number_to_provider, send_email_to_provider, is_flexible,
                 disable_notification, reply_to_message_id, reply_markup):
    """
    Use this method to send invoices. On success, the sent Message is returned.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int
    :type title: str
    :type description: str
    :type payload: str
    :type provider_token: str
    :type start_parameter: str
    :type currency: str
    :type prices: list
    :type provider_data: dict
    :type photo_url: str
    :type photo_size: int
    :type photo_width: int
    :type photo_height: int
    :type need_name: bool
    :type need_phone_number: bool
    :type need_email: bool
    :type need_shipping_address: bool
    :type send_phone_number_to_provider: bool
    :type send_email_to_provider: bool
    :type is_flexible: bool
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type reply_markup: dict or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'sendInvoice'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'chat_id': chat_id, 'title': title, 'description': description, 'payload': payload,
              'provider_token': provider_token, 'start_parameter': start_parameter, 'currency': currency,
              'prices': prices}
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


def answer_shipping_query(token, proxies, shipping_query_id, ok, shipping_options, error_message):
    """
    Use this method to reply to shipping queries.
    :type token: str
    :type proxies: dict or None
    :type shipping_query_id: str
    :type ok: bool
    :type shipping_options: list or None
    :type error_message: str or None
    :rtype: dict
    """
    method = r'post'
    api_method = 'answerShippingQuery'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'shipping_query_id': shipping_query_id, 'ok': ok}
    if shipping_options:
        params['shipping_options'] = shipping_options
    if error_message:
        params['error_message'] = error_message
    return _make_request(method, api_url, api_method, files, params, proxies)


def answer_pre_checkout_query(token, proxies, pre_checkout_query_id, ok, error_message):
    """
    Use this method to respond to such pre-checkout queries.
    :type token: str
    :type proxies: dict or None
    :type pre_checkout_query_id: str
    :type ok: bool
    :type error_message: str or None
    :rtype: dict
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
    :type token: str
    :type proxies: dict or None
    :type user_id: int
    :type errors: list[dict]
    :rtype: dict
    """
    method = r'post'
    api_method = r'setPassportDataErrors'
    api_url = 'https://api.telegram.org/bot{0}/{1}'.format(token, api_method)
    files = None
    params = {'user_id': user_id, 'errors': errors}
    return _make_request(method, api_url, api_method, files, params, proxies)


def send_game(token, proxies, chat_id, game_short_name, disable_notification, reply_to_message_id,
              reply_markup):
    """
    Use this method to send a game.
    :type token: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type game_short_name: str
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type reply_markup: dict or None
    :rtype: dict
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
def set_game_score(token, proxies, user_id, score, force, disable_edit_message, chat_id,
                   message_id,
                   inline_message_id):
    """
    Use this method to set the score of the specified user in a game.
    :type token: str
    :type proxies: dict or None
    :type user_id: int
    :type score: int
    :type force: bool
    :type disable_edit_message: bool
    :type chat_id: int
    :type message_id: int or None
    :type inline_message_id: str or None
    :rtype: dict
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
def get_game_high_scores(token, proxies, user_id, chat_id, message_id, inline_message_id):
    """
    Use this method to get data for high score tables.
    :type token: str
    :type proxies: dict or None
    :type user_id: int
    :type chat_id: int or None
    :type message_id: int or None
    :type inline_message_id: str or None
    :rtype: dict
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
