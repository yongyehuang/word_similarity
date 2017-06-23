# -*- coding:utf-8 -*-

import re
from primitive import Primitive
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

"""
对义原对象进行操作。
Example：

>>>import primitiveFunc as primFunc
# 判断一个词是否为 义原词
>>>boolean isP = primFunc.isPrimitive("义原词".encode("GBK"))
# 获得一个义原的从本节点到根节点的路径。
>>>list path = primFunc.getParents("义原词".encode("GBK"))
     ...
"""

# 保存所有的义原对象 key:Integer(编号),value:Primitive对象
ALLPRIMITIVES = {}

# 保存所有的义原词语的节点，用于路径查找 key:String(义原词语),value:Integer(结点编号)
PRIMITIVESID = {}

# 读入文件，创建义原树
import os
# path = os.path.abspath("..")
_get_module_path = lambda path: os.path.normpath(os.path.join(os.getcwd(),
                                                              os.path.dirname(__file__), path))
path = _get_module_path("../data/WHOLE.DAT")
with open(path) as file:
    line = file.readline()
    while line:
        line = line.strip()
        line = re.sub("\s+", " ", line)
        strs = line.split(" ")
        id = int(strs[0])
        words = strs[1].split("|")
        english = words[0]
        chinese = words[1]
        parentId = int(strs[2])
        ALLPRIMITIVES[id] = Primitive(id, chinese, parentId)
        PRIMITIVESID[chinese] = id
        PRIMITIVESID[english] = id
        line = file.readline()


def getParents(primitive):
    """
    获得一个义原的从本节点到根节点的路径。
    如果没有找到，则返回一个空list

    @:param primitive  String 义原词
    """
    global PRIMITIVESID
    global ALLPRIMITIVES
    list = []
    id = PRIMITIVESID.get(primitive)
    if id:
        parent = ALLPRIMITIVES.get(id)
        list.append(id)
        while(not parent.isTop()):
            parentId = parent.getParentId()
            list.append(parentId)
            parent = ALLPRIMITIVES.get(parentId)
    return list


def isPrimitive(primitive):
    """
    判断一个词语是否为义原词。
    """
    global PRIMITIVESID
    return PRIMITIVESID.has_key(primitive)


if __name__ == "__main__":
    list = getParents(u"军".encode("GBK"))
    print list
    print isPrimitive(u"忠诚".encode("GBK"))