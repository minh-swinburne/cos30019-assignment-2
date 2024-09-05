import sys, os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from syntax import *
from cnf import to_cnf


class DPLL:
    """
    The class to represent a DPLL Solver.
    DPLL is a sound and complete inference algorithm that works by recursively assigning truth values to symbols. It starts with the CNF of the KB and the negation of the query, and recursively applies unit propagation and pure literal elimination to derive new clauses until a contradiction is found.
    
    ### Attributes:
        - kb (Conjunction): The knowledge base.
        - query (Symbol): The query to be evaluated.
        - clauses (set): The set of clauses.
        
    ### Methods:
        - initialize_clauses(): Initialize the set of clauses.
        - solve(): Solve the query using DPLL.
        - dpll(clauses: set): Recursively apply DPLL algorithm.
        - is_literal(clause: Sentence): Check if a clause is a literal (either a symbol or the negation of a symbol).
        - contains_literal(literal: Symbol|Negation, clause: Sentence): Check if a clause is or contains a literal.
        - unit_propagate(literal: Symbol|Negation, clauses: set): Apply unit propagation and return modified clauses set.
        - is_pure_literal(literal: Symbol|Negation, clauses: set): Check if a literal is pure, meaning that only either itself or its negation (not both) appears in the clauses set.
        - find_pure_literals(clauses: set): Find all pure literals in a set of clauses.
        - pure_literal_assign(literal: Symbol|Negation, clauses: set): Assign a truth value to a pure literal.
    """
    def __init__(self, kb: Conjunction, query: Symbol):
        self.kb = kb
        self.query = query
        self.clauses = self.initialize_clauses()

    def initialize_clauses(self):
        kb_cnf = to_cnf(self.kb)
        query_negated = to_cnf(self.query.negate())
        combined_clauses = Conjunction(kb_cnf, query_negated)
        return {clause for clause in combined_clauses.args}

    def solve(self):
        negation_satisfied = self.dpll(self.clauses)
        if negation_satisfied:
            return { "entails": False }
        else: # Negation of the query is unsatisfiable
            return {
                "entails": True # The KB entails the query
            }

    def dpll(self, clauses:set[Sentence]):
        # Unit propagation
        unit_clauses = {clause for clause in clauses if self.is_literal(clause)}
        while unit_clauses:
            for unit_clause in unit_clauses:
                clauses = self.unit_propagate(unit_clause, clauses)
            unit_clauses = {clause for clause in clauses if self.is_literal(clause)}
            
        # Pure literal elimination
        pure_literals = self.find_pure_literals(clauses)
        for literal in pure_literals:
            clauses = self.pure_literal_assign(literal, clauses)
        
        # Stopping conditions
        if not clauses:
            return True
        if any(clause is None for clause in clauses):
            # Clauses contain an empty clause, which means the KB ^ ~Q is unsatisfiable
            return False
        
        # DPLL recursion
        literal = next(iter(clauses)).symbols().pop()
        return self.dpll(clauses.union({literal})) or self.dpll(clauses.union({literal.negate()}))
        
    def is_literal(self, clause:Sentence) -> bool:
        if isinstance(clause, Symbol):
            return True
        return isinstance(clause, Negation) and isinstance(clause.arg, Symbol)
    
    def contains_literal(self, literal:Symbol|Negation, clause:Sentence) -> bool:
        if literal == clause:
            return True
        if isinstance(clause, CommutativeSentence):
            return any(literal == arg for arg in clause.args)
        return False
    
    def unit_propagate(self, literal:Symbol|Negation, clauses:set[Sentence]) -> set[Sentence]:
        new_clauses = set()
        for clause in clauses:
            if self.contains_literal(literal, clause):
                continue
            if self.contains_literal(literal.negate(), clause):
                if isinstance(clause, Disjunction):
                    args = [arg for arg in clause.args if arg != literal.negate()]
                    # print("ARGS", args)
                    if len(args) > 1:
                        new_clause = Disjunction(*args)
                    elif len(args) == 1:
                        new_clause = args[0]
                    else:
                        new_clause = None
                    new_clauses.add(new_clause)
                elif clause == literal.negate():
                    new_clauses.add(None)
                else:
                    new_clauses.add(clause)
            else:
                new_clauses.add(clause)
        return new_clauses
    
    def is_pure_literal(self, literal:Symbol|Negation, clauses:set[Sentence]) -> bool:
        positive = any(self.contains_literal(literal, clause) for clause in clauses)
        negative = any(self.contains_literal(literal.negate(), clause) for clause in clauses)
        return positive != negative
    
    def find_pure_literals(self, clauses:set[Sentence]) -> set[Symbol|Negation]:
        pure_literals = set()
        for clause in clauses:
            if clause is None:
                continue
            for symbol in clause.symbols():
                if self.is_pure_literal(symbol, clauses):
                    pure_literals.add(symbol)
        return pure_literals
    
    def pure_literal_assign(self, literal:Symbol|Negation, clauses:set[Sentence]) -> set[Sentence]:
        return set([clause for clause in clauses if not self.contains_literal(literal, clause)])
