import heapq
from typing import Callable, Optional
import pygame

from src.maze import ITERATION_NODE_COLOR, START_KEY_COMB, Coord, Distances, Maze, PriorityNode
from src.shortest_path.metrics import manhattan_dist
from src.shortest_path.abstract_shortest_path import ShortestPath


class GBFS(ShortestPath):
    def __init__(self,  heuristic: Callable[[Coord, Coord], float] = manhattan_dist):
        self.heuristic = heuristic

    def run(self, maze: Maze, screen: Optional[pygame.surface.Surface] = None) -> list[Coord]:
        start_node = maze.get_start()
        maze.set_area_at(start_node)

        end_node = maze.get_end()
        maze.set_area_at(end_node)

        # g-score
        distances: Distances = {start_node: {START_KEY_COMB: 0}}

        # the float is heuristic cost to the end
        nodes_to_visit: list[PriorityNode] = [PriorityNode((0, START_KEY_COMB, start_node))]
        heapq.heapify(nodes_to_visit)

        while nodes_to_visit:
            # Get the node with the shortest heuristic distance to the end
            _, current_comb, current_node = heapq.heappop(nodes_to_visit)

            if(current_node == end_node):
                break

            # Draw the current node
            if screen is not None:
                maze.draw_node(screen, current_node, ITERATION_NODE_COLOR)

            # Get the adjacent_nodes of the current node that are reachable with current combination
            adjacent_edges = maze.get_adjacent_edges(current_node, current_comb)

            for weight, adjacent_comb, adjacent_node in adjacent_edges:
                if adjacent_node in distances and adjacent_comb in distances[adjacent_node]: continue

                distance = distances[current_node][current_comb] + weight
                distances.setdefault(adjacent_node, dict())[adjacent_comb] = distance

                priority = self.heuristic(adjacent_node, end_node)
                heapq.heappush(nodes_to_visit, PriorityNode((priority, adjacent_comb, adjacent_node)))

        return maze.get_path(distances)