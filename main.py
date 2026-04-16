

from pathlib import Path
import hashlib
import shutil
import sys

DEBUG = False


def format_size(size_in_bytes):
    for unit in ['B','KB','MB','GB','TB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes} {unit}"
        size_in_bytes /= 1024



def sync_to_destination(source_base,destination_base,diff):
    source_base = Path(source_base)
    destination_base = Path(destination_base)

    for category in ["new","modified"]:
        for relative_path in diff[category]:
            src = source_base / relative_path
            dst = destination_base / relative_path

            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src , dst)



def remove_missing(destination_base,diff):
    destination_base = Path(destination_base)

    for relative_path in diff['missing']:
        path = destination_base / relative_path

        if path.exists():
            if path.is_file():
                path.unlink()
                print(f"Deleted file: {path}")




def print_diff(diff):
    for category in ['new','modified','missing']:
        print(f"\n{category.upper()}: ")
        for item in sorted(diff.get(category , [])):
            print(f" - {item}")
            print("")



def print_metadata(data,title):
    print(f"\n{title}")

    for path,meta in sorted(data.items()):
        print(f"\n{path}")
        print(f"  Name      : {meta['name']}")
        print(f"  Extension : {meta['extension']}")
        print(f"  Size      : {format_size(meta['size'])}")
        print(f"  Hash      : {meta['hash']}")
        print("")



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



def main():
    source_directory = input("Enter the Source Directory: ").strip()
    if not Path(source_directory).is_dir():
        print("Invalid source directory!")
        return
    source_directory_dict = collect_file_metadata(source_directory,source_directory)
    # Passing the same path twice:
    # first argument = working path (may change during recursion)
    # second argument = original base path (remains constant for relative calculations)
    print_metadata(source_directory_dict,"Source Path")
    destination_directory = input("Enter the Destination Directory: ").strip()
    if not Path(destination_directory).is_dir():
        print("Invalid destination directory!")
        return
    if Path(source_directory).resolve() == Path(destination_directory).resolve():
        print("Source and destination cannot be the same!")
        return
    destination_directory_dict = collect_file_metadata(destination_directory,destination_directory)
    # Passing the same path twice:
    # first argument = working path (may change during recursion)
    # second argument = original base path (remains constant for relative calculations)
    print_metadata(destination_directory_dict,"Destination Path")

    sync_diff = compare_files(source_directory_dict,destination_directory_dict)
    print_diff(sync_diff)

    while True:
        print("Proceed with synchronization? (y/n):")
        choice = input("Enter Choice: ").strip().lower()

        if choice == "n":
            return 
        elif choice == "y":
            break
        else:
            print("Invalid Choice!!")
    
    try:
        sync_to_destination(source_directory, destination_directory, sync_diff)
    except Exception as e:
        print(f"Error during sync: {e}")
        if DEBUG:
            raise
        return
    while True:
        print("Proceed with Deletion of unique files in destination? (y/n):")
        choice = input("Enter Choice: ").strip().lower()

        if choice == "n":
            return
        elif choice == "y":
            break
        else:
            print("Invalid Choice!!")
    try:
        remove_missing(destination_directory, sync_diff)
    except Exception as e:
        print(f"Error during deletion: {e}")
        if DEBUG:
            raise
        return



if __name__ == "__main__":
    main()