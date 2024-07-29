import os, re
from syntax import *

INPUT_DIR = 'data'
KB_KEYWORD = 'TELL'
KB_SEPARATOR = ';'
QUERY_KEYWORD = 'ASK'


def sanitize(input:str):
    return input.replace('\n', ' ').replace(' ', '').strip()


def read_file(file_name:str) -> tuple[list[str], str]:
    file_path = os.path.join(INPUT_DIR, file_name)
    with open(file_path, 'r') as file:
        content = file.read()
        tell_index = content.index(KB_KEYWORD)
        ask_index = content.index(QUERY_KEYWORD)
        kb = content[tell_index + len(KB_KEYWORD) : ask_index].split(KB_SEPARATOR)
        query = content[ask_index + len(QUERY_KEYWORD):]
        return sanitize(kb), sanitize(query)
        

def tokenize(text:str) -> list[str]:
    token_specification = [
        ('SYMBOL',        r'[a-zA-Z][a-zA-Z0-9]*'),
        ('LPAREN',        r'\('),       # Left parenthesis
        ('RPAREN',        r'\)'),       # Right parenthesis
        ('NOT',           escaped_connective("NEGATION")), # Negation
        ('AND',           escaped_connective("CONJUNCTION")), # Conjunction
        ('OR',            escaped_connective("DISJUNCTION")),  # Disjunction
        ('IMPLIES',       escaped_connective("IMPLICATION")),  # Implication
        ('BICONDITIONAL', escaped_connective("BICONDITIONAL")),  # Biconditional
        ('SKIP',          r'[ \t]+'),
        ('MISMATCH',      r'.')
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    # print(tok_regex)
    get_token = re.compile(tok_regex).match
    pos = 0
    tokens = []
    while pos < len(text):
        match = get_token(text, pos)
        if match is None:
            raise SyntaxError('Unexpected character: %s' % text[pos])
        pos = match.end()
        token_type = match.lastgroup
        if token_type != 'SKIP' and token_type != 'MISMATCH':
            tokens.append((token_type, match.group(token_type)))
    return tokens


def escaped_connective(connective:str) -> str:
    return re.escape(fr'{Connective[connective].value}')


def parse(tokens:list[tuple[str, str]]) -> Sentence:
    expr, tokens = _parse_biconditional(tokens)
    if tokens:
        raise SyntaxError("Unexpected tokens at end of input")
    return expr


def _parse_biconditional(tokens:list[tuple[str, str]]) -> tuple[Sentence, list[tuple[str, str]]]:
    expr, tokens = _parse_implication(tokens)
    while tokens and tokens[0][0] == 'BICONDITIONAL':
        right, tokens = _parse_implication(tokens[1:])
        expr = Biconditional(expr, right)
    return expr, tokens


def _parse_implication(tokens:list[tuple[str, str]]) -> tuple[Sentence, list[tuple[str, str]]]:
    expr, tokens = _parse_disjunction(tokens)
    while tokens and tokens[0][0] == 'IMPLIES':
        right, tokens = _parse_implication(tokens[1:])
        expr = Implication(expr, right)
    return expr, tokens


def _parse_disjunction(tokens:list[tuple[str, str]]) -> tuple[Sentence, list[tuple[str, str]]]:
    expr, tokens = _parse_conjunction(tokens)
    while tokens and tokens[0][0] == 'OR':
        right, tokens = _parse_conjunction(tokens[1:])
        expr = Disjunction(expr, right)
    return expr, tokens


def _parse_conjunction(tokens:list[tuple[str, str]]) -> tuple[Sentence, list[tuple[str, str]]]:
    expr, tokens = _parse_negation(tokens)
    while tokens and tokens[0][0] == 'AND':
        right, tokens = _parse_negation(tokens[1:])
        expr = Conjunction(expr, right)
    return expr, tokens


def _parse_negation(tokens:list[tuple[str, str]]) -> tuple[Sentence, list[tuple[str, str]]]:
    if tokens and tokens[0][0] == 'NOT':
        expr, tokens = _parse_parentheses(tokens[1:])
        return Negation(expr), tokens
    return _parse_parentheses(tokens)


def _parse_parentheses(tokens:list[tuple[str, str]]) -> tuple[Sentence, list[tuple[str, str]]]:
    if tokens and tokens[0][0] == 'LPAREN':
        expr, tokens = _parse_biconditional(tokens[1:])
        if tokens and tokens[0][0] == 'RPAREN':
            # print(expr, type(expr), tokens)
            return expr, tokens[1:]
        raise SyntaxError("Expected ')'")
    return _parse_symbol(tokens)


def _parse_symbol(tokens:list[tuple[str, str]]) -> tuple[Symbol, list[tuple[str, str]]]:
    if tokens[0][0] == 'SYMBOL':
        token, tokens = tokens[0], tokens[1:]
        return Symbol(token[1]), tokens
    raise SyntaxError("Expected a symbol")


if __name__ == '__main__':
    sentence_str = "(a<=>(c=>~d)) & b & (b=>a)"
    print("Sentence string:", sentence_str, "\n")
    tokens = tokenize(sanitize(sentence_str))
    print("Tokens:", tokens, "\n")
    sentence = parse(tokens)
    print("Parsed sentence:", sentence, "(type:", type(sentence).__name__, ")")