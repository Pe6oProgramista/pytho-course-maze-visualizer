import heapq
from typing import Optional
import pygame

from src.maze import ITERATION_NODE_COLOR, START_KEY_COMB, Coord, Distances, Maze, MazeException, PriorityNode
from src.shortest_path.abstract_shortest_path import ShortestPath

class Dijkstra(ShortestPath):
    def run(self, maze: Maze, screen: Optional[pygame.surface.Surface] = None) -> list[Coord]:
        start_node = maze.get_start()
        maze.set_area_at(start_node)

        end_node = maze.get_end()
        maze.set_area_at(end_node)

        # Distances from start_node to all reached nodes
        distances: Distances = {start_node: {START_KEY_COMB: 0}}

        # Nodes that have to be checked
        nodes_to_visit: list[PriorityNode] = [PriorityNode((0, START_KEY_COMB, start_node))]
        heapq.heapify(nodes_to_visit)

        min_end_dist: Optional[float] = None

        while nodes_to_visit:
            # Get the node with the shortest distance from start
            current_dist, current_comb, current_node = heapq.heappop(nodes_to_visit)

            # skip the nodes that will not improve the path to the end (the neighbor check below dont do all the work because if have not reached the end yet we add some nodes that can be away from the end when we find it)
            if min_end_dist is not None and current_dist >= min_end_dist:
                continue

            # Draw the current node
            if screen is not None:
                maze.draw_node(screen, current_node, ITERATION_NODE_COLOR)

            # Get the adjacent_nodes of the current node that are reachable with current combination
            adjacent_edges = maze.get_adjacent_edges(current_node, current_comb)

            for weight, adjacent_comb, adjacent_node in adjacent_edges:
                distance = current_dist + weight

                # Update distance only if it can imporve the distance to the current neighbor
                # and the min distance to the end
                if (adjacent_node not in distances or adjacent_comb not in distances[adjacent_node] or distance < distances[adjacent_node][adjacent_comb]) and \
                    (min_end_dist is None or distance < min_end_dist):
                    
                    distances.setdefault(adjacent_node, dict())
                    distances[adjacent_node][adjacent_comb] = distance

                    if adjacent_node == end_node:
                        min_end_dist = distance
                    else:
                        heapq.heappush(nodes_to_visit, PriorityNode((distance, adjacent_comb, adjacent_node)))

        if min_end_dist is None:
            raise MazeException('No path to the end node')
        
        # Get the final path through distances
        return maze.get_path(distances)