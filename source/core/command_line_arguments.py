from pathlib import Path
from typing import Optional, Tuple
from source.core.exceptions import (
    InsufficientCommandLineArguments,
    InvalidCommandLineArgument,
)


def validate_path(
    path_argument: str, argument_name: str
) -> Tuple[Optional[Path], Optional[str]]:

    # Validate if Path Exists
    try:
        path = Path(path_argument)
        if not path.exists():
            return None, f"{argument_name} does not exist"

    except (FileNotFoundError, PermissionError, OSError) as e:
        return None, f"Error accessing {argument_name}: {str(e)}"

    except Exception as e:
        return (
            None,
            f"Unexpected error occurred while processing {argument_name}: {str(e)}",
        )

    return path, None


def read_command_line_arguments(argv: list[str]) -> Tuple[Path, Path, int, Path]:

    # Validate Number of Arguments
    if len(argv) != 5:
        raise InsufficientCommandLineArguments(number_of_arguments_given=len(argv) - 1)

    dict_errors = {}

    # Validate Source Path
    source_path, error_message = validate_path(argv[1], "Source Path")
    if error_message:
        dict_errors["Source Path"] = error_message

    # Validate Replica Path
    replica_path, error_message = validate_path(argv[2], "Replica Path")
    if error_message:
        dict_errors["Replica Path"] = error_message

    # Validate Synchronization Interval
    try:
        seconds = int(argv[3])
        if seconds <= 0:
            dict_errors["Synchronization Interval"] = (
                "Synchronization interval must be a positive integer"
            )
    except ValueError:
        dict_errors["Synchronization Interval"] = (
            "Synchronization interval must be a valid integer"
        )

    # Validate Log File Path
    log_file_path, error_message = validate_path(argv[4], "Log File Path")
    if error_message:
        dict_errors["Log File Path"] = error_message

    # If no errors, return validated values
    if not dict_errors:
        return source_path, replica_path, seconds, log_file_path
    else:
        raise InvalidCommandLineArgument(dict_errors)
