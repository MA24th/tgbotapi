from .utils import *
import json

""" Telegram Available methods
    All methods in the Bot API are case-insensitive. We support GET and POST HTTP methods. 
    Use either URL query string or application/json or application/x-www-form-urlencoded,
    Or multipart/form-data for passing parameters in Bot API requests.
    On successful call, a JSON-object containing the result will be returned.
"""


def get_updates(based_url, proxies, offset, limit, timeout, allowed_updates):
    """
    Use this method to receive incoming updates using long polling
    :type based_url: str
    :type proxies: dict or None
    :type offset: int or None
    :type limit: int or None
    :type timeout: int or None
    :type allowed_updates: list[str] or None
    :rtype: list
    """
    method = r'get'
    api_method = r'getUpdates'
    api_url = based_url + '/' + api_method
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
    return make_request(method, api_url, api_method, files, params, proxies)


def set_webhook(based_url, proxies, url, certificate, ip_address, max_connections, allowed_updates,
                drop_pending_updates):
    """
    Use this method to specify an url and receive incoming updates via an outgoing webhook
    :type based_url: str
    :type proxies: dict or None
    :type url: str
    :type certificate: any
    :type ip_address: str
    :type max_connections: int
    :type allowed_updates: list or None
    :type drop_pending_updates: bool
    :rtype: dict
    """
    method = r'post'
    api_method = r'setWebhook'
    api_url = based_url + '/' + api_method
    files = None
    params = {'url': url if url else ""}
    if certificate:
        files = {'certificate': certificate}
    if ip_address:
        params['ip_address'] = ip_address
    if max_connections:
        params['max_connections'] = max_connections
    if allowed_updates:
        params['allowed_updates'] = json.dumps(allowed_updates)
    if drop_pending_updates:
        params['drop_pending_updates'] = drop_pending_updates
    return make_request(method, api_url, api_method, files, params, proxies)


def delete_webhook(based_url, proxies, drop_pending_updates):
    """
    Use this method to remove webhook integration if you decide to switch back to getUpdates. 
    :type based_url: str
    :type proxies: dict or None
    :type drop_pending_updates: bool
    :rtype: dict
    """
    method = r'post'
    api_method = r'deleteWebhook'
    api_url = based_url + '/' + api_method
    files = None
    params = {}
    if drop_pending_updates:
        params['drop_pending_updates'] = drop_pending_updates
    return make_request(method, api_url, api_method, files, params, proxies)


def get_webhook_info(based_url, proxies):
    """
    Use this method to get current webhook status. 
    :type based_url: str
    :type proxies: dict or None
    :rtype: dict
    """
    method = r'get'
    api_method = r'getWebhookInfo'
    api_url = based_url + '/' + api_method
    files = None
    params = None
    return make_request(method, api_url, api_method, files, params, proxies)


def get_me(based_url, proxies):
    """
    A simple method for testing your bots auth token
    :type based_url: str
    :type proxies: dict or None
    :rtype: dict
    """
    method = r'get'
    api_method = r'getMe'
    api_url = based_url + '/' + api_method
    files = None
    params = None
    return make_request(method, api_url, api_method, files, params, proxies)


def log_out(based_url, proxies):
    """
    Use this method to log out from the cloud Bot API server before launching the bot locally
    :type based_url: str
    :type proxies: dict or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'logOut'
    api_url = based_url + '/' + api_method
    files = None
    params = None
    return make_request(method, api_url, api_method, files, params, proxies)


def close(based_url, proxies):
    """
    Use this method to close the bot instance before moving it from one local server to another
    :type based_url: str
    :type proxies: dict or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'close'
    api_url = based_url + '/' + api_method
    files = None
    params = None
    return make_request(method, api_url, api_method, files, params, proxies)


def send_message(based_url, proxies, chat_id, text, parse_mode, entities, disable_web_page_preview,
                 disable_notification, reply_to_message_id, allow_sending_without_reply, reply_markup):
    """
    Use this method to send text messages. On success, send Message is returned
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type text: str
    :type parse_mode: str or None
    :type entities: list or None
    :type disable_web_page_preview: bool
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type allow_sending_without_reply: bool
    :type reply_markup: dict or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'sendMessage'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id, 'text': text}
    if parse_mode:
        params['parse_mode'] = parse_mode
    if entities:
        params['entities'] = entities
    if disable_web_page_preview:
        params['disable_web_page_preview'] = disable_web_page_preview
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if allow_sending_without_reply:
        params['allow_sending_without_reply'] = allow_sending_without_reply
    if reply_markup:
        params['reply_markup'] = convert_markup(reply_markup)
    return make_request(method, api_url, api_method, files, params, proxies)


def forward_message(based_url, proxies, chat_id, from_chat_id, message_id, disable_notification):
    """
    Use this method to forward messages of any kind
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type from_chat_id: int or str
    :type disable_notification: bool
    :type message_id: int
    :rtype: dict
    """
    method = r'post'
    api_method = r'forwardMessage'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id, 'from_chat_id': from_chat_id, 'message_id': message_id}
    if disable_notification:
        params['disable_notification'] = disable_notification
    return make_request(method, api_url, api_method, files, params, proxies)


def copy_message(based_url, proxies, chat_id, from_chat_id, message_id, caption, parse_mode, caption_entities,
                 disable_notification, protect_content, reply_to_message_id, allow_sending_without_reply, reply_markup):
    """ 
    Use this method to copy messages of any kind
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type from_chat_id: int or str
    :type message_id: int
    :type caption: str or None
    :type parse_mode: str or None
    :type caption_entities: list or None
    :type disable_notification: bool
    :type protect_content: bool
    :type reply_to_message_id: int or None
    :type allow_sending_without_reply: bool
    :type reply_markup: list or None
    :rtype: dict  
    """
    method = r'post'
    api_method = r'copyMessage'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id, 'from_chat_id': from_chat_id, 'message_id': message_id}
    if caption:
        params['caption'] = caption
    if parse_mode:
        params['parse_mode'] = parse_mode
    if caption_entities:
        params['caption_entities'] = caption_entities
    if disable_notification:
        params['disable_notification'] = disable_notification
    if protect_content:
        params['protect_content'] = protect_content
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if allow_sending_without_reply:
        params['allow_sending_without_reply'] = allow_sending_without_reply
    if reply_markup:
        params['reply_markup'] = reply_markup

    return make_request(method, api_url, api_method, files, params, proxies)


def send_photo(based_url, proxies, chat_id, photo, caption, parse_mode, caption_entities, disable_notification,
               reply_to_message_id, allow_sending_without_reply,
               reply_markup):
    """
    Use this method to send photos
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type photo: bytes or str
    :type caption: str or None
    :type parse_mode: str or None
    :type caption_entities: list or None
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type allow_sending_without_reply: bool
    :type reply_markup: dict or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'sendPhoto'
    api_url = based_url + '/' + api_method
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
    if caption_entities:
        params['caption_entities'] = caption_entities
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if allow_sending_without_reply:
        params['allow_sending_without_reply'] = allow_sending_without_reply
    if reply_markup:
        params['reply_markup'] = convert_markup(reply_markup)
    return make_request(method, api_url, api_method, files, params, proxies)


