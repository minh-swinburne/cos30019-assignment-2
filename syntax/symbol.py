from .sentence import Sentence, Negation


class Symbol(Sentence): # atomic sentence
    def __init__(self, name:str):
        self.name = name

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)
    
    def negate(self):
        return Negation(self)

    def evaluate(self, model):
        if self.name not in model:
            return None
        return model[self.name] if self.name in model else False