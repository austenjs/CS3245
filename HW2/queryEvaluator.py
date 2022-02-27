from typing import List

class QueryEvaluator:
    '''
    Evaluator class that in charge of evalauting the parsed
    queries.
    '''

    def _is_operator(self, token) -> bool:
        '''
        Take a token and specify whether it is an operator or not.

        Argument:
        token (str): A token

        Return:
        A boolean denoting whether the token is an operator or not.
        '''
        return token == 'AND' or token == 'OR'

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
                argument1, argument2 = stack.pop(), stack.pop()
                stack.append('({} {} {})'.format(argument1, token, argument2))
            elif token == 'NOT NOT':
                # Double Negation
                continue
            else:
                stack.append(token)
        if len(stack) > 1:
            print('Error in Evaluation')
        return stack.pop()
