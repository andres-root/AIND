

class Sudoku:

    def __init__(self):
        self.rows = 'ABCDEFGHI'
        self.cols = '123456789'
        self.boxes = self.cross(self.rows, self.cols)
        self.row_units = [self.cross(r, self.cols) for r in self.rows]
        self.column_units = [self.cross(self.rows, c) for c in self.cols]
        self.square_units = [
            self.cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
            for cs in ('123', '456', '789')
        ]
        self.unitlist = self.row_units + self.column_units + self.square_units

    def cross(self, a, b):
        return [s + t for s in a for t in b]

    def grid_values(self, unsolved):
        unsolved = dict(zip(self.boxes, unsolved))
        unsolved = {k: self.cols if v == '.' else v for (k, v) in unsolved.items()}
        return unsolved

    def display(self, unsolved):
        """
        Display the values as a 2-D grid.
        Input: The sudoku in dictionary form
        Output: None
        """
        values = self.grid_values(unsolved)
        width = 1 + max(len(values[s]) for s in self.boxes)
        line = '+'.join(['-' * (width * 3)] * 3)
        for r in self.rows:
            g = ''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in self.cols)
            print(g)
            if r in 'CF':
                print(line)
        return

    def solve(self):
        return True

if __name__ == '__main__':
    sudoku = Sudoku()
    print(sudoku.display('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'))
