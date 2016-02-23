# coding=utf-8
from bs4 import UnicodeDammit


def mapList(func, sequence):
    resultList = []
    for item in sequence:
        result = func(item)
        if result: resultList += result
    return resultList


class NodeNullError(Exception):
    pass


class Dispatcher(object):
    def dispatch(self, prefix, name, **attrs):
        mname = prefix + name.capitalize()
        dname = 'default' + prefix.capitalize()
        method = getattr(self, mname, None)
        if not callable(method):
            method = getattr(self, dname, None)
        if callable(method):
            return method(**attrs)


class Data(object):
    def __init__(self):
        self.__name = None
        self.__id = None
        self.__data = {}

    def setName(self, name):
        self.__name = name

    def setId(self, id):
        self.__id = id

    def setData(self, key, value):
        self.__data[key] = value


def decode_html(html_string):
    converted = UnicodeDammit(html_string)
    if not converted.unicode_markup:
        raise UnicodeDecodeError(
            "Failed to detect encoding, tried [%s]",
            ', '.join(converted.tried_encodings))
    # print converted.original_encoding
    return converted.unicode_markup
