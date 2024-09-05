import sys, os, timeit, tracemalloc
from collections import Counter
from syntax import *
from methods import *
from parser import read_file, parse_kb_and_query


def get_solver(method, kb, query):
    if method == "TT":
        solver = TruthTable(kb, query)
    elif method == "FC":
        solver = ForwardChaining(kb, query)
    elif method == "BC":
        solver = BackwardChaining(kb, query)
    elif method == "RES":
        solver = Resolution(kb, query)
    elif method == "DPLL":
        solver = DPLL(kb, query)
    else:
        raise ValueError("Invalid method. Please use one of the following methods: TT, FC, BC, RES, DPLL")
    return solver


def space(solver):
    tracemalloc.reset_peak()
    tracemalloc.clear_traces()
    tracemalloc.start()
    result = solver.solve()
    current, peak = tracemalloc.get_traced_memory()
    
    # print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
    tracemalloc.stop()
    return result, peak


def time(file_name, method, number=1000):
    count_entails = Counter()
    
    def wrapped():
        kb, query = parse_kb_and_query(file_name)
        solver = get_solver(method, kb, query)
        result = solver.solve()
        count_entails[result["entails"]] += 1
    
    avg_time = timeit.timeit(wrapped, number=number)*1000/number
    return avg_time, count_entails


def analyze(file_name, method, number=1000):
    kb, query = parse_kb_and_query(file_name)
    _, _, expected_result = read_file(file_name)
    
    print("Information:")
    print(f"\t- Filename: {file_name}")
    print(f"\t- Method: {method}")
    print(f"\t- Knowledge Base / Tell: {kb}")
    print(f"\t- Query / Ask: {query}")
    if expected_result is not None:
        print(f"\t- Expected Result: {"YES" if expected_result else "NO"}")
    
    solver = get_solver(method, kb, query)
    result, peak = space(solver)
    
    print("\nResult:")
    print(f"\t- Entails: {"YES" if result["entails"] else "NO"}")
    if "message" in result.keys():
        print(f"\t- Message: {result['message']}")
    
    print("\nPerformance:")
    print(f"\t- Memory: {peak:,} B")
    
    sys.stdout = open(os.devnull, 'w')
    avg_time, count_entails = time(file_name, method, number)
    sys.stdout = sys.__stdout__
    
    print(f"\t- Time: {avg_time:,.4f} ms (average of {number} runs)")
    print(f"\t- Accuracy: {count_entails[expected_result]/number:.2%}")
    print()
    
    
if __name__ == "__main__":
    args = sys.argv

    file_name = args[2] if len(args) > 2 else 'horn_1.txt'
    # file_name = 'cnf_1.txt'
    file_name = 'generic_1.txt'
    method = args[3].upper() if len(args) > 3 else 'FC'
    number = int(args[4]) if len(args) > 4 else 100

    analyze(file_name, method, number)