
#!/usr/bin/python3
import re
import nltk
import sys
import getopt

from os import listdir
from preprocessor import Preprocessor
from index_table import IndexTable
from memory_indexing import MemoryIndexing

def usage():
    print("usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")

def build_index(in_dir, out_dict, out_postings):
    """
    build index from documents stored in the input directory,
    then output the dictionary file and postings file
    """
    print('indexing...')
    # This is an empty method
    # Pls implement your code in below

    directory = in_dir
    term_docid_list = [] # list to store the term_docid pairs
    posting_dictionary = dict()

    p = Preprocessor()
    mi = MemoryIndexing()

    # add all files in the directory for the indexing process
    for filename in listdir(directory):
        with open(filename,'r') as f:
            raw_data = [sentence.strip("\n") for sentence in f.readlines()]

        data = p.preprocess_file(raw_data)
        doc_id = int(filename.strip(".txt"))
        dictionary = mi.create_term_docid_pair(data,doc_id)
        term_docid_list.extend(dictionary)

    # sort by term, then sort by termID
    term_docid_list.sort(key=lambda x: (x[0],x[1]))

    terms = [term[0] for term in term_docid_list]
    posting_dictionary = mi.create_posting(term_docid_list)
    term_dictionary = mi.create_dictionary_trie(terms)

    with open(out_dict,'w',encoding='utf8') as f:
        f.write(term_dictionary)
        f.close()
    
    with open(out_postings,'w',encoding='utf8') as f:
        for term,docid in posting_dictionary:
            f.write(term + " " + " ".join(str(docid)) + '\n')
        f.close()
        

input_directory = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i': # input directory
        input_directory = a
    elif o == '-d': # dictionary file
        output_file_dictionary = a
    elif o == '-p': # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"

if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

build_index(input_directory, output_file_dictionary, output_file_postings)
