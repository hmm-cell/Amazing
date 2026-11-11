from typing import Any, Dict, Tuple

#grabs the confing txt and stores in a dict its values
def config_parser(filepath: str) -> dict[str, Any]:
    """Used to read and parse a maze configuration file.
    
    Args: 
        filepath: path to the configuration file
        
    Returns:
        config Dict: mapping each key to its value
        
    Raises:
        ValueError: if file is not accessible or has malformed line"""

    config: dict[str, Any] = {}
    try:
        with open(filepath, "r") as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()

                #if theres no #before move to next line
                if not line or line.startswith("#"):
                    continue

                #part whhere we get information for each obj
                if "=" in line:
                    #divides line into key and val, eg: wdth=25
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()

                #for bool in PERFECT mode
                    if value.lower() in ("true", "false"):
                        #the equality == gives a bool val that gets
                        #attributed to the val of config key
                        config[key] = (value.lower() == "true")
                    elif "," in value:
                        # Convert comma-separated values like "0,0" into a tuple of ints
                        try:
                            config[key] = tuple(map(int, value.split(",")))
                        except ValueError:
                            raise ValueError(f"{line_num}: '{line}' has improper coordinate input")
                    else:
                        try:
                            #convert str into int
                            config[key] = int(value)
                        except ValueError:
                            config[key] = value
                else:
                    raise ValueError(f"{line_num}: '{line}' is missing an '='")
                
    except OSError as err:
    #if the file doesnt exist we raiise error
        raise ValueError(f"cannot read '{filepath}': {err}") from err

    return config



#all values in the dict must be validated and if wrong error must be raised for any
def validate_config(config: dict[str, Any]) -> None:
    """Check that the parsed configuration is complete and consistent.

    Args:
        config: Dictionary produced by config_parser.

    Raises:
        ValueError: If a key is missing or a value is invalid.
    """
    #list with the correct keys names
    REQUIRED_KEYS = "WIDTH HEIGHT ENTRY EXIT OUTPUT_FILE PERFECT".split()
    for key in REQUIRED_KEYS:
        if key not in config:
            raise ValueError(f"Missing required configuration key: '{key}'")

    #   IMPORTANT we need to MIN discuss dimentions AND MAX

    for name in ("WIDTH", "HEIGHT"):
        if (
            not isinstance(config[name], int)
            or config[name] <= 0
            or isinstance(config[name], bool)
        ):
            raise ValueError(f"{name} must be a positive integer, got {config[name]}")

    #verify is entry/exit tuple is filled with 2 ints
    for name in ("ENTRY", "EXIT"):
        if not isinstance(config[name], tuple) or len(config[name]) != 2:
            raise ValueError(f"{name} must be two integers like 0,0")

    #VALIDATE IN-BOUNDS COORDS
    for name in ("ENTRY", "EXIT"):
        x, y = config[name]
        if not (0 <= x < config["WIDTH"] and 0 <= y < config["HEIGHT"]):
            raise ValueError(f"{name} coordinates ({x}, {y}) are out of bounds")

    #validate if entry is diff from exit
    if config["ENTRY"] == config["EXIT"]:
        raise ValueError("ENTRY and EXIT must have differnt coordinates")

    #validate if PERFECT IS BOOL
    if not isinstance(config["PERFECT"], bool):
        raise ValueError("PERFECT isnt a boolean value")

    #verify is OUTPUT_FILE is str and not empty
    if not isinstance(config["OUTPUT_FILE"], str) or not config["OUTPUT_FILE"].strip():
        raise ValueError("OUTPUT_FILE must be a non-empty filename")

    if "SEED" in config:
        #verify SEED being an int
        if not isinstance(config["SEED"], int) or isinstance(config["SEED"], bool):
            raise ValueError(f"SEED must be an integer")
