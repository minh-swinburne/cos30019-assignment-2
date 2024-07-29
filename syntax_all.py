from __future__ import annotations
from abc import abstractmethod
from enum import Enum

class Connective(Enum):
    NEGATION = "~"
    CONJUNCTION = "&"
    DISJUNCTION = "||"
    IMPLICATION = "=>"
    BICONDITIONAL = "<=>"

class Sentence:
    """
    This class represents a sentence in propositional logic. It is an abstract class that is inherited by other classes.
    
    ### Methods:
        - __repr__() <<abstract>>: Returns a string representation of the sentence
        - __hash__() <<abstract>>: Returns the hash value of the sentence
        - __eq__(other:Sentence): Compares the hash values of two sentences
        - negate() <<abstract>>: Returns the negation of the sentence
        - evaluate(model:Dict[str, bool]) <<abstract>>: Evaluates the sentence given
    """
    @abstractmethod
    def __repr__(self):
        pass
    
    @abstractmethod
    def __hash__(self):
        pass
    
    @abstractmethod
    def __eq__(self, other:Sentence):
        return type(self) == type(other)
    
    @abstractmethod
    def negate(self) -> Sentence:
        pass

    @abstractmethod
    def evaluate(self, model) -> bool:
        pass
    
    @abstractmethod
    def symbols(self) -> set[str]:
        pass


class Symbol(Sentence): # atomic sentence
    """
    This class represents a symbol (atomic sentence).

    ### Attributes:
        - name(str): The name of the symbol
        
    ### Methods:
        - negate(): Returns the negation of the symbol
        - evaluate(model:Dict[str, bool]): Evaluates the symbol given a model
    """
    priority = 0
    
    def __init__(self, name:str):
        self.name = name

    def __repr__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other:Symbol):
        return super().__eq__(other) and self.name == other.name
    
    def negate(self) -> Sentence:
        return Negation(self)

    def evaluate(self, model:dict[str, bool]) -> bool:
        if self.name not in model:
            return None
        return model[self.name] if self.name in model else None
    
    def symbols(self) -> set[str]:
        return {self.name}
    
    
class Negation(Sentence):
    """
    This class represents a negation sentence. It negates a sentence.

    ### Attributes:
        - arg(Sentence): The argument sentence to be negated
        
    ### Methods:
        - negate(): Returns the negation of the argument sentence
        - evaluate(model:Dict[str, bool]): Evaluates the negation of the argument sentence given a model
    """
    priority = 1
    
    def __init__(self, arg:Sentence):
        self.arg = arg

    def __repr__(self):
        if isinstance(self.arg, Symbol):
            return f"{Connective.NEGATION.value}{self.arg}"
        return f"{Connective.NEGATION.value}({self.arg})"
    
    def __hash__(self):
        return hash(self.arg)
    
    def __eq__(self, other:Negation):
        if super().__eq__(other):
            return self.arg == other.arg
        return False
    
    def negate(self) -> Sentence:
        return self.arg

    def evaluate(self, model) -> bool:
        return not self.arg.evaluate(model)
    
    def symbols(self) -> set[str]:
        return self.arg.symbols()
    

class CommutativeSentence(Sentence):
    def __init__(self, connective:Connective, *args:Sentence):
        if len(args) < 2:
            raise ValueError(f"Commutative sentence {connective.name} must have at least 2 arguments")
        if connective == Connective.IMPLICATION or connective == Connective.NEGATION:
            raise ValueError(f"Connective {connective.name} is not commutative")
        self.connective = connective
        self.args = frozenset(args)

    def __repr__(self):
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
    def evaluate(self, model):
        pass
    

class Conjunction(CommutativeSentence):
    priority = 2
    
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
        return Conjunction(*[arg.negate() for arg in self.args])

    def evaluate(self, model):
        values = [arg.evaluate(model) for arg in self.args]
        if None in values:
            return None
        return any(values)
    

