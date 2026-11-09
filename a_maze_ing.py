#this is where we will iimport everyhtiing
from typing import Any
from grid import Grid

#grabs the confing txt and stores in a dict its values
def config_parser(filepath: str) -> dict[str, Any]:
    
    config = {}
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
                    config[key] = tuple(map(int, value.split(",")))
                else:
                    try:
                        #convert str into int
                        config[key] = int(value)
                    except ValueError:
                        config[key] = value
            else:
                raise ValueError(f"{line_num}: '{line}' is missing an '='")