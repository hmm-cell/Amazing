from generator import Grid

def write_output(grid: Grid,path_solved: str, output_file: str) -> None:
    """Write the maze, its entry, its exit and the shortest path to a file.

    Args:
        grid: the generated maze.
        path: shortest path from entry to exit as N/E/S/W letters.
        output_file: name of the file to write.

    Raises:
        OSError: if the file cannot be created or written.
    """

    entry_x, entry_y = grid.entry
    exit_x, exit_y = grid.exit

    with open(output_file, "w") as f:
        f.write(grid.hex_convert() + "\n")
        f.write("\n")
        f.write(f"{entry_x},{entry_y}\n")
        f.write(f"{exit_x},{exit_y}\n")
        f.write(path_solved + "\n")