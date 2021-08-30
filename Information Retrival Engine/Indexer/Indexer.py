import os
import time
from xml.dom.minidom import parse, parseString
from porter import PorterStemmer


class Indexer:
    def __init__(self):
        self.stopWordSet = set()
        self.porter = PorterStemmer()
        self.allWordLists = []
        self.allCountLists = []
        self.forwardIndexResults = []
        self.invertedIndexResults = []
    #struct Node {}

    def set_stop_word_list(self, list_file):
        with open(list_file) as input_file:
            for input_line_raw in input_file:
                word = input_line_raw.lstrip().rstrip()
                self.stopWordSet.add(word)
        input_file.close()

    @staticmethod
    def getText(nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
        #for node in nodelist:
            #if node.noLen==node.Text_NODE_Len:   
                rc.append(node.data)
        return ''.join(rc)

    def handle_doc(self, doc):
        docNum = doc.getElementsByTagName("DOCNO")
        #doc=doc.getElementsByTagName("DOC")
        doc_i = docNum[0].firstChild.data
        result = doc_i + ": "
        textTag = doc.getElementsByTagName('TEXT')[0]
        text = self.getText(textTag.childNodes)
        lines = text.split('\n')
        wordList = []
        for line in lines:
            word = ''
            if line == '':
                continue
            for c in line:
                if c.isalpha():
                    word += c.lower()
                else:
                    if word:
                        if not (word in self.stopWordSet):
                            word = self.porter.stem(word, 0, len(word) - 1)
                            wordList.append(word)
                        word = ''
        wordList = sorted(wordList)
        nonRepeatWordList = []
        counts = [1]
        c = 0
        nonRepeatWordList.append(wordList[0])
        for index in range(1, len(wordList)):
            if wordList[index] == wordList[index - 1]:
                counts[c] = counts[c] + 1
            else:
                result += nonRepeatWordList[c] + ': ' + str(counts[c]) + ';'
                nonRepeatWordList.append(wordList[index])
                counts.append(1)
                c = c + 1
        result += nonRepeatWordList[c] + ': ' + str(counts[c]) + ';'
        self.allWordLists.append(nonRepeatWordList)
        self.allCountLists.append(counts)
        return result + '\n'

    def xml_parse(self, file_path):
        with open(file_path, "r") as xml_file:
            data = xml_file.read()
            data = '<Data>\n' + data + '\n</Data>'
            content = parseString(data)
            docs = content.getElementsByTagName("DOC")
            for doc in docs:
                r = self.handle_doc(doc)
                self.forwardIndexResults.append(r)
        xml_file.close()

    def inverted_index(self):
        self.wordSet = self.allWordLists[0].copy()
        lenDocs = len(self.allWordLists)

        for index in range(1, lenDocs):
            for word in self.allWordLists[index]:
                if word not in self.wordSet:
                    self.wordSet.append(word)
        self.countInDocs = [[] for x in range(len(self.wordSet))]
#doc_id = int(llist[0])
	#if pre_docid != doc_id:
		#if pre_docid != -1:
			#db.Put(str(pre_docid),'#'.join(doc_info))
        for index in range(len(self.wordSet)):
            self.invertedIndexResults += self.wordSet[index] + ': '
            for j in range(lenDocs):
                if self.wordSet[index] in self.allWordLists[j]:
                    c = self.allCountLists[j][self.allWordLists[j].index(self.wordSet[index])]
                    self.countInDocs[index].append(c)
                    self.invertedIndexResults += 'FT911-' + str(j + 1) + ': ' + str(c) + '; '
                else:
                    self.countInDocs[index].append(0)
            self.invertedIndexResults += '\n'


if __name__ == '__main__':
    print("ahdgfjfhgsl")
    indexer = Indexer()
    start = time.time()
    indexer.set_stop_word_list("./stopwordlist.txt")
    for root, dirs, files in os.walk("./data"):
        for file in files:
            indexer.xml_parse(root + '/' +file)
    # for i in range(1, 16):
    #     indexer.xml_parse('./data/ft911_' + str(i))
    end1 = time.time()
    indexer.inverted_index()
    end2 = time.time()
    with open('tag1.txt', 'w') as out_file:
        out_file.writelines(indexer.forwardIndexResults)
    out_file.close()
   #with open('forwardIndex.txt','r') as out_file:
        #out_file.writelines(i)
    with open('tag2.txt', 'w') as out_file:
        out_file.writelines(indexer.invertedIndexResults)
    out_file.close()
    print("jdsbfjkjfb")
    print('Fi: ' + str(end1 - start))
    print('Ii: ' + str(end2 - start))
    print('sz ' + str(len(indexer.wordSet)))

    exit = False
    while not exit:
	    print('Please enter a term:')
	    term = input()
	    if term == "quit" or term == "QUIT":
	    	exit = True;
	    else:
		    if term in indexer.stopWordSet:
		    	print(term + ' is stop word.')
		    else:
			    if term in indexer.wordSet:
			    	printStr = term + ': '
			    	d_id = 1
			    	for i in indexer.countInDocs[indexer.wordSet.index(term)]:
			    		if i > 0:
			    			printStr += 'FT911-' + str(d_id) + ': ' + str(i) + '; '
			    		d_id = d_id + 1
			    	print(printStr)
			    else:
			    	print(term + ' does not exist in any doc.')
