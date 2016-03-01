# coding=utf-8
import lxml.html.soupparser
import re


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


def decodeFile(filename, encoding):
    fileStr = open(filename).read()
    try:
        resultStr = fileStr.decode(encoding)
    except UnicodeDecodeError:
        print 'decode failed. try to read encoding info from file'
        docNode = lxml.html.soupparser.fromstring(fileStr)
        contentList = docNode.xpath("//meta[@http-equiv='Content-Type']")
        if contentList:
            content = contentList[0].attrib['content']
        else:
            raise
        encoding = re.search(r'charset=([^ ]*)', content).group(1)
        resultStr = fileStr.decode(encoding)
    return resultStr
