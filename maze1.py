import pyxel
import random
class Maze:
    def __init__(self, maze_layout, dot_color, big_dot_color, wall_color):
        self.maze_layout = maze_layout
        self.dot_color = dot_color
        self.big_dot_color = big_dot_color
        self.wall_color = wall_color

        # Initialize maze properties
        self.width = len(maze_layout[0])
        self.height = len(maze_layout)
        self.total_dots = 0
        for row in self.maze_layout:
            for dot in row:
                if dot in (0,2):
                    self.total_dots += 1
        self.big_dots = []  # List of coordinates for big dots
        
        # Place big dots randomly
        self.place_big_dots()

    def place_big_dots(self):
        self.big_dots = []
        available_spots = []

        # Find all the spots where there is a normal dot (0)
        for y in range(self.height):
            for x in range(self.width):
                if self.maze_layout[y][x] == 0:
                    available_spots.append((x, y))

        # Randomly select up to 6 spots to place the big dots
        big_dot_count = min(6, len(available_spots))
        self.big_dots = random.sample(available_spots, big_dot_count)

        # Mark those spots as big dots (special value 2 to represent big dots)
        for x, y in self.big_dots:
            self.maze_layout[y][x] = 2  # 2 represents a big dot
    
    def check_dot_collision(self, pacman_x, pacman_y, pacman):
        # Check for collision with normal and power up dots
        score_increment = 0
        if self.maze_layout[pacman_y][pacman_x] in [0, 2]:
            if self.maze_layout[pacman_y][pacman_x] == 0:
                score_increment = 10
            elif self.maze_layout[pacman_y][pacman_x] == 2:
                score_increment = 50
            self.maze_layout[pacman_y][pacman_x] = -1
            self.total_dots -= 1

        return score_increment

    def draw(self):
        # Draw the maze
        for y in range(self.height):
            for x in range(self.width):
                if self.maze_layout[y][x] == 1:
                    pyxel.rect(x * 8, y * 8, 8, 8, self.wall_color)  # Draw wall
                elif self.maze_layout[y][x] == 0:
                    pyxel.circ(x * 8 + 4, y * 8 + 4, 2, self.dot_color)  # Normal dot
                elif self.maze_layout[y][x] == 2:
                    pyxel.circ(x * 8 + 4, y * 8 + 4, 4, self.big_dot_color)  # Big dot