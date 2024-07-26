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
    def __init__(self, arg:Sentence):
        self.arg = arg

    def __str__(self):
        return f"{Connective.NEGATION.value}{self.arg}"
    
    def __eq__(self, other:Sentence):
        return super().__eq__(other) and self.arg == other.arg
    
    def negate(self) -> Sentence:
        return self.arg

    def evaluate(self, model) -> bool:
        return not self.arg.evaluate(model)