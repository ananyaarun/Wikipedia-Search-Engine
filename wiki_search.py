import sys
import getopt
import time
import os
import re
import xml.sax
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import Stemmer
from collections import defaultdict
import math
import bisect

sno = SnowballStemmer('english')
stemmer = Stemmer.Stemmer('english')
stop_words = set(stopwords.words('english'))
temp ='-'

mydict =  {
  "t": 0,
  "b": 1,
  "c": 2,
  "i": 3,
  "r": 4,
  "e": 5 
}

ftype = ['t', 'b', 'c', 'i', 'r', 'e']
fscore = [5,1.75,1.5,1.5,1,1]
fquery = ["t:", "b:", "c:", "i:",  "r:", "l:"]

limit = 10000
start_words = open('start_words.txt', 'r')
words = start_words.readlines()



def getlist(word):
    # print("done")
    ind = bisect.bisect_right(words, word) - 1
    if ind == -1:
        return ''
    file = open('./index/' + str(ind+1) + '.txt', 'r')
    lines = file.readlines()
    for line in lines:
        st = line.find(' ',0)
        if word == line[:st]:
            return line[st+1:]
    return ''


def fetch_title(docno):
    off = docno // 10000
    file = open("titles/" + str(off+1) + '.txt')
    return file.readlines()[docno % 10000].strip('\n')


def tokenize1(text):
    global temp
    tokensAndFields = []
    for token in text:
        tokenAndField = token.split(':', 1)
        if len(tokenAndField) == 1:
            tokensAndFields.append([tokenAndField[0], temp])
        else:
            tokenAndField[0]=tokenAndField[0].lower()
            tokenAndField[0] = re.split(r'[^A-Za-z0-9]+', tokenAndField[0])
            temp = tokenAndField[0]
            tokensAndFields.append([tokenAndField[1], tokenAndField[0]])
    return tokensAndFields


def removeStopWords1(tokensAndFields):
    tokens = [token for token in tokensAndFields if not token[0] in stop_words]
    return tokens


def stem1(tokensAndFields):
    stemmedTokens = [[sno.stem(token[0]), token[1]] for token in tokensAndFields]
    return stemmedTokens

def count(stri, ch):
    # print(stri)
    if ch not in stri:
        return 0
    p = stri.split(ch)[1]
    cnt = re.split(r'[^0-9]+', p)[0]
    return int(cnt)

def tokenize(text):
    tokens = re.split(r'[^A-Za-z0-9]+', text)
    return tokens


def removeStopWords(tokens):
    words = []
    for token in tokens:
        if token not in stop_words:
            words.append(token)
    return words


def stem(tokens):
    return stemmer.stemWords(tokens)



def ranking(dc, idcs, plist):
    no = count(dc, 'd')
    for i in range(6):
        if i in idcs:
            if ftype[i] not in dc:
                continue
            counts[no][i+1] += 1
            tf = 1 + math.log2(count(dc, ftype[i]))
            idf = math.log2(9829059 / dc.count(ftype[i]))
            tfidf = tf * idf
            counts[no][i+1] *= fscore[i]
            counts[no][7] += tfidf
    counts[no][0] = max(counts[no][1:7])



if __name__ == '__main__':


    print("preprocessing .... ")

    ansfile = open('queries_op.txt','w')

    path_to_file = sys.argv[1]

    file = open(path_to_file, 'r')

    lines = file.readlines()
    anan = 1
    for line in lines:

        print(" started query number - " + str(anan))
        ansfile.write('\n')
        ansfile.write('\n')
        
        anan+=1
        line = line.lower()
        query = line.split(',')
        num = query[0]
        query = query[1].strip('\n')
        query = query[1:]
        # print(query)
        counts = defaultdict(lambda : [0] * 8)
        chk = 0 
        idx = []

        if ':' in query:
            chk = 1

        st = time.time()
        if chk == 0:
            tokens = tokenize(query)
            tokens = removeStopWords(tokens)
            tokens = stem(tokens)

            for tok in tokens:
                if len(tok) > 0 :
                    posting = getlist(tok)
                if len(posting) == 0:
                    continue

                # print(posting)
                docc = posting.split(' ')
                docc = docc[1:]

                for doc in docc:
                    ranking(doc,[0,1],posting)

            results = sorted(counts.items(), key=lambda x: x[1], reverse = True)
            an = 0
            for result in results[:int(num)]:
                ansfile.write(str(result[0]) + " " + fetch_title(result[0])+'\n')
                an += 1

            while an < int(num):
                ansfile.write(str(an+1) + " " + fetch_title(an+1)+'\n')
                an += 1



            ansfile.write(str(time.time() - st) + " " + str((time.time() - st)/float(num)))

        else:
            querys = query.split(' ')
            temp = 't'

            for q in querys:
                ind = 1
                if 't:' in q:
                    ind = 0
                elif 'b:' in q:
                    ind = 1
                elif 'c:' in q:
                    ind = 2
                elif 'i:' in q:
                    ind = 3
                elif 'r:' in q:
                    ind = 4
                elif 'e:' in q:
                    ind = 5

                if ':' in q:
                    q = q.split(':')[1]

                tokens = tokenize(q)
                tokens = removeStopWords(tokens)
                tokens = stem(tokens)
                for i in tokens:
                    tokens = i

                if len(tokens) == 0 :
                    continue

                posting = getlist(tokens)
                if posting == '':
                    continue;

                docc = posting.split(' ')
                docc = docc[1:]

                for doc in docc:
                    ranking(doc,[ind],posting)


            results = sorted(counts.items(), key=lambda x: x[1], reverse = True)
            an = 0
            for result in results[:int(num)]:
                ansfile.write(str(result[0]) + " " + fetch_title(result[0])+'\n')
                an += 1


            while an < int(num):
                ansfile.write(str(an+1) + " " + fetch_title(an+1)+'\n')
                an += 1


            ansfile.write(str(time.time() - st) + " " + str((time.time() - st)/float(num)))
    
    file.close()

