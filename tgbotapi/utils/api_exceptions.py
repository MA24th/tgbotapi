import re
import random
import string

from six import string_types
from .json_handler import JsonSerializable


class ApiException(Exception):
    """
    This class represents an Exception thrown when a call to the Telegram API fails.
    In addition to an informative message, it has a `function_name` and a `result` attribute, which respectively
    contain the name of the failed function and the returned result that made the function to be considered  as
    failed.
    """

    def __init__(self, msg, function_name, result):
        super(ApiException, self).__init__(f"A request to the Telegram API was unsuccessful. {msg}")
        self.function_name = function_name
        self.result = result


def convert_markup(markup):
    if isinstance(markup, JsonSerializable):
        return markup.to_json()
    return markup


def extract_command(text):
    """
    Extracts the command from `text` (minus the '/') if `text` is a command (see is_command).
    If `text` is not a command, this function returns None.

    Examples:
    extract_command('/help'): 'help'
    extract_command('/help@BotName'): 'help'
    extract_command('/search black eyed peas'): 'search'
    extract_command('Good day to you'): None
    """
    """
    :param text: String to extract the command from
    :return: the command if `text` is a command (according to is_command), else None.
    """
    return text.split()[0].split('@')[0][1:] if is_command(text) else None


def extract_arguments(text):
    """
    Returns the argument after the command.

    Examples:
    extract_arguments("/get name"): 'name'
    extract_arguments("/get"): ''
    extract_arguments("/get@botName name"): 'name'
    """
    """
    :param text: String to extract the arguments from a command
    :return: the arguments if `text` is a command (according to is_command), else None.
    """
    regexp = re.compile(r"/\w*(@\w*)*\s*([\s\S]*)", re.IGNORECASE)
    result = regexp.match(text)
    return result.group(2) if is_command(text) else None


def generate_random_token():
    return ''.join(random.sample(string.ascii_letters, 16))


def is_command(text):
    """
    Checks if `text` is a command. Telegram chat commands start with the '/' character.
    """
    """
    :param text: Text to check.
    :return: True if `text` is a command, else False.
    """
    return text.startswith('/')


def is_string(var):
    return isinstance(var, string_types)


def split_string(text, chars_per_string):
    """
    Splits one string into multiple strings, with a maximum amount of `chars_per_string` characters per string.
    This is very useful for splitting one giant message into multiples.
    """
    """
    :param text: The text to split
    :param chars_per_string: The number of characters per line the text is split into.
    :return: The splitted text as a list of strings.
    """
    return [text[i:i + chars_per_string] for i in range(0, len(text), chars_per_string)]


def convert_list_json_serializable(results):
    ret = ''
    for r in results:
        if isinstance(r, JsonSerializable):
            ret = ret + r.to_json() + ','
    if len(ret) > 0:
        ret = ret[:-1]
    return '[' + ret + ']'


# def convert_input_media(media):
#     if isinstance(media, InputMedia):
#         return media.convert_input_media()
#     return None, None


# def convert_input_media_array(array):
#     media = []
#     files = {}
#     for input_media in array:
#         if isinstance(input_media, InputMedia):
#             media_dict = input_media.to_dict()
#             if media_dict['media'].startswith('attach://'):
#                 key = media_dict['media'].replace('attach://', '')
#                 files[key] = input_media.media
#             media.append(media_dict)
#     return json.dumps(media), files


def no_encode(func):
    def wrapper(key, val):
        if key == 'filename':
            return f'{key}={val}'
        else:
            return func(key, val)

    return wrapper
