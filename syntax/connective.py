from enum import Enum

class Connective(Enum):
    NEGATION = "~"
    CONJUNCTION = "&"
    DISJUNCTION = "||"
    IMPLICATION = "=>"
    BICONDITIONAL = "<=>"
    

if __name__ == "__main__":
    print(Connective.NEGATION.value)
    print(Connective.CONJUNCTION)
    print(Connective.DISJUNCTION.name)
    print(Connective.IMPLICATION > Connective.BICONDITIONAL)