# -*- coding:utf-8 -*-

"""
Class: 定义词对象。
"""

class Word(object):
    """
    定义词。
    """
    def __init__(self):
        self.word = ""
        self.type = ""
        # 第一基本义原
        self.firstPrimitive = ""
        # 其他基本义原
        self.otherPrimitive = []
        # 结构义原，如果本list非空，说明此词为一个虚词，列表中存放此虚词的一个义原，部分虚词没有中文解释
        self.structuralWords = []
        # 关系义原。key:关系义原，value：基本义原|(具体词)的一个列表
        self.relationalPrimitives = {}
        # 关系符号义原。key:关系符号，value：属于该关系符号的一组基本义原|(具体词)
        self.relationSymbolPrimitives = {}

    # 如果非空，则返回真
    def isStructuralWord(self):
        return self.structuralWords

    def getWord(self):
        return self.word

    def setWord(self, para_word):
        self.word = para_word

    def getType(self):
        return self.type

    def setType(self, para_type):
        self.type = para_type

    def getFirstPrimitive(self):
        return self.firstPrimitive

    def setFirstPrimitive(self, para_firstPrimitive):
        self.firstPrimitive = para_firstPrimitive

    def getOtherPrimitives(self):
        return self.otherPrimitive

    def setOtherPrimitives(self, para_otherPrimitive):
        self.otherPrimitive = para_otherPrimitive

    def addOtherPrimitives(self, para_otherPrimitive):
        self.otherPrimitive.append(para_otherPrimitive)

    def getStructuralWords(self):
        return self.structuralWords

    def setStructuralWords(self, para_structuralWords):
        self.structuralWords = para_structuralWords

    def addStructuralWords(self, para_structuralWords):
        self.structuralWords.append(para_structuralWords)

    def getRelationalPrimitives(self):
        return self.relationalPrimitives

    def addRelationalPrimitives(self, key, value):
        self.relationalPrimitives[key] = value

    def getRelationSymbolPrimitives(self):
        return self.relationSymbolPrimitives

    def addRelationSymbolPrimitives(self, key, value):
        self.relationSymbolPrimitives[key] = value
