import quopri
import re
from abc import ABC, abstractmethod


class RequestBase(ABC):
    """Generic request class"""

    @staticmethod
    def _parse_input(data: str) -> dict:
        """
        Parses parameters from URL string to dict
        :param data: URL string
        :return: parameters as dictionary
        """
        result = {}
        data = data.split('?')[-1]
        for key, value in re.findall(r'\&?([^=]+)\=([^&]+)', data):
            result.update({key: value})
        return result

    @staticmethod
    def get_params(environ) -> dict:
        """
        Gets request parameters from environment
        :param environ: environ dict
        :return: parameters as dictionary
        """
        query_str = environ['QUERY_STRING']
        return RequestBase._parse_input(query_str)

    @staticmethod
    @abstractmethod
    def get_request(environ) -> dict:
        """
        Parses request from environ and returns it as dict
        Must be implemented in all child classes
        :param environ: environ dict
        :return: request as dict
        """
        pass


class GetRequest(RequestBase):
    """Get request class"""

    @staticmethod
    def get_request(environ) -> dict:
        """
        Parses request from environ and returns it as dict
        :param environ: environ dict
        :return: request as dict
        """
        return {'method': 'GET', 'request_params': GetRequest.get_params(environ)}


class PostRequest(RequestBase):
    """Post request class"""

    @staticmethod
    def _get_input_bytes(environ) -> bytes:
        """
        Gets input bytes from environ dict
        :param environ: environ dict
        :return: data as bytes
        """
        content_length = environ.get('CONTENT_LENGTH')
        content_length = int(content_length) if content_length else 0
        data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    @staticmethod
    def _parse_input(data: str) -> dict:
        """
        Parses parameters from URL string to dict
        :param data: URL string
        :return: parameters as dictionary
        """
        data = super(PostRequest, PostRequest)._parse_input(data)
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace('+', ' '), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data

    @staticmethod
    def _parse_bytes(data: bytes) -> dict:
        """
        Parses bytes to dictionary
        :param data: data in bytes
        :return: data as dictionary
        """
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = PostRequest._parse_input(data_str)
        return result

    @staticmethod
    def get_params(environ) -> dict:
        """
        Gets request parameters from environment
        :param environ: environ dict
        :return: parameters as dictionary
        """
        data_bytes = PostRequest._get_input_bytes(environ)
        return PostRequest._parse_bytes(data_bytes)

    @staticmethod
    def get_request(environ) -> dict:
        """
        Parses request from environ and returns it as dict
        :param environ: environ dict
        :return: request as dict
        """
        return {'method': 'POST', 'data': PostRequest.get_params(environ)}


class Request:
    """Generic request class"""

    def __new__(cls, method: str):
        """
        Request creation function
        :param method: method type string
        """
        if method == 'POST':
            inst = PostRequest.__new__(PostRequest)
        elif method == 'GET':
            inst = GetRequest.__new__(GetRequest)
        else:
            raise ValueError('Unknown request method')
        return inst
