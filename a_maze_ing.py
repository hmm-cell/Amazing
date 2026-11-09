#this is where we will iimport everyhtiing
from grid import Grid

def config_parser(filepath: str) -> None:
    config = {}
    with open(filepath, "r") as f:
        for line in f:
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
            if value.lower in ("true", "false"):
                #the equality == gives a bool val that gets
                #attributed to the val of config key
                config[key] = (value.lower == "true")

            elif 



