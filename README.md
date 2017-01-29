# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  

The approach is similar to the 'eliminate' strategy, except that in this case, we are identifying pairs of 2-digit values, and are eliminating those digits from the rest of the 'unit' group (columns, rows, square units, diagonals) Here are the steps that was following to implement this:

	1. Identify all the 2-digit values in the given grid
	
	2. Construct a nested for loop with the twin value list to identify if there is a match
	
	3. If yes, loop through each set of unit groups (columns, rows, squares, left-to-right diagonals, and right-to-left diagonals), and check if the matched pair exists in the unit group. 
	
	4. If the pair exists, then remove the digits of the values of matched pair from the rest of the values in the unit group (sanity check: length of the values are checked. This operation is carried out only if the length is more than 1).
	
	5. Iterate the loop for all the unit groups

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  

A constraint on diagonals that they should have unique values is similar to the constraint we already have on regular Sudoku on column units, row units and square units.

So, in order to implement this, two sets of diagonals are created: Left-to-right (A1, B2, C3....I9), and Right-to-left (I1, H2, G3,....A9). They are zipped to their respective values to create diagonal dictionaries.

Then, an additional constraint on unit list is made in all the three solve strategies: eliminate, only_choice and naked_twins. The unit list which previously consisted of rows, columns and squares now have diagonals, and the constraint makes sure each unit list consist of unique values.

