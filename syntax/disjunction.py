from .connective import Connective
from .sentence import Sentence
from .commutative import CommutativeSentence


class Disjunction(CommutativeSentence):
    priority = 3
    
    def __init__(self, *args:Sentence):
        flattened_args = []
        for arg in args:
            if isinstance(arg, Disjunction):
                flattened_args.extend(arg.args)
            else:
                flattened_args.append(arg)
        super().__init__(Connective.DISJUNCTION, *flattened_args)

    def negate(self):
        from .conjunction import Conjunction
        return Conjunction(*[arg.negate() for arg in self.args])

    def evaluate(self, model):
        values = [arg.evaluate(model) for arg in self.args]
        if None in values:
            return None
        return any(values)