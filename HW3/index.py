#!/usr/bin/python3
import re
import nltk
import sys
import getopt

import os
import json

from preprocessor import Preprocessor
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

    ROOT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

    p = Preprocessor()
    mi = MemoryIndexing()
    
    filenames = sorted(os.listdir(in_dir), key = lambda filename: int(filename))

    # Generate the term_docid_pairs 
    term_docid_pairs = []
    document_length = dict()
    for filename in filenames:
        terms = p.preprocess_file(os.path.join(in_dir,filename))
        doc_id = int(filename)
        document_length[doc_id] = len(terms)
        term_docid_pair = mi.create_term_docid_pair(terms,doc_id)
        term_docid_pairs.extend(term_docid_pair)
    
    # Create the postings list, with tf normalization applied
    postings_list = mi.create_posting(term_docid_pairs,document_length)

    # Write the postings list to the postings file
    with open(os.path.join(ROOT_DIRECTORY,out_postings), 'w') as postings_file:
        for term, postings in postings_list.items():
            postings_file.write(term)
            for elem in postings:
                postings_file.write('|' + str(elem))
            postings_file.write('\n')
    
    # Read the postings file again to help with the seek() function when searching
    terms = []
    frequencies = dict()
    line_offset = dict()
    offset = 0

    with open(os.path.join(ROOT_DIRECTORY, out_postings), 'r') as posting_file:
        line = posting_file.readline()
        while line != '' and line != '\n':
            term = line.split('|')[0]
            terms.append(term)
            line_offset[term] = offset
            frequencies[term] = (len(line.split('|')) - 1)
            offset += len(line) + 1
            line = posting_file.readline() 

    term_dictionary = mi.create_dictionary_trie(terms,frequencies)

    for term in terms:
        root = term[0]
        current_node = term_dictionary[root]
        for char in term[1:]:
            current_node = current_node[char]
        current_node["_end_"].append(line_offset[term])
    
    # Set the dictionary for the _LENGTH_ term 
    term_dictionary['_LENGTH_'] = line_offset["_LENGTH_"]

    # Write the dictionary to the disk
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
