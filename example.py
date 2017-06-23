# -*- coding:utf-8 -*-

from src.wordsimilarity import sim4words

"""
基于《知网》的词汇语义相似度计算
示例代码。
"""

if __name__ == "__main__":
    # 计算两个词语的相似度
    word1, word2, word3 = [u"足球", u"运动", u"苹果"]
    sim = sim4words(word1, word2)
    print "similarity(%s, %s)=%g" % (word1, word2, sim)
    sim = sim4words(word1, word3)
    print "similarity(%s, %s)=%g" % (word1, word3, sim)

