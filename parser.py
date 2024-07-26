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
        ('NOT',           r'~'),
        ('AND',           r'&'),
        ('OR',            r'\|'),
        ('IMPLIES',       r'=>'),
        ('BICONDITIONAL', r'<=>'),
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


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        
    @property
    def current_token(self):
        return self.tokens[self.pos]
        
    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
            
    def parse(self):
        if self.current_token is None:
            return None
        result = self.expression()
        if self.current_token is not None:
            raise Exception("Invalid syntax: " + str(self.current_token))
        return result
    
    def expression(self):
        node = self.biconditional()
        return node
    
    def biconditional(self):
        node = self.implication()
        while self.current_token is not None and self.current_token[0] == 'BICONDITIONAL':
            self.advance()
            node = ('biconditional', node, self.implication())
        return node

grammar = f'''
    start: kb query
    kb: {KB_KEYWORD} sentence+
    
    %import common.WS
    %ignore WS
'''


if __name__ == '__main__':
    tokens = tokenize(sanitize('(a<=>(c=>~d))&b&(b=>a)'))
    print(tokens)