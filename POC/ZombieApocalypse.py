"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for row, col in self._zombie_list: 
            yield (row, col)

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for row, col in self._human_list: 
            yield (row, col)
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        
        grid_height, grid_width = self.get_grid_height(), self.get_grid_width()
        
        visited = poc_grid.Grid(grid_height, grid_width)
        distance_field = [ [grid_height * grid_width for dummy_row in range(grid_width)]\
                         for dummy_col in range(grid_height)]
               
        entity_list = []
        if entity_type == ZOMBIE: 
            entity_list = self._zombie_list
        else: 
            entity_list = self._human_list
            
        boundary = poc_queue.Queue()
        for row, col in entity_list:
            boundary.enqueue((row, col))
            visited.set_full(row, col)
            distance_field[row][col] = 0
        
        while len(boundary) != 0:
            current_cell = boundary.dequeue()
            neighbors = self.four_neighbors(current_cell[0], current_cell[1])
            for neighbor in neighbors:
                if self.is_empty(neighbor[0], neighbor[1]) and\
                visited.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue((neighbor[0], neighbor[1]))
                    distance_field[neighbor[0]][neighbor[1]] =\
                    distance_field[current_cell[0]][current_cell[1]] + 1

        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """ 
        for idx in range(len(self._human_list)):
            neighbors = self.eight_neighbors(self._human_list[idx][0],
                                             self._human_list[idx][1])
            maximum = -1
            move_to = []
            maxval = self.get_grid_height() * self.get_grid_width()
            for neighbor in neighbors:
                if maxval > zombie_distance_field[neighbor[0]][neighbor[1]] > maximum:
                    maximum = zombie_distance_field[neighbor[0]][neighbor[1]]
                    move_to = [neighbor,]
                elif maxval > zombie_distance_field[neighbor[0]][neighbor[1]] >= maximum:
                    move_to.append(neighbor)
            self._human_list[idx] = move_to[random.randrange(len(move_to))]
            
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for idx in range(len(self._zombie_list)):
            neighbors = self.four_neighbors(self._zombie_list[idx][0],
                                             self._zombie_list[idx][1])
            minimum = self.get_grid_height() * self.get_grid_width() - 1
            move_to = []
            no_move = 0
            for neighbor in neighbors:
                if human_distance_field[neighbor[0]][neighbor[1]] < minimum:
                    minimum = human_distance_field[neighbor[0]][neighbor[1]]
                    move_to = [neighbor, ]
                elif human_distance_field[neighbor[0]][neighbor[1]] == minimum:
                    move_to.append(neighbor)
                    no_move += 1
            if no_move == len(neighbors) - 1:
                pass
            else:
                self._zombie_list[idx] = move_to[random.randrange(len(move_to))]

#apoc = Apocalypse(3,3)
#print apoc.compute_distance_field(poc_zombie_gui.ZOMBIE)
# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40))
