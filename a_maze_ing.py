import sys
from parser import config_parser, validate_config
from generator import Grid

def main() -> None:
    #verify if only two args are received
    if len(sys.argv) != 2:
        sys.stderr.write(f"Usage: python <{sys.argv[0]}>\n")
        return
