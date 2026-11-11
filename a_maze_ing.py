import sys
from parser import config_parser, validate_config
from generator import Grid

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
        grid = Grid(config["WIDTH"], config["HEIGHT"], config["ENTRY"], config["EXIT"], config.get("SEED"))
        grid.generate_maze()
        #check if entry or exit inside 42 pattern
        grid.check_entry_exit()
    except (ValueError, OSError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    print(grid.hex_convert())

if __name__ == "__main__": main()