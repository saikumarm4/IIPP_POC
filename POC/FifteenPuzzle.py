"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """
    
    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._cyclic_cases = 	{
                        "DOWN" : "lddru",
                        "LEFT" : "ldru",
                        "RIGHT" : "rdlu"
                    }
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # replace with your code
        if self._grid[target_row][target_col] != 0:
            return False
        for col in range(target_col + 1, self._width):
            if self._grid[target_row][col] != self._width * target_row + col:
                return False
        for row in range(target_row + 1, self._height):
            for col in range(self._width):
                if self._grid[row][col] != self._width * row + col:
                    return False
        return True
    
    def move_zero_to_target_position(self, target_row, target_col):
        """
        To get the required string to rach target_row, target_col
        """
        zero_current_position = self.current_position(0, 0)
        target_position_string = ""
        if target_col - zero_current_position[1] > 0:
            target_position_string += 'r' * abs(target_col - zero_current_position[1])
        else:
            target_position_string += 'l' * abs(target_col - zero_current_position[1])
        if target_row - zero_current_position[0] > 0:
            target_position_string += 'd' * abs(target_row - zero_current_position[0])
        else:
            target_position_string += 'u' * abs(target_row - zero_current_position[0])
            
        self.update_puzzle(target_position_string)
        
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # replace with your code
        # assert self.lower_row_invariant(target_row, target_col)
        # Leverage the fact the lower_row_invariant(target_row, target_col) is true
        final_move_string = ""
        puzzle_clone = self.clone()
        
        assert puzzle_clone.lower_row_invariant(target_row, target_col)
        target_position = puzzle_clone.current_position(target_row, target_col)
        
        move_zero_target = "" + "u" * (target_row - target_position[0])
        if target_col - target_position[1] > 0:
            move_zero_target += "l" * abs(target_col - target_position[1])
        else:
            move_zero_target += "r" * abs(target_col - target_position[1])
        
        final_move_string += move_zero_target
        puzzle_clone.update_puzzle(move_zero_target)
        
        if (target_row, target_col) == puzzle_clone.current_position(target_row, target_col):
            self.update_puzzle(final_move_string)
            return final_move_string
        
        solve_string = self._cyclic_cases["DOWN"]
        current_zero_pos = puzzle_clone.current_position(0, 0)
        current_target_pos = puzzle_clone.current_position(target_row, target_col)
        
        if current_zero_pos[0] < current_target_pos[0]:
            pass
        elif current_zero_pos[1] > current_target_pos[1]:
            final_move_string += self._cyclic_cases["LEFT"]
            puzzle_clone.update_puzzle(self._cyclic_cases["LEFT"])
            while puzzle_clone.current_position(target_row, target_col)[1] != target_col:
                final_move_string += "ldrul"
                puzzle_clone.update_puzzle("ldrul")
        else:
            final_move_string += self._cyclic_cases["RIGHT"]
            puzzle_clone.update_puzzle(self._cyclic_cases["RIGHT"])
            while puzzle_clone.current_position(target_row, target_col)[1] != target_col:
                final_move_string += "rdlur"
                puzzle_clone.update_puzzle("rdlur")
        
        while (target_row, target_col) != puzzle_clone.current_position(target_row, target_col):
            final_move_string += solve_string
            puzzle_clone.update_puzzle(solve_string)
        
        final_move_string += "ld"
        self.update_puzzle(final_move_string)
        return final_move_string
            
    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code
        puzzle_clone = self.clone()
        puzzle_clone.update_puzzle("ur")
        if puzzle_clone.current_position(target_row, 0) == (target_row, 0):
            moving_to_end = "r" * (self._width - 2)
            self.update_puzzle("ur" + moving_to_end)
            return "ur" + moving_to_end
        else:
            final_move_string = ""
            puzzle_clone = self.clone()
            target_pos = puzzle_clone.current_position(target_row, 0)
            if target_pos[1] == 0:
                final_move_string = "u" * (target_row - target_pos[0])
                puzzle_clone.update_puzzle(final_move_string)
                while (target_row - 1, 0) != puzzle_clone.current_position(target_row, 0):
                    print puzzle_clone.current_position(target_row, 0)
                    final_move_string += "rddlu"
                    puzzle_clone.update_puzzle("rddlu")
                final_move_string += "rdl"
                puzzle_clone.update_puzzle("rdl")
                final_move_string += "ruldrdlurdluurddlur" + "r" * (self._width - 2)
                self.update_puzzle(final_move_string)
                return final_move_string
            else:
                final_move_string = ""
                final_move_string = "u" * (target_row - target_pos[0]) + "r" * (target_pos[1])
                puzzle_clone.update_puzzle(final_move_string)
                
                while target_row - 1 != (puzzle_clone.current_position(target_row, 0))[0]:
                    final_move_string += "dlurd"
                    puzzle_clone.update_puzzle("dlurd")
                    
                final_move_string += "ulld"
                puzzle_clone.update_puzzle("ulld")
                while (target_row -1, 1) != puzzle_clone.current_position(target_row, 0):
                    final_move_string += "rulld"
                    puzzle_clone.update_puzzle("rulld")
                final_move_string += "ruldrdlurdluurddlur" + "r" * (self._width - 2)
                self.update_puzzle(final_move_string)
                return final_move_string
    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        if (1, target_col) != self.current_position(1, target_col) or\
        (0, target_col) != self.current_position(0, 0):
            return False
        for row in range(0, min(2, self._height)):
            for col in range(target_col + 1, self._width):
                if (row, col) != self.current_position(row, col):
                    return False
        for row in range(2, self._height):
            for col in range(self._width):
                if (row, col) != self.current_position(row, col):
                    return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        zero_position = self.current_position(0, 0)
        if zero_position != (1, target_col):
            return False
        for col in range(target_col + 1, self._width):
            if self.current_position(zero_position[0], col) != (zero_position[0], col):
                return False
        for row in range(zero_position[0] + 1, self._height):
            for col in range(self._width):
                if self.current_position(row, col) != (row, col):
                    return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        puzzle_clone = self.clone()
        puzzle_clone.update_puzzle("ld")
        if (0, target_col) == puzzle_clone.current_position(0, target_col):
            self.update_puzzle("ld")
            return "ld"
        else:
            target_pos = self.current_position(0, target_col)
            if target_pos[0] == 1:
                self.update_puzzle("l" * (target_col - target_pos[1]))
                final_move_string = "l" * (target_col - target_pos[1])
                return self.solve_row0_iterator(target_col, final_move_string)
            else:
                self.update_puzzle("l" * (target_col - target_pos[1] - 1) + "dlu")
                final_move_string = "l" * (target_col - target_pos[1] - 1) + "dlu"
                return self.solve_row0_iterator(target_col, final_move_string)

    def solve_row0_iterator(self, target_col, final_move_string):
        """
        Helper function for cyclic function
        """
        count_rs  = final_move_string.count("l")
        iterator_string = "r" * (count_rs - 1)+ "dl"
        
        while True:
            final_move_string += iterator_string
            self.update_puzzle(iterator_string)
            if self.current_position(0, target_col) == (1, target_col - 1) and\
                                   self.current_position(0, 0) == (1, target_col - 2):
                                   break
            if iterator_string.count("r") == 0:
                tag = "l" * max(0, iterator_string.count("r") - 1) + "ur"
            else:
                tag = "l" * max(0, iterator_string.count("r") - 1) + "u"
            
            final_move_string += tag
            self.update_puzzle(tag)
            
        final_move_string += "urdlurrdluldrruld"
        self.update_puzzle("urdlurrdluldrruld")
        return final_move_string
                                   
    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        target_pos = self.current_position(1, target_col)
        if target_pos[1] == target_col:
            self.update_puzzle("u")
            return "u"
        elif target_pos[0] == 1:
            final_move_string = "" + "l" * (target_col - target_pos[1])
            self.update_puzzle(final_move_string)
            while (1, target_col) != self.current_position(1, target_col):
                final_move_string += "urrdl"
                self.update_puzzle("urrdl")
            self.update_puzzle("ur")
            return final_move_string + "ur"
        elif target_pos[1] < target_col and target_pos[0] == 0:
            final_move_string = "u" + "l" * (target_col - target_pos[1])
            self.update_puzzle(final_move_string)
            while target_col != self.current_position(1, target_col)[1]:
                final_move_string += "drrul"
                self.update_puzzle("drrul")
            final_move_string += "dru"
            self.update_puzzle("dru")
            return final_move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        cases = {
                    (0, 0) : "rdlu",
                    (0, 1) : "dlur",
                    (1, 0) : "urdl",
                    (1, 1) : "lurd"
                }
        zero_pos = self.current_position(0, 0)
        idx = 0
        final_move_string = ""
        while self.current_position(0, 0) != (0, 0):
            final_move_string += cases[zero_pos][idx % 4]
            self.update_puzzle(cases[zero_pos][idx % 4])
            idx += 1
        if self.current_position(0, 0) == (0, 0) and self.current_position(0, 1) == (1, 1):
            while not self.status_2x2():
                final_move_string += "rdlu"
                self.update_puzzle("rdlu")
            return final_move_string
        else:
            while not self.status_2x2():
                final_move_string += "drul"
                self.update_puzzle("drul")
            return final_move_string

    def status_2x2(self):
        """
        checking status of 2x2 puzzle
        """
        return self.current_position(0, 0) == (0, 0) and\
        self.current_position(0, 1) == (0, 1) and\
        self.current_position(1, 0) == (1, 0) and\
        self.current_position(1, 1) == (1, 1)
    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        return ""

# Start interactive simulation
# poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))

def test():
    """
    To Test multiple test scenarios
    """
    puzzle = Puzzle(4, 4)
    poc_fifteen_gui.FifteenGUI(puzzle)
    
#test()


