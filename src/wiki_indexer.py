import os
import sys
import time
import xml.sax
import re
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import Stemmer

mydict={}
tot = 0
tot1 = 0
stemmer = Stemmer.Stemmer('english')
stop_words = set(stopwords.words('english'))
count = 0

class Parsing():

    def __init__(self):
        self.wordCount = {}
        self.title = ""
        

    def process_Text(self, text, tagType, letterTag):

        if tagType == "title":
            self.title = text.rstrip().rstrip('\n')


        tokens = tokenize(text)
        tokens = removeStopWords(tokens)
        tokens = stem(tokens)

        for token in tokens:

            if token not in self.wordCount:
                self.wordCount[token] = [0,0,0,0,0,0]
            if tagType == "title":
                self.wordCount[token][0] += 1
            elif tagType == "text":
                self.wordCount[token][1] += 1
            elif tagType == "infobox":
                self.wordCount[token][2] += 1
            elif tagType == "categories":
                self.wordCount[token][3] += 1
            elif tagType == "references":
                self.wordCount[token][4] += 1
            elif tagType == "external_links":
                self.wordCount[token][5] += 1


    def create_Index(self, docID, output_dir, tag):

        global mydict
        global count

        sortedWords = self.wordCount.keys()

        for word in sortedWords:

            fString = ""
            fCount = self.wordCount[word]

            if fCount[0] > 0:
                fString += 't' + str(fCount[0])
            if fCount[1] > 0:
                fString += 'b' + str(fCount[1])
            if fCount[2] >  0:
                fString += 'i' + str(fCount[2])
            if fCount[3] >  0:
                fString += 'c' + str(fCount[3])
            if fCount[4] >  0:
                fString += 'r' + str(fCount[4])
            if fCount[5] >  0:
                fString += 'e' + str(fCount[5]) 

            if len(word) > 1:
                if word in mydict:
                    mydict[word] += ' ' + str(docID) +'d' + fString
                else:
                    mydict[word] = str(docID) +'d' + fString
        

        print('Parsing Doc number - ' + str(docID))
        self.wordCount = {}

        f = open("titles/" + str(count) + '.txt', "a+", encoding='utf-8')
        if docID == 0:
            f.write(str(docID) + '-' + self.title)
        else:
            f.write('\n' + str(docID) + '-' + self.title)
        f.close()



def tokenize(text):
    global tot
    tokens = re.split(r'[^A-Za-z0-9]+', text)
    tot += len(tokens)
    return tokens


def removeStopWords(tokens):
    words = []
    for token in tokens:
        if token not in stop_words:
            words.append(token)
    return words


def stem(tokens):
    return stemmer.stemWords(tokens)



def writeto(output_dir):
    global tot1
    global count
    f = open("index/" + str(count) + '.txt' , "w+", encoding='utf-8')
    for i in sorted(mydict.keys()):
        f.write(i + '-' + mydict[i] + '\n')
        tot1+=1;

    f.close()



def Infobox(text):
    data = text.split('\n')
    flag = 0
    i = ""
    for line in data:
        if re.match(r'\{\{infobox', line):
            flag = 1
            temp = re.sub(r'\{\{infobox(.*)', r'\1', line)
            i += temp
            i += ' '
        elif flag == 1:
            if line == '}}':
                flag = 0
                continue
            i += line
            i += ' '
    return i


def References(text):
    data = text.split('\n')
    r = ""
    for l in data:
        if re.search(r'<ref', l):
            temp = re.sub(r'.*title[\ ]*=[\ ]*([^\|]*).*', r'\1', l)
            r += temp
            r+= ' '
    
    return r
    
        


def Categories(text):
    data = text.split('\n')
    c = ""
    for line in data:
        if re.match(r'\[\[category', line):
            temp = re.sub(r'\[\[category:(.*)\]\]', r'\1', line)
            c += temp
            c += ' '
    return c
        


def ExternalLinks(text):
    data = text.split('\n')
    l = ""
    for line in data:
        if re.match(r'\*[\ ]*\[', line):
            l += line
            l += ' '
        
    return l
        



class WikiXMLHandler(xml.sax.ContentHandler):
    
   
    def __init__(self, output_dir):
        self.textParser = Parsing()
        self.docID = 0
        self.output_dir = output_dir
        self.new_merge = 0
        self.currentTag = ""
        self.title = ""
        self.infobox = ""
        self.body = ""
        self.categories = ""
        self.references = ""
        self.externalLinks = ""
        self.text=""
    

    def startElement(self, tag, attributes):
        self.currentTag = tag 
        if tag == "page":
            self.currentTag = ""
            self.title = ""
            self.text=""
            self.infobox = ""
            self.body = ""
            self.categories = ""
            self.references = ""
            self.externalLinks = ""
    
    
    def endElement(self, tag):
        if tag == "page":

            self.text = self.text.lower() 
            self.title = self.title.lower() 


            data = self.text.split('==references==')
            if len(data) == 1:
                data = self.text.split('== references ==')
            if len(data) > 1:

                self.references = References(data[1])
                self.externalLinks = ExternalLinks(data[1])
                self.categories = Categories(data[1])
            
            self.infobox = Infobox(data[0])
            self.body = re.sub(r'\{\{.*\}\}', r' ', data[0])

            self.textParser.process_Text(self.title, "title",'t')
            self.textParser.process_Text(self.body, "text",'b')
            self.textParser.process_Text(self.categories, "categories",'c')
            self.textParser.process_Text(self.infobox, "infobox",'i')
            self.textParser.process_Text(self.references, "references",'r')
            self.textParser.process_Text(self.externalLinks, "external_links",'e')
            
            self.textParser.create_Index(self.docID, self.output_dir,'create')

            self.docID += 1


    

    def characters(self, content):

        if self.currentTag == "title":
            self.title += content


        elif self.currentTag == "text":
            self.text += content



if __name__ == "__main__":
    
    start_time = time.time()
    xmlFilePath = sys.argv[1]

    os.mkdir('index')
    os.mkdir('titles')

    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    wikiHandler = WikiXMLHandler('index/')
    parser.setContentHandler(wikiHandler)

    for filename in os.listdir(xmlFilePath):
        mydict = {}
        print("Next file parsing started .... ")
        parser.parse(xmlFilePath+'/'+filename)
        writeto(output_dir)
        count+=1

    print("Total time taken is --- %s seconds ---" % (time.time() - start_time))
