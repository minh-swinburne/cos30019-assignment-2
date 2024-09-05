import sys, os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from syntax import *
from horn import check_horn_kb, check_horn_query


class ForwardChaining:
    """
    The class to represent a Forward Chaining Solver.
    Forward chaining is a simple inference algorithm that works by repeatedly applying Modus Ponens. It starts with the symbols known to be true and iteratively adds symbols to the knowledge base.
    Forward chaining is sound and complete for Horn clauses.
    
    ### Attributes:
        - kb (Conjunction): The knowledge base.
        - query (Symbol): The query to be evaluated.
        
    ### Methods:
        - solve(): Solve the query using forward chaining.
    """
    def __init__(self, kb: Conjunction, query: Symbol):
        self.kb = kb
        self.query = query
        check_horn_kb(self.kb)
        check_horn_query(self.query)
    
    def solve(self):
        # Initialize inferred and count dictionaries
        inferred = {symbol: False for symbol in self.kb.symbols()}
        count = {}
        
        # Initialize the agenda with symbols known to be true
        if isinstance(self.kb, Symbol):
            agenda = [self.kb]
        elif isinstance(self.kb, Implication):
            agenda = []
            count[self.kb] = len(self.kb.antecedent.symbols())
        else: # Conjunction
            agenda = [symbol for symbol in self.kb.args if isinstance(symbol, Symbol)]
            for clause in self.kb.args:
                if isinstance(clause, Implication):
                    count[clause] = len(clause.antecedent.symbols())
            # print(count)
        agenda.sort(key=lambda x: x.name)
        # print(agenda)        
        
        chain:list[Symbol] = []  # Track the result of forward chaining
        
        while agenda:
            p = agenda.pop(0)
            chain.append(p)
            if p == self.query:
                return {
                    "entails": True,
                    "message": ', '.join([symbol.name for symbol in chain])
                }
            # print(p, agenda, inferred, chain)
            if not inferred[p]:
                inferred[p] = True
                for clause in self.kb.args if isinstance(self.kb, Conjunction) else [self.kb]:
                    if isinstance(clause, Implication):
                        if p in clause.antecedent.symbols():
                            # print(clause.antecedent.symbols())
                            count[clause] -= 1
                            if count[clause] == 0:
                                agenda.append(clause.consequent)
        
        return { "entails": False }
     