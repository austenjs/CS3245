#!/usr/bin/python3
import getopt
import json
import os
import shutil
import sys

from bsbi import BSBI
from index_table import IndexTable
from memory_indexing import MemoryIndexing
from preprocessor import Preprocessor

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
    directory = os.path.join(ROOT_DIRECTORY, in_dir)
    temp_folder = os.path.join(ROOT_DIRECTORY, 'disks')

    # Check if folder exists
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)
    else:
        shutil.rmtree(temp_folder)
        os.mkdir(temp_folder)

    p = Preprocessor()
    mi = MemoryIndexing()
    it = IndexTable()

    # BSBI
    filenames = sorted(os.listdir(directory), key = lambda filename: int(filename))
    num_of_files_in_one_block = 1000
    bsbi = BSBI(num_of_files_in_one_block, filenames)
    chunks = bsbi.generate_chunks()

    term_docid_list = [] # list to store the term_docid pairs
    for i in range(len(chunks)):
        chunk = chunks[i]
        print('Processing {} - {}'.format(chunk[0], chunk[-1]))
        for filename in chunk:
            data = p.preprocess_file(os.path.join(directory, filename))
            doc_id = int(filename)
            dictionary = mi.create_term_docid_pair(data, doc_id)
            term_docid_list.extend(dictionary)

        # convert all the terms into term_id 
        terms = list(set(map(lambda pair: pair[0], term_docid_list)))
        index_table = it.term_to_termID(terms)
        termid_docid_list = [(index_table[pair[0]], pair[1]) for pair in term_docid_list]

        # create the postings list and the dictionary terms
        posting_dictionary = mi.create_posting(termid_docid_list)

        # write the postings list to the disk
        target_name = os.path.join(temp_folder, 'level0_chuck_{}.txt'.format(i))
        with open(target_name,'w') as posting_file:
            for term in sorted(terms, key = lambda t: index_table[t]):
                term_id = index_table[term]
                posting_file.write(str(term_id))
                for posting in posting_dictionary[term_id]:
                    posting_file.write("|" + str(posting))
                posting_file.write("\n")

        # Clear for next chunk
        term_docid_list.clear()

    ## Merging
    level = 1
    filenames_in_disks = os.listdir(temp_folder)
    while len(filenames_in_disks) > 1:
        bsbi.merge(filenames_in_disks, temp_folder, level)
        filenames_in_disks = os.listdir(temp_folder)
        level += 1

    # Write the _ALL_ for NOT operation in Search
    with open(os.path.join(temp_folder, filenames_in_disks[0]), 'a') as posting_file:
        posting_file.write("_ALL_")
        for filename in filenames:
            posting_file.write("|" + filename)

    # Create skip pointer and write it on the output file
    with open(os.path.join(ROOT_DIRECTORY, out_postings), 'w') as posting_file:
        with open(os.path.join(temp_folder, filenames_in_disks[0]), 'r') as bsbi_result:
            line = bsbi_result.readline().rstrip()
            while line != '' and line != '\n':
                termId, *postings = line.split('|')
                posting_with_skip = mi.create_skip_pointers(list(map(int, postings)))
                posting_file.write(termId)
                for posting in posting_with_skip:
                    posting_file.write("|" + str(posting))
                posting_file.write("\n")
                line = bsbi_result.readline()
    
    # Delete BSBI chunk
    os.remove(os.path.join(temp_folder, filenames_in_disks[0]))
    
    # read the postings file again to help with the seek() function when searching
    line_offset = []
    frequencies = []
    offset = 0
    with open(os.path.join(ROOT_DIRECTORY, out_postings), 'r') as posting_file:
        line = posting_file.readline()
        while line != '' and line != '\n':
            line_offset.append(offset)
            frequencies.append(len(line.split('|')) - 1)
            offset += len(line) + 1
            line = posting_file.readline()

    # create the dictionary of terms using the trie data structure
    terms = it.get_term_termID_dict().keys()
    term_dictionary = mi.create_dictionary_trie(terms, frequencies, index_table)

    for term in terms:
        term_id = index_table[term]
        root = term[0]
        current_node = term_dictionary[root]
        for char in term[1:]:
            current_node = current_node[char]
        current_node["_end_"].append(line_offset[term_id - 1])
    term_dictionary['_ALL_'] = (None, line_offset[-1])


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
