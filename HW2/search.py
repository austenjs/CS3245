#!/usr/bin/python3
import getopt
import json
import sys

from queryParser import QueryParser
from queryEvaluator import QueryEvaluator

def usage():
    print("usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")

def run_search(dict_file, postings_file, queries_file, results_file):
    """
    using the given dictionary file and postings file,
    perform searching on the given queries file and output the results to a file
    """
    print('running search on the queries...')
    # Create Parser and Evaluator
    parser = QueryParser()
    with open(dict_file, 'r') as f:
        trie = json.load(f)
    evaluator = QueryEvaluator(postings_file, trie)

    # Parse queries
    results = []
    queries = parser.parse_queries(queries_file)
    for query in queries:
        results.append(evaluator.evaluate(query))

    # Save result
    with open(results_file, 'w') as f:
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
