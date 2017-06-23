# -*- coding:utf-8 -*-

from word import Word
import primitiveFunc as primFunc
import re
import sys
reload(sys)

sys.setdefaultencoding("utf-8")

"""
计算词语相似度。
具体的算法实现参考论文：《基于＜知网＞的词汇语义相似度计算》论文.pdf

用法：
>>>from wordsimilarity import sim4words
>>>word1 = u"足球"
>>>word2 = u"体育"
>>>sim = sim4words(word1, word2)

"""

# 词库（来自文件glossary.dat）中的具体词，或者是义原词。
ALLWORDS = {}

# sim(p1,p2) = alpha / (d + alpha) alpha表示义原相似度为0.5时的距离
alpha = 1.6

# 计算实词的相似度，参数，基本义原的权重
beta1 = 0.5

# 计算实词的相似度，参数，其他义原的权重
beta2 = 0.2

# 计算实词的相似度，参数，关系义原的权重
beta3 = 0.17

# 计算实词的相似度，参数，关系符号义原的权重
beta4 = 0.13

# 具体词与义原的相似度一律处理为比较小的常数gamma。具体词与具体词相似度，如果两个词相等，则为1，否则为0
gamma = 0.2

# 任一非空值和空值之间的相似度定义为一个较小的常数delta
delta = 0.2

# 两个无关义原之间的默认距离定义为20
DEFAULT_PRIMITIVE_DIS = 20

# 知网的逻辑符号
LOGICAL_SYMBOL = ",~^"

# 知网的关系符号
RELATION_SYMBOL = "#%$*+&@?!"

# 知网的特殊符号，虚词或者具体词
SPECIAL_SYMBOL = "{"


def add_word(word):
    """往词库中添加一个词语"""
    global ALLWORDS
    list = ALLWORDS.get(word.getWord())
    if not list:
        list = []
        list.append(word)
        ALLWORDS[word.getWord()] = list
    else:
        list.append(word)


def get_primitive_type(str):
    global RELATION_SYMBOL
    global SPECIAL_SYMBOL
    first = str[0]
    if first in RELATION_SYMBOL:
        return 1
    if first in SPECIAL_SYMBOL:
        return 2
    return 0

def parse_detail(related, w):
    """ 解析具体的概念部分，并将解析结果保存到Word w中。"""
    parts = related.split(",")
    isFirst = True
    isRelational = False
    isSymbol = False
    chinese = ""
    relationalPrimitiveKey = ""
    symbolKey = ""
    for part in parts:
        # 如果是具体词，则会以括号开始和结尾，如 (China|中国)
        if part.startswith("("):
            part = part[:-1]
            part = part[1:]
        # 如果包含等号，则为关系义原，等号后面的全部义原都是关系义原
        if "=" in part:
            isRelational = True
            strs = part.split("=")
            relationalPrimitiveKey = strs[0]
            # 只取关系义原的中文部分
            value = strs[1].split("|")[1]
            w.addRelationalPrimitives(relationalPrimitiveKey, value)
            continue

        # 如果不是具体词或者关系义原
        sts = part.split("|")
        # 根据第一个字符本来判断是否只是义原或者是关系符号
        type = get_primitive_type(sts[0])
        # 部分虚词没有中文部分
        if len(sts) > 1:
            chinese = sts[1]
        if chinese and (chinese.endswith(")") or chinese.endswith("}")):
            # 去掉最后的半边括号
            chinese = chinese[:-1]
        # 基本义原
        if type == 0:
            # 如果前面有关系义原，则本义原也是关系义原
            if isRelational:
                w.addRelationalPrimitives(relationalPrimitiveKey, chinese)
                continue
            # 如果前面是符号义原，则本义原也是符号义原
            if isSymbol:
                w.addRelationSymbolPrimitives(symbolKey, chinese)
                continue
            # 否则是基本义原
            if isFirst:
                w.setFirstPrimitive(chinese)
                isFirst = False
                continue
            else:
                w.addOtherPrimitives(chinese)
                continue
        # 关系符号
        if type == 1:
            isSymbol = True
            isRelational = False
            symbolKey = sts[0][0]
            w.addRelationSymbolPrimitives(symbolKey, chinese)
            continue

        if type == 2:
            # 虚词
            if sts[0].startswith("{"):
                # 去掉第一个字符"{"
                english = sts[0][1:]
                if chinese:
                    w.addStructuralWords(chinese)
                    continue
                # 如果没有中文，则使用英文
                else:
                    w.addStructuralWords(english)
                    continue


"""
加载glossary.dat文件。
在import本模块的时候这段代码会自动执行，创建词语库ALLWORDS.
"""
import os
# _get_module_path = lambda path: os.path.normpath(os.path.join(os.getcwd(),
#                                                               os.path.dirname(__file__), path))
_get_module_path = lambda path: os.path.normpath(os.path.join(os.path.dirname(__file__), path))
path = _get_module_path("../data/glossary.dat")
with open(path) as file:
    line = file.readline()
    while line:
        line = line.strip()
        line = re.sub("\s+", " ", line)
        strs = line.split(" ")
        # print line
        word = strs[0]
        type = strs[1]
        related = strs[2]
        # 因为是按照空格切分的，文件中有些位置可能会出错多出空格，所以要把后面的部分加回来
        for i in range(3, len(strs)):
            related += strs[i]
        w = Word()
        w.setWord(word)
        w.setType(type)
        parse_detail(related, w)
        add_word(w)
        line = file.readline()


