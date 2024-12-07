import pyxel
import time

class Pacman:
    def __init__(self, x, y, speed, color):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.power_up_active = False
        self.power_up_timer = 300
        self.direction = None

    def handle_input(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.direction = 'UP'
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.direction = 'DOWN'
        elif pyxel.btnp(pyxel.KEY_LEFT):
            self.direction = 'LEFT'
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            self.direction = 'RIGHT'

    def move(self, maze_layout):
        if self.power_up_active:
            self.power_up_timer -= 1  # decrease power up time

        if self.power_up_timer <= 0:  # power up ends when timer reaches zero
            self.power_up_active = False
        
        new_x, new_y = self.x, self.y

        if self.direction == 'UP':
            new_y -= self.speed
        elif self.direction == 'DOWN':
            new_y += self.speed
        elif self.direction == 'LEFT':
            new_x -= self.speed
        elif self.direction == 'RIGHT':
            new_x += self.speed

        # Check collision with walls
        cell_x = new_x // 8  # Assuming each cell is 8x8 pixels
        cell_y = new_y // 8

        if maze_layout[cell_y][cell_x] != 1:  # Only move if the new cell is not a wall
            self.x, self.y = new_x, new_y
            
    def eat_big_dot(self):
        self.power_up_active = True
        self.power_up_timer = 300 # 5 second power up

    def draw(self):
        pyxel.circ(self.x, self.y, 4, self.color)
