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
        Grid(config["WIDTH"], config["HEIGHT"], config.get("SEED"))
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__": main()