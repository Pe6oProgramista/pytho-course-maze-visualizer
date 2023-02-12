'''
examples.example02
'''

from src.shortest_path import Dijkstra, AStar, GBFS
from src.visualizer import Visualizer

if __name__ == '__main__':
    algorithms = [Dijkstra(), AStar(), GBFS()]
    v = Visualizer('examples/02.input20x20.bmp', algorithms)
    v.run()
