# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Adding the Naked Twins Strategy adds more constraints to apply in our sudoku board.

The Naked Twins Strategy looks for two squares in a unit that share only two possible values.
That's why it's called "Twin". After finding those two squares we proceedremoving the two values
in the rest of the peers in that same unit.

Constraint Propagation reduces the number of possibilitites. So by applying this new constraint
repeatedly using our reduce_puzzle() function we propagate to every unit to reduce the number of possibilities
of units that has naked twins. Therefore, we are reducing the numbers of possibilities for the entire puzzle.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Constraint Propagation reduces the number of possibilitites by combining the strategies.

We just need the necessary information to solve the  diagonals.
By addig the diagonal units and peers we can now use constraint propagation
to solve the sudoku with this new restriction. But, how?

In order to solve a normal sudoku we need to create a good representation of the information needed to solve the puzzle. 
A sudoku consists of a 9x9 grid, and the objective is to fill the grid with digits in such a way that each unit, that is to say, each row, each column, and each of the 9 principal 3x3 subsquares contains all of the digits from 1 to 9.

So, we need a list of all possible units in the board. Then we apply our reduce function to every peer in them.
Now, a diagonal sudoku adds two extra diagonal units to the puzzle, so now we have to accounf also for the main diagonals.
However if we look closely we discover that there's not really a need to apply an extra function to solve the diagonals.
If we just add the peers and diagonals to our unitlist we can then apply the same constraints using our reduce funciont for those units, solving the diagonal sudoku.


### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.