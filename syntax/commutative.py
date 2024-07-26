from abc import abstractmethod
from .connective import Connective
from .sentence import Sentence


class CommutativeSentence(Sentence):
    def __init__(self, connective:Connective, *args:Sentence):
        if len(args) < 2:
            raise ValueError(f"Commutative sentence {connective.name} must have at least 2 arguments")
        if connective == Connective.IMPLICATION or connective == Connective.NEGATION:
            raise ValueError(f"Connective {connective.name} is not commutative")
        self.connective = connective
        self.args = set(args)

    def __str__(self):
        return f"({f" {self.connective.value} ".join(map(str, self.args))})"
    
    def __eq__(self, other: Sentence):
        return super().__eq__(other) and self.args == other.args

    @abstractmethod
    def evaluate(self, model):
        pass