from queryParser import QueryParser

parser = QueryParser()

print('Invalid Queries')
parser.parse_queries('invalidQueries.txt')

print('Valid Queries')
print(parser.parse_queries('validQueries.txt'))
