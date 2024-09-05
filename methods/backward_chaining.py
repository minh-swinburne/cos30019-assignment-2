import sys, os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from syntax import *
from horn import check_horn_kb, check_horn_query


class BackwardChaining:
    """
    The class to represent a Backward Chaining Solver.
    Backward chaining is a simple inference algorithm that works by recursively applying Modus Ponens. It starts with the query and recursively tries to prove the query by proving its antecedents.
    Backward chaining is sound and complete for Horn clauses.
    
    ### Attributes:
        - kb (Conjunction): The knowledge base.
        - query (Symbol): The query to be evaluated.
    
    ### Methods:
        - solve(): Solve the query using backward chaining.
        - prove(goal: Symbol, chain: list[Symbol], visited: set[Symbol]): Recursively prove the goal by proving its antecedents.
    """
    def __init__(self, kb: Conjunction, query: Symbol):
        self.kb = kb
        self.query = query
        check_horn_kb(self.kb)
        check_horn_query(self.query)

    def solve(self):
        if isinstance(self.kb, Symbol):
            if self.kb == self.query:
                return {
                    "entails": True,
                    "message": self.query.name
                }
            else:
                return { "entails": False }
        if isinstance(self.kb, Conjunction):
            if self.query in self.kb.args:
                return {
                    "entails": True,
                    "message": self.query.name
                }
                
        solution_found, chain = self.prove(self.query, [], set())
        if solution_found:
            return {
                "entails": True,
                "message": ', '.join([symbol.name for symbol in chain])
            }
        else:
            return { "entails": False }

    def prove(self, goal:Symbol, chain:list[Symbol], visited:set[Symbol]):
        # print(goal, chain, visited, end=" => ")
        visited.add(goal)
        
        clauses = self.kb.args if isinstance(self.kb, Conjunction) else [self.kb]
        # Check if the goal is a fact in the KB
        for clause in clauses:
            if isinstance(clause, Symbol) and clause == goal:
                # print()
                chain.append(goal)
                return True, chain
            # Check if the goal can be derived from implications in the KB
            if isinstance(clause, Implication) and clause.consequent == goal:
                all_true = True
                subgoals = clause.antecedent.args if isinstance(clause.antecedent, Conjunction) else [clause.antecedent]
                # print(subgoals)
                for subgoal in subgoals:
                    if subgoal in chain:
                        continue
                    if subgoal in visited:
                        all_true = False
                        break
                    established, chain = self.prove(subgoal, chain, visited)
                    if not established:
                        all_true = False
                        break
                if all_true:
                    chain.append(goal)
                    return True, chain
        return False, chain
