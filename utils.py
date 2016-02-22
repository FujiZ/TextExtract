# coding=utf-8
from lxml.cssselect import CSSSelector
import re


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


class Selector(Dispatcher):
    """
    根据selector的标签内容构造选择器，并使用select来对内容进行选择
    """

    def __init__(self, selectorNode):
        self.__selectList = []
        for select in selectorNode.findall('select'):
            # 创建子选择器
            selectNode = {}
            for child in select:
                selectNode[child.tag] = child.text
            self.__selectList.append(selectNode)

    def selectNode(self, node):
        """
        利用beautifulSoup对传入节点进行解析
        :param node:待解析的节点
        :return: 节点列表
        """
        resultList = []
        for selector in self.__selectList:
            result = self.__selectNode(node, **selector)
            if result:
                resultList += result
        return resultList

    def __selectNode(self, node, identificationType, identificationValue):
        return self.dispatch('parse', identificationType, node=node, value=identificationValue)

    def parseQuery(self, node, value):
        return self.parseCss(node, value)

    def parseCss(self, node, value):
        sel = CSSSelector(value)
        return sel(node)

    def parseXpath(self, node, value):
        return node.xpath(value)


class Filter(Dispatcher):
    def __init__(self, filterNode):
        self.__filterList = []
        #若为空，则生成默认filter
        if not filterNode:
            self.__filterList.append({'filtType':'.'})
        else:
            for filt in filterNode.findall('filt'):
                filtNode = {}
                for child in filt:
                    filtNode[child.tag] = child.text
                self.__filterList.append(filtNode)

    def filt(self, text):
        resultList = []
        for filter in self.__filterList:
            result = self.__filtText(text, **filter)
            if result:
                resultList += result
        return resultList

    def __filtText(self, text, filtType, filtValue='.+'):
        if filtType == '.':
            return [text]
        else:
            return self.dispatch('filt', filtType, value=filtValue, text=text)

    def filtRegex(self, text, value='.+'):
        return re.findall(value, text)

    def defaultFilt(self,text,value=None):
        return [text]
