import os
import sys
import time
import xml.sax
import re
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import Stemmer

# Code for splitting the index

def split():
    count = 0
    limit = 2
    i = 4
    os.rename('index/0.txt', 'index/all.txt')
    file = open('index/all.txt', 'r')
    lines = file.readlines()

    for line in lines:
        if i > limit:
            tempfile = open('index/' + str(count) + '.txt', 'w')
            tempfile.write(line)
            count+=1
            i = 0
        else:
            i+=1
            tempfile.write(line)


    os.remove('index/all.txt')
    file.close()



def getfile():

    f = open('index/helper.txt','w')

    for i in range(0,129,1):
        tempfile = open ('index/'+str(i)+'.txt','r')
        line = tempfile.readline()
        f.write(line.split(':')[0] + '\n')

    f.close()



if __name__ == '__main__':
    print("Splitting the index for easy searching")
    split()
    print("Getting the first line for every index file")
    getfile()