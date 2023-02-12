from typing import Iterator, NewType, Optional
import pygame
from math import sqrt
from collections import deque

from src.maze.key_comb import KeyCombination
from src.maze.pixel import Pixel, PixelType

WALL_COLOR = (0, 0, 0)
START_COLOR = (195, 195, 196)
END_COLOR = (126, 127, 127)
PATH_COLOR = (0, 0, 255)
ITERATION_NODE_COLOR = (255, 0, 255)

KEY_WIDTH = 20
KEY_HEIGHT = 20

END_NODE_HASHED_COORD = (-1, -1)
KEYCOMB_JUST_ONES_HASHED_VALUE = -1

START_KEY_COMB = KeyCombination()

Coord = NewType('Coord', tuple[int, int])
Edge = NewType('Edge', tuple[float, KeyCombination, Coord])
PriorityNode = NewType('PriorityNode', tuple[float, KeyCombination, Coord])
Distances = dict[Coord, dict[KeyCombination, float]]

class MazeException(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

class Maze:
    def __init__(self, image: pygame.surface.Surface) -> None:
        super().__init__()

        self.keys: dict[tuple[int, int, int], int] = dict()
        self.map: dict[Coord, Pixel] = dict()
        self.width = 0
        self.height = 0
        self.image = image

        self.load_map(image)

    def load_map(self, image: pygame.surface.Surface) -> None:
        self.map = dict()

        for x in range(image.get_width()):
            for y in range(image.get_height()):
                r, g, b, _ = image.get_at((x,y))
                self.map[Coord((x,y))] = Pixel((r, g, b))

        self.width = image.get_width()
        self.height = image.get_height()
        self.image = image

    def pixel_at(self, coord: Coord) -> Pixel:
        if coord not in self.map:
            raise MazeException(f'Invalid map coords: {coord}')

        return self.map[coord]

    def get_start(self) -> Coord:
        for key, value in self.map.items():
            if value.color == START_COLOR:
                return key

        raise MazeException('No starting point')

    def get_end(self) -> Coord:
        for key, value in self.map.items():
            if value.color == END_COLOR:
                return key

        raise MazeException('No ending point')

    def get_adjacent_edges(self, node: Coord, key_comb: KeyCombination) -> Iterator[Edge]:
        for adjacent_coord in self.get_adjacent_coords(node):
            if self.pixel_at(adjacent_coord).type == PixelType.UNSET:
                self.set_area_at(adjacent_coord)
            
            if self.pixel_at(adjacent_coord).type == PixelType.WALL: continue

            weight: float = 1 # self.pixel_at(adjacent_coord).color[0] if self.pixel_at(adjacent_coord).is_grey() else 1
            if adjacent_coord[0] != node[0] and adjacent_coord[1] != node[1]:
                weight *= sqrt(2)

            adjacent_key_comb = key_comb
            if self.pixel_at(adjacent_coord).type == PixelType.KEY:
                key_pos = self.keys.setdefault(self.pixel_at(adjacent_coord).color, len(self.keys))
                adjacent_key_comb = key_comb.set_at(key_pos)
            elif self.pixel_at(adjacent_coord).type == PixelType.ZONE:
                key_pos = self.keys.get(self.pixel_at(adjacent_coord).color) # type: ignore # It gives: 'Incompatible types in assignment (expression has type 'Optional[int]', variable has type 'int')'
                if key_pos is None or key_comb != key_comb.set_at(key_pos): continue

            yield Edge((weight, adjacent_key_comb, adjacent_coord))

    def get_adjacent_coords(self, coord: Coord) -> Iterator[Coord]:
        return (Coord((coord[0]+i, coord[1]+j)) for i in range(-1, 2) for j in range(-1, 2) 
            if ((i != 0) ^ (j != 0)) and
                (0 <= coord[0]+i < self.width) and
                (0 <= coord[1]+j < self.height))

    def set_area_at(self, coord: Coord) -> None:
        pixel: Pixel = self.pixel_at(coord)

        if pixel.color == WALL_COLOR:
            pixel.type = PixelType.WALL
        elif pixel.is_grey():
            pixel.type = PixelType.FREE
        else:
            pixel.type = PixelType.ZONE
            if pixel.color == START_COLOR: pixel.type = PixelType.START
            if pixel.color == END_COLOR: pixel.type = PixelType.END
            
            max_height, min_height, max_width, min_width = coord[1], coord[1], coord[0], coord[0]

            key_pixels: list[Pixel] = [pixel]
            wave: deque[Coord] = deque([coord])

            while wave:
                curr_coord = wave.pop()
                curr_pixel = self.pixel_at(curr_coord)

                for adjacent_coord in self.get_adjacent_coords(curr_coord):
                    adjacent_pixel = self.pixel_at(adjacent_coord)

                    if (adjacent_pixel.color != curr_pixel.color or
                        adjacent_pixel.type != PixelType.UNSET):
                        continue

                    adjacent_pixel.type = curr_pixel.type

                    wave.append(adjacent_coord)
                    if max_height < adjacent_coord[1]: max_height = adjacent_coord[1]
                    if min_height > adjacent_coord[1]: min_height = adjacent_coord[1]
                    if max_width < adjacent_coord[0]: max_width = adjacent_coord[0]
                    if min_width > adjacent_coord[0]: min_width = adjacent_coord[0]

                    # Add elements to key_pixels while there is a chance this zone to be a key
                    if (curr_pixel.type == PixelType.ZONE and
                        max_height - min_height + 1 <= KEY_HEIGHT and
                        max_width - min_width + 1 <= KEY_WIDTH and
                        len(key_pixels) < KEY_HEIGHT * KEY_WIDTH): # length of key_pixels cant be greater with this limitations of width and height
                        
                        key_pixels.append(adjacent_pixel)
                    elif len(key_pixels) != 0:
                        key_pixels.clear()

            if (pixel.type == PixelType.ZONE and
                max_height - min_height + 1 == KEY_HEIGHT and
                max_width - min_width + 1 == KEY_WIDTH and
                len(key_pixels) == KEY_HEIGHT * KEY_WIDTH):
                
                for key_pixel in key_pixels:
                    key_pixel.type = PixelType.KEY

    def draw_node(self, screen: pygame.surface.Surface, coord: Coord, color: Optional[tuple[int, int, int]] = None) -> None:
        if not color: color = self.pixel_at(coord).color

        screen.set_at(tuple(coord), color)
        pygame.display.update(pygame.Rect(coord[0], coord[1], 1, 1))

    def draw_path(self, screen: pygame.surface.Surface, path: list[Coord]) -> None:
        screen.blit(self.image, (0,0))
        pygame.display.update()
        for node in path:
            self.draw_node(screen, node, PATH_COLOR)

    def get_path(self, distances: Distances, end_node: Optional[Coord] = None) -> list[Coord]:
        # start_node: Coord = self.get_start()
        if end_node is None: end_node = self.get_end()

        if end_node not in distances:
            raise MazeException('Missing end_node in distances')

        path = []

        curr_node = end_node
        key_comb, min_dist = min(distances[end_node].items(), key=lambda comb_dist: comb_dist[1])

        while self.pixel_at(curr_node).type != PixelType.START or key_comb != START_KEY_COMB:
            next_node = curr_node
            
            # Get all neighbors and use only those that appear in distances
            # to find the one that is closer to the start
            for adjacent_coord in self.get_adjacent_coords(curr_node):
                adjacent_node = Coord(adjacent_coord)
                if adjacent_node not in distances or \
                    key_comb not in distances[adjacent_node]: continue

                if distances[adjacent_node][key_comb] < min_dist:
                    next_node = adjacent_node
                    min_dist = distances[adjacent_node][key_comb]
            
            # If we are still at the current node and its a key then
            # remove the key from key_comb and continue the loop with the same
            # node to check if it has neighbors with the new key_comb
            # If we came back to this key (key_comb bit for this key is unset) or
            # the node is not key then it dont have neighbors with shorter distance to the start
            # and raise and exception
            if next_node == curr_node:
                color = self.pixel_at(next_node).color
                if self.pixel_at(next_node).type == PixelType.KEY and \
                    key_comb.is_set_at(self.keys[color]):
                    
                    key_comb = key_comb.unset_at(self.keys[color])
                else:
                    raise MazeException('There is no path but end node is reachable')
            
            else:
                path.append(next_node)
                curr_node = next_node

        return path[::-1]



__all__ = ['WALL_COLOR', 'START_COLOR', 'END_COLOR', 'PATH_COLOR', 'ITERATION_NODE_COLOR', 'KEY_WIDTH', 'KEY_HEIGHT', 'END_NODE_HASHED_COORD', 'KEYCOMB_JUST_ONES_HASHED_VALUE', 'START_KEY_COMB', 'Coord', 'Edge', 'PriorityNode', 'Distances', 'MazeException', 'Maze']