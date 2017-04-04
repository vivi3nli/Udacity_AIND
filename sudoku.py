# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 16:29:53 2017

@author: v-fanhli
"""

rows = 'ABCDEFGHI'
cols = '123456789'
kl6

def cross(a,b):
    '''
    imput: 2 string standing for cols and rows
    output: a list including all boxs in board
    '''
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
'''
row_units[r]
will go through all the cols and the only row as imput
Element example:
row_units[0] = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
This is the most top row
'''

column_units = [cross(rows, c) for c in cols]
'''
column_units[0] = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
'''

square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
'''
square_units[0] = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
'''
diaginal_units = [[rows[i] + cols[i] for i in range(9)],[rows[i] + cols[8 - i] for i in range(9)]]
'''
[['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'],
 ['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]
'''
unitlist = row_units + column_units + square_units
unitlist_dia = diaginal_units + unitlist

#first version of grid, with '.' standing for empty box
def grid_values_1(grid):
    """
    Convert grid string into {<box>: <value>} dict with '.' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """
    #this is my solution and it passed the test
    fill = {}
    for i in range(len(boxes)):
        fill[boxes[i]] = grid[i]
    return fill
    #this is udacity's
def grid_values_answer(grid):
    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
    return dict(zip(boxes, grid))
 
# Apply the strategy of elimination to fill in the empty boxes
def grid_values(grid):
    """
    Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    #this is my solution and it passed the test
    fill = {}
    for i in range(len(boxes)):
        if grid[i] == '.':
            fill[boxes[i]] = "123456789"
            #after reading it more carefully I found the part below wrong
            #and commenting it out would be fine
            """
            fill[boxes[i]] = ""
            for j in '123456789':
                if j not in (row_units[i // 9] and column_units[i % 9] and square_units[i // 9]):
                    fill[boxes[i]] += j
            """
        else:
            fill[boxes[i]] = grid[i]
    return fill
    #this is udacity's solution
def grid_values_answers(grid):
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

def eliminate1(values):
    """
    Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    #this is my solution and it worked
    for key in values:
        if len(values[key]) == 1:
            for i in range(9): #going through all the units
#                unit_keys = ''    
                if key in row_units[i]: #find the unit this key in
                    for unit_keys in row_units[i]:
                        if unit_keys != key:
                            values[unit_keys] = values[unit_keys].replace(values[key],"")
                if key in column_units[i]: 
                    for unit_keys in column_units[i]:
                        if unit_keys != key:
                            values[unit_keys] = values[unit_keys].replace(values[key],"")
                if key in square_units[i]: 
                    for unit_keys in square_units[i]:
                        if unit_keys != key:
                            values[unit_keys] = values[unit_keys].replace(values[key],"")
    assert len(values) == 81
    return values
    #this is udacity's solution
def eliminate_answers(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1] #all the boxes with 1 item 
    #the step above is essential cause actually this is manipulating the dict
    #and if I did't record all the 1 item box at first, as I'm processing there might 
    #be new box of 1 item emerging
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

    #in the utils.py we've got two supplimentary dicts
    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    '''
    for s in boxes: #traversing every boxes in the grid
        for u in unitlist:
            if s in u:
                units[s] += u
    '''
    peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
    '''
    for s in boxes:
        peers[s] = set(sum(units[s].[])) - set([s])
        
    # sum(a list of lists,[]) returns a list containing all objects included in previous lists
    # set(sum(a list of lists,[])) returns a set with no two elements in common
    # set([s]) is converting a list to a set so that two sets can do calculation
    # so peers[key] is a type set
    '''
def eliminate(values):
    #this is my second try
    #write a peers dict in my word
    peers_lfh = {}
    for key in boxes: #every box's symbols
        peers_lfh[key] = []    
        for ul in unitlist:
            if key in ul:
                peers_lfh[key] += ul #creat a dict with every box need to be considerd
        peers_lfh[key] = set(peers_lfh[key])#removed the duplicates
#   print(peers_lfh)
    solved_values = []
    for key in values:
        if len(values[key]) == 1:
            solved_values.append(key)
    for key in solved_values:
        for unit_keys in peers_lfh[key]:
            if unit_keys != key:
                values[unit_keys] = values[unit_keys].replace(values[key],"")
#    assert len(values) == 81 #assume value is a standard grid
    return values

#my first and failed try
def only_choice1(values):
    """
    Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    # TODO: Implement only choice strategy here
    unsolved_values = [box for box in values.keys() if len(values[box]) > 1]
    for box in unsolved_values:
        for num in values[box]:  #number char in a str
            count = 0
            for peerbox in peers[box]:  #key of peer box 
            #this is not working cause every unit follows a set of rules 
            #it's too strict to ask every number not existing in all peerboxs
                if num in values[peerbox]:
                    count += 1
#            print(count)
            if count == 0:
                values[box] = num
    return values
#this is my second try
def only_choice(values):
    for unit in unitlist:
        for digit in "123456789":
            count = 0
            for box in unit:
                if digit in values[box]:
                    count += 1
#                    print(count)
            if count == 1:                
                for box in unit:
                    if digit in values[box]:
                        values[box] = digit
    return values
#this is udacity's code
def only_choice_answer(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

#out = eliminate(grid_values("..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."))
#only_choice(out)
#
grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
values = reduce_puzzle(grid_values(grid2))

#cannot solve this one without referring to answers
def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values == False:#if solution don't exist
        return False
    if max(len(values[s]) for s in boxes) == 1:
        return values #problem solved and this is the base case
    else:
        min_unsolved = min(len(values[s]) for s in boxes if len(values[s]) > 1)
    # Choose one of the unfilled squares with the fewest possibilities
    test = ''
    for key in boxes:
        if len(values[key]) == min_unsolved:
            test = key
    for value in values[test]:
        test_values = values.copy() #values should keep the same
        #what if I don't do the copy？ I cannot go back cause the original one is gone
        test_values[test] = value #give values of the try to the new grid
        attempt = search(test_values)
        if attempt: 
        #if false just go back and search the other, if true, it's the solution.
        #just curious will it cover all the possible solutions? definitely not
            return attempt
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!

    # If you're stuck, see the solution.py tab!
def search_answer(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
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




















