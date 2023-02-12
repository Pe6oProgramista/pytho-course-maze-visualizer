from typing import Optional
import pygame
import time

from src.maze import Maze, Coord
from src.shortest_path import ShortestPath

BACKGROUND_COLOR = (0, 0, 0)
TEXT_OFFSET_DOWN_Y = 50
BUTTON_COLOR = (255, 100, 100)
FONT_COLOR = (255, 255, 255)
BUTTONS_START_X = 700
BUTTONS_START_OFFSET_X = 50
BUTTONS_START_Y = 50
BUTTONS_OFFSET_Y = 100

Buttons = list[tuple[ShortestPath, pygame.surface.Surface, pygame.rect.Rect]]

class VisualizerException(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

class Visualizer:
    def __init__(self, file_name, algorithms: list[ShortestPath], width=800, height=600):
        if not algorithms:
            raise VisualizerException('Please provide at least one algorithm to the visualizer')

        self.width = width
        self.height = height
        self.current_algorithm = algorithms[0]
        self.path: list[Coord] = []

        self.running = True

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Maze Path Visualizer')

        # Load the image
        image = pygame.image.load(file_name)
        self.maze = Maze(image)

        self.font = pygame.font.SysFont('Arial', 20)

        # Create buttons for each algorithm
        self.buttons: Buttons = list()
        max_width = 0
        for alg in algorithms:
            button_text, button_rect = self.create_button(alg.name, (BUTTONS_START_X, BUTTONS_START_Y))
            if button_rect.width > max_width:
                max_width = button_rect.width
            self.buttons.append((alg, button_text, button_rect))
        
        for i, button in enumerate(self.buttons):
            x = self.width - max_width - BUTTONS_START_OFFSET_X
            y = BUTTONS_START_Y + i * BUTTONS_OFFSET_Y
            button[2].topleft = (x, y)

    def render_time(self, time: Optional[float] = None) -> None:
        text = 'Elapsed time:' + (f'{time:.4f} seconds' if time else '')
        
        # Create TimeBox
        time_surface = self.font.render(text, False, FONT_COLOR)
        time_rect = time_surface.get_rect()

        x = self.width / 2 - time_rect.width / 2
        y = self.height - TEXT_OFFSET_DOWN_Y
        time_rect.topleft = (x, y)
        
        tmp_rect = pygame.Rect(0, y, self.width, self.height)
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, tmp_rect)
        self.screen.blit(time_surface, time_rect)
        pygame.display.update(tmp_rect)

    def create_button(self, text: str, pos: tuple[int, int]) -> tuple[pygame.surface.Surface, pygame.rect.Rect]:
        button_text = self.font.render(text, False, FONT_COLOR)
        button_rect = button_text.get_rect()
        button_rect.topleft = pos
        return button_text, button_rect

    def run(self):
        # Draw the image on the screen
        self.screen.blit(self.maze.image, (0, 0))

        # Draw the buttons
        for button in self.buttons:
            pygame.draw.rect(self.screen, BUTTON_COLOR, button[2])
            self.screen.blit(button[1], button[2])

        pygame.display.update()
        a = 5
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    # Get the mouse click position
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    for button in self.buttons:
                        if button[2].collidepoint(mouse_x, mouse_y):
                            # Redraw the image on the screen
                            self.screen.blit(self.maze.image, (0, 0))
                            self.render_time()
                            pygame.display.update()

                            self.current_algorithm = button[0]
                            
                            start_time = time.time()
                            self.path = self.current_algorithm.run(self.maze, self.screen)
                            end_time = time.time()
                            elapsed_time = end_time - start_time
                            
                            self.maze.draw_path(self.screen, self.path)
                            self.render_time(elapsed_time)
                            
                            print(f'Algorithm {self.current_algorithm.name} running!')       
                        
            # wait for a while
            # pygame.time.wait(100)
            
        pygame.quit()