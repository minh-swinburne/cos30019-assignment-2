"""
This module contains functions to check if a given knowledge base is in Horn form and to check if a given query is in Horn form. Warning messages are printed if the knowledge base or query is not in Horn form.

The Horn form is a restricted form of first-order logic that is used in the resolution algorithm. In Horn form, each clause has at most one positive literal. This restriction allows for efficient algorithms to be used to solve the knowledge base.

### Functions:
    - check_horn_query(query: Sentence) -> bool: Check if the query is in Horn form.
    - check_horn_kb(kb: Conjunction) -> bool: Check if the knowledge base is in Horn form.
    - _is_horn_form(clause: Sentence) -> bool: Check if a clause is in Horn form.
"""
from syntax import *


def check_horn_query(query: Sentence) -> bool:
    if not isinstance(query, Symbol):
        print("Warning: Query is not a symbol. The algorithm may not function correctly.")
        return False
    return True


def check_horn_kb(kb: Conjunction) -> bool:
    if not all(_is_horn_form(clause) for clause in kb.args) if isinstance(kb, Conjunction) else not _is_horn_form(kb):
        # print(kb.args)
        print("Warning: Knowledge base is not in Horn form. The algorithm may not function correctly.")
        return False
    return True
    
    
def _is_horn_form(clause: Sentence) -> bool:
    if isinstance(clause, Symbol):
        return True
    if isinstance(clause, Negation) and isinstance(clause.arg, Symbol):
        return True
    if isinstance(clause, Disjunction):
        positive_symbols = [arg for arg in clause.args if isinstance(arg, Symbol)]
        return len(positive_symbols) <= 1 and \
            all(isinstance(arg, (Symbol, Negation)) for arg in clause.args)
    if isinstance(clause, Implication):
        if not isinstance(clause.consequent, Symbol):
            return False
        if isinstance(clause.antecedent, Symbol):
            return True
        if isinstance(clause.antecedent, Conjunction):
            return all(isinstance(arg, Symbol) for arg in clause.antecedent.args)
    # if isinstance(clause, Conjunction):
    #     return all(_is_horn_form(arg) for arg in clause.args)
    return False