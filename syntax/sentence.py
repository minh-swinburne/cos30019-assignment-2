from __future__ import annotations
from abc import abstractmethod


class Sentence:
    """
    This class represents a sentence in propositional logic. It is an abstract class that is inherited by other classes.
    
    ### Methods:
        - __str__() <<abstract>>: Returns a string representation of the sentence
        - __hash__() <<abstract>>: Returns the hash value of the sentence
        - __eq__(other:Sentence): Compares the hash values of two sentences
        - negate() <<abstract>>: Returns the negation of the sentence
        - evaluate(model:Dict[str, bool]) <<abstract>>: Evaluates the sentence given
    """
    @abstractmethod
    def __str__(self):
        pass
    
    # @abstractmethod
    # def __hash__(self):
    #     pass
    
    @abstractmethod
    def __eq__(self, other:Sentence):
        return type(self) != type(other)
    
    @abstractmethod
    def negate(self):
        pass

    @abstractmethod
    def evaluate(self, model):
        pass
