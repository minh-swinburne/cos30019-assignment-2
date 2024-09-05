from enum import Enum

class Connective(Enum):
    """
    This enum class represents the connectives used in propositional logic.

    ### Values:
        - NEGATION: The NOT connective
        - CONJUNCTION: The AND connective
        - DISJUNCTION: The OR connective
        - IMPLICATION: The IF connective
        - BICONDITIONAL: The IFF connective
    """
    NEGATION = "~"
    CONJUNCTION = "&"
    DISJUNCTION = "||"
    IMPLICATION = "=>"
    BICONDITIONAL = "<=>"
    