from enum import Enum

class Connective(Enum):
    NEGATION = "~"
    CONJUNCTION = "&"
    DISJUNCTION = "||"
    IMPLICATION = "=>"
    BICONDITIONAL = "<=>"