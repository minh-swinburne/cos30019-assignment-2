import unittest, sys, os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from syntax import *
from cnf import to_cnf

class TestCNF(unittest.TestCase):
    
        def setUp(self):
            self.p = Symbol("p")
            self.q = Symbol("q")
            self.r = Symbol("r")
            self.t = Symbol("t")
    
        def test_implication(self):
            # p → (q ∧ r)
            sentence = Implication(self.p, Conjunction(self.q, self.r))
            cnf_sentence = to_cnf(sentence)
            # (¬p ∨ q) ∧ (¬p ∨ r)
            self.assertEqual(cnf_sentence, Conjunction(
                Disjunction(
                    self.p.negate(), 
                    self.q
                    ), 
                Disjunction(
                    self.p.negate(), 
                    self.r
                    )
                )
            )
    
        def test_nested_implication(self):
            # p → (q → r)
            sentence = Implication(self.p, Implication(self.q, self.r))
            cnf_sentence = to_cnf(sentence)
            # (¬p ∨ ¬q ∨ r)
            self.assertEqual(cnf_sentence, Disjunction(self.p.negate(), self.q.negate(), self.r))
    
        def test_disjunction_of_conjunctions(self):
            # (p ∧ q) ∨ (r ∧ t)
            sentence = Disjunction(Conjunction(self.p, self.q), Conjunction(self.r, self.t))
            cnf_sentence = to_cnf(sentence)
            # (p ∨ r) ∧ (p ∨ t) ∧ (q ∨ r) ∧ (q ∨ t)
            self.assertEqual(cnf_sentence, Conjunction(Disjunction(self.p, self.r), Disjunction(self.p, self.t), Disjunction(self.q, self.r), Disjunction(self.q, self.t)))
    
        def test_contradictory_disjunction(self):
            # (p ∨ ¬p)
            sentence = Disjunction(self.p, Negation(self.p)) 
            cnf_sentence = to_cnf(sentence)
            # True
            self.assertEqual(cnf_sentence, Symbol("True"))
    
        def test_conjunction_of_disjunctions(self):
            # (p ∨ q) ∧ (r ∨ t)
            sentence = Conjunction(Disjunction(self.p, self.q), Disjunction(self.r, self.t))
            cnf_sentence = to_cnf(sentence)
            # (p ∨ q) ∧ (r ∨ t)
            self.assertEqual(cnf_sentence, Conjunction(Disjunction(self.p, self.q), Disjunction(self.r, self.t)))
    
        def test_conjunction_of_implications(self):
            # (p → q) ∧ (r → t)
            sentence = Conjunction(Implication(self.p, self.q), Implication(self.r, self.t))
            cnf_sentence = to_cnf(sentence)
            # (¬p ∨ q) ∧ (¬r ∨ t)
            self.assertEqual(cnf_sentence, Conjunction(Disjunction(self.p.negate(), self.q), Disjunction(self.r.negate(), self.t)))
    
        def test_negation_of_disjunction(self):
            # ¬(p ∨ q)
            sentence = Negation(Disjunction(self.p, self.q))
            cnf_sentence = to_cnf(sentence)
            # (¬p ∧ ¬q)
            self.assertEqual(cnf_sentence, Conjunction(self.p.negate(), self.q.negate()))
            
        def test_negation_of_conjunction(self):
            # ¬(p ∧ q)
            sentence = Negation(Conjunction(self.p, self.q))
            cnf_sentence = to_cnf(sentence)
            # (¬p ∨ ¬q)
            self.assertEqual(cnf_sentence, Disjunction(self.p.negate(), self.q.negate()))
            
        def test_biconditional(self):
            # p ↔ q
            sentence = Biconditional(self.p, self.q)
            cnf_sentence = to_cnf(sentence)
            # (p ∨ ¬q) ∧ (¬p ∨ q)
            self.assertEqual(cnf_sentence, Conjunction(Disjunction(self.p, self.q.negate()), Disjunction(self.p.negate(), self.q)))
            
        def test_complex_sentences(self):
            # (p ∧ (q ∨ r)) → t
            sentence = Implication(
                Conjunction(
                    self.p, 
                    Disjunction(
                        self.q, 
                        self.r
                        )
                    ), 
                self.t
                )
            cnf_sentence = to_cnf(sentence)
            # (¬p ∨ t ∨ ¬r) ∧ (¬p ∨ t ∨ ¬q)
            self.assertEqual(cnf_sentence, Conjunction(
                Disjunction(
                    self.p.negate(), 
                    self.t, 
                    self.r.negate()
                    ),
                Disjunction(
                    self.p.negate(), 
                    self.t, 
                    self.q.negate()
                    )
                )
            )
            
            # (p ∧ (q ∨ r)) → (t ↔ ¬p)
            sentence = Implication(
                Conjunction(
                    self.p, 
                    Disjunction(self.q, self.r)
                    ), 
                Biconditional(
                    self.t, 
                    Negation(self.p)
                    )
                )
            cnf_sentence = to_cnf(sentence)
            # (¬q ∨ t) ∧ (¬r ∨ t) ∧ (¬p ∨ ¬q ∨ ¬t) ∧ (¬p ∨ ¬r ∨ ¬t)
            self.assertEqual(cnf_sentence, Conjunction(
                Disjunction(
                    self.q.negate(), 
                    self.t
                    ), 
                Disjunction(
                    self.r.negate(), 
                    self.t
                    ), 
                Disjunction(
                    self.p.negate(), 
                    self.q.negate(), 
                    self.t.negate()
                    ),
                Disjunction(
                    self.p.negate(), 
                    self.r.negate(), 
                    self.t.negate()
                    )
                )
            )
            
            # p ↔ (q → r)
            sentence = Biconditional(self.p, Implication(self.q, self.r))
            cnf_sentence = to_cnf(sentence)
            # (¬p ∨ ¬q ∨ r) ∧ (p ∨ q) ∧ (p ∨ ¬r)
            self.assertEqual(cnf_sentence, Conjunction(
                Disjunction(
                    self.p, 
                    self.q
                    ), 
                Disjunction(
                    self.p, 
                    self.r.negate()
                    ), 
                Disjunction(
                    self.p.negate(), 
                    self.q.negate(), 
                    self.r
                    )
                )
            )
            
if __name__ == '__main__':
    unittest.main()