def send_audio(based_url, proxies, chat_id, audio, caption, parse_mode, caption_entities, duration, performer, title,
               thumb, disable_notification, reply_to_message_id, allow_sending_without_reply, reply_markup):
    """
    Use this method to send audio files
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type audio: bytes or str
    :type caption: str or None
    :type parse_mode: str or None
    :type caption_entities: list or None
    :type duration: int or None
    :type performer: str or None
    :type title: str or None
    :type thumb: any
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type allow_sending_without_reply: bool
    :type reply_markup: dict or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'sendAudio'
    api_url = based_url + '/' + api_method
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
    if caption_entities:
        params['caption_entities'] = caption_entities
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
    if allow_sending_without_reply:
        params['allow_sending_without_reply'] = allow_sending_without_reply
    if reply_markup:
        params['reply_markup'] = convert_markup(reply_markup)
    return make_request(method, api_url, api_method, files, params, proxies)


def send_document(based_url, proxies, chat_id, document, thumb, caption, parse_mode, caption_entities,
                  disable_content_type_detection, disable_notification,
                  reply_to_message_id, allow_sending_without_reply, reply_markup):
    """
    Use this method to send general files
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type document: bytes or str
    :type thumb: any or None
    :type caption: str or None
    :type parse_mode: str or None
    :type caption_entities: list or None
    :type disable_content_type_detection: bool
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type allow_sending_without_reply: bool
    :type reply_markup: dict or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'sendDocument'
    api_url = based_url + '/' + api_method
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
    if caption_entities:
        params['caption_entities'] = caption_entities
    if disable_content_type_detection:
        params['disable_content_type_detection'] = disable_content_type_detection
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if allow_sending_without_reply:
        params['allow_sending_without_reply'] = allow_sending_without_reply
    if reply_markup:
        params['reply_markup'] = convert_markup(reply_markup)
    return make_request(method, api_url, api_method, files, params, proxies)


def send_video(based_url, proxies, chat_id, video, duration, width, height, thumb, caption, parse_mode,
               caption_entities, supports_streaming, disable_notification, reply_to_message_id,
               allow_sending_without_reply, reply_markup):
    """
    Use this method to send video files
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type video: bytes or str
    :type duration: int or None
    :type width: int or None
    :type height: int or None
    :type thumb: any
    :type caption: str or None
    :type parse_mode: str or None
    :type caption_entities: list or None
    :type supports_streaming: bool
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type allow_sending_without_reply: bool
    :type reply_markup: dict or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'sendVideo'
    api_url = based_url + '/' + api_method
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
    if caption_entities:
        params['caption_entities'] = caption_entities
    if supports_streaming:
        params['supports_streaming'] = supports_streaming
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if allow_sending_without_reply:
        params['allow_sending_without_reply'] = allow_sending_without_reply
    if reply_markup:
        params['reply_markup'] = convert_markup(reply_markup)
    return make_request(method, api_url, api_method, files, params, proxies)


def send_animation(based_url, proxies, chat_id, animation, duration, width, height, thumb, caption, parse_mode,
                   caption_entities, disable_notification, reply_to_message_id, allow_sending_without_reply,
                   reply_markup):
    """
    Use this method to send animation files
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type animation: bytes or str
    :type duration: int or None
    :type width: int or None
    :type height: int or None
    :type thumb: any or None
    :type caption: str or None
    :type parse_mode: str or None
    :type caption_entities: list or None
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type allow_sending_without_reply: bool
    :type reply_markup: dict or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'sendAnimation'
    api_url = based_url + '/' + api_method
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
    if caption_entities:
        params['caption_entities'] = caption_entities
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if allow_sending_without_reply:
        params['allow_sending_without_reply'] = allow_sending_without_reply
    if reply_markup:
        params['reply_markup'] = convert_markup(reply_markup)
    return make_request(method, api_url, api_method, files, params, proxies)


def send_voice(based_url, proxies, chat_id, voice, caption, parse_mode, caption_entities, duration,
               disable_notification, reply_to_message_id, allow_sending_without_reply, reply_markup):
    """
    Use this method to send audio files
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type voice: bytes or str
    :type caption: str or None
    :type parse_mode: str or None
    :type caption_entities: list or None
    :type duration: int or None
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type allow_sending_without_reply: bool
    :type reply_markup: dict or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'sendVoice'
    api_url = based_url + '/' + api_method
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
    if caption_entities:
        params['caption_entities'] = caption_entities
    if duration:
        params['duration'] = duration
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if allow_sending_without_reply:
        params['allow_sending_without_reply'] = allow_sending_without_reply
    if reply_markup:
        params['reply_markup'] = convert_markup(reply_markup)
    return make_request(method, api_url, api_method, files, params, proxies)


def send_video_note(based_url, proxies, chat_id, video_note, duration, length, thumb, disable_notification,
                    reply_to_message_id, allow_sending_without_reply, reply_markup):
    """
    Use this method to send video messages
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type video_note: bytes or str
    :type duration: int or None
    :type length: int or None
    :type thumb: bytes or str
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type allow_sending_without_reply: bool
    :type reply_markup: dict or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'sendVideoNote'
    api_url = based_url + '/' + api_method
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
    if allow_sending_without_reply:
        params['allow_sending_without_reply'] = allow_sending_without_reply
    if reply_markup:
        params['reply_markup'] = convert_markup(reply_markup)
    return make_request(method, api_url, api_method, files, params, proxies)


