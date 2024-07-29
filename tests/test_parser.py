import unittest, sys, os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from parser import tokenize, sanitize, parse
from syntax import *

class TestParser(unittest.TestCase):
    
    def test_tokenize(self):
        sentence = "(a<=>(c=>~d)) & b & (b=>a)"
        expected_tokens = [
            ('LPAREN', '('), ('SYMBOL', 'a'), ('BICONDITIONAL', '<=>'),
            ('LPAREN', '('), ('SYMBOL', 'c'), ('IMPLIES', '=>'),
            ('NOT', '~'), ('SYMBOL', 'd'), ('RPAREN', ')'), ('RPAREN', ')'),
            ('AND', '&'), ('SYMBOL', 'b'), ('AND', '&'),
            ('LPAREN', '('), ('SYMBOL', 'b'), ('IMPLIES', '=>'),
            ('SYMBOL', 'a'), ('RPAREN', ')')
        ]
        tokens = tokenize(sanitize(sentence))
        self.assertEqual(tokens, expected_tokens)

    def test_parse_symbol(self):
        tokens = [('SYMBOL', 'a')]
        parsed_sentence = parse(tokens)
        expected_sentence = Symbol('a')
        self.assertEqual(parsed_sentence, expected_sentence)

    def test_parse_negation(self):
        tokens = [('NOT', '~'), ('SYMBOL', 'a')]
        parsed_sentence = parse(tokens)
        expected_sentence = Negation(Symbol('a'))
        self.assertEqual(parsed_sentence, expected_sentence)

    def test_parse_conjunction(self):
        tokens = [('SYMBOL', 'a'), ('AND', '&'), ('SYMBOL', 'b')]
        parsed_sentence = parse(tokens)
        expected_sentence = Conjunction(Symbol('a'), Symbol('b'))
        self.assertEqual(parsed_sentence, expected_sentence)

    def test_parse_disjunction(self):
        tokens = [('SYMBOL', 'a'), ('OR', '||'), ('SYMBOL', 'b')]
        parsed_sentence = parse(tokens)
        expected_sentence = Disjunction(Symbol('a'), Symbol('b'))
        self.assertEqual(parsed_sentence, expected_sentence)

    def test_parse_implication(self):
        tokens = [('SYMBOL', 'a'), ('IMPLIES', '=>'), ('SYMBOL', 'b')]
        parsed_sentence = parse(tokens)
        expected_sentence = Implication(Symbol('a'), Symbol('b'))
        self.assertEqual(parsed_sentence, expected_sentence)

    def test_parse_biconditional(self):
        tokens = [('SYMBOL', 'a'), ('BICONDITIONAL', '<=>'), ('SYMBOL', 'b')]
        parsed_sentence = parse(tokens)
        expected_sentence = Biconditional(Symbol('a'), Symbol('b'))
        self.assertEqual(parsed_sentence, expected_sentence)

    def test_complex_sentence(self):
        sentence = "(a<=>(c=>~d)) & b & (b=>a)"
        tokens = tokenize(sanitize(sentence))
        parsed_sentence = parse(tokens)
        # Define the expected complex structure here as needed
        expected_sentence = Conjunction(
            Conjunction(
                Biconditional(
                    Symbol('a'),
                    Implication(
                        Symbol('c'),
                        Negation(Symbol('d'))
                    )
                ),
                Symbol('b')
            ),
            Implication(Symbol('b'), Symbol('a'))
        )
        self.assertEqual(parsed_sentence, expected_sentence)

if __name__ == '__main__':
    unittest.main()
