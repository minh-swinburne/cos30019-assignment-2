from .connective import Connective
from .sentence import Sentence
from .symbol import Symbol
from .commutative import CommutativeSentence


class Biconditional(CommutativeSentence):
    """
    This class represents a biconditional sentence. A biconditional sentence is a sentence that has a biconditional connective, meaning that the sentence is true if both arguments have the same truth value.

    ### Attributes:
        - args(Sentence): The arguments of the biconditional
    
    ### Methods:
        - negate(): Returns the negation of the biconditional
        - evaluate(model:dict[Symbol, bool]): Evaluates the biconditional given a model
    """
    def __init__(self, *args:Sentence):
        if len(args) != 2:
            raise ValueError("Biconditional sentence must have exactly 2 arguments")
        super().__init__(Connective.BICONDITIONAL, *args)

    def negate(self) -> Sentence:
        arg_1, arg_2 = self.args
        return Biconditional(arg_1, arg_2.negate())

    def evaluate(self, model:dict[Symbol, bool]) -> bool:
        """
        Evaluates the biconditional given a model. Returns True if both arguments have the same truth value, False otherwise.

        ### Args:
            - model (dict[Symbol, bool]): The model to evaluate the biconditional
            
        ### Returns:
            - bool: The result of the evaluation
        """
        values = [arg.evaluate(model) for arg in self.args]
        if None in values:
            return None
        return values[0] == values[1]