def send_media_group(based_url, proxies, chat_id, media, disable_notification, reply_to_message_id,
                     allow_sending_without_reply):
    """
    Use this method to send a group of photos or videos as an album
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type media: list
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type allow_sending_without_reply: bool
    :rtype: list
    """
    method = r'post'
    api_method = r'sendMediaGroup'
    api_url = based_url + '/' + api_method
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
    if allow_sending_without_reply:
        params['allow_sending_without_reply'] = allow_sending_without_reply
    return make_request(method, api_url, api_method, files, params, proxies)


def send_location(based_url, proxies, chat_id, latitude, longitude, horizontal_accuracy, live_period, heading,
                  proximity_alert_radius, disable_notification, reply_to_message_id,
                  allow_sending_without_reply, reply_markup):
    """
    Use this method to send point on the map
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type latitude: float
    :type longitude: float
    :type horizontal_accuracy: float or None
    :type live_period: int or None:
    :type heading: int or None
    :type proximity_alert_radius: int or None
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type allow_sending_without_reply: bool
    :type reply_markup: dict or None
    :rtype: dict or bool
    """
    method = r'post'
    api_method = r'sendLocation'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id,
              'latitude': latitude, 'longitude': longitude}
    if horizontal_accuracy:
        params['horizontal_accuracy'] = horizontal_accuracy
    if live_period:
        params['live_period'] = live_period
    if heading:
        params['heading'] = heading
    if proximity_alert_radius:
        params['proximity_alert_radius'] = proximity_alert_radius
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if allow_sending_without_reply:
        params['allow_sending_without_reply'] = allow_sending_without_reply
    if reply_markup:
        params['reply_markup'] = convert_markup(reply_markup)
    return make_request(method, api_url, api_method, files, params, proxies)


def edit_message_live_location(based_url, proxies, latitude, longitude, horizontal_accuracy, heading,
                               proximity_alert_radius, chat_id, message_id, inline_message_id,
                               reply_markup):
    """
    Use this method to edit live location messages
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type message_id: int or None
    :type inline_message_id: int or None
    :type latitude: float
    :type longitude: float
    :type horizontal_accuracy: float or None
    :type heading: str or None
    :type proximity_alert_radius: int or None
    :type reply_markup: dict or None
    :rtype: dict or bool
    """
    method = r'post'
    api_method = r'editMessageLiveLocation'
    api_url = based_url + '/' + api_method
    files = None
    params = {'latitude': latitude, 'longitude': longitude}
    if horizontal_accuracy:
        params['horizontal_accuracy'] = horizontal_accuracy
    if heading:
        params['heading'] = heading
    if proximity_alert_radius:
        params['proximity_alert_radius'] = proximity_alert_radius
    if chat_id:
        params['chat_id'] = chat_id
    if message_id:
        params['message_id'] = message_id
    if inline_message_id:
        params['inline_message_id'] = inline_message_id
    if reply_markup:
        params['reply_markup'] = convert_markup(reply_markup)
    return make_request(method, api_url, api_method, files, params, proxies)


def stop_message_live_location(based_url, proxies, chat_id, message_id, inline_message_id, reply_markup):
    """
    Use this method to stop updating a live location message before live_period expires
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type message_id: int or None
    :type inline_message_id: int or None
    :type reply_markup: dict or None
    :rtype: dict or bool
    """
    method = r'post'
    api_method = r'stopMessageLiveLocation'
    api_url = based_url + '/' + api_method
    files = None
    params = {}
    if chat_id:
        params['chat_id'] = chat_id
    if message_id:
        params['message_id'] = message_id
    if inline_message_id:
        params['inline_message_id'] = inline_message_id
    if reply_markup:
        params['reply_markup'] = convert_markup(reply_markup)
    return make_request(method, api_url, api_method, files, params, proxies)


def send_venue(based_url, proxies, chat_id, latitude, longitude, title, address, foursquare_id, foursquare_type,
               google_place_id, google_place_type,
               disable_notification, reply_to_message_id, allow_sending_without_reply, reply_markup):
    """
    Use this method to send information about a venue
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type latitude: float
    :type longitude: float
    :type title: str or None
    :type address: str
    :type foursquare_id: str or None
    :type foursquare_type: str or None
    :type google_place_id: str or None
    :type google_place_type: str or None
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type allow_sending_without_reply: bool
    :type reply_markup: dict or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'sendVenue'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude, 'title': title, 'address': address}
    if foursquare_id:
        params['foursquare_id'] = foursquare_id
    if foursquare_type:
        params['foursquare_type'] = foursquare_type
    if google_place_id:
        params['google_place_id'] = google_place_id
    if google_place_type:
        params['google_place_type'] = google_place_type
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if allow_sending_without_reply:
        params['allow_sending_without_reply'] = allow_sending_without_reply
    if reply_markup:
        params['reply_markup'] = convert_markup(reply_markup)
    return make_request(method, api_url, api_method, files, params, proxies)


def send_contact(based_url, proxies, chat_id, phone_number, first_name, last_name, vcard, disable_notification,
                 reply_to_message_id, allow_sending_without_reply, reply_markup):
    """
    Use this method to send phone contacts
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or
    :type phone_number: str
    :type first_name: str
    :type last_name: str or None
    :type vcard: str or None
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type allow_sending_without_reply: bool
    :type reply_markup: dict or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'sendContact'
    api_url = based_url + '/' + api_method
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
    if allow_sending_without_reply:
        params['allow_sending_without_reply'] = allow_sending_without_reply
    if reply_markup:
        params['reply_markup'] = convert_markup(reply_markup)
    return make_request(method, api_url, api_method, files, params, proxies)


