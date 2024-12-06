import random
import pyxel

class Ghost:
    def __init__(self, x, y, color, speed = 1):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed  # ghost movement speed
        self.alive = True  # True if ghost is alive, False if eaten
        self.blinking = False  # True when ghost is vulnerable to being eaten
    
    def move(self, maze_layout, pacman_x, pacman_y):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)] # up, down, left, right respectively
        random.shuffle(directions)
        
        '''I will use Manhattan distances to calculate the shortest path to pacman'''
        distances = []
        for dx, dy in directions:
            new_x = self.x + dx * 8
            new_y = self.y + dy * 8
            distance = abs(new_x - pacman_x) + abs(new_y - pacman_y)
            distances.append((distance, (dx, dy)))
            
        distances.sort() # sort the distances, so the shortest path to pacman comes first
        for _, (dx, dy) in distances:
            new_x = self.x + dx * self.speed
            new_y = self.y + dy * self.speed
            if maze_layout[new_y // 8][new_x // 8] != 1: # ensure there is no wall
                self.x = new_x
                self.y = new_y
                break
        
    def become_vulnerable(self):
        self.blinking = True

    def reset_vulnerability(self):
        self.blinking = False

    def get_eaten(self):
        if self.blinking:
            self.alive = False  # ghost is eaten
            self.reset_position()  # respawn at the initial position
    
    def reset_position(self):
        self.x, self.y = 16, 16  # starting position, can be adjusted as needed
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
