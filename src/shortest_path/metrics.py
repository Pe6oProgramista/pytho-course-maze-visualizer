from src.maze import Coord

def manhattan_dist(c1: Coord, c2: Coord) -> float:
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])

def euclidean_dist(c1: Coord, c2: Coord) -> float:
    return (c1[0] - c2[0])**2 + (c1[1] - c2[1])**2