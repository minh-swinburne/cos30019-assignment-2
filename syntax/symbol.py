from .sentence import Sentence

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

    def __eq__(self, other:Sentence):
        return super().__eq__(other) and self.name == other.name
    
    def negate(self) -> Sentence:
        from .negation import Negation
        return Negation(self)

    def evaluate(self, model:dict[str, bool]) -> bool:
        if self.name not in model:
            return None
        return model[self.name] if self.name in model else False