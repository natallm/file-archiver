from glob import glob
from pathlib import Path
import os

paths_to_archive = Path("files-to-archive").rglob("**/*")
paths_to_archive = [os.path.relpath(path) for path in paths_to_archive]

with open("bytefile", "wb") as archive_file:
    for path_name in paths_to_archive:
        def write_to_archive(string: str):
            archive_file.write(bytes(string, "utf-8"))

        archive_path_name = os.path.relpath(path_name, "files-to-archive")
        if os.path.isdir(path_name):
            write_to_archive("\uF674" + archive_path_name) # U+F674=directory
        else:
            write_to_archive("\uF675" + archive_path_name + "\uF676") #U+F675=file, U+F676=end of file name
            with open(path_name) as file:
                write_to_archive(file.read())

        write_to_archive("\uF679") #U+F679=end of file
        break
        