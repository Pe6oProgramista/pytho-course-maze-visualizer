from src.maze import Coord
from src.shortest_path.metrics import manhattan_dist, euclidean_dist

def test_manhattan_dist():
    c1 = Coord((1, 1))
    c2 = Coord((4, 5))
    expected = 7
    assert manhattan_dist(c1, c2) == expected

    c1 = Coord((3, 4))
    c2 = Coord((0, 0))
    expected = 7
    assert manhattan_dist(c1, c2) == expected

def test_euclidean_dist():
    c1 = Coord((1, 1))
    c2 = Coord((4, 5))
    expected = 25
    assert euclidean_dist(c1, c2) == expected

    c1 = Coord((3, 4))
    c2 = Coord((0, 0))
    expected = 25
    assert euclidean_dist(c1, c2) == expected
