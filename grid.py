from typing import Dict, List, Tuple

#each orientation with its bit value
N = 1 #wall at north 0001
E = 2 #wall at east 0010
S = 4 #wall at south 0100
W = 8 #wall at wewst 1000
ALL = N | E | S | W #all sides walled 1111

# IMPORTANT to decide which direction you want to move

direction: Dict[int, tuple[int, int, int]] = {
    
}

class Grid:
    def __init__(self, width: int, height: int):
        if width < 1 or height < 1:
            raise ValueError("width and height must be biigger than (idk yet)")
        self.width = width
        self.height = height
        self.matrix = [[ALL for _ in range(width)] for _ in range(height)]

