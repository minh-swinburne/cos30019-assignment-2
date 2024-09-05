# COS30019 Assignment 2 - Inference Engine for Propositional Logic

## Description

This project is an inference engine developed for the Assignment 2 of course unit COS30019 - Introduction to Artificial Intelligence. It uses various logical inference methods to derive conclusions from a given knowledge base.

### General Information

* Programming Language: Python 3.12.3 (should work for Python 3.10 or higher)
* Objective: Provided a knowledge base ***KB*** and a query ***Q***, the inference engine will determine whether ***Q*** can be entailed from ***KB***.
* The program is designed to be executed with a CLI (e.g. Powershell for Windows).

### Implemented Inference Methods

* **Truth Table**: Evaluates all possible models. Sound and complete.
* **Forward Chaining**: Starts with the symbols known to be true and iteratively adds symbols to the knowledge base. Sound and complete for *Horn clauses*.
* **Backward Chaining**: Starts with the query and recursively tries to prove the query by proving its antecedents. Sound and complete for *Horn clauses*.
* **Resolution Theorem Proving**: Converts the KB to Conjunctive Normal Form (CNF) and negates the query, and recursively applies the resolution rule to derive new clauses until a contradiction is found.
* **Davis-Putnam-Logemann-Loveland (DPLL)**: Converts the KB to Conjunctive Normal Form (CNF) and negates the query, and recursively applies unit propagation and pure literal elimination to derive new clauses until a contradiction is found.

## Installation and Running

Before running the program, ensure that you have **Python 3.10 or higher** installed on your system. Then, follow these steps to set up a virtual environment and install the necessary packages:

1. Clone this repository to your local machine.
2. Create a virtual environment:

   ```
   python -m venv venv
   ```
3. Activate the virtual environment:

   * On Windows:

     ```
     .\venv\Scripts\activate
     ```
   * On macOS and Linux:

     ```
     source venv/bin/activate
     ```
4. Install the required packages:

   ```
   pip install -r requirements.txt
   ```
5. You can run the program with this command:

   ```
   ./iengine <method> <filename>
   ```

   Replace `<method>` with one of these method names:

   * `TT` for Truth Table
   * `FC` for Forward Chaining
   * `BC` for Backward Chaining
   * `RES` for Resolution
   * `DPLL` for DPLL

   Replace `<filename>` with a filename in the ***data/*** folder (not including the folder itself).

   For example, to run Truth Table checking for problem defined in file *horn_1.txt*:

   ```
   ./iengine TT horn_1.txt
   ```

   Output follows the standard stated in the assignment instruction: YES if the query ***Q*** can be entailed from ***KB***. TT, FC and BC also display additional information.
6. To use custom files, add the *.txt* file to the ***data/*** folder. Files are assumed to be in valid format, consisting of both the knowledge base and the query:

   * The knowledge base follows the keyword TELL and consists of Horn clauses separated by semicolons.
   * The query follows the keyword ASK and consists of a proposition symbol.
   * Additionally, there is an option to provide the expected result for the problem - keyword `EXPECT` followed by either `YES` or `NO` in a new line (refer to existing files for examples). This will not change the actual result of the inference, but can be used for debugging and performance analysis, because some methods may not give identical results when given the same data.

   For example, a file might look like this:

   ```
   TELL
   a=>b; a;
   ASK
   b
   EXPECT
   YES
   ```

   In this example, `a=>b; a;` is the knowledge base, `b` is the query, and `YES` is the expected result.
7. For help and more information, run the command:

   ```
   ./iengine help
   ```

   It will show lists of available inference methods and how to run the program.

## How It Works

1. First, the program will read the given filename and split the text string into knowledge base, query, and optionally expected result.
2. They will then be sanitized and tokenized, before parsed into appropriate logic syntax (implemented in `parser.py` and `syntax` package).
3. The `syntax` package includes classes to represent propositional logic components, specifically:
   * `Connective`: Represents the connectives used in propositional logic.
   * `Sentence`: The fundamental class, representing a sentence in propositional logic. It is an abstract class that is inherited by other classes.
   * `Symbol`: Represents a symbol, or positive literal, for example *A* or *B*.
   * `Negation`: Represents the negation of a sentence, for example *~A*.
   * `CommutativeSentence`: Represents a commutative sentence. A commutative sentence is a sentence that has a connective that is commutative, meaning that the order of the arguments does not matter.
     A commutative sentence must have at least 2 arguments.
   * `Conjunction`: Represents the logical AND (∧) of multiple sentences.
   * `Disjunction`: Represents the logical OR (∨) of multiple sentences.
   * `Implication`: Represents the logical implication (→) between two sentences.
   * `Biconditional`: Represents the logical biconditional (↔) between two sentences.
4. The logic syntax classes have some helpful methods, like `evaluate()` for **Truth Table** checking or `negate()` to get the negation of a sentence.
5. For **Forward Chaining** and **Backward Chaining**, a warning message will be displayed if the knowledge base and query do not satisfy Horn Form
6. For **Resolution** and **DPLL**, the knowledge base and query will be converted to CNF and combined into a set of clauses.

## Performance Evaluation

The `analyze.py` file in the root folder provides a simple tool to evaluate and analyze the performance of the algorithms in terms of result accuracy, memory usage, and execution time, utilizing Python packages like collections, timeit and tracemalloc. To run the script, use the command:

```
python analyze.py <method> <filename>
```

Or you can run the `iengine` command but with the `--analyze` option:

```
./iengine <method> <filename> --analyze [--number <number>]
```

### Arguments:

* `<method>`: an inference method name, as listed above (default is **TT** if left empty).
* `<filename>`: a filename in the ***data/*** folder (default is *horn_1.txt* if left empty when running as main script).
* `<number>`: the number of times the inference should be executed to measure the average computation time from (default is 100).

### Output

```
Information:
  - Filename
  - Method
  - Knowledge Base / Tell
  - Query / Ask
  - Expected Result (if defined)

Result:
  - Entails (YES or NO)

Performance:
  - Memory used in bytes
  - Average execution time in milliseconds
  - Accuracy
```

## Testing

Multiple unit tests have been implemented for the modules of the program using the `unittest` package. Unit test scripts are stored in the ***tests/*** folder.

For methods testing, we use the `debug.py` script in the root folder.

## Contributing

This project is a collaborative effort between Quang Thien and Thanh Minh. We both have contributed significantly to the development and success of this project.

## License

This project is licensed under the MIT License.
