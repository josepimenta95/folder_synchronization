import sys
from source.core.command_line_arguments import read_command_line_arguments
from source.core.file_handler import (
    synchronize_folders,
)


def main(argv):
    (
        source_path,
        replica_path,
        synchronization_interval_seconds,
        log_file_path,
    ) = read_command_line_arguments(argv)

    synchronize_folders(
        source_path, replica_path, synchronization_interval_seconds, log_file_path
    )


if __name__ == "__main__":

    main(sys.argv)
