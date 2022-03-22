from typing import List

from preprocessor import Preprocessor

class QueryParser:
    '''
    Parser class that in charge of parsing the query into
    abstract syntax tree.
    Attributes:
    preprocessor (Preprocessor): A class that handle to preprocess
    the tokens in the query
    '''

    def __init__(self):
        self.preprocessor = Preprocessor()

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

        # Parse each query using shunting yard algorithm
        for sentence in sentences:
            tokens = list(map(self.preprocessor.preprocess_word, sentence.split()))
            parsed_queries.append(tokens)

        return parsed_queries
