import sys, os
import itertools

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from syntax import *
from cnf import to_cnf

class Resolution:
    """
    The class to represent a Resolution Solver.
    Resolution is a sound and complete inference algorithm that works by refuting the negation of the query. It starts with the CNF of the KB and the negation of the query, and recursively applies the resolution rule to derive new clauses until a contradiction is found.
    
    ### Attributes:
        - kb (Conjunction): The knowledge base.
        - query (Symbol): The query to be evaluated.
        - clauses (set): The set of clauses.
        
    ### Methods:
        - initialize_clauses(): Initialize the set of clauses.
        - solve(): Solve the query using resolution.
        - resolve(clause1: Sentence, clause2: Sentence): Resolve two clauses. Return the resolvents.
    """
    def __init__(self, kb: Conjunction, query: Symbol):
        self.kb = kb
        self.query = query
        self.clauses = self.initialize_clauses()

    def initialize_clauses(self):
        # Convert KB to CNF
        kb_cnf = to_cnf(self.kb)
        # Negate the query and convert to CNF
        query_negated = to_cnf(self.query.negate())
        # Combine the KB and the negated query into a single set of clauses
        combined_clauses = Conjunction(kb_cnf, query_negated)
        # Flatten the conjunction into individual clauses
        # print(f"Combined Clauses: {combined_clauses}")
        return {clause for clause in combined_clauses.args}

    def solve(self):
        # print(f"Clauses: {self.clauses}")
        new_clauses = set()

        while True:
            pairs = itertools.combinations(self.clauses, 2)

            for (clause1, clause2) in pairs:
                resolvents = self.resolve(clause1, clause2)
                # print(f"Resolvents: {resolvents} - {clause1} - {clause2}")
                for resolvent in resolvents:
                    if resolvent is None:
                        return {
                            "entails": True
                        }
                    new_clauses.add(resolvent)

            if new_clauses.issubset(self.clauses):
                return { "entails": False }

            self.clauses = self.clauses.union(new_clauses)
    
    def resolve(self, clause1, clause2):
        resolvents = []
        literals1 = clause1.args if isinstance(clause1, Disjunction) else [clause1]
        literals2 = clause2.args if isinstance(clause2, Disjunction) else [clause2]

        for literal1, literal2 in itertools.product(literals1, literals2):
            if (isinstance(literal1, Negation) and literal1.arg == literal2) or \
                (isinstance(literal2, Negation) and literal2.arg == literal1):
                # print(f"Resolving {clause1} and {clause2} on {literal1} (from {literals1}) and {literal2} (from {literals2})")
                args = [l for l in literals1 if l != literal1] + [l for l in literals2 if l != literal2]
                # print(args)
                if len(args) > 1: 
                    # Create a new disjunction if there are more than one literals
                    new_clause = Disjunction(*args)
                elif len(args) == 1: 
                    # If there is only one literal, return the literal
                    new_clause = args[0]
                else: 
                    # If there are no literals, return an empty clause, meaning the set of clauses is unsatisfiable
                    new_clause = None
                # print(f"New Clause: {new_clause}")
                resolvents.append(new_clause)

        return resolvents
