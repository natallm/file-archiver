from glob import glob
from pathlib import Path
import os

paths_to_archive = Path("files-to-archive").rglob("**/*")
paths_to_archive = [os.path.relpath(path) for path in paths_to_archive]

with open("archive.nbz", 'wb') as archive_file:
    for path_name in paths_to_archive:
        archive_path_name = os.path.relpath(path_name, "files-to-archive")
        print("DEBUG: Archiving", path_name + "!")
        print(os.stat(path_name))
        if os.path.isdir(path_name):
            archive_file.write("\uF674" + archive_path_name) # U+F674=directory
        else:
            archive_file.write("\uF675" + archive_path_name + "\uF676") #U+F675=file, U+F676=end of file name
            with open(path_name) as file:
                archive_file.write(file.read())

        archive_file.write("\uF679") #U+F679=end of file