### Project Description:

An IR Engine includes the following three major components: 
  * Text parser
  * Indexer
  * Retriever

For this project we will build the Indexer. It will include building a forward index and an inverted index for a larger document collection. we will use this infrastructure in the future which involves implementing the query processing and retrieval portion of the vector space model for IR.

## Forward Index
The forward index stores a list of words for each document. The following is an illustration of the forward index:

####  Forward Index
Document |            Words
---------|-----------------------------
  1      | cow 2;  moon 4; sum 10; ……..
  2      | cat 1; hat 6; flower 4; …….
  3      |  dish 5;  spoon 4; ……….

In our built forward index file, stores the document information in the following format:
 * docID1: …; wordIdi: freq in docID1; wordIdi+1: freq in docID1; ……….
 * docID2: …; wordIdj: freq in docID2; wordIdj+1: freq in docID2; ……….
 * (only record the words (and frequencies) occurring in a document)

## Inverted Index
The inverted index stores a list of documents for each word. The following is an illustration of the inverted index:

#### Inverted Index
Word        |       Documents
------------|-------------------------
  orange    |Doc1: 3, Doc3: 4, Doc4: 5
  cow       |Doc2: 5, Doc3: 8, Doc4:1
  computer  |Doc5: 10
  moon      |Doc7: 9

In our built inverted index file, stores the word information will be in the following format:
 * wordID1: docId1: freq in docID1; docId2: freq in docID2; ……….
 * wordID2: docId10: freq in docID10; docId12: freq in docID12; ……….
