from glob import glob
from pathlib import Path
import os

paths_to_archive = Path("files-to-archive").rglob("**/*")
paths_to_archive = [os.path.relpath(path) for path in paths_to_archive]

with open("archive.nbz", "wb") as archive_file:
    for path_name in paths_to_archive:
        def write_to_archive(data: str | bytes):
            if type(data) is str:
                archive_file.write(bytes(data, "utf-8"))
            else:
                archive_file.write(data)
        
        archive_path_name = os.path.relpath(path_name, "files-to-archive")
        if os.path.isdir(path_name):
            write_to_archive("\uF674" + archive_path_name) # U+F674=directory [EF 99 B4] [239, 153, 180]
        else:
            write_to_archive("\uF675" + archive_path_name + "\uF676") 
            # U+F675=file [EF 99 B5] [239, 153, 181]
            # U+F676=end of file name [EF 99 B6] [239, 153, 182]
            write_to_archive(Path(path_name).read_bytes())

        write_to_archive("\uF679") # U+F679, [EF 99 B9], [239, 153, 185] = end of file (EOF)
        