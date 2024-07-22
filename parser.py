import os, re
from syntax import *
from lark import Lark, Transformer


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
        sanitize(kb), sanitize(query)
        

def tokenize(text:str) -> list[str]:
    token_specification = [
        ('SYMBOL', r'[a-zA-Z][a-zA-Z0-9]*'),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('NOT', r'~'),
        ('AND', r'&'),
        ('OR', r'\|'),
        ('IMPLIES', r'=>'),
        ('BICONDITIONAL', r'<=>')
    ]
    tokens = []
    for tok_type, tok_regex in token_specification:
        for match in re.finditer(tok_regex, text):
            tok = match.group(0)
            tokens.append((match.start(), tok_type, tok))
    tokens.sort(key=lambda x: x[0])
    return [(token[1], token[2]) for token in tokens]


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