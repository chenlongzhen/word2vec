#!/usr/bin/env python

from huffman import HuffmanTree,HuffmanTreeNode
from count import WordCounter
from collections import defaultdict
from numpy import random
import numpy as np
import math,time
from sklearn import preprocessing

class trainHuffman():
    '''
    train method
    '''
    def __init__(self,segWordPath,window=5,vecLen=400,minValue=0,learnRate=0.001):
        '''
        init 
        segWordPath: 分好词的文件路径
        '''
        #self.wordDict = WordCounter(segWordPath).larger_than(minValue)
        self.wordDict = WordCounter(segWordPath).wordDict
        self.segPath = segWordPath
        tree = HuffmanTree(self.wordDict,vecLen) 
        self.treeRoot = tree.root
        self.HuffmanDict = tree.HuffmanDict
        #print(self.wordDict)
        #print(tree.HuffmanDict)
        self.wordVec = defaultdict()
        self.window = window
        self.vecLen = vecLen
        self.learnRate = learnRate

    def _getSeg(self):
        '''
        获取每行的词list
        '''
        with open(self.segPath, 'r') as infile:
            for line in infile:
                #print("_getSeg：{}".format(line))
                yield line.strip().split(' ')

    def _getVec(self,word):
        '''
        获取每个词的vec
        '''
        if word in self.wordVec:
            return self.wordVec[word]
        else:
            randomVec =  random.random(size=[self.vecLen,1])
            self.wordVec[word] = randomVec
            return randomVec

    def _getWindow(self):
        '''
        projection layer
        '''
        window = self.window
        simulation = np.zeros([self.vecLen,1])
        for line in self._getSeg():
            sumulation = np.zeros(self.vecLen)
            length = line.__len__()

            if length <= window: # 小于窗口直接加
                mid = length >> 1
                for i in range(length):
                    if i != mid:    
                        simulation += self._getVec(line[i])
                        input_word.append(line[i])
                yield simulation,line[mid] #返回vec 和中间的预测词

            else: # 大于窗口
                for i in range((length)-(window-1)):
                    input_word=[]
                    #print(line[i:(i+window)])
                    for j in range(i,i+window):    
                        if j != i+int((window/2)):
                            simulation += self._getVec(line[j])
                            #print(self._getVec(line[j]))
                            input_word.append(line[j])
                        else:
                            #print("skip {}".format(line[j]))
                            pass
                    yield input_word,simulation,line[i+int(window/2)]

    def _oneIter(self,huffmancode,simulation):
        '''
        一个window从root到叶子节点的迭代
        '''
        nodeRoot =self.treeRoot

        node = nodeRoot #从根节点开始
        sig = lambda x: 1/(1+math.exp(-x)) #sigmoid
        e = np.zeros([self.vecLen,1]) # 累加误差，更新vec用
        for i in range(huffmancode.__len__()):
            huffmanLable = int(huffmancode[i])
            theta = node.value
            q = simulation.T.dot(theta)
            grad = self.learnRate *(1 - int(huffmanLable) - q) #梯度
            e += grad * theta # 累计梯度
            node.value = node.value +grad * theta #更新树节点的权重向量
            #print("lable:{},theta_before:{},q:{},grad:{},e:{},diff:{},theta_end:{}".format(huffmanLable,theta,q,grad *theta,grad,e,node.value))
            node.value = preprocessing.normalize(node.value,axis=0) #归一化
            #print("theta_end:{}".format(node.value))
            node = node.left if huffmanLable == 1 else node.right #走下一个分支

        self.treeRoot = nodeRoot # 更新树
        return e

    def train(self):
        '''
        训练 CBOW
        '''
        node = self.treeRoot #根节点
        iter_num = 0
        for input_word,simulation,word in self._getWindow(): #对每个window进行训练
            huffmanCode = self.HuffmanDict[word]
            e = self._oneIter(huffmanCode,simulation)
            for word in input_word: #跟新input的词
                if iter_num % 10000 == 0:
                    print("[INFO] processed {} words...".format(iter_num))
                vec = self._getVec(word)
                vec += e
                self.wordVec[word] = preprocessing.normalize(vec,axis=0)
                iter_num+=1

if __name__ == "__main__":
    train_op = trainHuffman(segWordPath="../data/testout",
                window=5,
                vecLen=5,
                minValue=0,
                learnRate=0.01)
    train_op.train() 
    print(train_op.wordVec)
