from .connective import Connective
from .sentence import Sentence
from .commutative import CommutativeSentence


class Conjunction(CommutativeSentence):
    def __init__(self, *args:Sentence):
        flattened_args = []
        for arg in args:
            if isinstance(arg, Conjunction):
                flattened_args.extend(arg.args)
            else:
                flattened_args.append(arg)
        super().__init__(Connective.CONJUNCTION, *flattened_args)

    def negate(self):
        from .disjunction import Disjunction
        return Disjunction(*[arg.negate() for arg in self.args])

    def evaluate(self, model):
        values = [arg.evaluate(model) for arg in self.args]
        if None in values:
            return None
        return all(values)