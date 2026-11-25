from collections import deque
from typing import Optional

from .generator import DIRECTIONS, LETTERS, Grid


def solve_maze(grid: Grid) -> str:
    """Return the shortest path from entry to goal as N/E/S/W letters."""
    height = grid.height
    width = grid.width
    matrix = grid.matrix
    entry = grid.entry
    goal = grid.exit

    parent: dict[
        tuple[int, int],
        Optional[tuple[tuple[int, int], int]],
    ] = {entry: None}

    queue: deque[tuple[int, int]] = deque([entry])

    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            break

        for direction, (dx, dy, _) in DIRECTIONS.items():
            nx = x + dx
            ny = y + dy

            if nx < 0 or nx >= width or ny < 0 or ny >= height:
                continue

            wall_bit = matrix[y][x] & direction
            if wall_bit != 0:
                continue

            if (nx, ny) in parent:
                continue

            parent[(nx, ny)] = ((x, y), direction)
            queue.append((nx, ny))

    if goal not in parent:
        raise ValueError("no path from entry to exit")

    path: list[str] = []
    cell = goal
    step = parent[cell]
    while step is not None:
        cell, direction = step
        path.append(LETTERS[direction])
        step = parent[cell]
    return "".join(reversed(path))
