from __future__ import annotations
from abc import abstractmethod
from .connective import Connective
from .sentence import Sentence
from .symbol import Symbol


class CommutativeSentence(Sentence):
    """
    This class represents a commutative sentence. A commutative sentence is a sentence that has a connective that is commutative, meaning that the order of the arguments does not matter.
    A commutative sentence must have at least 2 arguments.

    ### Attributes:
        - connective(Connective): The connective of the sentence
        - args(set[Sentence]): The arguments of the sentence
        
    ### Methods:
        - evaluate(model:dict[Symbol, bool]): Evaluates the sentence given a model
        - symbols(): Returns the set of symbols in the sentence
    """
    def __init__(self, connective:Connective, *args:Sentence):
        if len(args) < 2:
            raise ValueError(f"Commutative sentence {connective.name} must have at least 2 arguments")
        if connective == Connective.IMPLICATION or connective == Connective.NEGATION:
            raise ValueError(f"Connective {connective.name} is not commutative")
        self.connective = connective
        self.args = frozenset(args)

    def __repr__(self):
        from .symbol import Symbol
        from .negation import Negation
        arg_strs = []
        args = list(self.args)
        args.sort(key=lambda x: str(x))
        for arg in args:
            if not isinstance(arg, (Symbol, Negation)):
                arg_strs.append(f"({arg})")
            else:
                arg_strs.append(str(arg))
        return f" {self.connective.value} ".join(arg_strs)
        
    def __hash__(self):
        return hash(self.args)
    
    def __eq__(self, other: CommutativeSentence):
        if super().__eq__(other):
            return self.args == other.args
        return False

    @abstractmethod
    def evaluate(self, model) -> bool:
        pass
    
    def symbols(self) -> set[Symbol]:
        symbols = set()
        for arg in self.args:
            symbols |= arg.symbols()
        return symbols