def send_poll(based_url, proxies, chat_id, question, options, is_anonymous, ttype, allows_multiple_answers,
              correct_option_id,
              explanation, explanation_parse_mode, explanation_entities, open_period, close_date, is_closed,
              disable_notifications,
              reply_to_message_id, allow_sending_without_reply, reply_markup):
    """
    Use this method to send a native poll
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type question: str
    :type options: list
    :type is_anonymous: bool
    :type ttype: str or None
    :type allows_multiple_answers: bool
    :type correct_option_id: int or None
    :type explanation: str or None
    :type explanation_parse_mode: str or None
    :type explanation_entities: list or None
    :type open_period: int or None
    :type close_date: int or None
    :type is_closed: bool
    :type disable_notifications: bool
    :type reply_to_message_id: int or None
    :type allow_sending_without_reply: bool
    :type reply_markup: dict or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'sendPoll'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id, 'question': question, 'options': options}
    if is_anonymous:
        params['is_anonymous'] = is_anonymous
    if ttype:
        params['type'] = ttype
    if allows_multiple_answers:
        params['allows_multiple_answers'] = allows_multiple_answers
    if correct_option_id:
        params['correct_option_id'] = correct_option_id
    if explanation:
        params['explanation'] = explanation
    if explanation_parse_mode:
        params['explanation_parse_mode'] = explanation_parse_mode
    if explanation_entities:
        params['explanation_entities'] = explanation_entities
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
    if allow_sending_without_reply:
        params['allow_sending_without_reply'] = allow_sending_without_reply
    if reply_markup:
        params['reply_markup'] = convert_markup(reply_markup)
    return make_request(method, api_url, api_method, files, params, proxies)


def send_dice(based_url, proxies, chat_id, emoji, disable_notification, reply_to_message_id,
              allow_sending_without_reply, reply_markup):
    """
    Use this method to send a dice
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type emoji: str or None
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type allow_sending_without_reply: bool
    :type reply_markup: dict or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'sendDice'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id, 'emoji': emoji}
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if allow_sending_without_reply:
        params['allow_sending_without_reply'] = allow_sending_without_reply
    if reply_markup:
        params['reply_markup'] = convert_markup(reply_markup)
    return make_request(method, api_url, api_method, files, params, proxies)


def send_chat_action(based_url, proxies, chat_id, action):
    """
    Use this method when you need to tell the user that something is happening on the bots side
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type action: str
    :rtype: bool
    """
    method = r'post'
    api_method = r'sendChatAction'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id, 'action': action}
    return make_request(method, api_url, api_method, files, params, proxies)


