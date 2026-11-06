from typing import Dict, List, Tuple

#each orientation with its bit value
N = 1 #wall at north 0001
E = 2 #wall at east 0010
S = 4 #wall at south 0100
W = 8 #wall at wewst 1000
ALL = N | E | S | W #all sides walled 1111

# IMPORTANT. direction is used to determine where youll move to.

# For example if youre at (y=3, x=2) and you move N youll end up at (y=2, x=2).
# Moving N from (3, 2) to (2, 2) means removing the N wall from (3, 2) and the S wall from (2, 2).
# Hence N has S as the third value in the dict. It tells the future
# wall remover function which wall to remove on the new cell.

# This repeats for all directions with their respective opposite: (N-S), (W-E)
# Everything in this project is (y, x): row first, then column.

DIRECTIONS: Dict[int, tuple[int, int, int]] = {
    N: (-1, 0, S),
    S: (1, 0, N),
    E: (0, 1, W),
    W: (0, -1, E),
}

#cell PATTERN of 42 symbol with its coords

PATTERN_42: Set[tuple[int, int]] = {
    #4 shape
    (0, 0), (1, 0), (2, 0),
    (2, 1), (2, 2), (1, 2),
    (0, 2), (3, 2), (4, 2),

    #2 shape
    (0, 5), (0, 6), (0, 7),
    (1, 7), (2, 7), (2, 6),
    (2, 5), (3, 5), (4, 5), 
    (4, 6), (4, 7) 
}

class Grid:
    """Grid of CELLS in the matrix, each cell is 4bit to determine the value of the respective 4 walls"""

#grid generator method, it puts every cell of the matrix at ALL(15) value
    def __init__(self, width: int, height: int):
        if width < 1 or height < 1:
            raise ValueError("width and height must be biigger than (idk yet)")
        self.width = width
        self.height = height
        self.matrix = [[ALL for _ in range(width)] for _ in range(height)]

#wall remover method, removes specific walls based on where the algo is randomly moving to

    def remove_wall(self, y: int, x: int, direction: int) -> None:
        #get coord movements and opposite wall from  DIRECTIONS cosnt
        dy, dx, opposite_wall = DIRECTIONS[direction]

        #go to the next direction
        ny = y + dy
        nx = x + dx

        if not ((0 <= ny < self.height) and (0 <= nx < self.width)):
            raise ValueError("out of bounds")

        # remove wall from current cell! ~negative bitwise operator. ~0001 = 1110
        # &operator is to check the ~direction vs the current cell and lets say 1111 to &1110 then we get 1110.
        # but if its &1110 and the cell is 1110, nothing is changed!
        self.matrix[y][x] &= ~direction
        self.matrix[ny][nx] &= ~opposite_wall

#teste
g = Grid(5, 3)
g.remove_wall(0, 2, S)
print(g.matrix[0][2], g.matrix[1][2])   # expect 11 14
try:
    g.remove_wall(0, 2, N)
except ValueError as e:
    print("caught:", e)
