#!/usr/bin/env python

from collections import defaultdict
import operator
import time

class WordCounter():

    def __init__(self, segPath):
        self.segPath = segPath
        self.wordDict = defaultdict(int)
        self.wordCount()

    def getSeg(self):
        with open(self.segPath,'r') as infile:
            for line in infile:
                yield line.strip().split(' ')

    def wordCount(self):
        for lis in self.getSeg():
            for word in lis:
                self.wordDict[word] += 1

    def larger_than(self,minvalue,ret='dict'):
        '''
            bug! 缺词。 
        '''
        if ret=='list':
            input = self.wordDict
            temp = sorted(input)
        else:
            input = self.wordDict.items()
            temp = sorted(input,key=operator.itemgetter(1))
    
        low = 0
        high = temp.__len__()
        while(high - low > 1):
            mid = (high + low) >> 1 
            if temp[mid][1] <= minvalue:
                low = mid
            else:
                high = mid
            time.sleep(0.5)
    
        if minvalue > temp[mid][1]:
            if ret == 'list':
                return []
            else:
                return {}
    
        if ret == 'dict':
            ret_data={}
            for ele,count in temp[low+1:]:
                ret_data[ele] = count
            return ret_data
        else:
            return temp[low+1:]
if __name__ == "__main__":
    aa = WordCounter("../data/testout")
    aa.wordCount()
    bb = aa.larger_than(2)
    print(bb)
