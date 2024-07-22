import re

def tokenize(input_str):
    # Define regex for symbols and operators
    token_specification = [
        ('SYMBOL', r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('NOT', r'~'),
        ('AND', r'&'),
        ('OR', r'\|\|'),
        ('IMPLIES', r'=>'),
        ('BICONDITIONAL', r'<=>'),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('SEMICOLON', r';'),
        ('SKIP', r'[ \t]+'),  # Skip over spaces and tabs
        ('MISMATCH', r'.')    # Any other character
    ]
    tokens = []
    for tok_type, tok_regex in token_specification:
        for match in re.finditer(tok_regex, input_str):
            tok = match.group(0)
            if tok_type != 'SKIP':
                tokens.append((tok_type, tok))
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.pos = -1
        self.advance()

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def parse(self):
        if self.current_token is None:
            return None
        print(self.current_token)
        result = self.expression()
        print(self.current_token, result)
        if self.current_token is not None:
            raise Exception("Invalid syntax")
        return result

    def expression(self):
        node = self.implication()
        return node

    def implication(self):
        node = self.biconditional()
        while self.current_token is not None and self.current_token[0] == 'IMPLIES':
            self.advance()
            node = ('implies', node, self.biconditional())
        return node

    def biconditional(self):
        node = self.or_expr()
        while self.current_token is not None and self.current_token[0] == 'BICONDITIONAL':
            self.advance()
            node = ('biconditional', node, self.or_expr())
        return node

    def or_expr(self):
        node = self.and_expr()
        while self.current_token is not None and self.current_token[0] == 'OR':
            self.advance()
            node = ('or', node, self.and_expr())
        return node

    def and_expr(self):
        node = self.not_expr()
        while self.current_token is not None and self.current_token[0] == 'AND':
            self.advance()
            node = ('and', node, self.not_expr())
        return node

    def not_expr(self):
        if self.current_token is not None and self.current_token[0] == 'NOT':
            self.advance()
            return ('not', self.not_expr())
        return self.atom()

    def atom(self):
        token = self.current_token
        if token[0] == 'SYMBOL':
            self.advance()
            return ('symbol', token[1])
        elif token[0] == 'LPAREN':
            self.advance()
            node = self.expression()
            if self.current_token is not None and self.current_token[0] == 'RPAREN':
                self.advance()
                return node
            else:
                raise Exception("Invalid syntax")
        raise Exception("Invalid syntax")

def parse_input(input_str):
    tokens = tokenize(input_str)
    parser = Parser(tokens)
    return parser.parse()

def parse_kb_and_query(input_str):
    # Split the input into TELL and ASK parts
    tell_part = re.search(r'TELL\s+(.+?)\s+ASK', input_str, re.DOTALL).group(1)
    ask_part = re.search(r'ASK\s+(.+)', input_str).group(1).strip()

    # Parse the knowledge base
    kb_clauses = tell_part.split(';')
    parsed_kb = [parse_input(clause.strip()) for clause in kb_clauses if clause.strip()]

    # Parse the query
    parsed_query = parse_input(ask_part)

    return parsed_kb, parsed_query

# Example usage
kb_query = """
TELL
p2=> p3; p3 => p1; c => e; b&e => f; f&g => h; p1=>d; p1&p3 => c; a; b; p2;
ASK
d
"""

parsed_kb, parsed_query = parse_kb_and_query(kb_query)
print("Knowledge Base:")
print(parsed_kb)
print("\nQuery:")
print(parsed_query)
