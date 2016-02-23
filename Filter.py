# coding=utf-8
import re
import Utils


class Filter(Utils.Dispatcher):
    def __init__(self, filterNode):
        self.__filterList = []
        # 若为空，则生成默认filter
        if not filterNode:
            self.__filterList.append({'filtType': '.'})
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
            if result: resultList += result
        return resultList

    def __filtText(self, text, filtType, filtValue='.+'):
        if filtType == '.':
            return [text]
        else:
            return self.dispatch('filt', filtType, value=filtValue, text=text)

    def filtRegex(self, text, value='.+'):
        return re.findall(value, text)

    def defaultFilt(self, text, value=None):
        return [text]
