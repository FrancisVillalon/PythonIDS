import shutil
import os

def delete_all_files_in_folder(folder_path):
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

def clean_up(target=None):
    print(f"\n *** Clean up ***")
    if target:
        delete_all_files_in_folder(target)
    else:
        delete_all_files_in_folder("./logs")
        delete_all_files_in_folder("./data")
        delete_all_files_in_folder("./exports")

    # * Make folder it not exists
    if not os.path.exists("./logs"):
        os.makedirs("./logs")
    if not os.path.exists("./data"):
        os.makedirs("./data")
    if not os.path.exists("./exports"):
        os.makedirs("./exports")
    print("Clean up completed")