from abc import ABC, abstractmethod
from typing import Optional
import pygame

from src.maze import Maze, Coord

class ShortestPath(ABC):
    @property
    def name(self) -> str:
        return type(self).__name__

    @abstractmethod
    def run(self, maze: Maze, screen: Optional[pygame.surface.Surface] = None) -> list[Coord]:
        pass