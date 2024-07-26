from abc import abstractmethod
from enum import Enum

class Connective(Enum):
    NEGATION = "~"
    CONJUNCTION = "&"
    DISJUNCTION = "||"
    IMPLICATION = "=>"
    BICONDITIONAL = "<=>"

class Sentence:
    @abstractmethod
    def __str__(self):
        pass
    
    def __eq__(self, other:'Sentence'):
        if type(self) != type(other):
            return False
        if isinstance(self, Symbol):
            return self.name == other.name
        if isinstance(self, Negation):
            return self.arg == other.arg
        if isinstance(self, CommutativeSentence):
            return self.connective == other.connective and self.args == other.args
        if isinstance(self, Implication):
            return self.antecedent == other.antecedent and self.consequent == other.consequent
    
    @abstractmethod
    def negate(self):
        pass

    @abstractmethod
    def evaluate(self, model):
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
    def __init__(self, name:str):
        self.name = name

    def __str__(self):
        return self.name
    
    def negate(self):
        return Negation(self)

    def evaluate(self, model):
        if self.name not in model:
            return None
        return model[self.name] if self.name in model else False
    
    
class Negation(Sentence):
    """
    This class represents a negation sentence. It negates a sentence.

    ### Attributes:
        - arg(Sentence): The argument sentence to be negated
        
    ### Methods:
        - negate(): Returns the negation of the argument sentence
        - evaluate(model:Dict[str, bool]): Evaluates the negation of the argument sentence given a model
    """
    def __init__(self, arg:Sentence):
        self.arg = arg

    def __str__(self):
        return f"{Connective.NEGATION.value}{self.arg}"
    
    def negate(self):
        return self.arg

    def evaluate(self, model):
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

    @abstractmethod
    def evaluate(self, model):
        pass
    

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
    """
    This class represents an implication sentence.
    
    ### Attributes:
        - antecedent(Sentence): The antecedent (left clause) of the implication
        - consequent(Sentence): The consequent (right clause) of the implication
    
    ### Methods:
        - negate(): Returns the negation of the implication
        - evaluate(model:Dict[str, bool]): Evaluates the implication given a model
    """
    def __init__(self, antecedent:Sentence, consequent:Sentence):
        self.antecedent = antecedent
        self.consequent = consequent

    def __str__(self):
        return f"({self.antecedent} {Connective.IMPLICATION.value} {self.consequent})"

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