def get_user_profile_photos(based_url, proxies, user_id, offset, limit):
    """
    Use this method to get a list of profile pictures for a user
    :type based_url: str
    :type proxies: dict or None
    :type user_id: int or str
    :type offset: int or None
    :type limit: int or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'getUserProfilePhotos'
    api_url = based_url + '/' + api_method
    files = None
    params = {'user_id': user_id}
    if offset:
        params['offset'] = offset
    if limit:
        params['limit'] = limit
    return make_request(method, api_url, api_method, files, params, proxies)


def get_file(based_url, proxies, file_id):
    """
    Use this method to get basic info about a file and prepare it for downloading
    :type based_url: str
    :type proxies: dict or None
    :type file_id: str
    :rtype: dict
    """
    method = r'post'
    api_method = r'getFile'
    api_url = based_url + '/' + api_method
    files = None
    params = {'file_id': file_id}
    return make_request(method, api_url, api_method, files, params, proxies)


def kick_chat_member(based_url, proxies, chat_id, user_id, until_date, revoke_messages):
    """
    Use this method to kick a user from a group, a supergroup or a channel
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type user_id: int
    :type until_date: int or None
    :type revoke_messages: bool
    :rtype: bool
    """
    method = r'post'
    api_method = 'kickChatMember'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id, 'user_id': user_id}
    if until_date:
        params['until_date'] = until_date
    if revoke_messages:
        params['revoke_messages'] = revoke_messages
    return make_request(method, api_url, api_method, files, params, proxies)


def unban_chat_member(based_url, proxies, chat_id, user_id, only_if_banned):
    """
    Use this method to unban a previously kicked user in a supergroup or channel
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type user_id: int
    :type only_if_banned: bool
    :rtype: bool
    """
    method = r'post'
    api_method = 'unbanChatMember'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id, 'user_id': user_id}
    if only_if_banned:
        params['only_if_banned'] = only_if_banned
    return make_request(method, api_url, api_method, files, params, proxies)


def restrict_chat_member(based_url, proxies, chat_id, user_id, permissions, until_date):
    """
    Use this method to restrict a user in a supergroup
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type user_id: int
    :type permissions: dict
    :type until_date: int or None
    :rtype: bool
    """
    method = r'post'
    api_method = 'restrictChatMember'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id, 'user_id': user_id, 'permissions': permissions}
    if until_date:
        params['until_date'] = until_date
    return make_request(method, api_url, api_method, files, params, proxies)


def promote_chat_member(based_url, proxies, chat_id, user_id, is_anonymous, can_manage_chat, can_change_info,
                        can_post_messages, can_edit_messages, can_delete_messages, can_manage_voice_chats,
                        can_invite_users, can_restrict_members, can_pin_messages, can_promote_members):
    """
    Use this method to promote or demote a user in a supergroup or a channel
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type user_id: int
    :type is_anonymous: bool
    :type can_manage_chat: bool
    :type can_change_info: bool
    :type can_post_messages: bool
    :type can_edit_messages: bool
    :type can_delete_messages: bool
    :type can_manage_voice_chats: bool
    :type can_invite_users: bool
    :type can_restrict_members: bool
    :type can_pin_messages: bool
    :type can_promote_members: bool
    :rtype: bool
    """
    method = r'post'
    api_method = 'promoteChatMember'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id, 'user_id': user_id}
    if is_anonymous:
        params['is_anonymous'] = is_anonymous
    if can_manage_chat:
        params['can_manage_chat'] = can_manage_chat
    if can_change_info:
        params['can_change_info'] = can_change_info
    if can_post_messages:
        params['can_post_messages'] = can_post_messages
    if can_edit_messages:
        params['can_edit_messages'] = can_edit_messages
    if can_manage_voice_chats:
        params['can_manage_voice_chats'] = can_manage_voice_chats
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
    return make_request(method, api_url, api_method, files, params, proxies)


def set_chat_administrator_custom_title(based_url, proxies, chat_id, user_id, custom_title):
    """
    Use this method to set a custom title for an administrator in a supergroup promoted by the bot
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type user_id: int
    :type custom_title: str\
    :rtype: bool
    """
    method = r'post'
    api_method = r'setChatAdministratorCustomTitle'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id, 'user_id': user_id, 'custom_title': custom_title}
    return make_request(method, api_url, api_method, files, params, proxies)


def set_chat_permissions(based_url, proxies, chat_id, permissions):
    """
    Use this method to set default chat permissions for all members
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type permissions: dict
    :rtype: bool
    """
    method = r'post'
    api_method = r'setChatPermissions'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id, 'permissions': permissions}
    return make_request(method, api_url, api_method, files, params, proxies)


def export_chat_invite_link(based_url, proxies, chat_id):
    """
    Use this method to generate a new invite link for a chat
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :rtype: str
    """
    method = r'get'
    api_method = r'exportChatInviteLink'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id}
    return make_request(method, api_url, api_method, files, params, proxies)


def create_chat_invite_link(based_url, proxies, chat_id, name, expire_date, member_limit, creates_join_request):
    """
    Use this method to create an additional invite link for a chat
    :type based_url: str
    :type proxies: list or None
    :type chat_id: int or str
    :type name: str or None
    :type expire_date: int or None
    :type member_limit: int or None
    :type creates_join_request: bool
    :rtype: dict
    """
    method = r'post'
    api_method = r'createChatInviteLink'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id}
    if name:
        params['name'] = name
    if expire_date:
        params['expire_date'] = expire_date
    if member_limit:
        params['member_limit'] = member_limit
    if creates_join_request:
        params['creates_join_request'] = creates_join_request
    return make_request(method, api_url, api_method, files, params, proxies)


def edit_chat_invite_link(based_url, proxies, chat_id, invite_link, name, expire_date, member_limit,
                          creates_join_request):
    """
    Use this method to edit a non-primary invite link created by the bot
    :type based_url: str
    :type proxies: list or None
    :type chat_id: int or str
    :type invite_link: str
    :type name: str or None
    :type expire_date: int or None
    :type member_limit: int or None
    :type creates_join_request: bool
    :rtype: dict
    """
    method = r'post'
    api_method = r'editChatInviteLink'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id, 'invite_link': invite_link}
    if name:
        params['name'] = name
    if expire_date:
        params['expire_date'] = expire_date
    if member_limit:
        params['member_limit'] = member_limit
    if creates_join_request:
        params['creates_join_request'] = creates_join_request
    return make_request(method, api_url, api_method, files, params, proxies)


def revoke_chat_invite_link(based_url, proxies, chat_id, invite_link, ):
    """
    Use this method to revoke an invitation link created by the bot
    :type based_url: str
    :type proxies: list or None
    :type chat_id: int or str
    :type invite_link: str
    :rtype: dict
    """
    method = r'post'
    api_method = r'revokeChatInviteLink'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id, 'invite_link': invite_link}
    return make_request(method, api_url, api_method, files, params, proxies)


def set_chat_photo(based_url, proxies, chat_id, photo):
    """
    Use this method to set a new profile photo for the chat
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type photo: bytes
    :rtype: bool
    """
    method = r'post'
    api_method = r'setChatPhoto'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id}
    if not is_string(photo):
        files = {'photo': photo}
    else:
        params['photo'] = photo
    return make_request(method, api_url, api_method, files, params, proxies)


def delete_chat_photo(based_url, proxies, chat_id):
    """
    Use this method to delete a chat photo
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :rtype: bool
    """
    method = r'post'
    api_method = r'deleteChatPhoto'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id}
    return make_request(method, api_url, api_method, files, params, proxies)


def set_chat_title(based_url, proxies, chat_id, title):
    """
    Use this method to change the title of a chat
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type title: str
    :rtype: bool
    """
    method = r'post'
    api_method = r'setChatTitle'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id, 'title': title}
    return make_request(method, api_url, api_method, files, params, proxies)


def set_chat_description(based_url, proxies, chat_id, description):
    """
    Use this method to change the description of a group, a supergroup or a channel
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type description: str or None
    :rtype: bool
    """
    method = r'post'
    api_method = r'setChatDescription'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id}
    if description:
        params['description'] = description
    return make_request(method, api_url, api_method, files, params, proxies)


def pin_chat_message(based_url, proxies, chat_id, message_id, disable_notification):
    """
    Use this method to pin a message in a group, a supergroup, or a channel
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type message_id: int
    :type disable_notification: bool
    :rtype: bool
    """
    method = r'post'
    api_method = r'pinChatMessage'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id, 'message_id': message_id}
    if disable_notification:
        params['disable_notification'] = disable_notification
    return make_request(method, api_url, api_method, files, params, proxies)


def unpin_chat_message(based_url, proxies, chat_id, message_id):
    """
    Use this method to unpin a message in a group, a supergroup, or a channel
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type message_id: str or None
    :rtype: bool
    """
    method = r'post'
    api_method = r'unpinChatMessage'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id}
    if message_id:
        params['message_id'] = message_id
    return make_request(method, api_url, api_method, files, params, proxies)


def unpin_all_chat_message(based_url, proxies, chat_id):
    """
    Use this method to clear the list of pinned messages in a chat
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :rtype: bool
    """
    method = r'post'
    api_method = r'unpinAllChatMessage'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id}
    return make_request(method, api_url, api_method, files, params, proxies)


def leave_chat(based_url, proxies, chat_id):
    """
    Use this method for your bot to leave a group, supergroup or channel
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :rtype: dict
    """
    method = r'post'
    api_method = r'leaveChat'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id}
    return make_request(method, api_url, api_method, files, params, proxies)


def get_chat(based_url, proxies, chat_id):
    """
    Use this method to get up-to-date information about the chat
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :rtype: dict
    """
    method = r'get'
    api_method = r'getChat'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id}
    return make_request(method, api_url, api_method, files, params, proxies)


def get_chat_administrators(based_url, proxies, chat_id):
    """
    Use this method to get a list of administrators in a chat
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :rtype: list
    """
    method = r'get'
    api_method = r'getChatAdministrators'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id}
    return make_request(method, api_url, api_method, files, params, proxies)


def get_chat_members_count(based_url, proxies, chat_id):
    """
    Use this method to get the number of members in a chat
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :rtype: int
    """
    method = r'get'
    api_method = r'getChatMembersCount'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id}
    return make_request(method, api_url, api_method, files, params, proxies)


def get_chat_member(based_url, proxies, chat_id, user_id):
    """
    Use this method to get information about a member of a chat
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type user_id: int
    :rtype: dict
    """
    method = r'get'
    api_method = r'getChatMember'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id, 'user_id': user_id}
    return make_request(method, api_url, api_method, files, params, proxies)


def set_chat_sticker_set(based_url, proxies, chat_id, sticker_set_name):
    """
    Use this method to set a new group sticker set for a supergroup
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type sticker_set_name: str
    :rtype: bool
    """
    method = r'post'
    api_method = r'setChatStickerSet'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id, 'sticker_set_name': sticker_set_name}
    return make_request(method, api_url, api_method, files, params, proxies)


def delete_chat_sticker_set(based_url, proxies, chat_id):
    """
    Use this method to delete a group sticker set from a supergroup
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :rtype: bool
    """
    method = r'post'
    api_method = r'deleteChatStickerSet'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id}
    return make_request(method, api_url, api_method, files, params, proxies)


def answer_callback_query(based_url, proxies, callback_query_id, text, show_alert, url, cache_time):
    """
    Use this method to send answers to callback queries sent from inline keyboards
    :type based_url: str
    :type proxies: dict or None
    :type callback_query_id: str
    :type text: str or None
    :type show_alert: bool
    :type url: str or None
    :type cache_time: int or None
    :rtype: bool
    """
    method = r'post'
    api_method = r'answerCallbackQuery'
    api_url = based_url + '/' + api_method
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
    return make_request(method, api_url, api_method, files, params, proxies)


def set_my_commands(based_url, proxies, commands):
    """
    Use this method to change the list of the bots commands
    :type based_url: str
    :type proxies: dict or None
    :type commands: list
    :rtype: bool
    """
    method = r'post'
    api_method = r'setMyCommands'
    api_url = based_url + '/' + api_method
    files = None
    params = {'commands': commands}
    return make_request(method, api_url, api_method, files, params, proxies)


def get_my_commands(based_url, proxies):
    """
    Use this method to get the current list of the bots commands
    :type based_url: str
    :type proxies: dict or None
    :rtype: list
    """
    method = r'get'
    api_method = r'getMyCommands'
    api_url = based_url + '/' + api_method
    files = None
    params = None
    return make_request(method, api_url, api_method, files, params, proxies)


def edit_message_text(based_url, proxies, text, chat_id, message_id, inline_message_id, parse_mode, entities,
                      disable_web_page_preview,
                      reply_markup):
    """
    Use this method to edit text and game messages
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type message_id: int or None
    :type inline_message_id: str or None
    :type text: str
    :type parse_mode: str or None
    :type entities: list or None
    :type disable_web_page_preview: bool
    :type reply_markup: dict or None
    :rtype: dict or bool
    """
    method = r'post'
    api_method = r'editMessageText'
    api_url = based_url + '/' + api_method
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
    if entities:
        params['entities'] = entities
    if disable_web_page_preview:
        params['disable_web_page_preview'] = disable_web_page_preview
    if reply_markup:
        params['reply_markup'] = convert_markup(reply_markup)
    return make_request(method, api_url, api_method, files, params, proxies)


def edit_message_caption(based_url, proxies, caption, chat_id, message_id, inline_message_id, parse_mode,
                         caption_entities, reply_markup):
    """
    Use this method to edit captions of messages
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type message_id: int or None
    :type inline_message_id: str or None
    :type caption: str or None
    :type parse_mode: str or None
    :type caption_entities: list or None
    :type reply_markup: dict or None
    :rtype: dict or bool
    """
    method = r'post'
    api_method = r'editMessageCaption'
    api_url = based_url + '/' + api_method
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
    if caption_entities:
        params['caption_entities'] = caption_entities
    if reply_markup:
        params['reply_markup'] = convert_markup(reply_markup)
    return make_request(method, api_url, api_method, files, params, proxies)


def edit_message_media(based_url, proxies, media, chat_id, message_id, inline_message_id, reply_markup):
    """
    Use this method to edit animation, audio, document, photo, or video messages
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type message_id: int or None
    :type inline_message_id: str or None
    :type media: dict
    :type reply_markup: dict or None:
    :rtype: dict or bool
    """
    method = r'post'
    api_method = r'editMessageMedia'
    api_url = based_url + '/' + api_method
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
        params['reply_markup'] = convert_markup(reply_markup)
    return make_request(method, api_url, api_method, files, params, proxies)


def edit_message_reply_markup(based_url, proxies, chat_id, message_id, inline_message_id, reply_markup):
    """
    Use this method to edit only the reply markup of messages
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type message_id: int or None
    :type inline_message_id: str or None
    :type reply_markup: dict or None
    :rtype: dict or bool
    """
    method = r'post'
    api_method = r'editMessageReplyMarkup'
    api_url = based_url + '/' + api_method
    files = None
    params = {}
    if chat_id:
        params['chat_id'] = chat_id
    if message_id:
        params['message_id'] = message_id
    if inline_message_id:
        params['inline_message_id'] = inline_message_id
    if reply_markup:
        params['reply_markup'] = convert_markup(reply_markup)
    return make_request(method, api_url, api_method, files, params, proxies)


def stop_poll(based_url, proxies, chat_id, message_id, reply_markup):
    """
    Use this method to stop a poll which was sent by the bot
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type message_id: int or None
    :type reply_markup: dict or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'stopPoll'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id, 'message_id': message_id}
    if reply_markup:
        params['reply_markup'] = convert_markup(reply_markup)
    return make_request(method, api_url, api_method, files, params, proxies)


