from time import process_time as time

import jsonpickle

from .creational_patterns import Logger

logger = Logger('main')


def route(routes: dict, url: str):
    """
    Adds view class to routes dictionary
    :param routes: routes dictionary
    :param url: view url
    """

    def wrapper(cls):
        """
        Wrapper that received a class, instantiates
        it and adds it to routes
        :param cls: view class
        """
        routes[url] = cls()

    return wrapper


def method_debug(method):
    """
    Debugs a class method
    :param method: method to debug
    """

    def wrapper(cls, *args, **kwargs):
        """
        Wrapper that receives a method class, args and kwargs
        :param cls: class of a method
        :param args: arguments
        :param kwargs: key-value arguments
        :return: method call result
        """
        t = time()
        result = method(cls, *args, **kwargs)
        delta = time() - t
        logger.debug(f'Call of method "{method.__name__}" of class "{cls.__class__.__name__}" took {delta} s')
        return result

    return wrapper


class BaseSerializer:
    """Base Serializer class"""

    def __init__(self, obj):
        self.obj = obj

    def dump(self):
        """
        Converts obj dict to JSON string
        :return: JSON string
        """
        return jsonpickle.dumps(list(self.obj))

    @staticmethod
    def load(data):
        """
        Converts JSON string to dict
        :param data: JSON string
        :return: JSON dict
        """
        return jsonpickle.loads(data)
