import math
import random
import pygame as pg
import display as dsp
import constants as const

from pygame.locals import *
from copy import deepcopy

pg.init()


class Abalone(pg.sprite.Sprite):
    """
    A class used to represent a standard Abalone board.
    Both players have 14 marbles (blue and yellow).
    A white marble defines an empty spot.
    A player loses whenever 6 of his marbles are out.
    IMPORTANT: Top-left marble's position defines the position of all marbles.
    This position is given by the const.FIRST_X and const.FIRST_Y given in constants.py
    
    Parameter
    ---------
    configuration: list (optional, default=STANDARD)
        Initial positions of the marbles on the board.
        the STANDARD configuration (default) is the one commonly used in
        mainstream abalone games.
        See constants.py for more configurations.
    Attributes
    ----------
    data: list (of lists)
        List of list. Defines the state of every marble on the Abalone board.
        A state can have 3 values: 1: empty spot, 2: blue marble, 3: yellow marble
        Each list defines a row of the board.
        By convention, the first row represents the board's top row.
    blue_deadzone: list (of lists)
        Defines the zone where the blue marbles are resting in piece.
        This is purely for display purposes. It does not affect the state of the board.
    yellow_deadzone: list (of lists)
        Same than above, but for yellow marbles
    current_color: int
        Current color being played. Randomly chosen when starting a new game.
        Can take two values: 2 (blue marbles) or 3 (yellow marbles)
    scores: dict
        key: string, value: int
        Defines the score of the blue and yellow players.
        Note: this isn't really necessary as the score can be obtained by analyzing the deadzones.
        But it requires to convert the values of the deadzones into lists and count the marbles.
        So the scores dict is simply easier to work with.
    new_colors: dict
        Defines the marbles that will change color when displaying the board.
        Used for display purposes only. It does not affect the state of the board.
    new_marbles: dict
        key: tuple of ints (new marbles positions), value: int (new marbles values)
        Defines the marbles that will be changed after a valid move
    """
    
    ######### Constructor #########
    def __init__(self, configuration=const.STANDARD):
        """
        Initializes the starting configuration and all the atributes.
        Parameter
        ---------
        configuration: list (optional, default=STANDARD)
            Starting configuration. Other configurations can be found in constants.py
        """
        super().__init__()
        self.data = deepcopy(configuration)
        self.blue_deadzone = deepcopy(const.BLUE_DEADZONE)
        self.yellow_deadzone = deepcopy(const.YELLOW_DEADZONE)
        self.current_color = random.choice((2, 3))
        self.scores = {"Blue": 0, "Yellow": 0}
        self.new_colors = {}
        self.new_marbles = {}
        self.buffer_dead_marble = {}

    ######### Methods #########
    def get_enemy(self) -> int:
        """Returns the enemy of the current color being played."""
        return 3 if self.current_color == 2 else 2

    def get_center(self, loc) -> tuple:
        """
        Returns the center (tuple of ints) of a marble 
        given its corresponding location in self.data
        The center is expressed in the Pygame frame (x-pixels x y-pixels)
        Parameter
        ---------
        index: tuple of ints
            (row, column) location of a given marble in self.data
        """
        r, c = loc
        len_r = len(self.data[r])
        m_x = const.FIRST_X - const.MARBLE_SIZE * (0.5*(len_r-5) - c)
        m_x += const.MARBLE_SIZE*0.5
        m_y = const.FIRST_Y + const.MARBLE_SIZE * r
        m_y += const.MARBLE_SIZE*0.5
        return int(m_x), int(m_y)

    def get_value(self, loc) -> int:
        """
        Returns the value (int) of a specific location.
        Used for better readability only to avoid writing self.data[r][c] each time.
        Parameter
        ---------
        index: tuple of ints
            (row, column) location of a given marble in self.data
        """
        r, c = loc
        return self.data[r][c]

    def check_win(self):
        """
        Check if a player has won the game.
        Returns False if not.
        Returns the color of the corresponding player otherwise.
        """
        if self.scores["Blue"] == 6:
            return 2
        if self.scores["Yellow"] == 6:
            return 3
        return False

    def normalize_coordinates(self, position):
        """
        TODO
        """
        x, y = position
        # Getting row index
        r = (y - const.FIRST_Y) // const.MARBLE_SIZE 
        if 0 <= r < len(self.data): # len(self.data) = 9: Abalone board game has 9 rows
            len_row = len(self.data[r])
            c = (x - (const.FIRST_X - 0.5*(len_row-5) * const.MARBLE_SIZE))
            c //= const.MARBLE_SIZE
            if 0 <= int(c) in range(0, len_row):
                return r, int(c)
        return False
    
    def move_single_marble(self, origin, target) -> bool:
        """
        TODO
        """
        self.clear_buffers()
        self.new_marbles[origin] = 1 # If the move is valid, the picked marble will become free
        origin_center = self.get_center(origin)
        target_center = self.get_center(target)
        target_value = self.get_value(target)
        buffer_target = target
        friend = self.current_color
        enemy = self.get_enemy()
        colors = [friend] # To keep track of the colors we meet
        sumito = False        

        while True:        
            # Checking if we're killing a marble (this cannot occur during the first iteration)
            if not target:
                # Position of the buffer dead marble
                dead = next_spot[0], next_spot[1]
                if self.buffer_dead_marble: 
                    self.buffer_dead_marble.clear()
                last_marble = colors[-1]
                self.buffer_dead_marble[dead] = -last_marble
                return True
            else:
                target_center = self.get_center(target)
                target_value = self.get_value(target)
                    
            if target_value in (enemy, friend):
                colors.append(target_value)
            own_marble = target_value == friend
            other_marble = target_value in (enemy, 1)
            # A potential sumito occurs when the enemy color is met
            sumito = enemy in colors
            # Cannot push more than 3 marbles
            too_much_marbles = colors.count(friend) > 3
            # Checking for a potential invalid sumito
            too_much_enemy = colors.count(enemy) >= colors.count(friend)
            squeezed_enemy = enemy in colors and target_value == friend
            invalid_sumito = too_much_enemy or squeezed_enemy
            if too_much_marbles or invalid_sumito:
                self.new_colors[buffer_target] = const.MARBLE_RED # Invalid move
                return False
            # If we keep finding our own marbles
            if own_marble and target not in self.new_marbles.keys():
                self.new_marbles[target] = friend
            # Meeting an enemy or a free spot
            elif other_marble:
                if sumito:
                    if self.get_value(origin) == friend:
                        self.new_marbles[target] = friend
                    else:
                        self.new_marbles[target] = enemy
                else:
                    self.new_marbles[target] = friend
                # Loop ends if a free spot is reached
                if target_value == 1:
                    return True
            # Getting the next spot
            n_x = (target_center[0] - origin_center[0]) / const.MARBLE_SIZE
            n_y = (target_center[1] - origin_center[1]) / const.MARBLE_SIZE
            next_spot = self.next_spot(target_center, n_x, n_y)
            # Updating origin/target positions
            origin_center = target_center
            origin = self.normalize_coordinates(origin_center)
            target = self.normalize_coordinates(next_spot)
    
    def select_range(self, pick):
        """
        TODO
        """
        # No need to check as a possibility (valid or not) has been found already
        if const.MARBLE_GREEN in self.new_colors.values():
            return None
        elif const.MARBLE_RED in self.new_colors.values():
            return None 
        value = self.get_value(pick)
        if value == self.current_color:
            # Selected marble will become a free spot (if possible)
            self.new_marbles[pick] = 1 
        centers = [self.get_center(c) for c in self.new_marbles.keys()]
        # Checking range validity
        if self.check_range(value, centers):
            self.new_colors[pick] = const.MARBLE_PURPLE 
        return centers

    def check_range(self, value, centers) -> bool:
        """
        TODO
        """
        if value != self.current_color:
            return False
        if len(centers) == 2:
            p0, p1 = centers[0], centers[1]
            d_p0_p1 = self.distance(p0, p1)
            # Only neighbouring marbles can form a range of 2
            if d_p0_p1 > const.MAX_DISTANCE_MARBLE:
                return False
        if len(centers) == 3:
            p0, p1, p2 = centers[0], centers[1], centers[2]
            d_p0_p1 = self.distance(p0, p1)
            d_p0_p2 = self.distance(p0, p2)
            # A misaligned range of 3 results in an invalid range
            if int(d_p0_p2) != int(d_p0_p1*2):
                return False
        # A range of more than 3 marbles is invalid 
        elif len(centers) > 3:
            return False 
        return True 

    def new_range(self, pick, value, centers):
        """
        TODO
        """
        if value != self.current_color and len(centers) in (2, 3):
            target = self.get_center(pick)
            origin = centers[-1][0], centers[-1][1]
            nx = (target[0] - origin[0]) / const.MARBLE_SIZE
            ny = (target[1] - origin[1]) / const.MARBLE_SIZE
            new_centers = [self.next_spot(c, nx, ny) for c in centers]
            new_centers = [self.normalize_coordinates(c) for c in new_centers]
            # If new_centers cannot be all normalized, an out of bounds has been reached
            if not all(new_centers):
                nonfree_spots = False
            else:
                # If one on the new spots isn't free
                nonfree_spots = any(self.get_value(c) != 1 for c in new_centers)
            # Or if the target isn't in the neigbourhood
            not_neighbour = self.distance(centers[-1], target) > const.MAX_DISTANCE_MARBLE
            if nonfree_spots or not_neighbour:
                if const.MARBLE_RED not in self.new_colors.values():
                    self.new_colors[new_centers[-1]] = const.MARBLE_RED
                    self.new_marbles.clear()
                    return False
            # Valid move otherwise
            for new_c in new_centers:
                self.new_colors[new_c] = const.MARBLE_GREEN 
                self.new_marbles[new_c] = self.current_color
            return True
        return False
    
    def update(self) -> None:
        """Update the board and deadzones states"""
        # Updating board
        for pos, value in self.new_marbles.items():
            x, y = pos
            self.data[x][y] = value
        # Updating deadzone if killing one marble
        if self.buffer_dead_marble:
            value = next(iter(self.buffer_dead_marble.values()))
            # Getting the deadzone corresponding to the killed marble (blue or yellow)
            if value == -2:
                self.scores["Yellow"] += 1
                deadzone = self.blue_deadzone
            else:
                self.scores["Blue"] += 1
                deadzone = self.yellow_deadzone
            # Filling the deadzone with killed marble
            for pos in deadzone:
                if deadzone[pos] == 1:
                    deadzone[pos] = value
                    break
        # Updating current player's color
        self.current_color = self.get_enemy()
        
    def reset(self, configuration=const.STANDARD):
        """
        Reset and set a new game.
        Parameter
        ---------
        configuration: list (optional, default=STANDARD)
        """
        self.current_color = random.choice((2, 3))
        self.scores["Blue"] = 0
        self.scores["Yellow"] = 0
        self.data = deepcopy(configuration)
        self.blue_deadzone = deepcopy(const.BLUE_DEADZONE)
        self.yellow_deadzone = deepcopy(const.YELLOW_DEADZONE)
        self.clear_buffers()

    def clear_buffers(self):
        """Clear ????"""
        
        self.new_marbles.clear()
        self.new_colors.clear()
        self.buffer_dead_marble.clear()
            
    ######### Static Methods #########
    @staticmethod
    def next_spot(origin, n_x, n_y):
        """Compute the next spot of a marble given a vector.
        The vector defines a direction (N, S, E, O, SE, SW, NE, NW)

        Parameters
        ----------
        origin: tuple of integers (required)
            Initial marble
        n_x: double
            x-component of the vector
        n_y: double
            y_compnent of the vector
        Returns
        -------
        spot_x, spot_y: tuple of integers
            Coordinates of the next spot
        """
        spot_x = origin[0] + const.MARBLE_SIZE * n_x
        spot_y = origin[1] + const.MARBLE_SIZE * n_y
        return int(spot_x), int(spot_y)
        
    @staticmethod
    def distance(p1, p2):
        """Compute the distance between two points (p1, p2)."""
        return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def main():
    pass

if __name__ == "__main__":
    main()




