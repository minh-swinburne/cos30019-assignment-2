from __future__ import annotations
from .sentence import Sentence

class Symbol(Sentence): # atomic sentence
    """
    This class represents a symbol (atomic sentence).

    ### Attributes:
        - name(str): The name of the symbol
        
    ### Methods:
        - negate(): Returns the negation of the symbol
        - evaluate(model:dict[Symbol, bool]): Evaluates the symbol given a model
        - symbols(): Returns the set of symbols in the symbol
    """
    def __init__(self, name:str):
        self.name = name

    def __repr__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other:Symbol):
        return super().__eq__(other) and self.name == other.name
    
    def negate(self) -> Sentence:
        from .negation import Negation
        return Negation(self)

    def evaluate(self, model:dict[Symbol, bool]) -> bool:
        return model[self] if self in model else None
    
    def symbols(self) -> set[Symbol]:
        return {self}
    
    