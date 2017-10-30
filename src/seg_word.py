import sys 
import time
import jieba

S_PATH= sys.path[0]
D_PATH = S_PATH + "/../data/"

class WordSeg():
    def __init__(self, filePath, outPath):
        self.filePath = filePath
        self.stopWordList = self.getStopWord()
        self.outPath = outPath
                
    def getStopWord(self):
        stop_words=[]
        with open("../data/stopwords",'r') as infile:
            for line in infile:
                stop_words.append(line.strip('\n'))
        return stop_words 

    def seg(self):

        jieba.load_userdict(D_PATH+"seg_dict")
        jieba.enable_parallel(16)
        
        content = open(self.filePath,"rb").read()
        t1 = time.time()
        
        cut_list = jieba.cut(content)
        filter_list = [word for word in cut_list if word not in stop_words]
        words = " ".join(filter_list)
        
        t2 = time.time()
        tm_cost = t2-t1
        
        log_f = open(self.outPath,"wb")
        log_f.write(words.encode('utf-8'))

        print('speed %s bytes/second' % (len(content)/tm_cost))