def delete_message(based_url, proxies, chat_id, message_id):
    """
    Use this method to delete a message, including service messages
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type message_id: int or None
    :rtype: bool
    """
    method = r'post'
    api_method = r'deleteMessage'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id, 'message_id': message_id}
    return make_request(method, api_url, api_method, files, params, proxies)


def send_sticker(based_url, proxies, chat_id, sticker, disable_notification, reply_to_message_id,
                 allow_sending_without_reply, reply_markup):
    """
    Use this method to send static .WEBP or animated .TGS stickers
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type sticker: any
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type allow_sending_without_reply: bool
    :type reply_markup: dict or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'sendSticker'
    api_url = based_url + '/' + api_method
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
    if allow_sending_without_reply:
        params['allow_sending_without_reply'] = allow_sending_without_reply
    if reply_markup:
        params['reply_markup'] = convert_markup(reply_markup)
    return make_request(method, api_url, api_method, files, params, proxies)


def get_sticker_set(based_url, proxies, name):
    """
    Use this method to get a sticker set
    :type based_url: str
    :type proxies: dict or None
    :type name: str
    :rtype: dict
    """
    method = r'post'
    api_method = r'getStickerSet'
    api_url = based_url + '/' + api_method
    files = None
    params = {'name': name}
    return make_request(method, api_url, api_method, files, params, proxies)


def upload_sticker_file(based_url, proxies, user_id, png_sticker):
    """
    Use this method to upload a .PNG file with a sticker
    :type based_url: str
    :type proxies: dict or None
    :type user_id: int
    :type png_sticker: bytes or str
    :rtype: dict
    """
    method = r'post'
    api_method = r'uploadStickerFile'
    api_url = based_url + '/' + api_method
    files = {'png_sticker': png_sticker}
    params = {'user_id': user_id}
    return make_request(method, api_url, api_method, files, params, proxies)


def create_new_sticker_set(based_url, proxies, user_id, name, title, png_sticker, tgs_sticker, emojis, contains_masks,
                           mask_position):
    """
    Use this method to create a new sticker set owned by a user
    :type based_url: str
    :type proxies: dict or None
    :type user_id: int
    :type name: str
    :type title: str
    :type png_sticker: any or None
    :type tgs_sticker: any or None
    :type emojis: str
    :type contains_masks: bool
    :type mask_position: dict
    :rtype: bool
    """
    method = r'post'
    api_method = r'createNewStickerSet'
    api_url = based_url + '/' + api_method
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
    return make_request(method, api_url, api_method, files, params, proxies)


def add_sticker_to_set(based_url, proxies, user_id, name, png_sticker, emojis, tgs_sticker, mask_position):
    """
    Use this method to add a new sticker to a set created by the bot
    :type based_url: str
    :type proxies: dict or None
    :type user_id: int
    :type name: str
    :type png_sticker: any or None
    :type tgs_sticker: any or None
    :type emojis: str
    :type mask_position: dict
    :rtype: bool
    """
    method = r'post'
    api_method = r'addStickerToSet'
    api_url = based_url + '/' + api_method
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
    return make_request(method, api_url, api_method, files, params, proxies)


def set_sticker_position_in_set(based_url, proxies, sticker, position):
    """
    Use this method to move a sticker in a set created by the bot to a specific position
    :type based_url: str
    :type proxies: dict or None
    :type sticker: str
    :type position: int
    :rtype: bool
    """
    method = r'post'
    api_method = r'setStickerPositionInSet'
    api_url = based_url + '/' + api_method
    files = None
    params = {'sticker': sticker, 'position': position}
    return make_request(method, api_url, api_method, files, params, proxies)


def delete_sticker_from_set(based_url, proxies, sticker):
    """
    Use this method to delete a sticker from a set created by the bot
    :type based_url: str
    :type proxies: dict or None
    :type sticker: str
    :rtype: bool
    """
    method = r'post'
    api_method = r'deleteStickerFromSet'
    api_url = based_url + '/' + api_method
    files = None
    params = {'sticker': sticker}
    return make_request(method, api_url, api_method, files, params, proxies)


def set_sticker_set_thumb(based_url, proxies, name, user_id, thumb):
    """
    Use this method to set the thumbnail of a sticker set
    :type based_url: str
    :type proxies: dict or None
    :type name: str
    :type user_id: int
    :type thumb: any or None
    :rtype: bool
    """
    method = r'post'
    api_method = r'setStickerSetThumb'
    api_url = based_url + '/' + api_method
    files = None
    params = {'name': name, 'user_id': user_id}
    if thumb:
        params['thumb'] = thumb
    return make_request(method, api_url, api_method, files, params, proxies)


def answer_inline_query(based_url, proxies, inline_query_id, results, cache_time, is_personal, next_offset,
                        switch_pm_text, switch_pm_parameter):
    """
    Use this method to send answers to an inline query
    :type based_url: str
    :type proxies: dict or None
    :type inline_query_id: str
    :type results: list[dict]
    :type cache_time: int or None
    :type is_personal: bool
    :type next_offset: str or None
    :type switch_pm_text: str or None
    :type switch_pm_parameter: str or None
    :rtype: bool
    """
    method = r'post'
    api_method = r'answerInlineQuery'
    api_url = based_url + '/' + api_method
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
    return make_request(method, api_url, api_method, files, params, proxies)


def send_invoice(based_url, proxies, chat_id, title, description, payload, provider_token, currency, prices,
                 max_tip_amount, suggested_tip_amounts,  start_parameter, provider_data, photo_url, photo_size,
                 photo_width, photo_height, need_name, need_phone_number, need_email, need_shipping_address,
                 send_phone_number_to_provider, send_email_to_provider, is_flexible, disable_notification,
                 reply_to_message_id, allow_sending_without_reply, reply_markup):
    """
    Use this method to send invoices. On success, the sent Message is returned
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int
    :type title: str
    :type description: str
    :type payload: str
    :type provider_token: str
    :type currency: str
    :type prices: list
    :type max_tip_amount: int or None
    :type suggested_tip_amounts: list[int] or None
    :type start_parameter: str
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
    :type allow_sending_without_reply: bool
    :type reply_markup: dict or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'sendInvoice'
    api_url = based_url + '/' + api_method
    files = None
    params = {
        'chat_id': chat_id,
        'title': title,
        'description': description,
        'payload': payload,
        'provider_token': provider_token,
        'currency': currency,
        'prices': prices}
    if max_tip_amount:
        params['max_tip_amount'] = max_tip_amount
    if suggested_tip_amounts:
        params['suggested_tip_amounts'] = suggested_tip_amounts
    if start_parameter:
        params['start_parameter'] = start_parameter
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
    # if protect_content:
    #     params['protect_content'] = protect_content
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if allow_sending_without_reply:
        params['allow_sending_without_reply'] = allow_sending_without_reply
    if reply_markup:
        params['reply_markup'] = convert_markup(reply_markup)
    return make_request(method, api_url, api_method, files, params, proxies)


