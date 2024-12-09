import os


def check_path(path_from_root: str) -> bool:
    result = False
    path = f"{os.getcwd()}/{path_from_root}"
    if os.path.exists(path):
        result = True
    return result


def delete_all_in_subdir(file_type: str, subdir_path: str = "") -> None:
    # As it stands, this will only ever delete items in the named subfolder where this script runs.
    # Altering this function could cause it to delete the entire contents of other folders where you wouldn't want it to.
    # Alter this at your own risk.
    if subdir_path != "":
        delete_path = f"{os.getcwd()}/{subdir_path}"
        if os.path.exists(delete_path):
            for f in os.listdir(delete_path):
                if f.endswith(file_type):
                    os.remove(os.path.join(delete_path, f))
    return
