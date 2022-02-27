from queryParser import QueryParser
from queryEvaluator import QueryEvaluator

parser = QueryParser()
evaluator = QueryEvaluator()

queries = parser.parse_queries('validQueries.txt')
for query in queries:
    print(evaluator.evaluate(query))