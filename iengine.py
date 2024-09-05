import sys
from syntax import *
from methods import *
from parser import parse_kb_and_query

def main(method, file_name):
    # Parse the knowledge base and query from the file
    kb, query = parse_kb_and_query(file_name)

    # Based on the method, create the appropriate object and solve
    if method == "TT":
        # Truth Table
        solver = TruthTable(kb, query)
    elif method == "FC":
        # Forward Chaining
        solver = ForwardChaining(kb, query)
    elif method == "BC":
        # Backward Chaining
        solver = BackwardChaining(kb, query)
    elif method == "RES":
        # Resolution
        solver = Resolution(kb, query)
    elif method == "DPLL":
        # DPLL
        solver = DPLL(kb, query)
    else:
        raise ValueError("Invalid method. Please use one of the following methods: TT, FC, BC, RES, DPLL")
    
    result = solver.solve()
    entails = "YES" if result["entails"] else "NO"
    message = f": {result['message']}" if "message" in result.keys() else ""
    print("\n" + entails + message + "\n")
    
def suggest_help():
    print("For help, use the command: './iengine help'")
    
def display_help():
    print("\nInference Engine for Propositional Logic - CLI Help")
    print("\nCommand Format: './iengine <method> <filename>'")
    print("\nMethods:")
    print("  TT   - Truth Table")
    print("  FC   - Forward Chaining")
    print("  BC   - Backward Chaining")
    print("  RES  - Resolution")
    print("  DPLL - Davis-Putnam-Logemann-Loveland (DPLL)")
    print("\nFilename: The name of the file (in the data/ folder) containing the knowledge base and query. The file should be in the format specified in the assignment.")
    print("\nExample: './iengine TT horn_1.txt'")
    print()
    
def get_available_files():
    import os
    return os.listdir("data")
    

if __name__ == "__main__":
    try:
        method = sys.argv[1]
        if method == "help":
            display_help()
            sys.exit()
        file_name = sys.argv[2]
        if "--analyze" in sys.argv:
            from analyze import analyze
            if "--number" in sys.argv:
                number = int(sys.argv[sys.argv.index("--number") + 1])
            else:
                number = 100
            analyze(file_name, method, number)
            sys.exit()
        main(method, file_name)
        
    # Handle exceptions
    # In case of missing arguments
    except IndexError:
        print("ERROR: Missing arguments.")
        print("Please provide the name of an inference method and a filename (in the data/ directory) using this command format: './iengine <method> <filename>'")
        print("Example: './iengine TT horn_1.txt'")
        suggest_help()

    # In case of inexistent file
    except FileNotFoundError:
        print("ERROR: File not found.")
        print("Available files are:", get_available_files())
        suggest_help()

    # In case of invalid method
    except ValueError as e:
        print("ERROR:", e)
        suggest_help()