def answer_shipping_query(based_url, proxies, shipping_query_id, ok, shipping_options, error_message):
    """
    Use this method to reply to shipping queries
    :type based_url: str
    :type proxies: dict or None
    :type shipping_query_id: str
    :type ok: bool
    :type shipping_options: list or None
    :type error_message: str or None
    :rtype: bool
    """
    method = r'post'
    api_method = 'answerShippingQuery'
    api_url = based_url + '/' + api_method
    files = None
    params = {'shipping_query_id': shipping_query_id, 'ok': ok}
    if shipping_options:
        params['shipping_options'] = shipping_options
    if error_message:
        params['error_message'] = error_message
    return make_request(method, api_url, api_method, files, params, proxies)


def answer_pre_checkout_query(based_url, proxies, pre_checkout_query_id, ok, error_message):
    """
    Use this method to respond to such pre-checkout queries
    :type based_url: str
    :type proxies: dict or None
    :type pre_checkout_query_id: str
    :type ok: bool
    :type error_message: str or None
    :rtype: bool
    """
    method = r'post'
    api_method = r'answerPreCheckoutQuery'
    api_url = based_url + '/' + api_method
    files = None
    params = {'pre_checkout_query_id': pre_checkout_query_id, 'ok': ok}
    if error_message:
        params['error_message'] = error_message
    return make_request(method, api_url, api_method, files, params, proxies)


