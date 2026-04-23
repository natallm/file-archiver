from pathlib import Path
Path("extracted").mkdir(parents=True, exist_ok=True)

with open("archive.nbz", encoding="utf-8") as archive_file:
    archive_content = archive_file.read()
    read_index = 0

    while len(archive_content) > read_index:
        file_type = archive_content[read_index] # Can be: None, U+F674 (folder/directory) or U+F675 (file) | Co the la: None, U+674 (Thu muc) hoac U+675 (Tep)
        file_name = ""
        
        read_index += 1

        if file_type == "\uF674":
            while archive_content[read_index] != "\uF679":
                file_name = file_name + archive_content[read_index]
                read_index += 1
            print("DIRECTORY NAME: " + file_name)
            Path("extracted", file_name).mkdir(parents=True, exist_ok=True)
            read_index += 1
            continue

        while archive_content[read_index] != "\uF676":
            file_name = file_name + archive_content[read_index]
            read_index += 1

        print("FILE NAME: " + file_name)
        read_index += 1

        file_content = ""
        while archive_content[read_index] != "\uF679":
            file_content = file_content + archive_content[read_index]
            read_index += 1

        print("FILE CONTENT: " + file_content)
        read_index += 1

        file_path = Path("extracted", file_name)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_content = file_content
        file_path.write_text(file_content)


