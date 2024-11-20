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

def clean_up():
    print(f"\n *** Clean up ***")
    delete_all_files_in_folder("./logs")
    if not os.path.exists("./logs"):
        os.makedirs("./logs")
    delete_all_files_in_folder("./data")
    if not os.path.exists("./data"):
        os.makedirs("./data")
    delete_all_files_in_folder("./exports")
    if not os.path.exists("./exports"):
        os.makedirs("./exports")
    print("Clean up completed")