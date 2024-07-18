from .sentence import *


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
        return Disjunction(*[arg.negate() for arg in self.args])

    def evaluate(self, model):
        values = [arg.evaluate(model) for arg in self.args]
        if None in values:
            return None
        return all(values)
            
    

class Disjunction(CommutativeSentence):
    def __init__(self, *args:Sentence):
        flattened_args = []
        for arg in args:
            if isinstance(arg, Disjunction):
                flattened_args.extend(arg.args)
            else:
                flattened_args.append(arg)
        super().__init__(Connective.DISJUNCTION, *flattened_args)

    def negate(self):
        return Conjunction(*[arg.negate() for arg in self.args])

    def evaluate(self, model):
        values = [arg.evaluate(model) for arg in self.args]
        if None in values:
            return None
        return any(values)
    

class Implication(Sentence):
    def __init__(self, antecedent:Sentence, consequent:Sentence):
        self.antecedent = antecedent
        self.consequent = consequent

    def __str__(self):
        return f"({self.antecedent} {Connective.IMPLICATION.value} {self.consequent})"

    def __hash__(self):
        return hash((self.antecedent, self.consequent))

    def negate(self):
        return Conjunction(self.antecedent, self.consequent.negate())

    def evaluate(self, model):
        return not self.antecedent.evaluate(model) or self.consequent.evaluate(model)
    

class Biconditional(CommutativeSentence):
    def __init__(self, *args:Sentence):
        if len(args) != 2:
            raise ValueError("Biconditional sentence must have exactly 2 arguments")
        super().__init__(Connective.BICONDITIONAL, *args)

    def negate(self):
        return Biconditional(self.args[0], self.args[1].negate())

    def evaluate(self, model):
        # args = list(self.args)
        # return Conjunction(Implication(args[0], args[1]), Implication(args[1], args[0]))
        values = [arg.evaluate(model) for arg in self.args]
        if None in values:
            return None
        return values[0] == values[1]