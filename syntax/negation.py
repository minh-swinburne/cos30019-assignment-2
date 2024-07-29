from __future__ import annotations
from .connective import Connective
from .sentence import Sentence


class Negation(Sentence):
    """
    This class represents a negation sentence. It negates a sentence.

    ### Attributes:
        - arg(Sentence): The argument sentence to be negated
        
    ### Methods:
        - negate(): Returns the negation of the argument sentence
        - evaluate(model:Dict[str, bool]): Evaluates the negation of the argument sentence given a model
    """
    priority = 1
    
    def __init__(self, arg:Sentence):
        self.arg = arg

    def __repr__(self):
        from .symbol import Symbol
        if isinstance(self.arg, Symbol):
            return f"{Connective.NEGATION.value}{self.arg}"
        return f"{Connective.NEGATION.value}({self.arg})"
    
    def __hash__(self):
        return hash(self.arg)
    
    def __eq__(self, other:Negation):
        if super().__eq__(other):
            return self.arg == other.arg
        return False
    
    def negate(self) -> Sentence:
        return self.arg

    def evaluate(self, model) -> bool:
        result = self.arg.evaluate(model)
        if result is None:
            return None
        return not result
    
    def symbols(self) -> set[str]:
        return self.arg.symbols()