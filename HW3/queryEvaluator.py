import heapq
from math import log10
import os
from typing import List, Tuple
import yaml

from utils import normalize

# Obtain hyperparameters
ROOT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(ROOT_DIRECTORY, "config.yaml"), "r") as config:
    hyperparameters = yaml.full_load(config)
idf_cutoff = hyperparameters['heuristic1']['idf_cutoff']
score_contribution_cutoff = hyperparameters['heuristic3']['score_contribution_cutoff']

class QueryEvaluator:
    '''
    Evaluator class that in charge of evalauting the parsed
    queries.
    Attributes:
    posting_lists (Dict[str, List[int]]) : A Dict of posting-lists.
    trie (Trie) : A trie to convert term into id
    '''
    def __init__(self, path_to_postings, trie):
        '''
        Initialize the posting lists.
        Argument:
        path_to_postings (str): Path to posting lists
        '''
        self.posting_lists = open(path_to_postings, 'r')
        self.trie = trie

    def _exist(self, term) -> bool:
        '''
        Check whether the term is in the Posting Lists.
        Argument:
            term (str): A word
        Return:
            A boolean specifying whether it exists or not
        '''
        current = self.trie
        for letter in term:
            if letter not in current:
                return False
            current = current[letter]
        return ('_end_' in current)
    
    def _get_doc_frequency(self, term) -> int:
        '''
        Get the document frequency of a term.
        Argument:
            term (str): A word
        Return:
            The document frequency of the term
        '''
        current = self.trie
        for letter in term:
            if letter not in current:
                return []
            current = current[letter]
        # Not leaf
        if '_end_' not in current:
            return 0
        return current['_end_'][0]

    def _get_posting_list(self, term) -> List[int]:
        '''
        Get the posting list of a term.
        Argument:
            term (str): A word
        Return:
            A posting list
        '''
        current = self.trie
        for letter in term:
            if letter not in current:
                return []
            current = current[letter]
        # Not leaf
        if '_end_' not in current:
            return []
        position = current['_end_'][1]
        self.posting_lists.seek(position, 0)
        lines = self.posting_lists.readline().split('|')
        relevant_lines = list(map(lambda clause: eval(clause.rstrip()), lines[1:]))
        return relevant_lines

    def _get_list_of_doc_term_counts(self) -> List[Tuple[int, int]]:
        '''
        Get the list of doc term counts.

        Return:
            List of doc term counts.
        '''
        position = self.trie["_LENGTH_"]
        self.posting_lists.seek(position, 0)
        lines = self.posting_lists.readline().split('|')
        relevant_lines = list(map(lambda clause: eval(clause.rstrip()), lines[1:]))
        return relevant_lines

    def evaluate(self, parsed_query) -> List[str]:
        '''
        Take a parsed queries in the form of postfix notation
        and evaluate it.
        Argument:
            parsed_query (List[str]): The parsed query in postfix notations
        Return:
            A list of string
        '''
        length = self._get_list_of_doc_term_counts()
        N = len(length)
        scores = [[posting[0], 0] for posting in length]

        # Create dict for O(1) scores retrieval
        doc_to_index = {}
        for i, score in enumerate(scores):
            doc_to_index[score[0]] = i

        # Calculate tf and idf of query
        tf_list = []
        idf_list = []
        index = 0
        term_to_index = {}
        for term in parsed_query:
            # The term doesn't exist in dictionary
            if not self._exist(term):
                continue
            if term in term_to_index:
                tf_list[term_to_index[term]] += 1
                continue
            doc_freq = self._get_doc_frequency(term)
            idf = log10(N / doc_freq)
            # Ignore low idf term
            if idf < idf_cutoff:
                continue
            tf_list.append(1)
            idf_list.append(idf)
            term_to_index[term] = index
            index += 1

        # tf-wt
        for i in range(index):
            tf_list[i] = 1 + log10(tf_list[i])

        # tf-idf normalized
        w_tq = []
        for i in range(index):
            w_tq.append(tf_list[i] * idf_list[i])
        w_tq = normalize(w_tq)

        for term, term_index in term_to_index.items():
            posting_list = self._get_posting_list(term)
            for doc, w_td in posting_list:
                doc_index = doc_to_index[doc]
                score_contribution = w_td * w_tq[term_index]
                scores[doc_index][1] += score_contribution
                # Continue to next term
                if score_contribution < score_contribution_cutoff:
                    break

        # Get top 10
        top_10 = heapq.nlargest(10, scores, key = lambda x : x[1])
        results = []

        # Sort by score, then by doc id
        results = sorted(results, key = lambda x : (x[1], x[0]))

        # Give docs that have values > 0
        for pair in top_10:
            if pair[1] == 0:
                continue
            results.append(pair[0])

        return results
