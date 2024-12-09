import random
import pyxel
import time
from pacman import Pacman

class Ghost:
    def __init__(self, x, y, img, u, v, w, h, colkey, speed = 1):
        self.start_x = x
        self.start_y = y
        self.img = img # image bank (for sprite loading)
        self.u = u # x coordinate of the sprite
        self.v = v # y coordinate of the sprite
        self.w = w # width of the sprite
        self.h = h # height of the sprite
        self.colkey = colkey # transparency
        self.x = x # x coordinate
        self.y = y # y coordinate
        self.speed = speed  # ghost movement speed
        self.alive = True  # True if ghost is alive, False if eaten
        self.blinking = False  # True when ghost is vulnerable to being eaten
        self.respawn_time = 0
        
    '''property and setter for x coordinate'''
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self._x = value
        else:
            raise ValueError('Incorrent type')
    
    '''property and setter for y coordinate'''
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self._y = value
        else:
            raise ValueError('Incorrent type')

    '''propery and setter for speed'''
    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self._speed = value
        else:
            raise ValueError('Incorrent type')

    '''propery and setter for alive'''
    @property
    def alive(self):
        return self._alive
    
    @alive.setter
    def alive(self, value):
        if isinstance(value, bool):
            self._alive = value
        else:
            raise ValueError('Incorrent type')
    
    '''propery and setter for blinking'''
    @property
    def blinking(self):
        return self._blinking
    
    @blinking.setter
    def blinking(self, value):
        if isinstance(value, bool):
            self._blinking = value
        else:
            raise ValueError('Incorrent type')
    
    def move(self, maze_layout, pacman_x, pacman_y, power_up):
        valid_moves = []
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)] # up, down, left, right respectively
        
        '''I will use Manhattan distances to calculate the shortest path to pacman'''
        for dx, dy in directions:
            new_x = self.x + dx * self.speed
            new_y = self.y + dy * self.speed   
            if maze_layout[new_y // 8][new_x // 8] != 1:  # not a wall
                valid_moves.append((dx, dy))
            
        if not valid_moves:
            return # no possible moves, dont move
            
        chosen_move = None
        min_dist = float('inf') # set to infinity to find min distance
        max_dist = 0 # set to 0 to find max distance 
            
        for dx, dy in valid_moves:
            new_x = self.x + dx * self.speed
            new_y = self.y + dy * self.speed
            distance = abs(new_x - pacman_x) + abs(new_y - pacman_y) # calculate distance
            
            if not power_up: # ghosts are moving towards the pacman
                if distance < min_dist:
                    min_dist = distance
                    chosen_move = (dx, dy)
            else: # ghosts are running away from pacman
                if distance > max_dist:
                    max_dist = distance
                    chosen_move = (dx, dy)
                
        if not chosen_move:
            return
            
        # move the ghost
        self.x += chosen_move[0] * self.speed
        self.y += chosen_move[1] * self.speed
        
    def become_vulnerable(self):
        self.blinking = True

    def reset_vulnerability(self):
        self.blinking = False

    def get_eaten(self):
        self.alive = False  # ghost is eaten
        self.respawn_time += pyxel.frame_count + 180 # 3 seconds to resplawn
        self.x, self.y = -100, -100 # move of screen for that time
    
    # respawn ghost
    def update(self):
        if not self.alive and pyxel.frame_count >= self.respawn_time:
            self.reset_position()
    
    def reset_position(self):
        self.x, self.y = self.start_x, self.start_y  # starting position, can be adjusted as needed
        self.alive = True
        self.reset_vulnerability()

    def draw(self):
        if self.alive:
            if self.blinking:
                # alternate between white and the ghosts original color
                pyxel.blt(self.x, self.y, self.img, 20, 36, 8, 8, self.colkey)
            else:
                # draw the ghost normally
                pyxel.blt(self.x, self.y, self.img, self.u, self.v, self.w, self.h, self.colkey)
