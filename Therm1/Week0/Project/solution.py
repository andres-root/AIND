from visualize import visualize_assignments


class Sudoku:

    def __init__(self, diagonal=False):
        """
        Constructor
        Input: diagonal Bool. Indicates it the sudoku is diagonal
        Output: None
        """
        self.rows = 'ABCDEFGHI'
        self.cols = '123456789'
        self.boxes = self.cross(self.rows, self.cols)
        self.diagonal_units = self.diagonal(self.rows, self.cols)
        self.row_units = [self.cross(r, self.cols) for r in self.rows]
        self.column_units = [self.cross(self.rows, c) for c in self.cols]
        self.square_units = [
            self.cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
            for cs in ('123', '456', '789')
        ]
        self.unitlist = self.row_units + self.column_units + self.square_units
        if diagonal is True:
            self.diagonal_units = self.diagonal(self.rows, self.cols)
            self.unitlist = self.unitlist + self.diagonal_units
        self.units = dict((s, [u for u in self.unitlist if s in u]) for s in self.boxes)
        self.peers = dict((s, set(sum(self.units[s], [])) - set([s])) for s in self.boxes)
        self.values = None
        self.assignments = []

    def assign_value(self, values, box, value):
        """
        Assigns a value to a given box. If it updates the board record it.
        """
        values[box] = value
        if len(value) == 1:
            self.assignments.append(values.copy())
        return values

    def cross(self, a, b):
        """
        Cross product of elements in A and elements in B.
        """
        return [s + t for s in a for t in b]

    def diagonal(self, a, b):
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

    def grid_values(self, values):
        """
        Convert grid into a dict of {square: char} with '123456789' for empties.
        Args:
            grid(string) - A grid in string form.
        Returns:
            A grid in dictionary form
                Keys: The boxes, e.g., 'A1'
                Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
        """
        values = dict(zip(self.boxes, values))
        values = {k: self.cols if v == '.' else v for (k, v) in values.items()}
        return values

    def eliminate(self, values, n=None, value=None):
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
            for peer in self.peers[box]:
                values = self.assign_value(values, peer, values[peer].replace(n, ''))
        return values

    def one_choice(self, values):
        """
        Strategy 2: Only Choice
        If there is only one box in a unit which would allow a certain digit,
        then that box must be assigned that digit.
        """
        for unit in self.unitlist:
            for n in '123456789':
                boxes = [box for box in unit if n in values[box]]
                if len(boxes) == 1:
                    values[boxes[0]] = n
        return values

    def naked_twins(self, values):
        """
        Strategy 3: Naked Twins
        If two boxes in the same unit have only two values and they are equal
        then we remove every of those values for every peer in that unit
            Args:
                values(dict): a dictionary of the form {'box_name': '123456789', ...}
            Returns:
                the values dictionary with the naked twins eliminated from peers.
        """
        unit_values = [{box: values[box] for box in unit} for unit in self.unitlist]
        for unit in unit_values:
            twins = {k: v for (k, v) in unit.items() if len(v) == 2 if list(unit.values()).count(v) > 1}
            if len(twins) > 0:
                twin_boxes = list(twins.keys())
                for k, v in twins.items():
                    for box in unit.keys():
                        if box not in twin_boxes:
                            values = self.assign_value(values, box, values[box].replace(v[0], ''))
                            values = self.assign_value(values, box, values[box].replace(v[1], ''))

        return values

    def reduce_puzzle(self, values):
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
            values = self.eliminate(values)

            # Naked twins strategy
            values = self.naked_twins(values)

            # One choice strategy
            values = self.one_choice(values)

            # Check how many boxes have a determined value, to compare
            solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
            # If no new values were added, stop the loop.
            stalled = solved_values_before == solved_values_after
            # Sanity check, return False if there is a box with zero available values:
            if len([box for box in values.keys() if len(values[box]) == 0]):
                return False
        return values

    def search(self, values):
        """
        Strategy 3: Search
        Pick a box with a minimal number of possible values.
        Try to solve each of the puzzles obtained by choosing each of these values, recursively.
        """
        values = self.reduce_puzzle(values)
        if values is False:
            return False
        if all(len(values[s]) == 1 for s in self.boxes):
            return values
        n, s = min((len(values[s]), s) for s in self.boxes if len(values[s]) > 1)
        for value in values[s]:
            new_sudoku = values.copy()
            new_sudoku = self.assign_value(new_sudoku, s, value)
            attempt = self.search(new_sudoku)
            if attempt:
                return attempt

    def display(self, values, gui=False):
        """
        Display the values as a 2-D grid.
        Args:
            values(dict): The sudoku in dictionary form
            gui(bool): Flag that indicates if gui should be shown
        """
        try:
            width = 1 + max(len(values[s]) for s in self.boxes)
            line = '+'.join(['-' * (width * 3)] * 3)
            for r in self.rows:
                g = ''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in self.cols)
                print(g)
                if r in 'CF':
                    print(line)
            if gui is True:
                visualize_assignments(self.assignments)
        except SystemExit:
            pass
        except:
            print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
        return

    def solve(self, grid, display=False, gui=False):
        """
        Find the solution to a Sudoku grid.
        Args:
            grid(string): a string representing a sudoku grid.
                Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
            display(bool): Flag that indicates we should display grid in console
            display(bool): Flag that indicates we should display grid in GUI
        Returns:
            The dictionary representation of the final sudoku grid. False if no solution exists.
        """
        self.values = self.grid_values(grid)
        self.values = self.reduce_puzzle(self.values)
        self.values = self.search(self.values)
        if display is True:
            self.display(self.values, gui)
        else:
            return self.values


if __name__ == '__main__':
    easy_unsolved = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    hard_unsolved = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    diagonal_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    sudoku = Sudoku(diagonal=True)
    sudoku.solve(diagonal_grid, display=True, gui=True)
