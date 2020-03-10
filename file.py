import os

def create_folder_if_not_existing(folder_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)