import random
import pyxel
import time
from pacman1 import Pacman

class Ghost:
    def __init__(self, x, y, color, speed = 1):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed  # ghost movement speed
        self.alive = True  # True if ghost is alive, False if eaten
        self.blinking = False  # True when ghost is vulnerable to being eaten
        self.respawn_time = 0
        self.stuck_timer = None
        self.last_position = None
    
    def move(self, maze_layout, pacman_x, pacman_y, power_up):
        # current_position = (self.x, self.y) # track current position
        
        # # check if ghost is stuck
        # if current_position == self.last_position:
        #     if self.stuck_timer is None:
        #         self.stuck_timer = time.time()
        #     elif time.time() - self.stuck_timer > 1: # if ghost is stuck for 1 second
        #         self.stuck_timer = None
        #         random_move = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        #         new_x = self.x + random_move[0] * self.speed
        #         new_y = self.y + random_move[1] * self.speed
        #         if maze_layout[new_y // 8][new_x // 8] != 1: # check if new move is not to the wall
        #             self.x = new_x
        #             self.y = new_y
        #         return
        # else:
        #     self.stuck_timer = None
        
        # save the current position
        # self.last_position = current_position
                
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
        min_dist = float('inf')
        max_dist = 0
            
        for dx, dy in valid_moves:
            new_x = self.x + dx * self.speed
            new_y = self.y + dy * self.speed
            distance = abs(new_x - pacman_x) + abs(new_y - pacman_y)
            
            if not power_up:
                if distance < min_dist:
                    min_dist = distance
                    chosen_move = (dx, dy)
            else:
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
                pyxel.circ(self.x, self.y, 4, pyxel.COLOR_WHITE if pyxel.frame_count % 10 < 5 else self.color)
            else:
                # draw the ghost normally
                pyxel.circ(self.x, self.y, 4, self.color)
