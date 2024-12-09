import pyxel
import time

class Pacman:
    def __init__(self, x, y, speed):
        pyxel.load('my_resource.pyxres') # load the resources
        self.x = x
        self.y = y
        self.speed = speed
        self.power_up_active = False
        self.power_up_timer = 0
        self.direction = None
        self.power_up_limit = 5
    
    '''property and setter for x coodrinate'''
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self._x = value
        else:
            raise ValueError('Incorrent type')

    '''property and setter for y coodrinate'''
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self._y = value
        else:
            raise ValueError('Incorrent type')

    '''property and setter for speed'''
    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self._speed = value
        else:
            raise ValueError('Incorrent type')

    '''property and setter for power_up_active'''
    @property
    def power_up_active(self):
        return self._power_up_active

    @power_up_active.setter
    def power_up_active(self, value):
        if isinstance(value, bool):
            self._power_up_active = value
        else:
            raise ValueError('Incorrent type')

    '''property and setter for power_up_timer'''
    @property
    def power_up_timer(self):
        return self._power_up_timer

    @power_up_timer.setter
    def power_up_timer(self, value):
        if isinstance(value, (int, float)):
            self._power_up_timer = value
        else:
            raise ValueError('Incorrent type')

    '''property and setter for power_up_limit'''
    @property
    def power_up_limit(self):
        return self._power_up_limit

    @power_up_limit.setter
    def power_up_limit(self, value):
        if isinstance(value, int) and value >= 0:
            self._power_up_limit = value
        else:
            raise ValueError('Incorrent type')

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
            
    def eat_big_dot(self): # get power-up
        self.power_up_timer = time.time()
        self.power_up_active = True

    def draw(self):
        if self.direction == 'UP':
            pyxel.blt(self.x, self.y, 0, 36, 36, 8, 8, 0)
        elif self.direction == 'RIGHT':
            pyxel.blt(self.x, self.y, 0, 4, 4, 8, 8, 0)
        elif self.direction == 'LEFT':
            pyxel.blt(self.x, self.y, 0, 36, 20, 8, 8, 0)
        elif self.direction == 'DOWN':
            pyxel.blt(self.x, self.y, 0, 36, 4, 8, 8, 0)