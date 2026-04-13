

from pathlib import Path
from pprint import pprint
import hashlib


def format_size(size_in_bytes):
    for unit in ['B','KB','MB','GB','TB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes} {unit}"
        size_in_bytes /= 1024


def print_diff(diff):
    for category in ['new','modified','missing']:
        print(f"")
def print_metadata(data,title):
    print(f"\n{title}")

    for path,meta in sorted(data.items()):
        print(f"\n{path}")
        print(f"  Name      : {meta['name']}")
        print(f"  Extension : {meta['extension']}")
        print(f"  Size      : {format_size(meta['size'])}")
        print(f"  Hash      : {meta['hash']}")



def get_file_hash(file_path , algo="sha256"):
    hash_function = hashlib.new(algo)
    with open(file_path , "rb") as f:
        for chunk in iter(lambda: f.read(8192),b""):
            hash_function.update(chunk)
    return hash_function.hexdigest()



def collect_file_metadata(path_str,base_path):
    path = Path(path_str).resolve()
    base_path = Path(base_path).resolve()
    keys = {}
    for item in path.iterdir():
        if item.is_file():
            keys[item.relative_to(base_path)] = {
                "name" : item.name,
                "extension" : item.suffixes,
                "size" : item.stat().st_size,
                "hash" : get_file_hash(item)
            }
        elif item.is_dir():
            keys.update(collect_file_metadata(item,base_path))
        else:
            print("Path does not exist or is something else")
    return keys
    


def compare_files(source,destination):
    result = {
        "new" : [],
        "modified" : [],
        "missing" : []
    }

    for key in source:
        if key not in destination:
            result["new"].append(key)
        else:
            if source[key]["size"] != destination[key]["size"]:
                result["modified"].append(key)
            elif source[key]["hash"] != destination[key]["hash"]:
                result["modified"].append(key)
        
    
    for key in destination:
        if key not in source:
            result["missing"].append(key)
    

    return result



if __name__ == "__main__":
    source_directory = input("Enter the Source Directory: ")
    source_directory_dict = collect_file_metadata(source_directory,source_directory)
    print_metadata(source_directory_dict,"Source Path")
    destination_directory = input("Enter the Destination Directory: ")
    destination_directory_dict = collect_file_metadata(destination_directory,destination_directory)
    print_metadata(destination_directory_dict,"Destination Path")

    sync_diff = compare_files(source_directory_dict,destination_directory_dict)
    pprint(sync_diff)
