# Wikipedia-Search-Engine

A Mini Wikipedia search engine, which uses Block Sort Based Indexing to create the inverted index of a given wikipedia dump, queries on the index and retrieves top N results via relevance ranking of the documents.

[Link to Wikipedia XML dumps](https://en.wikipedia.org/wiki/Wikipedia:Database_download)

python3 and nltk are required to run the scripts

## Utility

- wiki_indexer.py - parses wikipedia dump and makes inverted index
- merge_index.py - merges the index files created
- split_index.py - splits the index into smaller chunks sorted alphabetically for easy searching
- wiki_search.py - script for querying 

# Creation of Inverted Index

Creation of the inverted index happens in 3 steps. 
- First the individual XML dumps are indexed in these steps
  - Parsing: The XML corpus given is parsed using SAX parser
  - Casefolding: Then Upper Case is converted to Lower Case
  - Tokenisation: Sentences are split into tokens using regex
  - Stop Word Removal: Stop words are removed using stopwords from nltk.corpus
  - Stemming: PyStemmer is used to step individual words
- Once preprocessing is done, individual index files are created with tokens and their respective posting list
- All the indexed files created in the previous step are merged
- Then we split the index into separate files in alphabetically sorted order
- The index is now ready for querying

# Steps for querying

The script for searching handles both simple and multiple field queries. 

- Input for searching is given in the form of a text file with n followed by a comma and then the query string
- The query string is parsed differently for simple and field queries
- All words present in the query string along with field value (if present) are searched for in the index
- The document IDs and term frequencies are retrieved
- A weighted TF-IDF scheme is them used with predefined weights to rank the documents and return the top N titles in the output file for all queries

# Steps to run the code

## Indexing

Create the Index

`python3 wiki_index.py <path to wiki dump files`

`python3 merge_index.py`

`python3 split_index.py`

## Searching

`python3 wiki_search.py <path to input file with queries>`





