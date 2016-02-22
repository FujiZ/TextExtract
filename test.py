# coding=utf-8

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import lxml.etree
import lxml.html.soupparser
import utils
import exceptions


class StoreNode(object):
    def __init__(self, node):
        # 获取selector
        self.__selector = utils.Selector(node.find('selector'))
        self.__filter = utils.Filter(node.find('filter'))

        extractType = node.find('extractType')
        if extractType:
            self.__extractType = node.find('extractType').text
        else:
            self.__extractType = '.'

        self.__title = node.find('saveTitle').text
        self.__allowNull = node.find('allowNull').text

    def extract(self, docNode):
        elementList = self.__selector.selectNode(docNode)
        # 如果为.抽取文本，否则抽取对应的属性内容
        textList = []
        if self.__extractType == '.':
            textList = [element.text for element in elementList if element.text]
        else:
            for element in elementList:
                result = element.attrib[self.__extractType]
                if result: textList.append(textList)
        resultList = []
        for text in textList:
            result = self.__filter.filt(text)
            if result: resultList += result

        # 判断是否允许为空，若不允许则引发一个异常，由section捕捉
        if not resultList and self.__allowNull == 'no':
            raise exceptions.NodeNullError
        return self.__title, resultList


class StoreSection(object):
    def __init__(self, node):
        # 获取selector
        self.__selector = utils.Selector(node.find('selector'))
        self.__storeNodeList = [StoreNode(storeNode) for storeNode in node.findall('storeNode')]

    def extract(self, docNode):
        elementList = self.__selector.selectNode(docNode)
        # 通过resultMap存储结果
        resultMap = {}
        try:
            for storeNode in self.__storeNodeList:
                for element in elementList:
                    title, resultList = storeNode.extract(element)
                    if title in resultMap:
                        resultMap[title] += resultList
                    else:
                        resultMap[title] = resultList
        except exceptions.NodeNullError:
            print 'Extract failed'
            return False
        return resultMap


class Extractor(utils.Dispatcher):
    def __init__(self, template):
        self.__template = ET.ElementTree(file=template).getroot()
        self.__storeSectionList = None
        self.__data = utils.Data()
        for child in self.__template:
            self.dispatch('parse', child.tag, node=child)

    def extract(self, filename):
        docNode = lxml.html.soupparser.parse(filename).getroot()
        for storeSection in self.__storeSectionList:
            result = storeSection.extract(docNode)
            if result:  # 表示抽取成功
                # 写入data中
                return result
        else:
            print 'Extract failed: ', filename

    def parseName(self, node):
        self.__data.setName(node.text)

    def parseSourceid(self, node):
        self.__data.setId(node.text)

    def parseStorelist(self, node):
        """对storeList中的每个section进行迭代,获得抽取信息
        :param node:
        """
        self.__storeSectionList = [StoreSection(storeSection) for storeSection in node.findall('storeSection')]

    def defaultParse(self, node):
        print node.tag + ': pass'


extractor = Extractor('163.xml')
for key, value in extractor.extract('163utf8.html').items():
    print key + ": "
    for node in value:
        print node
    print