def set_passport_data_errors(based_url, proxies, user_id, errors):
    """
    Use this if the data submitted by the user doesn't satisfy the standards your service requires for any reason
    :type based_url: str
    :type proxies: dict or None
    :type user_id: int
    :type errors: list
    :rtype: bool
    """
    method = r'post'
    api_method = r'setPassportDataErrors'
    api_url = based_url + '/' + api_method
    files = None
    params = {'user_id': user_id, 'errors': errors}
    return make_request(method, api_url, api_method, files, params, proxies)


def send_game(based_url, proxies, chat_id, game_short_name, disable_notification, reply_to_message_id,
              allow_sending_without_reply, reply_markup):
    """
    Use this method to send a game
    :type based_url: str
    :type proxies: dict or None
    :type chat_id: int or str
    :type game_short_name: str
    :type disable_notification: bool
    :type reply_to_message_id: int or None
    :type allow_sending_without_reply: bool
    :type reply_markup: dict or None
    :rtype: dict
    """
    method = r'post'
    api_method = r'sendGame'
    api_url = based_url + '/' + api_method
    files = None
    params = {'chat_id': chat_id, 'game_short_name': game_short_name}
    if disable_notification:
        params['disable_notification'] = disable_notification
    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
    if allow_sending_without_reply:
        params['allow_sending_without_reply'] = allow_sending_without_reply
    if reply_markup:
        params['reply_markup'] = convert_markup(reply_markup)
    return make_request(method, api_url, api_method, files, params, proxies)


def set_game_score(based_url, proxies, user_id, score, force, disable_edit_message, chat_id,
                   message_id,
                   inline_message_id):
    """
    Use this method to set the score of the specified user in a game
    :type based_url: str
    :type proxies: dict or None
    :type user_id: int
    :type score: int
    :type force: bool
    :type disable_edit_message: bool
    :type chat_id: int
    :type message_id: int or None
    :type inline_message_id: str or None
    :rtype: dict or bool
    """
    method = r'post'
    api_method = r'setGameScore'
    api_url = based_url + '/' + api_method
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
    return make_request(method, api_url, api_method, files, params, proxies)


def get_game_high_scores(based_url, proxies, user_id, chat_id, message_id, inline_message_id):
    """
    Use this method to get data for high score tables
    :type based_url: str
    :type proxies: dict or None
    :type user_id: int
    :type chat_id: int or None
    :type message_id: int or None
    :type inline_message_id: str or None
    :rtype: list
    """
    method = r'get'
    api_method = r'getGameHighScores'
    api_url = based_url + '/' + api_method
    files = None
    params = {'user_id': user_id}
    if chat_id:
        params['chat_id'] = chat_id
    if message_id:
        params['message_id'] = message_id
    if inline_message_id:
        params['inline_message_id'] = inline_message_id
    return make_request(method, api_url, api_method, files, params, proxies)
