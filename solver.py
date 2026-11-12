from collections import deque
from typing import Optional
from generator import DIRECTIONS, LETTERS, Grid

def solve_maze(grid: Grid) -> str:
    """Return the shortest path from entry to goal as N/E/S/W letters."""
    height = grid.height
    width = grid.width
    matrix = grid.matrix
    entry = grid.entry
    goal = grid.exit

    parent: dict[
        tuple[int, int],
        # key: a cell (x, y)
        Optional[tuple[tuple[int, int], int]],  
        # value: None(Optional), or (cell, direction)
    ] = {entry: None}

    #the queue stars at ENTRY coords
    #deque data type allows for seamless FIFO without shifting items in memory
    queue: deque[tuple[int, int]] = deque([entry])

    # repeats as long as queue isnt empty
    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            break

        for direction, (dx, dy, _) in DIRECTIONS.items():
            nx = x + dx
            ny = y + dy

            #skip if the neighbour is outside the grid
            if nx < 0 or nx >= width or ny < 0 or ny >= height:
                continue

            #skip if the current cell has a wall in this direction
            wall_bit = matrix[y][x] & direction
            if wall_bit != 0:
                continue

            #skip if the neighbour was already found
            if (nx, ny) in parent:
                continue

            # none of the skips applied: register and queue the neighbour
            parent[(nx, ny)] = ((x, y), direction)
            queue.append((nx, ny))

    #if after cycle parent != exit
    if goal not in parent:
        raise ValueError("no path from entry to exit")

    # walk back from goal to entry, then reverse
    path: list[str] = []
    #the actual path entry to exit
    cell = goal
    step = parent[cell]
    #parent gives value to every coord
    #if value == None that means were back at entry!
    while step is not None:
        cell, direction = step
        # direction grabs from parent its value
        path.append(LETTERS[direction])
        step = parent[cell]
        # attribute to step next coord key in parent dict
    return "".join(reversed(path))