class Implication(Sentence):
    """
    This class represents an implication sentence.
    
    ### Attributes:
        - antecedent(Sentence): The antecedent (left clause) of the implication
        - consequent(Sentence): The consequent (right clause) of the implication
    
    ### Methods:
        - negate(): Returns the negation of the implication
        - evaluate(model:Dict[str, bool]): Evaluates the implication given a model
    """
    priority = 4
    
    def __init__(self, antecedent:Sentence, consequent:Sentence):
        self.antecedent = antecedent
        self.consequent = consequent

    def __repr__(self):
        return f"({self.antecedent} {Connective.IMPLICATION.value} {self.consequent})"
        
    def __hash__(self):
        return hash((self.antecedent, self.consequent))
    
    def __eq__(self, other:Implication):
        if super().__eq__(other):
            return self.antecedent == other.antecedent and self.consequent == other.consequent
        return False

    def negate(self):
        return Conjunction(self.antecedent, self.consequent.negate())

    def evaluate(self, model):
        antedecent = self.antecedent.evaluate(model)
        consequent = self.consequent.evaluate(model)
        if antedecent is None or consequent is None:
            return None
        return not antedecent or consequent
    
    def symbols(self):
        return self.antecedent.symbols() | self.consequent.symbols()
    

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


if __name__ == "__main__":
    p = Symbol("p")
    q = Symbol("q")
    r = Symbol("r")
    model = {'p': True, 'q': False, 'r': None}
    print(f"p: {p} ({p.evaluate(model)})")
    print(f"q: {q} ({q.evaluate(model)})")
    print(f"r: {r} ({r.evaluate(model)})")
    print(f"~p: {p.negate()} ({p.negate().evaluate(model)})")
    print(f"~(~q): {q.negate().negate()} ({q.negate().negate().evaluate(model)})")
    print(f"p & q: {Conjunction(p, q)} ({Conjunction(p, q).evaluate(model)})")
    print(f"p || q: {Disjunction(p, q)} ({Disjunction(p, q).evaluate(model)})")
    print(f"p => q: {Implication(p, q)} ({Implication(p, q).evaluate(model)})")
    print(f"~p => ~q: {Implication(p.negate(), q.negate())} ({Implication(p.negate(), q.negate()).evaluate(model)})")
    print(f"q => p: {Implication(q, p)} ({Implication(q, p).evaluate(model)})")
    print(f"~q => ~p: {Implication(q.negate(), p.negate())} ({Implication(q.negate(), p.negate()).evaluate(model)})")
    print(f"p <=> q: {Biconditional(p, q)} ({Biconditional(p, q).evaluate(model)})")
    print(f"p & q & r: {Conjunction(p, q, r)} ({Conjunction(p, q, r).evaluate(model)})")
    print(f"p || q || r: {Disjunction(p, q, r)} ({Disjunction(p, q, r).evaluate(model)})")
    print(f"p => (q => r): {Implication(p, Implication(q, r))} ({Implication(p, Implication(q, r)).evaluate(model)})")
    print(f"~(p & q): {Conjunction(p, q).negate()} ({Conjunction(p, q).negate().evaluate(model)})")
    print(f"~(p || q): {Disjunction(p, q).negate()} ({Disjunction(p, q).negate().evaluate(model)})")
    print(f"~(p => q): {Implication(p, q).negate()} ({Implication(p, q).negate().evaluate(model)})")
    print(f"~(p <=> q): {Biconditional(p, q).negate()} ({Biconditional(p, q).negate().evaluate(model)})")
    print(f"~(p & q & r): {Conjunction(p, q, r).negate()} ({Conjunction(p, q, r).negate().evaluate(model)})")
    print(f"~(p || q || r): {Disjunction(p, q, r).negate()} ({Disjunction(p, q, r).negate().evaluate(model)})")
    print(f"~(p => (q => r)): {Implication(p, Implication(q, r)).negate()} ({Implication(p, Implication(q, r)).negate().evaluate(model)})")