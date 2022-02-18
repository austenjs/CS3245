
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
    term_dictionary = [] # list to store the term_docid pairs
    posting_dictionary = dict()

    # add all files in the directory for the indexing process
    for filename in listdir(directory):
        with open(filename,'r') as f:
            raw_data = [sentence.strip("\n") for sentence in f.readlines()]
        
        data = Preprocessor.preprocess_file(raw_data)
        doc_id = int(filename.strip(".txt"))
        dictionary = MemoryIndexing.create_dictionary(data,doc_id)
        term_dictionary.extend(dictionary)

    # sort by term, then sort by termID
    term_dictionary.sort(key=lambda x: x[0]).sort(key=lambda x: x[1])

    posting_dictionary = MemoryIndexing.create_posting(term_dictionary)
    term_dictionary.clear()

    pointer_id = 0
    for key,value in posting_dictionary:
        term_dictionary.append((key,len(value),pointer_id))
        pointer_id +=1 

    with open(out_dict,'w',encoding='utf8') as f:
        for elem in term_dictionary:
            f.write(str(elem[0]) + " " + str(elem[1]) + " " + str(elem[2]) + '\n')
        f.close()
    
    with open(out_postings,'w',encoding='utf8') as f:
        for term,docid in posting_dictionary:
            f.write(term + " " + " ".join(str) + '\n')
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
