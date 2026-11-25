from typing import Any


def config_parser(filepath: str) -> dict[str, Any]:
    """Read and parse a maze configuration file."""

    config: dict[str, Any] = {}
    try:
        with open(filepath, "r") as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()

                    if value.lower() in ("true", "false"):
                        config[key] = (value.lower() == "true")
                    elif "," in value:
                        try:
                            config[key] = tuple(map(int, value.split(",")))
                        except ValueError:
                            raise ValueError(
                                f"{line_num}: '{line}' has improper "
                                "coordinate input"
                            )
                    else:
                        try:
                            config[key] = int(value)
                        except ValueError:
                            config[key] = value
                else:
                    raise ValueError(f"{line_num}: '{line}' is missing an '='")
    except OSError as err:
        raise ValueError(f"cannot read '{filepath}': {err}") from err

    return config


def validate_config(config: dict[str, Any]) -> None:
    """Check that the parsed configuration is complete and consistent.

    Args:
        config: Dictionary produced by config_parser.

    Raises:
        ValueError: If a key is missing or a value is invalid.
    """
    REQUIRED_KEYS = "WIDTH HEIGHT ENTRY EXIT OUTPUT_FILE PERFECT".split()
    for key in REQUIRED_KEYS:
        if key not in config:
            raise ValueError(f"Missing required configuration key: '{key}'")

    for name in ("WIDTH", "HEIGHT"):
        if (
            not isinstance(config[name], int)
            or config[name] <= 0
            or isinstance(config[name], bool)
        ):
            raise ValueError(
                f"{name} must be a positive integer, got {config[name]}"
            )

    for name in ("ENTRY", "EXIT"):
        if (
            not isinstance(config[name], tuple)
            or len(config[name]) != 2
        ):
            raise ValueError(f"{name} must be two integers like 0,0")

    for name in ("ENTRY", "EXIT"):
        x, y = config[name]
        if not (
            0 <= x < config["WIDTH"]
            and 0 <= y < config["HEIGHT"]
        ):
            raise ValueError(
                f"{name} coordinates ({x}, {y}) are out of bounds"
            )

    if config["ENTRY"] == config["EXIT"]:
        raise ValueError("ENTRY and EXIT must have differnt coordinates")

    if not isinstance(config["PERFECT"], bool):
        raise ValueError("PERFECT isnt a boolean value")

    if (
        not isinstance(config["OUTPUT_FILE"], str)
        or not config["OUTPUT_FILE"].strip()
    ):
        raise ValueError("OUTPUT_FILE must be a non-empty filename")

    if "SEED" in config:
        if (
            not isinstance(config["SEED"], int)
            or isinstance(config["SEED"], bool)
        ):
            raise ValueError("SEED must be an integer")
