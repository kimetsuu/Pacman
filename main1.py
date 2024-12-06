import pyxel
from pacman1 import Pacman
from maze1 import Maze
from ghost1 import Ghost

class App:
    def __init__(self):
        pyxel.init(240, 128)

        self.game_paused = False
        self.ghosts = [
            Ghost(32, 32, pyxel.COLOR_RED),
            Ghost(64, 32, pyxel.COLOR_CYAN),
            Ghost(32, 64, pyxel.COLOR_ORANGE),
            Ghost(64, 64, pyxel.COLOR_PINK),
        ]

        # Predefined maze layouts
        self.mazes = [
            [
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
                [1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,0,0,0,0,0,1],
                [1,0,1,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1],
                [1,0,0,0,1,1,1,0,1,0,1,1,1,1,0,1,0,1,1,1,1,0,0,0,1,1,1,0,0,0,1],
                [1,1,1,0,1,0,1,0,1,0,1,0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,1,0,1,1,1],
                [1,0,0,0,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,0,0,0,1],
                [1,0,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,1,0,1],
                [1,0,0,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1,0,0,0,1],
                [1,1,1,0,1,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,1,0,1,1,1],
                [1,0,0,0,1,1,1,0,1,0,1,1,1,1,0,1,0,1,1,1,1,0,1,0,1,1,1,0,0,0,1],
                [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1],
                [1,0,0,0,0,0,1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1],
                [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ]
        ]

        # Create the first maze
        self.current_maze_index = 0
        self.maze = Maze(
            maze_layout = self.mazes[self.current_maze_index],
            dot_color=pyxel.COLOR_YELLOW,
            big_dot_color = pyxel.COLOR_RED,
            wall_color = pyxel.COLOR_DARK_BLUE,
        )
        self.pacman = Pacman(x = 200, y = 16, speed = 2, color = pyxel.COLOR_YELLOW)
        self.score = 0
        
        print(f"Pacman initialized at ({self.pacman.x}, {self.pacman.y})")
        
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_paused:
            # show 'game over' text on the screen (in draw method)
                if pyxel.btnp(pyxel.KEY_R):
                    self.restart_game()
                elif pyxel.btnp(pyxel.KEY_Q):                        
                    pyxel.quit()
                return
                    
        self.pacman.handle_input()
        self.pacman.move(self.maze.maze_layout)
        
        # Update ghosts
        for ghost in self.ghosts:
            ghost.move(self.maze.maze_layout, self.pacman.x, self.pacman.y)
            
        for ghost in self.ghosts:
            if abs(ghost.x - self.pacman.x) < 8 and abs(ghost.y - self.pacman.y) < 8:
                if ghost.blinking:
                    ghost.alive = False  # ghost is eaten
                    self.score += 200   # add points for eating a ghost
                else:
                    self.game_paused = True
                    break
                    
                    
        # Collision detection with dots
        score_increment = self.maze.check_dot_collision(self.pacman.x // 8, self.pacman.y // 8, self.pacman)
        self.score += score_increment

        # Check if maze is complete
        if self.maze.total_dots == 0:
            self.current_maze_index += 1
            if self.current_maze_index < len(self.mazes):
                self.maze = Maze(
                    maze_layout = self.mazes[self.current_maze_index],
                    dot_color = pyxel.COLOR_YELLOW,
                    big_dot_color = pyxel.COLOR_RED,
                    wall_color = pyxel.COLOR_DARK_BLUE,
                )
                self.pacman.x, self.pacman.y = 16, 16
            else:
                pyxel.quit()
                
    def restart_game(self):
        self.current_maze_index = 0
        self.maze = Maze(
            maze_layout = self.mazes[self.current_maze_index],
            dot_color=pyxel.COLOR_YELLOW,
            big_dot_color = pyxel.COLOR_RED,
            wall_color = pyxel.COLOR_DARK_BLUE,
        )
        self.pacman = Pacman(x = 200, y = 16, speed = 2, color = pyxel.COLOR_YELLOW)
        self.score = 0
        
        self.ghosts = [
            Ghost(32, 32, pyxel.COLOR_RED),
            Ghost(64, 32, pyxel.COLOR_CYAN),
            Ghost(32, 64, pyxel.COLOR_ORANGE),
            Ghost(64, 64, pyxel.COLOR_PINK),
        ]
        self.game_paused = False

    def draw(self):
        pyxel.cls(0)
        self.maze.draw()
        self.pacman.draw()
        
        # Draw ghosts
        for ghost in self.ghosts:
            ghost.draw()

        # Draw the score
        pyxel.text(5, 5, f"Score: {self.score}", pyxel.COLOR_WHITE)
        
        if self.pacman.power_up_active:
            pyxel.text(5, 20, "Power up active", pyxel.COLOR_GREEN)
        
        # draw 'Game Over' text
        if self.game_paused:
            pyxel.text(50, 60, 'GAME OVER', pyxel.COLOR_RED)
            pyxel.text(35, 80, "PRESS 'R' TO RESTART OR 'Q' TO QUIT", pyxel.COLOR_WHITE)


App()
