import unittest, sys, os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from syntax import *
from horn import *

class TestHorn(unittest.TestCase):
    
    def setUp(self):
        self.a = Symbol('a')
        self.b = Symbol('b')
        self.c = Symbol('c')
        self.d = Symbol('d')
        self.negation = Negation(self.a)
        self.conjunction = Conjunction(self.a, self.b)
        
        self.disjunction = Disjunction(self.a, self.b)
        self.disj_of_conj = Disjunction(Conjunction(self.a, self.b), Conjunction(self.c, self.d))
        self.disj_horn = Disjunction(self.a.negate(), self.b.negate(), self.c)
        
        self.implication = Implication(self.a, self.b)
        self.impl_horn = Implication(self.conjunction, self.d)
        self.impl_not_horn = Implication(self.disjunction, self.d)
        
        self.conj_of_disj = Conjunction(Disjunction(self.a, self.b), Disjunction(self.c, self.d))
        self.conj_horn = Conjunction(self.disj_horn, self.impl_horn)
    
    def test_check_horn_query(self):
        self.assertTrue(check_horn_query(self.a))
        self.assertFalse(check_horn_query(self.negation))
        self.assertFalse(check_horn_query(self.conjunction))
        
    def test_check_horn_kb(self):
        self.assertTrue(check_horn_kb(self.a))
        self.assertTrue(check_horn_kb(self.negation))
        self.assertTrue(check_horn_kb(self.conjunction))
        self.assertTrue(check_horn_kb(self.implication))
        self.assertTrue(check_horn_kb(self.disj_horn))
        self.assertTrue(check_horn_kb(self.impl_horn))
        self.assertTrue(check_horn_kb(self.conj_horn))
        
        self.assertFalse(check_horn_kb(self.disjunction))
        self.assertFalse(check_horn_kb(self.disj_of_conj))
        self.assertFalse(check_horn_kb(self.impl_not_horn))
        self.assertFalse(check_horn_kb(self.conj_of_disj))


if __name__ == '__main__':
    sys.stdout = open(os.devnull, 'w')
    unittest.main()