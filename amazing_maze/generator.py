import random
from typing import Dict, List, Tuple, Set, Optional

N = 1  # Wall at north.
E = 2  # Wall at east.
S = 4  # Wall at south.
W = 8  # Wall at west.
ALL = N | E | S | W

LETTERS: dict[int, str] = {N: "N", E: "E", S: "S", W: "W"}

DIRECTIONS: Dict[int, tuple[int, int, int]] = {
    N: (0, -1, S),
    S: (0, 1, N),
    E: (1, 0, W),
    W: (-1, 0, E),
}

PATTERN_42: set[tuple[int, int]] = {
    # 4 shape.
    (0, 0), (0, 1), (0, 2),
    (1, 2), (2, 2), (2, 1),
    (2, 0), (2, 3), (2, 4),

    # 2 shape.
    (4, 0), (5, 0), (6, 0),
    (6, 1), (6, 2), (5, 2),
    (4, 2), (4, 3), (4, 4),
    (5, 4), (6, 4)
}


class Grid:
    """Grid of cells, each represented by four wall bits."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool,
        seed: Optional[int] = None,
    ):
        if width < 1 or height < 1:
            raise ValueError("width and height must be positive")
        self.width = width
        self.height = height
        self.matrix: List[List[int]] = [
            [ALL for _ in range(width)] for _ in range(height)
        ]
        self.fixed: Set[Tuple[int, int]] = set()
        self.entry = entry
        self.exit = exit
        self.perfect = perfect

        if seed is None:
            seed = random.randint(0, 999999)
        self.seed = seed

        self.rng = random.Random(self.seed)

        px_vals = [p[0] for p in PATTERN_42]
        py_vals = [p[1] for p in PATTERN_42]
        pattern_width = max(px_vals) - min(px_vals) + 1
        pattern_height = max(py_vals) - min(py_vals) + 1

        if self.width >= 10 and self.height >= 10:
            ox = (self.width - pattern_width) // 2
            oy = (self.height - pattern_height) // 2

            self.fixed = {(ox + px, oy + py) for px, py in PATTERN_42}
        else:
            print("Error: Grid is too small to fit the 42 pattern.")

    def is_fixed_cell(self, x: int, y: int) -> bool:
        return (x, y) in self.fixed

    """Raise ValueError if ENTRY or EXIT is inside the 42 pattern."""
    def check_entry_exit(self) -> None:
        for name, (x, y) in (("ENTRY", self.entry), ("EXIT", self.exit)):
            if self.is_fixed_cell(x, y):
                raise ValueError(f"{name} ({x}, {y}) is inside the 42 pattern")

    def remove_wall(self, x: int, y: int, direction: int) -> None:
        dx, dy, opposite_wall = DIRECTIONS[direction]
        nx = x + dx
        ny = y + dy

        if not ((0 <= nx < self.width) and (0 <= ny < self.height)):
            raise ValueError("out of bounds")

        if self.is_fixed_cell(x, y) or self.is_fixed_cell(nx, ny):
            raise ValueError("going to locked cell or in locked cell")
        self.matrix[y][x] &= ~direction
        self.matrix[ny][nx] &= ~opposite_wall

    def generate_maze(self) -> None:
        if self.perfect:
            self.perfect_maze()
        else:
            self.imperfect_maze()

    def perfect_maze(self) -> None:
        available_cells = [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if not self.is_fixed_cell(x, y)
        ]
        if not available_cells:
            raise ValueError("There are no available cells")

        start = self.rng.choice(available_cells)
        visited: Set[Tuple[int, int]] = {start}
        stack: List[Tuple[int, int]] = [start]

        while stack:
            x, y = stack[-1]

            neighbours = []
            for direction, (dx, dy, _) in DIRECTIONS.items():
                nx = x + dx
                ny = y + dy
                if (
                    0 <= nx < self.width
                    and 0 <= ny < self.height
                    and (nx, ny) not in visited
                    and not self.is_fixed_cell(nx, ny)
                ):
                    neighbours.append((nx, ny, direction))

            if neighbours:
                nx, ny, direction = self.rng.choice(neighbours)
                self.remove_wall(x, y, direction)
                visited.add((nx, ny))
                stack.append((nx, ny))

            else:
                stack.pop()

    def is_it_dead_end(self, x: int, y: int) -> bool:
        walls = self.matrix[y][x]
        return ((4 - bin(walls).count("1")) == 1)

    def get_dead_ends(self) -> List[Tuple[int, int]]:
        dead_ends = []
        special_ones = [
            ((self.width - 7) // 2 + x, (self.height - 5) // 2 + y)
            for x, y in [(6, 3), (6, 1)]
        ]

        for y in range(self.height):
            for x in range(self.width):
                if self.is_fixed_cell(x, y):
                    continue

                if (x, y) in special_ones:
                    continue

                if self.is_it_dead_end(x, y):
                    dead_ends.append((x, y))

        return dead_ends

    def remove_dead_ends(self) -> None:
        dead_ends = self.get_dead_ends()

        while dead_ends:
            self.rng.shuffle(dead_ends)
            removed_wall = False

            for x, y in dead_ends:
                possible_walls = []

                for direction, (dx, dy, _) in DIRECTIONS.items():
                    nx = x + dx
                    ny = y + dy

                    if not (0 <= nx < self.width
                            and 0 <= ny < self.height):
                        continue

                    if self.is_fixed_cell(nx, ny):
                        continue

                    if self.matrix[y][x] & direction:
                        possible_walls.append(direction)

                if possible_walls:
                    direction = self.rng.choice(possible_walls)
                    self.remove_wall(x, y, direction)
                    removed_wall = True
                    break

            if not removed_wall:
                break

            dead_ends = self.get_dead_ends()

    def imperfect_maze(self) -> None:
        self.perfect_maze()
        self.remove_dead_ends()

    def hex_convert(self) -> str:
        converted_rows = [
            "".join(format(x, "X") for x in row) for row in self.matrix
        ]
        return "\n".join(converted_rows)
