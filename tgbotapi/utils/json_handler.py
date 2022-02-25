import json
import six


class Dictionaryable(object):
    """
    Subclasses of this class are guaranteed to be able to be converted to dictionary,
    All subclasses of this class must override to_dict.
    """

    def to_dict(self):
        """
        Returns a JSON string representation of this class.

        This function must be overridden by subclasses.
        :return: a Dict formatted string.
        """
        raise NotImplementedError


class JsonDeserializable(object):
    """
    Subclasses of this class are guaranteed to be able to be created from a json-style dict or json formatted string,
    All subclasses of this class must override de_json.
    """

    @classmethod
    def de_json(cls, obj_type):
        """
        Returns an instance of this class from the given json dict or string.

        This function must be overridden by subclasses.
        :return: an instance of this class created from the given json dict or string.
        """
        raise NotImplementedError

    @staticmethod
    def check_type(obj_type):
        """
        Checks whether obj_type is a dict or a string. If it is already a dict, it is returned as-is,
        If it is not, it is converted to a dict by means of json.loads(obj_type),
        :param str or dict obj_type:
        :return: dict
        """

        if type(obj_type) == dict:
            return obj_type
        elif type(obj_type) == str:
            return json.loads(obj_type)
        else:
            raise ValueError("obj_type should be a dict or string.")

    def __str__(self):
        d = {}
        for x, y in six.iteritems(self.__dict__):
            if hasattr(y, '__dict__'):
                d[x] = y.__dict__
            else:
                d[x] = y

        return six.text_type(d)


class JsonSerializable(object):
    """
    Subclasses of this class are guaranteed to be able to be converted to JSON format,
    All subclasses of this class must override to_json.
    """

    def to_json(self):
        """
        Returns a JSON string representation of this class.

        This function must be overridden by subclasses.
        :return: a JSON formatted string.
        """
        raise NotImplementedError
