"""
This module contains the parser for the knowledge base and query.

### Functions:
    - parse_kb_and_query(file_name: str) -> tuple[Sentence, Sentence]: Parse the knowledge base and query from the file.
    - sanitize(input: str) -> str: Sanitize the input string by removing all whitespaces and newlines.
    - read_file(file_name: str) -> tuple[list[str], str, bool]: Read the content of the file and return the knowledge base, query, and optionally expected result as strings.
    - tokenize(text: str) -> list[tuple[str, str]]: Tokenize the input text into a list of tokens.
    - escaped_connective(connective: str) -> str: Escape the connective for regex.
    - parse(tokens: list[tuple[str, str]]) -> Sentence: Parse the tokens into a Sentence object.
    - _parse_biconditional(tokens): Parse the biconditional connective.
    - _parse_implication(tokens): Parse the implication connective.
    - _parse_disjunction(tokens): Parse the disjunction connective.
    - _parse_conjunction(tokens): Parse the conjunction connective.
    - _parse_negation(tokens): Parse the negation connective.
    - _parse_parentheses(tokens): Parse the parentheses.
    - _parse_symbol(tokens): Parse the symbol.
"""
import os, re
from syntax import *

INPUT_DIR = 'data'
KB_KEYWORD = 'TELL\n'
KB_SEPARATOR = ';'
QUERY_KEYWORD = 'ASK\n'
RESULT_KEYWORD = 'EXPECT\n'
    

def parse_kb_and_query(file_name:str) -> tuple[Sentence, Sentence]:
    """
    Parse the knowledge base and query from the file.

    ### Args:
        - file_name (str): The name of the file to read from.
    
    ### Returns:
        - tuple[Sentence, Sentence]: A tuple containing the knowledge base and query as Sentence objects.
    """
    kb, query, _ = read_file(file_name)
    kb = [parse(tokenize(sentence)) for sentence in kb]
    query = parse(tokenize(query))
    return Conjunction(*kb) if len(kb) > 1 else kb[0], query


def sanitize(input:str):
    """
    Sanitize the input string by removing all whitespaces and newlines.
        
    ### Args:
        - input (str): The input string to sanitize.
    
    ### Returns:
        - str: The sanitized string
    """
    return input.replace('\n', ' ').replace(' ', '').strip()


def read_file(file_name:str) -> tuple[list[str], str, bool]:
    """
    Read the content of the file and return the knowledge base and query as strings.

    ### Args:
        - file_name (str): The name of the file to read from.
        
    ### Returns:
        - tuple[list[str], str, bool]: A tuple containing the knowledge base and query as strings.
    """
    file_path = os.path.join(INPUT_DIR, file_name)
    with open(file_path, 'r') as file:
        content = file.read()
        tell_index = content.index(KB_KEYWORD)
        ask_index = content.index(QUERY_KEYWORD)
        result_index = content.index(RESULT_KEYWORD) if RESULT_KEYWORD in content else len(content)
        
        kb = content[tell_index + len(KB_KEYWORD) : ask_index].split(KB_SEPARATOR)
        sanitized_kb = [sanitize(sentence) for sentence in kb if sanitize(sentence)]
        query = content[ask_index + len(QUERY_KEYWORD) : result_index]
        # Expected result is optional, to be used for testing and debugging
        expected_result = content[result_index + len(RESULT_KEYWORD) :].strip() if RESULT_KEYWORD in content else None
        return sanitized_kb, sanitize(query), sanitize(expected_result) == 'YES' if expected_result else None


def tokenize(text:str) -> list[tuple[str, str]]:
    """
    Tokenize the input text into a list of tokens.

    ### Args:
        - text (str): The text to tokenize.

    ### Returns:
        - list[tuple[str, str]]: The list of tokens.
        
    ### Raises:
        - SyntaxError: If an unexpected character is found.
    """
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
    """
    Parse the tokens into a Sentence object.

    ### Args:
        - tokens (list[tuple[str, str]]): The list of tokens to parse.
        
    ### Returns:
        - Sentence: The Sentence object.
    
    ### Raises:
        - SyntaxError: If there are unexpected tokens at the end of the input.
    """
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
        # Handle double negation
        if isinstance(expr, Negation):
            return expr.arg, tokens
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
