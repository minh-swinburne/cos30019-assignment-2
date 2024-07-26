from .connective import Connective
from .sentence import Sentence


class Implication(Sentence):
    """
    This class represents an implication sentence.
    
    ### Attributes:
        - antecedent(Sentence): The antecedent (left clause) of the implication
        - consequent(Sentence): The consequent (right clause) of the implication
    
    ### Methods:
        - negate(): Returns the negation of the implication
        - evaluate(model:Dict[str, bool]): Evaluates the implication given a model
    """
    def __init__(self, antecedent:Sentence, consequent:Sentence):
        self.antecedent = antecedent
        self.consequent = consequent

    def __str__(self):
        return f"({self.antecedent} {Connective.IMPLICATION.value} {self.consequent})"

    def negate(self):
        from .conjunction import Conjunction
        return Conjunction(self.antecedent, self.consequent.negate())

    def evaluate(self, model):
        return not self.antecedent.evaluate(model) or self.consequent.evaluate(model)
