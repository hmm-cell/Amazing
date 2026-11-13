import sys
from parser import config_parser, validate_config
from generator import Grid
from solver import solve_maze
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
        #generate the maze
        grid = Grid(config["WIDTH"], config["HEIGHT"], config["ENTRY"],
                     config["EXIT"], config.get("SEED"))
        grid.perfect_maze()
        #check if entry or exit inside 42 pattern
        grid.check_entry_exit()
    except (ValueError, OSError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    print(grid.hex_convert())
    path_solved = solve_maze(grid)
    print(path_solved)
    #use python .\a_maze_ing.py .\config.txt to run
    write_output(grid, path_solved, config["OUTPUT_FILE"])

if __name__ == "__main__": main()