def sim4words(word1, word2):
    """计算两个词语(两个String)的相似度。"""
    global ALLWORDS
    word1 = word1.encode("GBK")
    word2 = word2.encode("GBK")
    if word1 in ALLWORDS and word2 in ALLWORDS:
        list1 = ALLWORDS.get(word1)
        list2 = ALLWORDS.get(word2)
        max = 0
        for w1 in list1:
            for w2 in list2:
                sim = get_sim4words(w1, w2)
                if sim > max:
                    max = sim
        return max
    else:
        if word1 in ALLWORDS:
            print word2 + "没有被收录"
        else:
            print u"其中有词没有被收录"
        return 0.0


def get_sim4words(w1, w2):
    """计算两个Word对象的相似度。"""
    # 虚词和实词的相似度为0
    if w1.isStructuralWord() != w2.isStructuralWord():
        return 0
    # 虚词与虚词之间的距离
    if w1.isStructuralWord() and w2.isStructuralWord():
        list1 = w1.getStructuralWords()
        print "struct list1 is "
        print list1
        list2 = w2.getStructuralWords()
        print "struct list2 is "
        print list2
        return sim4lists(list1, list2)
    # 实词之间的距离,分为4部分进行计算
    # 基本义原相似度
    firstPrimitive1 = w1.getFirstPrimitive()
    firstPrimitive2 = w2.getFirstPrimitive()
    sim1 = sim4primitives(firstPrimitive1, firstPrimitive2)
    # 其余基本义原相似度
    list1 = w1.getOtherPrimitives()
    list2 = w2.getOtherPrimitives()
    sim2 = sim4lists(list1, list2)
    # 关系义原相似度
    dict1 = w1.getRelationalPrimitives()
    dict2 = w2.getRelationalPrimitives()
    sim3 = get_sim4dicts(dict1, dict2)
    # 关系符号义原相似度
    dict1 = w1.getRelationSymbolPrimitives()
    dict2 = w2.getRelationSymbolPrimitives()
    sim4 = get_sim4dicts(dict1,dict2)
    # 计算总的相似度
    product = sim1
    sum = beta1 * product
    product *= sim2
    sum += beta2 * product
    product *= sim3
    sum += beta3 * product
    product *= sim4
    sum += beta4 * product
    return sum


def sim4primitives(primitive1, primitive2):
    """计算基本义原之间的距离"""
    dis = get_sim4primitives(primitive1, primitive2)
    return alpha / (dis + alpha)


def get_sim4primitives(primitive1, primitive2):
    """计算两个基本义原在义原树中的距离。如果两个节点不在同一棵树上，设定默认距离为20."""
    list1 = primFunc.getParents(primitive1)
    list2 = primFunc.getParents(primitive2)
    for index in list1:
        if index in list2:
            return list1.index(index) + list2.index(index)
    return DEFAULT_PRIMITIVE_DIS


def get_sim4dicts(dict1, dict2):
    """计算特征结构的相似度"""
    # 如果map都是空的话，则设定相似度为1
    if not dict1 and not dict2:
        return 1
    total = len(dict1) + len(dict2)
    if not dict1 or not dict2:
        return delta
    sim = 0
    count = 0
    for (key, value) in dict1.items():
        # 如果两个结构中具有相同的属性，计算相似度
        if dict2.has_key(key):
            list1 = value
            list2 = dict2.get(key)
            sim += sim4lists(list1, list2)
            count += 1
    # 没有相同属性，即对应的是空值设定相似度位delta.总共有(total - count)对相似度。
    return (sim + delta * (total - 2 * count)) / (total - count)


def sim4lists(list1, list2):
    """计算两个集合的相似度。"""
    if not list1 and not list2:
        return 1
    m = len(list1)
    n = len(list2)
    if m > n:
        big = m
        N = n
    else:
        big = n
        N = m
    count = 0
    index1 = 0
    index2 = 0
    sum = 0
    while count < N:
        max = 0
        for i in range(len(list1)):
            for j in range(len(list2)):
                sim = inner_sim4words(list1[i], list2[j])
                if(sim > max):
                    index1 = i
                    index2 = j
                    max = sim
        sum += max
        list1 = list1[:index1] + list1[index1+1:]
        list2 = list2[:index2] + list2[index2+1:]
        count += 1
    return (sum + delta * (big - N)) / big


def inner_sim4words(word1, word2):
    """比较两个词之间的距离，这两个词可能是义原,也可能是具体词。"""
    isPrimitive1 = primFunc.isPrimitive(word1)
    isPrimitive2 = primFunc.isPrimitive(word2)
    # 两个义原
    if isPrimitive1 and isPrimitive2:
        return sim4primitives(word1, word2)
    # 具体词
    if not isPrimitive1 and not isPrimitive2:
        if word1 == word2:
            return 1
        else:
            return 0
    # 义原和具体词的相似度默认位gamma = 0.2
    return gamma



