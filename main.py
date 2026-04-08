from pathlib import Path
from pprint import pprint



def collect_file_metadata(path_str,base_path):
    path = Path(path_str).resolve()
    base_path = Path(base_path).resolve()
    keys = {}
    for item in path.iterdir():
        if item.is_file():
            keys[item.relative_to(base_path)] = {
                "name" : item.name,
                "extension" : item.suffixes,
                "size" : item.stat().st_size
            }
        elif item.is_dir():
            keys.update(collect_file_metadata(item,base_path))
        else:
            print("Path does not exist or is something else")
    return keys
    



if __name__ == "__main__":
    source_directory = input("Enter the Source Directory: ")
    source_directory_dict = collect_file_metadata(source_directory,source_directory)
    pprint(source_directory_dict)
    destination_directory = input("Enter the Destination Directory: ")
    destination_directory_dict = collect_file_metadata(destination_directory,destination_directory)
    pprint(destination_directory_dict)
