import logging
from pathlib import Path

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def create_file_handler(log_file_path: Path):
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return file_handler


FOLDER = "[FOLDER]"
FILE = "[FILE]"

CREATION = " [CREATION]"
COPYING = " [COPYING]"
REMOVAL = " [REMOVAL]"

FOLDER_COPYING = FOLDER + COPYING
FOLDER_REMOVAL = FOLDER + REMOVAL

FILE_CREATION = FILE + CREATION
FILE_COPYING = FILE + COPYING
FILE_REMOVAL = FILE + REMOVAL


def format_log_from_to(from_path: str, to_path: str, type_operation: str) -> str:
    return f"{type_operation} FROM {from_path} TO {to_path}"


def format_log_operation(path: str, type_operation: str) -> str:
    return f"{type_operation} ON {path}"
