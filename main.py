from pathlib import Path



def print_all_files(path_str):
    path = Path(path_str)

    for item in path.iterdir():
        if item.is_file():
            print(f"{item.name} ->> {item}")
        elif item.is_dir():
            print_all_files(item)
        else:
            print("Path does not exist or is something else")
    



if __name__ == "__main__":
    source_directory = input("Enter the Source Directory: ")
    destination_directory = input("Enter the Destination Directory: ")
    print_all_files(source_directory)
    print_all_files(destination_directory)