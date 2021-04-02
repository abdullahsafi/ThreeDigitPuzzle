# ThreeDigitPuzzle

Overview of the puzzle :mag_right:
----------------
Given are two 3-digit numbers called 𝑆 (start) and 𝐺 (goal) and also a set of 3-digit numbers called
_𝑓𝑜𝑟𝑏𝑖𝑑𝑑𝑒𝑛_. To solve the puzzle, we want to get from 𝑆 to 𝐺 in the smallest number of moves. A move is a
transformation of one number into another number by adding or subtracting 1 to one of its digits. For
example, a move can take you from 123 to 124 by adding 1 to the last digit or from 953 to 853 by subtracting
1 from the first digit. Moves must satisfy the following constraints:
1. You cannot add to the digit 9 or subtract from the digit 0;
2. You cannot make a move that transforms the current number into one of the forbidden numbers;
3. You cannot change the same digit twice in two successive moves.
Note that since the numbers have 3 digits, at the beginning there are at most 6 possible moves from 𝑆. After
the first move, the branching factor is at most 4, due to the constraints on the moves and especially due to
constraint 3.
For the purpose of this assignment numbers starting with 0, e.g. 018, are considered 3-digit numbers.

Input and Output
----------------
To run the program:
`python ThreeDigits.py B sample.txt`

- The first argument `B` can be replaced by a single letter representing the algorithm to search with, out of B for BFS, D for DFS, I for IDS, G for
Greedy, A for A*, H for Hill-climbing.
- The second argument should specify a filename of a file to open for the search details that contains three lines:
  - start-state
  - goal-state
  - forbidden1,forbidden2,forbidden3,…,forbiddenN (optional)
- The `sample.txt` is an example provided in the repository 
