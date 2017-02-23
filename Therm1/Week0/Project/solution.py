
assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'


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
    """
    Strategy 3: Naked Twins
    If two boxes in the same unit have only two values and they are equal
    then we remove every of those values for every peer in that unit
        Args:
            values(dict): a dictionary of the form {'box_name': '123456789', ...}
        Returns:
            the values dictionary with the naked twins eliminated from peers.
    """
    unit_values = [{box: values[box] for box in unit} for unit in unitlist]
    for unit in unit_values:
        twins = {k: v for (k, v) in unit.items() if len(v) == 2 if list(unit.values()).count(v) > 1}
        if len(twins) > 0:
            twin_boxes = list(twins.keys())
            for k, v in twins.items():
                for box in unit.keys():
                    if box not in twin_boxes:
                        values = assign_value(values, box, values[box].replace(v[0], ''))
                        values = assign_value(values, box, values[box].replace(v[1], ''))

    return values


def cross(A, B):
    """
    Cross product of elements in A and elements in B.
    """
    return [s + t for s in A for t in B]


def diagonal(a, b):
    """
    Returns the two diagonal units
    """
    rows = list(a)
    cols = list(b)
    left_diag = []
    right_diag = []
    i = 0
    for e in rows:
        left_diag.append(e + cols[i])
        i += 1
    i = 8
    for e in rows:
        right_diag.append(e + cols[i])
        i -= 1
    return [left_diag, right_diag]

boxes = cross(rows, cols)
diagonal_units = diagonal(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [
    cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
    for cs in ('123', '456', '789')
]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)
diagonal_units = diagonal(rows, cols)
unitlist = unitlist + diagonal_units


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = dict(zip(boxes, grid))
    values = {k: cols if v == '.' else v for (k, v) in values.items()}
    return values


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        g = ''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in cols)
        print(g)
        if r in 'CF':
            print(line)
    return


def eliminate(values):
    """
    Strategy 1: Elimination
    If a box has a value assigned, then none of the peers of this box can
    have this value.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    solved_boxes = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_boxes:
        n = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(n, ''))
    return values


def only_choice(values):
    """
    Strategy 2: Only Choice
    If there is only one box in a unit which would allow a certain digit,
    then that box must be assigned that digit.
    """
    for unit in unitlist:
        for n in '123456789':
            boxes = [box for box in unit if n in values[box]]
            if len(boxes) == 1:
                values[boxes[0]] = n
    return values


def reduce_puzzle(values):
    """
    Combines each strategy to find a solution.
    If a solution is found we return the values.
    If no solution is found we stop trying.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Eliminate strategy
        values = eliminate(values)

        # Naked twins strategy
        values = naked_twins(values)

        # One choice strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """
    Strategy 3: Search
    Pick a box with a minimal number of possible values.
    Try to solve each of the puzzles obtained by choosing each of these values, recursively.
    """
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku = assign_value(new_sudoku, s, value)
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
    values = grid_values(grid)
    values = reduce_puzzle(values)
    values = search(values)
    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
