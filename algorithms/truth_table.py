import sys, os
from itertools import product
from tabulate import tabulate

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from syntax import *
from parser import parse_kb_and_query


def solve(kb:Conjunction, query:Sentence):
    # Define symbols
    symbols = kb.symbols() | query.symbols()
    symbols = sorted(symbols)
    return check_all(kb, query, symbols, {symbol: None for symbol in symbols})
    
    
def check_all(kb:Conjunction, query:Sentence, symbols:set[str], model:dict):
    if not symbols:
        print(f"Model: {model}")
        print(f"KB: {kb.evaluate(model)}, Query: {query.evaluate(model)}")
        return kb.evaluate(model) == True if query.evaluate(model) == True else None
    else:
        symbol, *rest = symbols
        return any([
            check_all(kb, query, rest, {**model, symbol: True}),
            check_all(kb, query, rest, {**model, symbol: False})
        ])
    
    
if __name__ == "__main__":
    # file_name = 'test_genericKB.txt'
    file_name = 'test_HornKB.txt'
    kb, query = parse_kb_and_query(file_name)
    print(f"Knowledge Base: {kb}")
    print(f"Query: {query}")
    result = solve(kb, query)
    print(f"Result: {result}")