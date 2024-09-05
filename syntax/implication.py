from __future__ import annotations
from .connective import Connective
from .sentence import Sentence
from .symbol import Symbol


class Implication(Sentence):
    """
    This class represents an implication sentence.
    
    ### Attributes:
        - antecedent(Sentence): The antecedent (left clause) of the implication
        - consequent(Sentence): The consequent (right clause) of the implication
    
    ### Methods:
        - negate(): Returns the negation of the implication
        - evaluate(model:dict[Symbol, bool]): Evaluates the implication given a model
        - symbols(): Returns the set of symbols in the implication
    """
    def __init__(self, antecedent:Sentence, consequent:Sentence):
        self.antecedent = antecedent
        self.consequent = consequent

    def __repr__(self):
        from .negation import Negation
        antecedent = self.antecedent if isinstance(self.antecedent, (Symbol, Negation)) else f"({self.antecedent})"
        consequent = self.consequent if isinstance(self.consequent, (Symbol, Negation)) else f"({self.consequent})"
        return f"{antecedent} {Connective.IMPLICATION.value} {consequent}"
        
    def __hash__(self):
        return hash((self.antecedent, self.consequent))
    
    def __eq__(self, other:Implication):
        if super().__eq__(other):
            return self.antecedent == other.antecedent and self.consequent == other.consequent
        return False

    def negate(self) -> Sentence:
        from .conjunction import Conjunction
        return Conjunction(self.antecedent, self.consequent.negate())

    def evaluate(self, model:dict[Symbol, bool]) -> bool:
        """
        Evaluates the implication given a model. Returns True if the antecedent is False or the consequent is True, False otherwise.

        ### Args:
            - model (dict[Symbol, bool]): The model to evaluate the implication
            
        ### Returns:
            - bool: The result of the evaluation
        """
        antedecent = self.antecedent.evaluate(model)
        consequent = self.consequent.evaluate(model)
        if antedecent is None or consequent is None:
            return None
        return not antedecent or consequent
    
    def symbols(self) -> set[Symbol]:
        return self.antecedent.symbols() | self.consequent.symbols()
