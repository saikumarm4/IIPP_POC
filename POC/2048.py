"""
Clone of 2048 game.
"""

import poc_2048_gui
import random
# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # replace with your code from the previous mini-project
    temp_list = [0] * len(line);
    count = 0;
    for number in line:
        if number != 0:
            temp_list[count] = number;
            count +=1;
    for loop_var in range(len(temp_list)-1):
        if temp_list[loop_var] == temp_list[loop_var+1]:
            temp_list[loop_var] += temp_list[loop_var+1]
            temp_list[loop_var+1:-1] = temp_list[loop_var+2:];
            temp_list[-1] =0;
            
    return temp_list;

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self._height = grid_height
        self._width = grid_width
        self._new_game = True
        self._grid_2048 = []
        self._initial_tiles = {}
        self._initial_tiles[UP] = [ [0, dummy_col] for dummy_col in range(self._width)]
        self._initial_tiles[DOWN] = [ [self._height - 1, dummy_col] for dummy_col in range(self._width)]        
        self._initial_tiles[RIGHT] = [ [dummy_row, self._width -1] for dummy_row in range(self._height)]
        self._initial_tiles[LEFT] = [ [dummy_row, 0] for dummy_row in range(self._height)]
        self.reset()
       
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # replace with your code
        self._new_game = True
        self._grid_2048 = [ [0 for dummy_col in range(self._width)]
                           for dummy_row in range(self._height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        grid_representation = ""
        for row in range(self._height):
            for col in range(self._width):
                grid_representation += str(self._grid_2048[row][col]) + " "
            grid_representation += "\n"
        return grid_representation

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        list_size = 0
        test_for_change = False
        
        if direction == UP or direction == DOWN:
            list_size = self._height
        else:
            list_size = self._width
            
        for initial_tile in self._initial_tiles[direction]:
            temp_list = []
            for index in range(list_size):
                temp_list.append(self._grid_2048[initial_tile[0] + index*OFFSETS[direction][0]][initial_tile[1] + index*OFFSETS[direction][1]])
            merged_list = merge(temp_list)
             
            for index in range(list_size):
                if self._grid_2048[initial_tile[0] + index*OFFSETS[direction][0]][initial_tile[1] + index*OFFSETS[direction][1]] != merged_list[index]:
                    test_for_change = True
                self._grid_2048[initial_tile[0] + index*OFFSETS[direction][0]][initial_tile[1] + index*OFFSETS[direction][1]] = merged_list[index]
        if test_for_change:
            self.new_tile()
                                 
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
        tile_position = (random.randrange(self._height), random.randrange(self._width))
        if not self._new_game:
            while 1:
                if self._grid_2048[tile_position[0]][tile_position[1]] == 0:
                    break
                else:
                    tile_position = (random.randrange(self._height), random.randrange(self._width))
        self._new_game = False
        if random.randrange(100) < 90:
            self._grid_2048[tile_position[0]][tile_position[1]] = 2;
        else:
            self._grid_2048[tile_position[0]][tile_position[1]] = 4;

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # replace with your code
        self._grid_2048[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self._grid_2048[row][col]
    
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
