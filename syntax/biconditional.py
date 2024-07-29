from .connective import Connective
from .sentence import Sentence
from .commutative import CommutativeSentence


class Biconditional(CommutativeSentence):
    priority = 5
    
    def __init__(self, *args:Sentence):
        if len(args) != 2:
            raise ValueError("Biconditional sentence must have exactly 2 arguments")
        super().__init__(Connective.BICONDITIONAL, *args)

    def negate(self):
        arg_1, arg_2 = self.args
        return Biconditional(arg_1, arg_2.negate())

    def evaluate(self, model):
        # args = list(self.args)
        # return Conjunction(Implication(args[0], args[1]), Implication(args[1], args[0]))
        values = [arg.evaluate(model) for arg in self.args]
        if None in values:
            return None
        return values[0] == values[1]