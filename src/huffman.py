#!/usr/bin/env python

from collections import defaultdict
import numpy as np

class HuffmanTreeNode():
    '''
    huffman 节点类。
    value 非叶节点是中间向量，叶节点是单词本身
    possibility 该节点频率
    Huffman 叶节点需要存放huffmancode
    '''
    def __init__(self, value, possibility):
        self.possibility = possibility
        self.left = None
        self.right = None
        self.value = value
        self.Huffman = ""

class HuffmanTree():
    def __init__(self, wordDict,vecLen=400):
        self.vecLen = vecLen
        self.root = None
        self.nodeList = [HuffmanTreeNode(k,v) for k,v in wordDict.items()]
        self.HuffmanDict = defaultdict() 
        self.buildTree()
        self.getHuffmanCode()


    def merge(self,node1,node2):
        '''
        合并最小的两个节点, node1 最小， node2 次小
        '''
        topNodePossibility = node1.possibility + node2.possibility
        value = np.random.random(size=[self.vecLen,1])
        topNode = HuffmanTreeNode(value,topNodePossibility)
        topNode.left = node1
        topNode.right = node2
        return topNode
        
    def buildTree(self):
        '''
        merge tow min node
        '''
        node = self.nodeList
        while node.__len__() > 1:
            min1 = 0 #最小的节点
            min2 = 1 #次小的节点
            if node[min2].possibility < node[min1].possibility:
                [min1,min2]  = [min2,min1]
            for i in range(2,node.__len__()): #遍历找最小节点
                if node[i].possibility < node[min2].possibility:
                    min2 = i
                    if node[min2].possibility < node[min1].possibility:
                        [min1,min2] = [min2,min1]
            top_node = self.merge(node[min1],node[min2])
            if min1 < min2:
                node.pop(min2)
                node.pop(min1)
            elif min1 > min2:
                node.pop(min1)
                node.pop(min2)
            else:
                raise RuntimeError(" min1 should not be equal to min2")
            node.insert(0,top_node)
        self.root = node[0]

    def getHuffmanCode(self):
        '''
        '''
        stack = [self.root]
        while (stack.__len__() > 0):
            node = stack.pop()
            while node.left or node.right:
                node.left.Huffman = node.Huffman + "1"
                node.right.Huffman = node.Huffman + "0"
                stack.append(node.right)
                node = node.left
            word = node.value
            code = node.Huffman
            self.HuffmanDict[word] = code
