from pathlib import Path
from typing import Optional, Tuple
from source.core.exceptions import (
    InsufficientCommandLineArguments,
    InvalidCommandLineArgument,
)


def validate_path(
    path_argument: str, argument_name: str, create_folder: bool = False
) -> Tuple[Optional[Path], Optional[str]]:

    path = Path(path_argument)

    # Validate if Path Exists as a Folder
    if not path.exists():
        if create_folder:
            try:
                path.mkdir(parents=True, exist_ok=True)
                return path, None

            except (PermissionError, OSError) as e:
                return None, f"Failed to create {argument_name}: {str(e)}"
        return None, f"{argument_name} does not exist"

    if create_folder and not path.is_dir():
        return None, f"{argument_name} exists but is not a folder"

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
    replica_path, error_message = validate_path(
        argv[2], "Replica Path", create_folder=True
    )
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
    log_file_path, error_message = validate_path(
        argv[4], "Log File Path", create_folder=True
    )
    if error_message:
        dict_errors["Log File Path"] = error_message

    # If no errors, return validated values
    if not dict_errors:
        return source_path, replica_path, seconds, log_file_path
    else:
        raise InvalidCommandLineArgument(dict_errors)
