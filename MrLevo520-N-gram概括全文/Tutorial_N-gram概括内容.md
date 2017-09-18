**From [利用N-Gram模型概括数据（Python描述)](http://blog.csdn.net/mrlevo520/article/details/52149545)**

Python 2.7
IDE PyCharm 5.0.3

---



讲在开头
----	
	此文需要用到的相关知识包括数据清洗，正则表达式，字典，列表等。不然可能有点费劲。
----------


什么是N-Gram模型？
----------

> 在自然语言里有一个模型叫做n-gram，表示文字或语言中的n个连续的单词组成序列。在进行自然语言分析时，使用n-gram或者寻找常用词组，可以很容易的把一句话分解成若干个文字片段。摘自Python网络数据采集[RyanMitchell著]

简单来说，就是找到核心主题词，那怎么算核心主题词呢，一般而言，重复率也就是提及次数最多的也就是最需要表达的就是核心词。下面的例子也就从这个开始展开

----------

临时补充
----
在栗子中出现，这里拿出来单独先试一下效果

1.string.punctuation获取所有标点符号，和strip搭配使用
```
import string
list = ['a,','b!','cj!/n']
item=[]
for i in list:
    i =i.strip(string.punctuation)
    item.append(i)
print item
```

```
['a', 'b', 'cj!/n']

```

----------

2.operator.itemgetter()
operator模块提供的itemgetter函数用于获取对象的哪些维的数据，参数为一些序号（即需要获取的数据在对象中的序号）

栗子
```
import operator
dict_={'name1':'2',
      'name2':'1'}

print sorted(dict_.items(),key=operator.itemgetter(0),reverse=True)
#dict_.items()，键值对
```

```
[('name2', '1'), ('name1', '2')]
```

当然，你可以直接直接使用这个

```
dict_={'name1':'2',
      'name2':'1'}
print sorted(dict_.iteritems(),key=lambda x:x[1],reverse=True)
```

----------


2-gram
------
就以两个关键词来说吧，上个栗子来进行备注讲解

```
import urllib2
import re
import string
import operator

def cleanText(input):
    input = re.sub('\n+', " ", input).lower() # 匹配换行,用空格替换换行符
    input = re.sub('\[[0-9]*\]', "", input) # 剔除类似[1]这样的引用标记
    input = re.sub(' +', " ", input) #  把连续多个空格替换成一个空格
    input = bytes(input)#.encode('utf-8') # 把内容转换成utf-8格式以消除转义字符
    #input = input.decode("ascii", "ignore")
    return input

def cleanInput(input):
    input = cleanText(input)
    cleanInput = []
    input = input.split(' ') #以空格为分隔符，返回列表


    for item in input:
        item = item.strip(string.punctuation) # string.punctuation获取所有标点符号

        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'): #找出单词，包括i,a等单个单词
            cleanInput.append(item)
    return cleanInput

def getNgrams(input, n):
    input = cleanInput(input)

    output = {} # 构造字典
    for i in range(len(input)-n+1):
        ngramTemp = " ".join(input[i:i+n])#.encode('utf-8')
        if ngramTemp not in output: #词频统计
            output[ngramTemp] = 0 #典型的字典操作
        output[ngramTemp] += 1
    return output

#方法一：对网页直接进行读取
content = urllib2.urlopen(urllib2.Request("http://pythonscraping.com/files/inaugurationSpeech.txt")).read()
#方法二：对本地文件的读取，测试时候用，因为无需联网
#content = open("1.txt").read()
ngrams = getNgrams(content, 2)
sortedNGrams = sorted(ngrams.items(), key = operator.itemgetter(1), reverse=True) #=True 降序排列
print(sortedNGrams)

```

```
[('of the', 213), ('in the', 65), ('to the', 61), ('by the', 41), ('the constitution', 34),,,巴拉巴拉一堆
```
**上述栗子作用在于抓到2连接词的频率大小来排序的，但是这并不是我们想要的，你说这出现两百多次的 of the 有个猫用啊，所以，我们要进行对这些连接词啊介词啊的剔除工作。**

----------

Deeper
------

> 完整代码和测试图都在同级目录下的`2_gram.ipynb`,请用jupyter打开，不知道jupyter？百度啊，自己装

```
# -*- coding: utf-8 -*-
import urllib2

import re
import string
import operator

#剔除常用字函数
def isCommon(ngram):
    commonWords = ["the", "be", "and", "of", "a", "in", "to", "have",
                   "it", "i", "that", "for", "you", "he", "with", "on", "do", "say",
                   "this", "they", "is", "an", "at", "but","we", "his", "from", "that",
                   "not", "by", "she", "or", "as", "what", "go", "their","can", "who",
                   "get", "if", "would", "her", "all", "my", "make", "about", "know",
                   "will","as", "up", "one", "time", "has", "been", "there", "year", "so",
                   "think", "when", "which", "them", "some", "me", "people", "take", "out",
                   "into", "just", "see", "him", "your", "come", "could", "now", "than",
                   "like", "other", "how", "then", "its", "our", "two", "more", "these",
                   "want", "way", "look", "first", "also", "new", "because", "day", "more",
                   "use", "no", "man", "find", "here", "thing", "give", "many", "well"]

    if ngram in commonWords:
        return True
    else:
        return False

def cleanText(input):
    input = re.sub('\n+', " ", input).lower() # 匹配换行用空格替换成空格
    input = re.sub('\[[0-9]*\]', "", input) # 剔除类似[1]这样的引用标记
    input = re.sub(' +', " ", input) #  把连续多个空格替换成一个空格
    input = bytes(input)#.encode('utf-8') # 把内容转换成utf-8格式以消除转义字符
    #input = input.decode("ascii", "ignore")
    return input

def cleanInput(input):
    input = cleanText(input)
    cleanInput = []
    input = input.split(' ') #以空格为分隔符，返回列表


    for item in input:
        item = item.strip(string.punctuation) # string.punctuation获取所有标点符号

        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'): #找出单词，包括i,a等单个单词
            cleanInput.append(item)
    return cleanInput

def getNgrams(input, n):
    input = cleanInput(input)

    output = {} # 构造字典
    for i in range(len(input)-n+1):
        ngramTemp = " ".join(input[i:i+n])#.encode('utf-8')

        if isCommon(ngramTemp.split()[0]) or isCommon(ngramTemp.split()[1]):
            pass
        else:
            if ngramTemp not in output: #词频统计
                output[ngramTemp] = 0 #典型的字典操作
            output[ngramTemp] += 1
    return output

#获取核心词在的句子
def getFirstSentenceContaining(ngram, content):
    #print(ngram)
    sentences = content.split(".")
    for sentence in sentences:
        if ngram in sentence:
            return sentence
    return ""

#方法一：对网页直接进行读取
content = urllib2.urlopen(urllib2.Request("http://pythonscraping.com/files/inaugurationSpeech.txt")).read()
#对本地文件的读取，测试时候用，因为无需联网
#content = open("1.txt").read()
ngrams = getNgrams(content, 2)
sortedNGrams = sorted(ngrams.items(), key = operator.itemgetter(1), reverse=True) # reverse=True 降序排列
print(sortedNGrams)
for top3 in range(3):
    print "###"+getFirstSentenceContaining(sortedNGrams[top3][0],content.lower())+"###"
```

```
[('united states', 10), ('general government', 4), ('executive department', 4), ('legisltive bojefferson', 3), ('same causes', 3), ('called upon', 3), ('chief magistrate', 3), ('whole country', 3), ('government should', 3),,,,巴拉巴拉一堆

### the constitution of the united states is the instrument containing this grant of power to the several departments composing the government###
### the general government has seized upon none of the reserved rights of the states###
### such a one was afforded by the executive department constituted by the constitution###

```
从上述栗子我们可以看出，我们对有用词进行了删选，去掉了连接词，取出核心词排序，然后再把包含核心词的句子抓出来，这里我只是抓了前三句，对于有两三百个句子的文章，用三四句话概括起来，我想还是比较神奇的。



----------

最后
--
> ​	材料来自于Python网络数据采集第八章，但是代码是python3.x的,而且有一些代码案例上跑不出来，所以整理一下，自己修改了一些代码片段，才跑出书上的效果。

​	

----------

致谢
--

- Python网络数据采集[Ryan Mitchell著][人民邮电出版社] 
- [python strip()函数 介绍](http://www.jb51.net/article/37287.htm)
- [Python中的sorted函数以及operator.itemgetter函数](http://www.cnblogs.com/100thMountain/p/4719503.html)