# coding=utf-8
from lxml.cssselect import CSSSelector
import Utils


class Selector(Utils.Dispatcher):
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

    def __call__(self, node):
        resultList = []
        for selector in self.__selectList:
            result = self.__selectNode(node, **selector)
            if result: resultList += result
        return resultList

    def __selectNode(self, node, selectType, selectValue):
        return self.dispatch('parse', selectType, node=node, value=selectValue)

    def parseQuery(self, node, value):
        return self.parseCss(node, value)

    def parseCss(self, node, value):
        sel = CSSSelector(value)
        return sel(node)

    def parseXpath(self, node, value):
        return node.xpath(value)
