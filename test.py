# coding=utf-8

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import lxml.etree
import utils


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


class Extractor(utils.Dispatcher):
    def __init__(self, template):
        self.__template = ET.ElementTree(file=template)
        self.__html = None
        self.__data = Data()

    def extract(self, filename):
        self.__html = lxml.etree.parse(filename)
        root = self.__template.getroot()
        for child in root:
            self.dispatch('parse', child.tag, node=child)

    def parseName(self, node):
        self.__data.setName(node.text)

    def parseSourceid(self, node):
        self.__data.setId(node.text)

    def parseStorelist(self, node):
        """对storeList中的每个section进行迭代,获得抽取信息
        :param node:
        """
        for storeSection in node.findall('storeSection'):
            # 获取selector
            selector = utils.Selector(node.find('selector'))
            # 根据selector得到满足条件的元素集合
            elementList = selector.selectNode(self.__html)
            for storeNode in storeSection.findall('storeNode'):
                # 获取selector
                selector = utils.Selector(storeNode.find('selector'))
                # 根据selector，从上面的elementList中找到满足条件的元素集合
                targetList = [selector.selectNode(element) for element in elementList]
                # 从targetList中抽取内容，存入resultList
                pass

            pass

    def defaultParse(self, node):
        print node.tag + ': pass'


extractor = Extractor('temp.xml')
extractor.extract('test')
