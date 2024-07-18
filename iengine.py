import sympy
from itertools import product

# Define symbols
A = sympy.Symbol('A')
B = sympy.Symbol('B')
C = sympy.Symbol('C')

# Define the knowledge base (KB) and query (q)
KB = sympy.And(A, sympy.Implies(A, B), sympy.Implies(B, C))
query = C

# Check if query is entailed by KB
result = sympy.satisfiable(sympy.Not(sympy.Implies(KB, query)))

if not result:
    print("The query is entailed by the knowledge base.")
else:
    print("The query is not entailed by the knowledge base.")
