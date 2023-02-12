import heapq
from typing import Callable, Optional
import pygame

from src.maze import ITERATION_NODE_COLOR, START_KEY_COMB, Coord, Distances, Maze, MazeException, PriorityNode
from src.shortest_path.metrics import manhattan_dist
from src.shortest_path.abstract_shortest_path import ShortestPath


class AStar(ShortestPath):
    def __init__(self,  heuristic: Callable[[Coord, Coord], float] = manhattan_dist):
        self.heuristic = heuristic

    def run(self, maze: Maze, screen: Optional[pygame.surface.Surface] = None) -> list[Coord]:
        start_node = maze.get_start()
        maze.set_area_at(start_node)

        end_node = maze.get_end()
        maze.set_area_at(end_node)

        # g-score
        distances: Distances = {start_node: {START_KEY_COMB: 0}}

        # the float is f-score(real distance + heuristic)
        nodes_to_visit: list[PriorityNode] = [PriorityNode((0, START_KEY_COMB, start_node))]
        heapq.heapify(nodes_to_visit)

        min_end_dist: Optional[float] = None

        while nodes_to_visit:
            # Get the node with the shortest f-score from start
            current_f_score, current_comb, current_node = heapq.heappop(nodes_to_visit)

            # Skip the nodes that will not improve the path to the end (the neighbor check below dont do all the work because if have not reached the end yet we add some nodes that can be away from the end when we find it)
            if min_end_dist is not None and current_f_score >= min_end_dist:
                continue

            # Draw the current node
            if screen is not None:
                maze.draw_node(screen, current_node, ITERATION_NODE_COLOR)

            # Get the adjacent_nodes of the current node that are reachable with current combination
            adjacent_edges = maze.get_adjacent_edges(current_node, current_comb)

            for weight, adjacent_comb, adjacent_node in adjacent_edges:
                distance = distances[current_node][current_comb] + weight

                # Update distance only if it can imporve the distance to the current neighbor
                # and the min distance to the end
                if (adjacent_node not in distances or adjacent_comb not in distances[adjacent_node] or distance < distances[adjacent_node][adjacent_comb]) and \
                    (min_end_dist is None or distance < min_end_dist):
                    
                    distances.setdefault(adjacent_node, dict())
                    distances[adjacent_node][adjacent_comb] = distance

                    # Update the end distance if we reached it and push just nodes different than the end
                    # because we cant improve the end after we have already passed it once
                    if adjacent_node == end_node:
                        min_end_dist = distance
                    else:
                        priority = distance + self.heuristic(adjacent_node, end_node)
                        heapq.heappush(nodes_to_visit, PriorityNode((priority, adjacent_comb, adjacent_node)))

        if min_end_dist is None:
            raise MazeException('No path to the end node')

        return maze.get_path(distances)