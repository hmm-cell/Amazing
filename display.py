from typing import Callable

from amazing_maze.generator import DIRECTIONS, E, LETTERS, N, S, W, Grid


WALL_COLORS = {
    "white": "37",
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "magenta": "35",
    "cyan": "36",
}


def render_maze(
    grid: Grid,
    path_solved: str,
    show_path: bool = True,
    wall_color: str = "white",
) -> str:
    """Draw the maze, marking its entry, exit, and optionally its solution."""
    if wall_color not in WALL_COLORS:
        raise ValueError(f"Unknown wall color: {wall_color}")

    def wall(text: str) -> str:
        return f"\033[{WALL_COLORS[wall_color]}m{text}\033[0m"

    path_cells = {grid.entry}
    x, y = grid.entry
    direction_by_letter = {
        letter: direction for direction, letter in LETTERS.items()
    }
    for letter in path_solved:
        dx, dy, _ = DIRECTIONS[direction_by_letter[letter]]
        x += dx
        y += dy
        path_cells.add((x, y))

    lines: list[str] = []
    for y in range(grid.height):
        north = wall("+")
        middle = ""
        for x in range(grid.width):
            cell = grid.matrix[y][x]
            north += wall("---") if cell & N else "   "
            north += wall("+")

            if x == 0:
                middle += wall("|") if cell & W else " "
            if grid.is_fixed_cell(x, y):
                label = "###"
            elif (x, y) == grid.entry:
                label = " S "
            elif (x, y) == grid.exit:
                label = " E "
            elif show_path and (x, y) in path_cells:
                label = " . "
            else:
                label = "   "
            middle += label
            middle += wall("|") if cell & E else " "

        lines.extend((north, middle))

    south = wall("+")
    for cell in grid.matrix[-1]:
        south += wall("---") if cell & S else "   "
        south += wall("+")
    lines.append(south)
    return "\n".join(lines)


def run_display(create_maze: Callable[[bool], tuple[Grid, str]]) -> None:
    """Show the maze and handle interactive controls."""
    grid, path_solved = create_maze(False)
    show_path = True
    wall_color = "white"

    while True:
        print("\033[2J\033[H", end="")
        print(render_maze(grid, path_solved, show_path, wall_color))
        path_status = "shown" if show_path else "hidden"
        print(f"\nSolution: {path_status} | Wall color: {wall_color}")
        print("[R]egenerate  [P]ath on/off  [C]olor  [Q]uit")
        choice = input("> ").strip().lower()

        if choice == "r":
            grid, path_solved = create_maze(True)
        elif choice == "p":
            show_path = not show_path
        elif choice == "c":
            print(
                "Choose a color: " + ", ".join(WALL_COLORS)
            )
            selected_color = input("> ").strip().lower()
            if selected_color in WALL_COLORS:
                wall_color = selected_color
            else:
                input("Unknown color. Press Enter to continue.")
        elif choice == "q":
            return
        else:
            input("Choose R, P, C, or Q. Press Enter to continue.")
