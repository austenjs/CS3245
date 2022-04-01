from math import sqrt

from typing import List

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
        return True

    def _get_posting_list(self, term) -> List[int]:
        '''
        Get the posting list of an existing term.

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
        # Not leave
        if '_end_' not in current:
            return []
        position = current['_end_'][1]
        self.posting_lists.seek(position, 0)
        lines = self.posting_lists.readline().split('|')
        relevant_lines = list(map(lambda clause: eval(clause.rstrip()), lines[1:]))
        return relevant_lines

    def _is_operator(self, token) -> bool:
        '''
        Take a token and specify whether it is an operator or not.

        Argument:
        token (str): A token

        Return:
        A boolean denoting whether the token is an operator or not.
        '''
        return token == 'AND' or token == 'OR' or token == 'NOT'

    def _create_skip_pointers(self, posting_list) -> List[int]:
        '''
        Convert the element of the posting list into tuple that has format of
        (docId, nextValue, nextIndex)
        
        Argument:
        posting_list (List[int]): A posting list

        Return:
        A posting list with skip pointers
        '''
        skip_jump = int(sqrt(len(posting_list)))
        length = len(posting_list)
        new_posting_list = []

        for i in range(length):
            if i % skip_jump == 0 and i + skip_jump < length:
                new_posting_list.append((posting_list[i], posting_list[i + skip_jump], i + skip_jump))
            else:
                new_posting_list.append((posting_list[i], None, None))

        return new_posting_list

    def _intersection(self, posting_list1, posting_list2) -> List[int]:
        '''
        Perform intersection of 2 posting lists.

        Argument:
        posting_list1 (List[int]) : Posting list of term 1
        posting_list2 (List[int]): Posting list of term 2

        Return:
        A posting-list that consists of the intersection of the two posting lists
        '''
        i = j = 0
        M, N = len(posting_list1), len(posting_list2)
        
        final_posting_list = []
        while i < M and j < N:
            if posting_list1[i][0] == posting_list2[j][0]:
                final_posting_list.append(posting_list1[i][0])
                i += 1
                j += 1
            elif posting_list2[j][1] != None and posting_list1[i][0] >= posting_list2[j][1]:
                j = posting_list2[j][2]
            elif posting_list1[i][1] != None and posting_list1[i][1] <= posting_list2[j][0]:
                i = posting_list1[i][2]
            elif posting_list1[i][0] >= posting_list2[j][0]:
                j += 1
            elif posting_list1[i][0] <= posting_list2[j][0]:
                i += 1
        return self._create_skip_pointers(final_posting_list)

    def _union(self, posting_list1, posting_list2) -> List[int]:
        '''
        Perform union of 2 posting lists.

        Argument:
        posting_list1 (List[int]) : Posting list of term 1
        posting_list2 (List[int]): Posting list of term 2

        Return:
        A posting-list that consists of the union of the two posting lists
        '''
        i = j = 0
        M, N = len(posting_list1), len(posting_list2)
        
        final_posting_list = []
        while i < M and j < N:
            if posting_list1[i][0] == posting_list2[j][0]:
                final_posting_list.append(posting_list1[i][0])
                i += 1
                j += 1
            elif posting_list1[i][0] > posting_list2[j][0]:
                final_posting_list.append(posting_list2[j][0])
                j += 1
            else:
                final_posting_list.append(posting_list1[i][0])
                i += 1

        # Leftovers
        while i < M:
            final_posting_list.append(posting_list1[i][0])
            i += 1
        while j < N:
            final_posting_list.append(posting_list2[j][0])
            j += 1
        return self._create_skip_pointers(final_posting_list)

    def _negate(self, posting_list):
        '''
        Get the complement of a posting list.

        Argument:
        posting_list List[int]: Posting list

        Return:
        A list of integers that is the complement of the posting_list
        '''
        avoided_files = set(map(lambda x: x[0], posting_list))
        all_position = self.trie['_ALL_'][1]
        self.posting_lists.seek(all_position, 0)
        lines = self.posting_lists.readline().split('|')
        relevant_lines = list(map(lambda clause: eval(clause.rstrip()), lines[1:]))

        final_posting_list = []
        for id, _, _ in relevant_lines:
            if id in avoided_files:
                continue
            final_posting_list.append(id)
        return self._create_skip_pointers(final_posting_list)

    def evaluate(self, parsed_query) -> List[str]:
        '''
        Take a parsed queries in the form of postfix notation
        and evaluate it.

        Argument:
            parsed_query (List[str]): The parsed query in postfix notations

        Return:
            A list of string
        '''
        stack = []
        for token in parsed_query:
            if self._is_operator(token):
                # NOT operation
                if token == 'NOT':
                    term = stack.pop()
                    if isinstance(term, str):
                        if not self._exist(term):
                            term = []
                        else:
                            term = self._get_posting_list(term)
                    new_posting_list = self._negate(term)
                    stack.append(new_posting_list)
                    continue

                term1, term2 = stack.pop(), stack.pop()
                # Both tokens
                if isinstance(term1, str) and isinstance(term2, str):
                    if not self._exist(term1):
                        posting_list1 = []
                    else:
                        posting_list1 = self._get_posting_list(term1)
                    if not self._exist(term2):
                        posting_list2 = []
                    else:
                        posting_list2 = self._get_posting_list(term2)
                # Both list
                if isinstance(term1, list) and isinstance(term2, list):
                    posting_list1, posting_list2 = term1, term2

                # Token - list
                if isinstance(term1, str) and isinstance(term2, list):
                    if not self._exist(term1):
                        posting_list1 = []
                    else:
                        posting_list1 = self._get_posting_list(term1)
                    posting_list2 = term2

                # List - token
                if isinstance(term1, list) and isinstance(term2, str):
                    if not self._exist(term2):
                        posting_list2 = []
                    else:
                        posting_list2 = self._get_posting_list(term2)
                    posting_list1 = term1

                # Merge operation
                if token == 'AND':
                    combined_posting_list = self._intersection(posting_list1, posting_list2)
                else:
                    combined_posting_list = self._union(posting_list1, posting_list2)
                stack.append(combined_posting_list)
            else:
                stack.append(token)
        if len(stack) > 1:
            print('Error in Evaluation {}'.format(parsed_query))
            return []

        final_result = []
        # Query of single word
        if isinstance(stack[0], str):
            final_result = self._get_posting_list(stack.pop())
        else:
            final_result = stack.pop()
        return list(map(lambda x: x[0], final_result))
