import xml.sax
import os
import sys
import re
import time
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer 

# Global variables

# counts = {}

stemming = SnowballStemmer('english')
lemma = WordNetLemmatizer()
stop = set(stopwords.words('english'))



# function to parse

def parse_text(text, tagType, key,counts,hash_map,title):

    if tagType == "title":
        title = text.rstrip().rstrip('\n')
        
    # case folding
    text = text.lower()
        
    # tokenization
    tokens,hash_map = tokenize(text,hash_map)
    tokens,hash_map = removeStopWords (tokens,hash_map)
    tokens,hash_map = stem(tokens,hash_map)

    for token in tokens:

        if token not in counts:
            counts[token] = [0,0,0,0,0,0]

        if tagType == "title":
            counts[token][0] += 1;
            
        elif tagType == "text":
            counts[token][1] += 1;

        elif tagType == "infobox":
            counts[token][2] += 1;

        elif tagType == "categories":
            counts[token][3] += 1;

        elif tagType == "references":
            counts[token][4] += 1;

        elif tagType == "external_links":
            counts[token][5] += 1;


# Function to create Index

def create_index(pagen, output_dir,counts,hash_map,title):
        
    sortedWords = sorted(counts.keys())

    f = open(output_dir + "/" + str(pagen) + '-0.txt', "w+", encoding='utf-8')

    for word in sortedWords:

        fieldString = ""
        fieldCount = counts[word]
        if fieldCount[0] > 0:
            fieldString += 't' + str(fieldCount[0])
        if fieldCount[1] > 0:
            fieldString += 'b' + str(fieldCount[1])
        if fieldCount[2] >  0:
            fieldString += 'i' + str(fieldCount[2])
        if fieldCount[3] >  0:
            fieldString += 'c' + str(fieldCount[3])
        if fieldCount[4] >  0:
            fieldString += 'r' + str(fieldCount[4])
        if fieldCount[5] >  0:
            fieldString += 'e' + str(fieldCount[5])        
            
        f.write(word + '-' + str(pagen) + 'd' + fieldString + '\n')     
        
    f.close()
    counts = {}
        
    f = open(output_dir + "/titles.txt", "a+", encoding='utf-8')
    if pagen == 0:
        f.write(str(pagen) + '-' + title)
    else:
        f.write('\n' + str(pagen) + '-' + title)
    f.close()


def tokenize(text,hash_map):
    text = text.replace("'", "").replace("_", "")
    tokens = re.findall(r"[\w']{3,}", text)
    return tokens,hash_map

def removeStopWords(tokens,hash_map):
    words = []
    for token in tokens:
        if token not in stop:
            flag = 0
            for c in token:
                if ord(c) > ord('z'):
                    flag = 1
            if flag == 0:
                words.append(token)
    return words,hash_map


def stem(tokens,hash_map):
    stemmedTokens = []
    for token in tokens:
        if token not in hash_map:
            hash_map[token] = [0, stemming.stem(token)]
        stemmedTokens.append(hash_map[token][1])
        hash_map[token][0] += 1

    if len(hash_map) > 10000:
        delete_list = sorted(hash_map.items(), key=lambda x: x[1][0])[:1000]
        for delete_word in delete_list:
            del hash_map[delete_word[0]]

    return stemmedTokens,hash_map



def lemmatize(tokens,hash_map):
    lemmatizedTokens = [lemma.lemmatize(token) for token in tokens]
    return lemmatizedTokens,hash_map






# class for wiki xml handler

class WikiXMLHandler(xml.sax.ContentHandler):
    def __init__(self, output_dir):
        self.pagenum = 0
        self.output_dir = output_dir
        self.counts = {}
        self.hash_map = {}
        self.title =""
    


    def startElement(self, tag, attributes):
        self.currentTag = tag 
        if tag == "page":
        	self.currentTag = ""
        	self.title = ""
        	self.info = ""
        	self.body = ""
        	self.cate = ""
        	self.ref = ""
        	self.ext = ""
        	self.iFlag = 0
        	self.rFlag = 0
        	self.eFlag = 0



    def endElement(self, tag):
        if tag == "page":
          
            parse_text(self.title, "title", "t", self.counts,self.hash_map,self.title)
            parse_text(self.body, "text", "b",self.counts,self.hash_map,self.title)
            parse_text(self.cate, "categories", "c",self.counts,self.hash_map,self.title)
            parse_text(self.info, "infobox", "i",self.counts,self.hash_map,self.title)
            parse_text(self.ref, "references", "r",self.counts,self.hash_map,self.title)
            parse_text(self.ext, "external_links", "e",self.counts,self.hash_map,self.title)
            
            create_index(self.pagenum, self.output_dir,self.counts,self.hash_map,self.title)
            self.pagenum += 1



    def characters(self, content):

        if self.currentTag == "title":
            self.title += content

        elif self.currentTag == "text":
            if "[[Category:" in content or "[[category:" in content:
                pos = content.find("[[Category:")
                if pos == -1:
                    pos = content.find("[[category:")
                self.cate += content[pos:]

            elif "{{Infobox" in content or "{{infobox" in content:
                self.iFlag = 1
                pos = content.find("{{Infobox")
                if pos == -1:
                    pos = content.find("{{infobox")
                content = content[pos:]

            elif "==Reference" in content or "== Reference" in content or "==reference" in content:
                self.rFlag = 1 
            elif "==External links==" in content or "== External links==" in content:
                self.eFlag = 1
            
            else:
                self.body += content

            if self.iFlag >= 1:
                self.rFlag = 0
                self.eFlag = 0
                if "{{" in content:
                    self.iFlag += 1
                if "}}" in content:
                    self.iFlag -= 1
                if content == "}}":
                    self.iFlag = 0
                self.info += content

            if self.rFlag == 1:
                self.iFlag = 0
                self.eFlag = 0
                if self.ref != "" and len(content) > 1 and content[0] != '{' and content[1] != '{':
                    self.rFlag = 0
                elif len(content) > 1 and content[0] == '{' and content[1] == '{':
                    self.ref += content

            if self.eFlag == 1:
                self.iFlag = 0
                self.rFlag = 0
                if self.ext != "" and len(content) > 1 and content[0] != '{':
                    self.eFlag = 0
                elif len(content) > 0 and content[0] == '*':
                    self.ext += content
            


if __name__ == "__main__":

    st = time.time()

    xmlPath = sys.argv[1]
    outputPath = sys.argv[2]

    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    wikiHandler = WikiXMLHandler(outputPath)
    parser.setContentHandler(wikiHandler)
    parser.parse(xmlPath)

    fin_time = (time.time() - st)
    print("Total time taken - %s seconds" % fin_time)
    

