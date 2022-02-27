import re
from typing import Generator, List

class QueryParser:
    '''
    Parser class that in charge of parsing the query into
    abstract syntax tree.
    '''

    def _tokenize(self, expression) -> Generator[str, None, None]:
        '''
        Take a query string and parsed it into tokens. The main difference
        with nltk tokenizer is that it treats '(' and ')' as a single token.

        Argument:
        expression (str): String to be parsed

        Return:
        A generator of tokens
        '''
        return (re.findall("NOT [a-zA-Z0-9]+|[()]|[a-zA-Z0-9]+", expression))

    def _is_operator(self, token) -> bool:
        '''
        Take a token and specify whether it is an operator or not.

        Argument:
        token (str): A token

        Return:
        A boolean denoting whether the token is an operator or not.
        '''
        return token == 'AND' or token == 'OR'

    def parse_queries(self, file_path) -> List[List[str]]:
        '''
        Take a queries file and answer each of the query.

        Argument:
        file_path (str): Path to file

        Return:
        A list where the i-th is a list that contains the parsing of
            the i-th query.
        '''
        with open(file_path, "r", encoding="utf8") as f:
            sentences = f.readlines()

        parsed_queries = []
        output_stack = []
        operator_stack = []

        # Parse each query using shunting yard algorithm
        for sentence in sentences:
            valid_query = True
            num_of_unmatched_brackets = 0
            is_previous_token = False
            for token in self._tokenize(sentence):
                if self._is_operator(token):
                    # Duplicate AND / OR
                    if is_previous_token:
                        valid_query = False
                        break

                    # Push the operators in operator stack with higher precedence
                    if token == 'AND':
                        while operator_stack and operator_stack[-1] == 'AND':
                            output_stack.append(operator_stack.pop())
                    elif token == 'OR':
                        while operator_stack and self._is_operator(operator_stack[-1]):
                            output_stack.append(operator_stack.pop())
                    operator_stack.append(token)
                    is_previous_token = True
                elif token == '(':
                    operator_stack.append(token)
                    num_of_unmatched_brackets += 1
                    is_previous_token = False
                elif token == ')':
                    # Empty Stack
                    if len(operator_stack) == 0:
                        valid_query = False
                        break

                    # Find '('
                    current = operator_stack.pop()
                    while current != '(':
                        output_stack.append(current)
                        try:
                            current = operator_stack.pop()
                        except: # No '(' in operator stack
                            valid_query = False
                            break
                    num_of_unmatched_brackets -= 1
                    is_previous_token = False
                else:
                    output_stack.append(token)
                    is_previous_token = False

            # Invalid Query
            if not valid_query or num_of_unmatched_brackets > 0:
                print('Invalid query: {}'.format(sentence))
                output_stack.clear()
                operator_stack.clear()
                continue

            # Empty operator stack
            while operator_stack:
                output_stack.append(operator_stack.pop())
            parsed_queries.append(output_stack.copy())
            output_stack.clear()

        return parsed_queries
