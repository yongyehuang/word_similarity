# -*- coding:utf-8 -*-

"""
Class, 定义义原对象。
"""

class Primitive(object):
    """
    义原类：创建义原对象。
    """
    def __init__(self, id, primitive, parentId):
        self.id = id
        self.primitive = primitive
        self.parentId = parentId

    def getPrimitive(self):
        return self.primitive

    def getId(self):
        return self.id

    def getParentId(self):
        return self.parentId

    def isTop(self):
        return self.id == self.parentId

    @staticmethod
    def test():
        print "hahaha"

