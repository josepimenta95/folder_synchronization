from pathlib import Path
from source.logger import (
    FOLDER_COPYING,
    FOLDER_REMOVAL,
    FILE_CREATION,
    FILE_COPYING,
    FILE_REMOVAL,
    create_file_handler,
    format_log_from_to,
    format_log_operation,
    logger,
)
import shutil
import hashlib
import time


# Create Dict of Folders Inside Current Folder
def create_dict_of_folders(folder_path: Path) -> dict:
    folders_dict = {}
    for sub_path in folder_path.glob("*"):
        if sub_path.is_dir():
            folders_dict[sub_path.name] = sub_path

    return folders_dict


# Create Dict of Files Inside Current Folder
def create_dict_of_files(folder_path: Path) -> dict:
    files_dict = {}
    for sub_path in folder_path.glob("*"):
        if sub_path.is_file():
            files_dict[sub_path.name] = sub_path

    return files_dict


# Compares Files Hashes and Replaces File if Different
def compare_files(source_path: Path, replica_path: Path) -> None:
    source_bytes = source_path.read_bytes()
    source_file_hash = hashlib.md5(source_bytes).digest()

    replica_bytes = replica_path.read_bytes()
    replica_file_hash = hashlib.md5(replica_bytes).digest()

    if source_file_hash != replica_file_hash:
        remove_file(replica_path)
        copy_file_to_replica(source_path, replica_path, FILE_COPYING)


# Copy Folder from Source to Replica and Synchronizes Tree of Said Folder
def copy_folder_and_contents_to_replica(
    source_path: Path, parent_replica_path: Path
) -> None:
    child_path = make_folder(source_path, parent_replica_path, FOLDER_COPYING)
    synchronize_folder_tree(source_path, child_path)


# Create Copy of Folder from Source to Replica
def make_folder(source_path: Path, parent_replica_path: Path, operation: str) -> Path:
    child_path = parent_replica_path.joinpath(source_path.name)
    child_path.mkdir()
    logger.info(format_log_from_to(source_path, child_path, operation))
    return child_path


# Copy File from Source To Replica
def copy_file_to_replica(source_path: Path, replica_path: Path, operation: str) -> None:
    file_path = shutil.copy2(source_path, replica_path)
    logger.info(format_log_from_to(source_path, file_path, operation))


# Remove File from Replica
def remove_file(path: Path) -> None:
    path.unlink()


# Remove Folder from Replica
def remove_folder(path: Path, operation: str) -> None:
    path.rmdir()
    logger.info(format_log_operation(path, operation))


# Remove Folder from Replica and All Content Inside Said Folder
def remove_folder_and_contents_from_replica(path: Path) -> None:
    replica_folder_dict = create_dict_of_folders(path)
    replica_file_dict = create_dict_of_files(path)

    for folder_name in replica_folder_dict:
        remove_folder_and_contents_from_replica(replica_folder_dict[folder_name])
        remove_folder(replica_folder_dict[folder_name], FOLDER_REMOVAL)

    for file_name in replica_file_dict:
        remove_file(replica_file_dict[file_name])
        logger.info(format_log_operation(replica_file_dict[file_name], FILE_REMOVAL))

    remove_folder(path, FOLDER_REMOVAL)


# Synchronize Folders on the Same Level and Lower Levels
def synchronize_folder_tree(source_path: Path, replica_path: Path) -> None:
    source_folder_dict = create_dict_of_folders(source_path)
    source_file_dict = create_dict_of_files(source_path)

    replica_folder_dict = create_dict_of_folders(replica_path)
    replica_file_dict = create_dict_of_files(replica_path)

    for file_name in source_file_dict:
        if file_name in replica_file_dict:
            compare_files(source_file_dict[file_name], replica_file_dict[file_name])
        elif file_name not in replica_file_dict:
            copy_file_to_replica(
                source_file_dict[file_name], replica_path, FILE_CREATION
            )

    for file_name in replica_file_dict:
        if file_name not in source_file_dict:
            remove_file(replica_file_dict[file_name])
            logger.info(
                format_log_operation(replica_file_dict[file_name], FILE_REMOVAL)
            )

    for folder_name in source_folder_dict:
        if folder_name in replica_folder_dict:
            synchronize_folder_tree(
                source_folder_dict[folder_name], replica_folder_dict[folder_name]
            )
        elif folder_name not in replica_folder_dict:
            copy_folder_and_contents_to_replica(
                source_folder_dict[folder_name], replica_path
            )

    for folder_name in replica_folder_dict:
        if folder_name not in source_folder_dict:
            remove_folder_and_contents_from_replica(replica_folder_dict[folder_name])


def synchronize_folders(
    source_path: Path, replica_path: Path, seconds: int, log_file_path: Path
) -> None:
    while True:
        # Create Log File
        timestr = time.strftime("%Y%m%d-%H%M%S")
        new_log_file = Path(
            log_file_path.resolve(), f"{timestr}_synchronization_log_file.txt"
        )

        # Start File Handler
        file_handler = create_file_handler(new_log_file)

        synchronize_folder_tree(source_path, replica_path)

        # Close File Handler
        file_handler.close()

        print(f"Time Between Synchronizations: {seconds} Seconds")
        time.sleep(seconds)
