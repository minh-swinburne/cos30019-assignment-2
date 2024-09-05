from .connective import Connective
from .sentence import Sentence
from .symbol import Symbol
from .commutative import CommutativeSentence


class Disjunction(CommutativeSentence):
    """
    This class represents a disjunction sentence.
    
    ### Attributes:
        - args(Sentence): The arguments of the disjunction
        
    ### Methods:
        - negate(): Returns the negation of the disjunction
        - evaluate(model:dict[Symbol, bool]): Evaluates the disjunction given a model
    """
    def __init__(self, *args:Sentence):
        flattened_args = []
        for arg in args:
            if isinstance(arg, Disjunction):
                flattened_args.extend(arg.args)
            else:
                flattened_args.append(arg)
        super().__init__(Connective.DISJUNCTION, *flattened_args)

    def negate(self) -> Sentence:
        from .conjunction import Conjunction
        return Conjunction(*[arg.negate() for arg in self.args])

    def evaluate(self, model:dict[Symbol, bool]) -> bool:
        """
        Evaluates the disjunction given a model. Returns True if any argument is True, False otherwise.

        ### Args:
            - model (dict[Symbol, bool]): The model to evaluate the conjunction

        ### Returns:
            - bool: The result of the evaluation
        """
        values = [arg.evaluate(model) for arg in self.args]
        if None in values:
            return None
        return any(values)