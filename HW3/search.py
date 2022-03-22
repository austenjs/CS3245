#!/usr/bin/python3
import getopt
import json
import os
import sys

from queryEvaluator import QueryEvaluator
from queryParser import QueryParser

def usage():
    print("usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")

def run_search(dict_file, postings_file, queries_file, results_file):
    """
    using the given dictionary file and postings file,
    perform searching on the given queries file and output the results to a file
    """
    print('running search on the queries...')
    # This is an empty method
    # Pls implement your code in below

    # Paths
    ROOT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    path_to_dict = os.path.join(ROOT_DIRECTORY, dict_file)
    path_to_postings = os.path.join(ROOT_DIRECTORY, postings_file)
    path_to_queries = os.path.join(ROOT_DIRECTORY, queries_file)
    path_to_results = os.path.join(ROOT_DIRECTORY, results_file)

    # Initialize Query related classes
    with open(path_to_dict, 'r') as f:
        trie = json.load(f)
    queryParser = QueryParser()
    queryEvaluator = QueryEvaluator(path_to_postings, trie)

    # Process queries
    queries = queryParser.parse_queries(path_to_queries)
    results = []
    for parsed_query in queries:
        results.append(queryEvaluator.evaluate(parsed_query))

    # Save result
    with open(path_to_results, 'w') as f:
        for result in results:
            if result == []:
                f.write("\n")
            else:
                f.write(" ".join(map(str, result)) + "\n")

dictionary_file = postings_file = file_of_queries = output_file_of_results = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-d':
        dictionary_file  = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        file_of_output = a
    else:
        assert False, "unhandled option"

if dictionary_file == None or postings_file == None or file_of_queries == None or file_of_output == None :
    usage()
    sys.exit(2)

run_search(dictionary_file, postings_file, file_of_queries, file_of_output)
