from syntax import *

def to_cnf(sentence: Sentence):
    # Convert to NNF first
    nnf = to_nnf(sentence)
    # Then convert NNF to CNF
    return distribute_or_over_and(nnf)

def to_nnf(sentence: Sentence):
    if isinstance(sentence, Symbol):
        return sentence
    elif isinstance(sentence, Negation):
        if isinstance(sentence.arg, Symbol):
            return sentence
        elif isinstance(sentence.arg, Negation):
            return to_nnf(sentence.arg.arg)
        elif isinstance(sentence.arg, Conjunction):
            return Disjunction(*[to_nnf(Negation(arg)) for arg in sentence.arg.args])
        elif isinstance(sentence.arg, Disjunction):
            return Conjunction(*[to_nnf(Negation(arg)) for arg in sentence.arg.args])
        elif isinstance(sentence.arg, Implication):
            return Conjunction(to_nnf(sentence.arg.antecedent), to_nnf(Negation(sentence.arg.consequent)))
    elif isinstance(sentence, Conjunction):
        return Conjunction(*[to_nnf(arg) for arg in sentence.args])
    elif isinstance(sentence, Disjunction):
        return Disjunction(*[to_nnf(arg) for arg in sentence.args])
    elif isinstance(sentence, Implication):
        return to_nnf(Disjunction(Negation(sentence.antecedent), sentence.consequent))
    elif isinstance(sentence, Biconditional):
        return Conjunction(to_nnf(Implication(sentence.args[0], sentence.args[1])), 
                           to_nnf(Implication(sentence.args[1], sentence.args[0])))

def distribute_or_over_and(sentence: Sentence):
    if isinstance(sentence, Disjunction):
        if any(isinstance(arg, Conjunction) for arg in sentence.args):
            conj = next(arg for arg in sentence.args if isinstance(arg, Conjunction))
            others = [arg for arg in sentence.args if arg is not conj]
            return Conjunction(*[distribute_or_over_and(Disjunction(*(others + [arg]))) for arg in conj.args])
        else:
            return sentence
    elif isinstance(sentence, Conjunction):
        return Conjunction(*[distribute_or_over_and(arg) for arg in sentence.args])
    else:
        return sentence

# Example usage
p = Symbol("p")
q = Symbol("q")
r = Symbol("r")
sentence = Implication(p, Conjunction(q, r))
cnf_sentence = to_cnf(sentence)
print(cnf_sentence)
