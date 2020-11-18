import os
import sys
import time
import xml.sax
import re
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import Stemmer


# Code to merge the 34 index files created into one

def merge_files(file1, file2):
    
    if file1 == file2:
        return
    
    else:

        f1 = open('index/' + str(file1) + '.txt' , 'r')
        f2 = open('index/' + str(file2) + '.txt' , 'r')
        f3 = open('index/temp.txt', "w+", encoding='utf-8')

        l1 = f1.readline()
        l1 = l1.strip('\n')
        # print(l1)
        l2 = f2.readline()
        l2 = l2.strip('\n')
        # print(l2)
    
        while (l1 and l2):
            word1 = l1.split(":")[0]
            word2 = l2.split(":")[0]
            if word1 > word2:
                f3.write(l2)
                f3.write('\n')
                l2 = f2.readline()
                l2 = l2.strip('\n')
            elif word2 > word1:
                f3.write(l1)
                f3.write('\n')
                l1 = f1.readline()
                l1 = l1.strip('\n')
            else:
                l1 = l1.strip()
                l2 = l2.strip()
                list1 = l1.split(":")[1]
                list2 = l2.split(':')[1]
                final = word1 + ':' + list1 + list2
                f3.write(final + '\n')
                l1 = f1.readline()
                l1 = l1.strip('\n')
                l2 = f2.readline()
                l2 = l2.strip('\n')
    
        while l1:
            f3.write(l1 + '\n')
            l1 = f1.readline()
            l1 = l1.strip('\n')
    
        while l2:
            f3.write(l2 + '\n')
            l2 = f2.readline()
            l2 = l2.strip('\n')
    
        os.remove('index/' + str(file1) + '.txt')
        os.remove('index/' + str(file2) + '.txt')
        os.rename('index/' + 'temp.txt', 'index/' + str(file1//2) + '.txt')


if __name__ == '__main__':

    tot = 6
    
    print("Merging the dump files ....")
    
    while tot != 1:
        for i in range(0, tot, 2):
            if i == tot - 1:
                t1 = 'index/' + str(i) + '.txt'
                t2 = 'index/' + str(i // 2) + '.txt'

                os.rename(t1, t2)
                break
            nextt = i + 1
            merge_files(i, nextt)

        if tot % 2 != 1:
            tot = tot // 2
        else:
            tot = tot // 2
            tot += 1