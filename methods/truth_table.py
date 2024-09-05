import sys, os
# from itertools import product
from tabulate import tabulate

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from syntax import *


class TruthTable:
    """
    The class to represent a Truth Table Solver.
    The truth table method is a sound and complete inference algorithm that works by evaluating all possible models. It starts with the symbols in the knowledge base and the query, and recursively checks all models.
    
    ### Attributes:
        - kb (Conjunction): The knowledge base.
        - query (Sentence): The query to be evaluated.
        - symbols (set[Symbol]): The set of symbols in the knowledge base and the query.
        - table (list): The truth table.
        - valid_models_count (int): The number of valid models.
        
    ### Methods:
        - solve(): Solve the truth table.
        - check_all(kb: Conjunction, query: Sentence, symbols: set[Symbol], model: dict): Recursively check all models.
        - generate_table(): Generate the truth table.
    """
    def __init__(self, kb: Conjunction, query: Sentence):
        self.kb = kb
        self.query = query
        self.symbols = sorted(kb.symbols() | query.symbols(), key=lambda x: x.name)
        self.table = []
        self.valid_models_count = 0

    def solve(self):
        model = {}
        valid = self.check_all(self.kb, self.query, self.symbols, model)
        if valid and self.valid_models_count > 0:
            return {
                "entails": True,
                "message": self.valid_models_count
            }
            # print(f'YES: {self.valid_models_count}')
        else:
            return { "entails": False }

    def check_all(self, kb: Conjunction, query: Sentence, symbols: set[Symbol], model: dict):
        if not symbols:
            kb_eval = kb.evaluate(model)
            query_eval = query.evaluate(model)
            self.table.append((model.copy(), kb_eval, query_eval))
            if kb_eval and query_eval:
                self.valid_models_count += 1
            return query_eval if kb_eval else True
        else:
            symbol, *rest = symbols
            return all([
                self.check_all(kb, query, rest, {**model, symbol: True}),
                self.check_all(kb, query, rest, {**model, symbol: False})
            ])

    def generate_table(self):
        if not self.table:
            self.solve()
        headers = [symbol for symbol in self.symbols] 
        headers += ['KB: ' + str(self.kb), 'Query: ' + str(self.query)]
        rows = []
        for model, kb_eval, query_eval in self.table:
            row = [str(model[symbol]) for symbol in self.symbols] + [str(kb_eval), str(query_eval)]
            rows.append(row)
        # print(len(headers), len(rows[0]))
        return tabulate(rows, headers, tablefmt='fancy_grid')
     