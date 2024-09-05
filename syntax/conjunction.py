from .connective import Connective
from .sentence import Sentence
from .symbol import Symbol
from .commutative import CommutativeSentence


class Conjunction(CommutativeSentence):
    """
    This class represents a conjunction sentence.

    ### Attributes:
        - args(Sentence): The arguments of the conjunction
        
    ### Methods:
        - negate(): Returns the negation of the conjunction
        - evaluate(model:dict[Symbol, bool]): Evaluates the conjunction given a model
    """
    def __init__(self, *args:Sentence):
        flattened_args = []
        for arg in args:
            if isinstance(arg, Conjunction):
                flattened_args.extend(arg.args)
            else:
                flattened_args.append(arg)
        super().__init__(Connective.CONJUNCTION, *flattened_args)

    def negate(self) -> Sentence:
        from .disjunction import Disjunction
        return Disjunction(*[arg.negate() for arg in self.args])

    def evaluate(self, model:dict[Symbol, bool]) -> bool:
        """
        Evaluates the conjunction given a model. Returns True if all arguments are True, False otherwise.

        ### Args:
            - model (dict[Symbol, bool]): The model to evaluate the conjunction
            
        ### Returns:
            - bool: The result of the evaluation
        """
        values = [arg.evaluate(model) for arg in self.args]
        if None in values:
            return None
        return all(values)