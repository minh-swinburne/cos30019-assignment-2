import unittest, sys, os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from parser import *
from syntax import *

class TestParser(unittest.TestCase):
    
    def setUp(self):
        self.file_name = 'horn_1.txt'
    
    def test_read_file(self):
        kb_str, query_str, expected_result = read_file(self.file_name)
        expected_kb_str = ['p2=>p3', 'p3=>p1', 'c=>e', 'b&e=>f', 'f&g=>h', 'p1=>d', 'p1&p3=>c', 'a', 'b', 'p2']
        expected_query_str = 'd'
        self.assertEqual(kb_str, expected_kb_str)
        self.assertEqual(query_str, expected_query_str)
        self.assertTrue(expected_result)
    
    def test_sanitize(self):
        sentence = "  (a <=>(c=> ~d)) & b & (b =>a)  \n"
        sanitized_sentence = sanitize(sentence)
        self.assertEqual(sanitized_sentence, "(a<=>(c=>~d))&b&(b=>a)")
        
    def test_escaped_connective(self):
        self.assertEqual(escaped_connective("NEGATION"), r"\~")
        self.assertEqual(escaped_connective("CONJUNCTION"), r"\&")
        self.assertEqual(escaped_connective("DISJUNCTION"), r"\|\|")
        self.assertEqual(escaped_connective("IMPLICATION"), r"=>")
        self.assertEqual(escaped_connective("BICONDITIONAL"), r"<=>")
    
    def test_tokenize(self):
        sentence = "(a <=>(c=> ~d)) & b & (b =>a)"
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
        
    def test_parse_kb_and_query(self):
        kb, query = parse_kb_and_query(self.file_name)
        expected_kb = Conjunction(
            Implication(Symbol('p2'), Symbol('p3')),
            Implication(Symbol('p3'), Symbol('p1')),
            Implication(Symbol('c'), Symbol('e')),
            Implication(Conjunction(Symbol('b'), Symbol('e')), Symbol('f')),
            Implication(Conjunction(Symbol('f'), Symbol('g')), Symbol('h')),
            Implication(Symbol('p1'), Symbol('d')),
            Implication(Conjunction(Symbol('p1'), Symbol('p3')), Symbol('c')),
            Symbol('a'),
            Symbol('b'),
            Symbol('p2')
        )
        expected_query = Symbol('d')
        self.assertEqual(kb, expected_kb)
        self.assertEqual(query, expected_query)
        

if __name__ == '__main__':
    unittest.main()
