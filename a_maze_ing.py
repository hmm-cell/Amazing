import sys
from parser import config_parser, validate_config
from generator import Grid
from solver import solve_maze
from display import run_display
from output import write_output

def main() -> None:
    #verify if only two args are received
    if len(sys.argv) != 2:
        sys.stderr.write(f"Usage: python3 {sys.argv[0]} <config_file>\n")
        sys.exit(1)
    try:
        #get the config.txt and validate it
        config = config_parser(sys.argv[1])
        validate_config(config)

        def create_maze(regenerate: bool) -> tuple[Grid, str]:
            seed = None if regenerate else config.get("SEED")
            grid = Grid(
                config["WIDTH"],
                config["HEIGHT"],
                config["ENTRY"],
                config["EXIT"],
                config["PERFECT"],
                seed,
            )
            grid.check_entry_exit()
            grid.generate_maze()
            path_solved = solve_maze(grid)
            write_output(grid, path_solved, config["OUTPUT_FILE"])
            return grid, path_solved

        run_display(create_maze)
    except (ValueError, OSError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__": main()