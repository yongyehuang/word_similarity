# 基于《知网》的语义相似度计算 python2.7 API
[知网](http://www.keenage.com/)

本项目使用python语言实现根据义原树来计算词语之间的语义相似度，并提供对应的 API。

词语距离有两类常见的计算方法，一种是根据某种世界知识（Ontology）或分类体系（Taxonomy）来计算，一种利用大规模的语料库进行统计。

本项目研究基于前者，通过人工处理，将词汇组织在多棵树结构中，树中每个节点表示一个“义原”（概念语义）。在一棵树中，任何两个节点之间有且只有一条路径，这条路径的长度就可以作为两个概念语义之间距离的一种度量。

更多具体的计算原理请参考： /docs/《基于＜知网＞的词汇语义相似度计算》论文.pdf

## 功能介绍

- 计算两个词汇的语义相似度
- 相似度计算中的参数调整


## 使用说明

- 方法一：在word_similarity/ 目录下运行代码。

1.在 word-similarity/ 目录下按照 example.py 实例代码运行。
```python
from src.wordsimilarity import sim4words

word1, word2, word3 = [u"足球", u"运动", u"苹果"]
sim = sim4words(word1, word2)
print "similarity(%s, %s)=%g" % (word1, word2, sim)
sim = sim4words(word1, word3)
print "similarity(%s, %s)=%g" % (word1, word3, sim)
```
> similarity(足球, 运动)=0.8

> similarity(足球, 苹果)=0.186047

- 方法二：在word_similarity/ 路径外运行代码。

1.将 word-similarity/ 目录添加到系统路径下。
cd /usr/local/python/lib/python2.7/site-packages/
vim word_similarity.pth
写入： your-path-of/word_similarity/

2.然后按照下面代码运行
```python
from word_similarity.src.wordsimilarity import sim4words

word1, word2= [u"足球", u"运动"]
sim = sim4words(word1, word2)
print "similarity(%s, %s)=%g" % (word1, word2, sim)
```
> similarity(足球, 运动)=0.8


## 参考文献

- [刘群 2002] 刘群，李素建，基于《知网》的词汇语义相似度计算，第三届汉语词汇语义学研讨会，台北，2002年5月
- [知网] http://www.keenage.com


## 使用体验
### 优点

- 原理简单，不需要使用语料库来进行训练
- 不需要考虑句法，语用等特点，能够比较准确地反映语义方面的相似性和差异性

### 缺点

- 处理比较复杂。需要花费大量的人力来构建义原语料库,每次添加新的内容都需要人工修改义原树库。
- 无法对特定的语料进行训练，这样在针对特定问题，比如一些新的领域问题的处理中效果会很差。
- 效果一般。和 word2vec 相比，个人觉得效果要比后者差很多。即使仅使用少量数据（比如：20W 个句子），word2vec 都能取得比《知网》更好的效果。


## 其他

- 1.在 /software/ 目录下提供了知网的语义相似度计算软件： WordSimilarity.exe
- 2.在 /java/ 目录下提供了 java 版本的实现。该版本为本项目提供了很多参考。
