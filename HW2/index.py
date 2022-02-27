#!/usr/bin/python3
import getopt
import json
import os
from posixpath import dirname
import re
import sys

import nltk

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
    it = IndexTable()

    # add all files in the directory for the indexing process
    for filename in sorted(os.listdir(directory), key = lambda filename: int(filename)):
        data = p.preprocess_file(os.path.join(directory, filename))
        doc_id = int(filename)
        dictionary = mi.create_term_docid_pair(data,doc_id)
        term_docid_list.extend(dictionary)
    
    # convert all the terms into term_id 
    terms = [term[0] for term in term_docid_list]
    index_table = it.term_to_termID(terms)
    termid_docid_list = [(index_table[pair[0]],pair[1]) for pair in term_docid_list]
    term_ids = [index_table[term] for term in terms]

    # sort by term, then sort by docID
    term_docid_list.sort(key=lambda x: (x[0], x[1]))

    # create the postings list and the dictionary terms
    posting_dictionary = mi.create_posting(termid_docid_list)
    all_docid = list(map(int,os.listdir(directory)))
    all_docid.sort()
    posting_dictionary["_ALL_"] = all_docid.copy()

    # create the dictionary of terms using the trie data structure
    term_dictionary = mi.create_dictionary_trie(terms,posting_dictionary,index_table)

    with open(out_dict, 'w') as dict_file:
        json.dump(term_dictionary, dict_file)
    
    with open(out_postings,'w') as posting_file:
        json.dump(posting_dictionary, posting_file)
        

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
