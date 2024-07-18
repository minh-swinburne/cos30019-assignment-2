from abc import abstractmethod
from .connective import Connective


class Sentence:
    @abstractmethod
    def __str__(self):
        pass
    
    @abstractmethod
    def __hash__(self):
        pass
    
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
    
    @abstractmethod
    def negate(self):
        pass

    @abstractmethod
    def evaluate(self, model):
        pass


class Negation(Sentence):
    def __init__(self, arg:Sentence):
        self.arg = arg

    def __str__(self):
        return f"{Connective.NEGATION.value}{self.arg}"

    def __hash__(self):
        return self.arg.__hash__()
    
    def negate(self) -> Sentence:
        return self.arg

    def evaluate(self, model) -> bool:
        return not self.arg.evaluate(model)
    
    
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

    def __hash__(self):
        return hash((self.connective, self.args))

    @abstractmethod
    def evaluate(self, model):
        pass