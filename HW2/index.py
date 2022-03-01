#!/usr/bin/python3
import getopt
import json
import os
from posixpath import dirname
import re
import sys
from math import sqrt

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

    # sort by term, then sort by docID
    term_docid_list.sort(key=lambda x: (x[0], x[1]))

    # create the postings list and the dictionary terms
    posting_dictionary = mi.create_posting(termid_docid_list)
    all_docid = list(map(int,os.listdir(directory)))
    all_docid.sort()
    posting_dictionary["_ALL_"] = tuple(map(lambda id: (id, None, None), all_docid))

    # create the dictionary of terms using the trie data structure
    term_dictionary = mi.create_dictionary_trie(terms,posting_dictionary,index_table)

    # write the postings list to the disk
    with open(out_postings,'w') as posting_file:
        for term, postings in posting_dictionary.items():
            posting_file.write(str(term))
            for posting in postings:
                posting_file.write("|" + str(posting))
            posting_file.write("\n")
    
    # read the postings file again to help with the seek() function when searching
    with open(out_postings,'r') as posting_file:
        posting_data = posting_file.readlines()

    line_offset = []
    offset = 0
    for line in posting_data:
        line_offset.append(offset)
        offset += len(line) + 1

    checked_terms = set()
    for term in terms:
        if term in checked_terms:
            continue
        term_id = index_table[term]
        root = term[0]
        current_node = term_dictionary[root]
        for char in term[1:]:
            current_node = current_node[char]
        current_node["_end_"].append(line_offset[term_id - 1])
        checked_terms.add(term)
    term_dictionary['_ALL_'] = (None, len(checked_terms), line_offset[-1])


    # write the dictionary to the disk
    with open(out_dict, 'w') as dict_file:
        json.dump(term_dictionary, dict_file)
        
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
