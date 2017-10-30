#!/usr/bin/env python
from count import WordCounter
from seg_word import WordSeg
from huffman import HuffmanTreeNode,HuffmanTree
from trainCBOW import trainHuffman

#1. seg
#para1 资讯，每行一条 para2 分词后的文件
WS = WordSeg("../data/test/test","../data/testout")

#2. word2vec
train_op = trainHuffman(segWordPath="../data/testout",
                window=5,
                vecLen=5,
                minValue=0,
                learnRate=0.01)
train_op.train() 
#vec
print(train_op.wordVec)


###########for test###################
## count
## 统计词频
#WD = WordCounter("../data/testout")
#wordDict = WD.wordDict
#
##Huffman
## 构建huffman树
#Tree = HuffmanTree(wordDict,400)
#huffCode = Tree.HuffmanDict

