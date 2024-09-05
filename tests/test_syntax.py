import unittest, sys, os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from syntax import *

class TestSyntax(unittest.TestCase):

    def setUp(self):
        self.p = Symbol("p")
        self.q = Symbol("q")
        self.r = Symbol("r")
        self.model = {self.p: True, self.q: False, self.r: None}
        
    def test_connective(self):
        # Test Connective
        self.assertEqual(Connective.NEGATION.value, '~')
        self.assertEqual(Connective.CONJUNCTION.value, '&')
        self.assertEqual(Connective.DISJUNCTION.value, '||')
        self.assertEqual(Connective.IMPLICATION.value, '=>')
        self.assertEqual(Connective.BICONDITIONAL.value, '<=>')

    def test_symbol(self):
        # p: True, q: False, r: None
        self.assertTrue(self.p.evaluate(self.model))
        self.assertFalse(self.q.evaluate(self.model))
        self.assertIsNone(self.r.evaluate(self.model))
        self.assertSetEqual(self.p.symbols(), {self.p})

    def test_negation(self):
        # ~p: False, ~q: True, ~~q: False, ~r: None
        self.assertFalse(self.p.negate().evaluate(self.model))
        self.assertFalse(Negation(self.p).evaluate(self.model))
        self.assertTrue(self.q.negate().evaluate(self.model))
        self.assertFalse(self.q.negate().negate().evaluate(self.model))
        self.assertIsNone(self.r.negate().evaluate(self.model))
        self.assertSetEqual(self.q.negate().symbols(), {self.q})

    def test_conjunction(self):
        # p & q: False, p & q & r: None
        self.assertFalse(Conjunction(self.p, self.q).evaluate(self.model))
        self.assertIsNone(Conjunction(self.p, self.q, self.r).evaluate(self.model))
        self.assertSetEqual(Conjunction(self.p, self.q).symbols(), {self.p, self.q})

    def test_disjunction(self):
        # p || q: True, p || q || r: None
        self.assertTrue(Disjunction(self.p, self.q).evaluate(self.model))
        self.assertIsNone(Disjunction(self.p, self.q, self.r).evaluate(self.model))
        self.assertSetEqual(Disjunction(self.p, self.q, self.r).symbols(), {self.p, self.r, self.q})

    def test_implication(self):
        # p => q: False, q => p: True, p => (q => r): None
        self.assertFalse(Implication(self.p, self.q).evaluate(self.model))
        self.assertTrue(Implication(self.q, self.p).evaluate(self.model))
        self.assertIsNone(Implication(self.p, Implication(self.q, self.r)).evaluate(self.model))
        self.assertSetEqual(Implication(self.p, self.q).symbols(), {self.p, self.q})
        self.assertSetEqual(Implication(self.p, Implication(self.q, self.r)).symbols(), {self.p, self.q, self.r})

    def test_biconditional(self):
        # p <=> q: False
        self.assertFalse(Biconditional(self.p, self.q).evaluate(self.model))
        self.assertSetEqual(Biconditional(self.p, self.q).symbols(), {self.p, self.q})

    def test_complex_sentences(self):
        # (p & (q || r)) => t: True, (p & (q || r)) => (t <=> ~p): None
        self.assertTrue(Implication(self.p.negate(), self.q.negate()).evaluate(self.model))
        self.assertFalse(Implication(self.q.negate(), self.p.negate()).evaluate(self.model))
        self.assertTrue(Conjunction(self.p, self.q).negate().evaluate(self.model))
        self.assertFalse(Disjunction(self.p, self.q).negate().evaluate(self.model))
        self.assertTrue(Implication(self.p, self.q).negate().evaluate(self.model))
        self.assertTrue(Biconditional(self.p, self.q).negate().evaluate(self.model))
        self.assertIsNone(Conjunction(self.p, self.q, self.r).negate().evaluate(self.model))
        self.assertIsNone(Disjunction(self.p, self.q, self.r).negate().evaluate(self.model))
        self.assertIsNone(Implication(self.p, Implication(self.q, self.r)).negate().evaluate(self.model))


if __name__ == '__main__':
    unittest.main()