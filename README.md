# Folder Synchronization

## How to execute Script:

python -m source.main "original_path" "replica_path" number_of_seconds "logs_folder_path"

where "original_path" is the path of the original folder,
"replica_path" is the path of where to copy the contents of original folder,
number of seconds is the number of seconds between synchronizations
and "logs_folder_path" is the path where the log files will be created (one file for each synchronization)

### Example:

python -m source.main "C:\Users\username\Documents\original_folder" "C:\Users\username\Documents\replica_folder" 60 "C:\Users\username\Documents\logs_folder"

In this case we will have 60 seconds (1 minute) between synchronizations
