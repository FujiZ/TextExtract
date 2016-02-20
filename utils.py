# coding=utf-8
class Dispatcher(object):
    def dispatch(self, prefix, name, **attrs):
        mname = prefix + name.capitalize()
        dname = 'default' + prefix.capitalize()
        method = getattr(self, mname, None)
        if not callable(method):
            method = getattr(self, dname, None)
        if callable(method):
            method(**attrs)


class Selector(Dispatcher):
    """
    根据selector的标签内容构造选择器，并使用select来对内容进行选择
    """

    def __init__(self, selectorNode):
        self.__selectList = []
        for select in selectorNode.find('select'):
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
            resultList += self.__selectNode(node=node, **selector)
        return resultList

    def __selectNode(self, node, identificationType, identificationValue):
        self.dispatch('parse', identificationType, node=node, value=identificationValue)

    def parseQuery(self, node, value):
        """
        使用css解析
        :param node:
        :param value:
        :return:
        """
        return self.parseCss(node, value)

    def parseCss(self, node, value):
        return node.cssselect(value)

    def parseXpath(self, node, value):
        return node.xpath(value)
