assignments = []

def cross(A, B):
    #"Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

## A few global variables are defined that would be used in the functions

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols) 

diagonal_ltr = [ rows[i] + cols[i] for i in range(9)] # List of diagonal box addresses, starting from left to right (A1, B2,..)
diagonal_rtl = [ rows[8-i] + cols[i] for i in range(9)] # List of diagonal box addresses, starting from right to left (I1, H2,..)

row_units = [cross(r, cols) for r in rows] # List of row addresses
column_units = [cross(rows, c) for c in cols] # List of column addresses
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')] # List of 3X3 squares

diagonal_ltr = [ rows[i] + cols[i] for i in range(9)] # List of diagonal box addresses, starting from left to right (A1, B2,..)
diagonal_rtl = [ rows[8-i] + cols[i] for i in range(9)] # List of diagonal box addresses, starting from right to left (I1, H2,..)

unitlist = row_units + column_units + square_units # Nested list of all the units in the grid

units = dict((s, [u for u in unitlist if s in u]) for s in boxes) # Dictionary of all the units
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes) # Peers of all the units in the grid

units = dict((s, [u for u in unitlist if s in u]) for s in boxes) # Dictionary of all the units
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes) # Peers of all the units in the grid

diag_ltr = dict((s, set(diagonal_ltr) - set([s])) for s in boxes if s in diagonal_ltr) # Diagonal peer set 1: Left to Right
diag_rtl = dict((s, set(diagonal_rtl) - set([s])) for s in boxes if s in diagonal_rtl) # Diagonal peer set 2: Right to Left

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):

    # Finds all the boxes with two digit possibilities
    twins = [box for box in values.keys() if len(values[box]) == 2]

    # Among the twin set, this subroutine finds a pair that matches
    # If there is a match it searches through the two diagonal sets
    # to remove the digits in the twin set in the other boxes
    len_twins = len(twins)
    fullunitlist = row_units + column_units + square_units + diagonal_rtl + diagonal_ltr

    for i in range(len(twins) - 1):
        for j in range(i+1, len(twins)):
            if values[twins[i]] == values[twins[j]]:
                for peerunit in fullunitlist:
                    if twins[i] in peerunit and twins[j] in peerunit:
                        twin_digits = values[twins[i]]
                        for u in peerunit:
                            if values[u] == values[twins[i]]:
                                pass
                            elif len(values[u])>1:
                                for d in twin_digits:
                                    values[u] = values[u].replace(d,'')


    return values

def grid_values(grid):

    # This function replaces the empty values with all the possibilities '123456789'
    # Then zips the values with the respective cell id and returns a dictionary
    new_values = []
    for val in grid:
        if val == ".":
            new_values.append('123456789')
        else:
            new_values.append(val)

    return(dict(zip(boxes, new_values)))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):

    ## This function looks at the peers groups of each box and eliminates the redundancies

    ## There are three peer groups: Two diagonal sets, and the 'regular' sudoku peer group--rows, columns and square units

    ## First the solved values are identified from the length of their values (if length = 1, then it is a solved value)
    ## Then each peer group is iterated to remove these solved values from the set


    ## Set 1 & 2 : Diagonals from left to right [A1, B2, C3...I9] and right to left [I1, H2, ...A9]
    diagonal_list = [diag_ltr, diag_rtl]

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for diagonals in diagonal_list:
            if box in diagonals.keys():
                for diag in diagonals[box]:
                    values[diag] = values[diag].replace(digit, '')
    

    ## Set 3: Regular Sudoku Peer group: Rows, Columns and 3X3 square units

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'') 

    
    return values

def only_choice(values):


    ## This function checks the duplicates of possiblities in the peer group and isolates the 'only choice'
    ## similar to 'eliminate' function, it searches the three peer groups in the puzzle
    ## Three peer groups: Two diagonal groups and the regular sudoku peer group

    ## It loops through every digit, keeps a digit counter. 
    ## First, it loops through the peer group units, and the counter is updated when it finds the digit in the box
    ## At the end of the loop, if the digit count is '1', then the cell which contains that value is assigned that digit

    ## Set 1: Regular sudoku peer group
                
    for digit in '123456789':
        for sq in unitlist:
            digit_count = 0
            for each_sq in sq:
                if digit in values[each_sq]:
                    digit_count = digit_count + 1
            if digit_count == 1:
                for each_sq in sq:
                    if digit in values[each_sq]:
                        values[each_sq] = digit 

        ## Set 2: Diagonal group left to right: [A1, B2, ... I9]

        digit_count = 0
        for diag in diagonal_ltr:
            if digit in values[diag]:
                digit_count = digit_count + 1
        if digit_count == 1:
            for diag in diagonal_ltr:
                if digit in values[diag]:
                    values[diag] = digit


        ## Set 3: Diagonal group right to left: [I1, H2, ... A9]

        digit_count = 0
        for diag in diagonal_ltr:
            if digit in values[diag]:
                digit_count = digit_count + 1
        if digit_count == 1:
            for diag in diagonal_ltr:
                if digit in values[diag]:
                    values[diag] = digit


    return values

def reduce_puzzle(values):

    ## This function takes the narrowed down possibilities and reduces the puzzle using the different strategies
    ## The solved values are retained
    ## Rest of the boxes go through the eliminate, only_choice and naken_twins strategies for reduction
    ## The process is repeated until there cannot be any more reduction
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):

    ## Depth-first search is used to solve the sudoku grids that is obtained after reduction

    values = reduce_puzzle(values) ## Reduces the puzzle until there is no choice to reduce further
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    val = grid_values(grid) # uses the grid_values function to get the dictionary representation 
    final_sudoku = search(val) ## Reduces the puzzle, and depth-first search is conducted until a solution is found

    return final_sudoku


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    

    ## A few global variables are defined that would be used in the functions  
    '''rows = 'ABCDEFGHI'
    cols = '123456789'
    boxes = cross(rows, cols) # List of box addresses in the sudoku grid
 
    row_units = [cross(r, cols) for r in rows] # List of row addresses
    column_units = [cross(rows, c) for c in cols] # List of column addresses
    square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')] # List of 3X3 squares

    diagonal_ltr = [ rows[i] + cols[i] for i in range(9)] # List of diagonal box addresses, starting from left to right (A1, B2,..)
    diagonal_rtl = [ rows[8-i] + cols[i] for i in range(9)] # List of diagonal box addresses, starting from right to left (I1, H2,..)

    unitlist = row_units + column_units + square_units # Nested list of all the units in the grid

    units = dict((s, [u for u in unitlist if s in u]) for s in boxes) # Dictionary of all the units
    peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes) # Peers of all the units in the grid

    diag_ltr = dict((s, set(diagonal_ltr) - set([s])) for s in boxes if s in diagonal_ltr) # Diagonal peer set 1: Left to Right
    diag_rtl = dict((s, set(diagonal_rtl) - set([s])) for s in boxes if s in diagonal_rtl) # Diagonal peer set 2: Right to Left'''

    solved_puzzle = solve(diag_sudoku_grid) # Calls the solve function to obtain the solved puzzle

    # If the sudoku grid is solved, then the output is visualized
    # Else the program gives the output as 'False'
    if solved_puzzle == False:
        print(False)
    else:
        display(solved_puzzle)

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
