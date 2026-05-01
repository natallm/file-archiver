from pathlib import Path
Path("extracted").mkdir(parents=True, exist_ok=True)

with open("archive.nbz", "rb") as archive_file:
    from collections import deque

    archive_content = archive_file.read()
    seek_index = 0
    last_three_bytes = deque([])

    file_name = []
    file_content = []
    file_type = 0 # 0: not reading file, 1: directory, 2: file
    read_mode = 0 # 0: filename, 1: file content. only used for regular files

    while len(archive_content) > seek_index:
        read_byte = archive_content[seek_index]
        
        if len(last_three_bytes) < 3:
            last_three_bytes.append(read_byte)
        else:
            last_three_bytes.popleft()
            last_three_bytes.append(read_byte)

        if [*last_three_bytes] == [239, 153, 180]: # last three bytes indicate "\uF674"
            file_type = 1
            seek_index += 1
            continue

        if [*last_three_bytes] == [239, 153, 181]: # last three bytes indicate "\uF675"
            file_type = 2
            file_mode = 0
            seek_index += 1
            continue

        seek_index += 1

        if file_type == 0: continue
        if file_type == 1: 
            file_name.append(read_byte)

            if [*last_three_bytes] == [239, 153, 185]: # last three bytes indicate "\uF679"
                file_name[-3:] = []
                file_name = bytes(file_name).decode("utf-8")

                Path("extracted", file_name).mkdir(parents=True, exist_ok=True)
            else: continue

        if file_type == 2:
            if read_mode == 0: 
                file_name.append(read_byte)

                if [*last_three_bytes] == [239, 153, 182]: # last three bytes indicate "\uF676"
                    file_name[-3:] = []
                    file_name = bytes(file_name).decode("utf-8")

                    read_mode = 1

                continue

            if read_mode == 1:
                file_content.append(read_byte)

                if [*last_three_bytes] == [239, 153, 185]: # last three bytes indicate "\uF679"
                    file_content[-3:] = []
                    file_content = bytes(file_content)

                    file_path = Path("extracted", file_name)
                    file_path.parent.mkdir(parents=True, exist_ok=True)

                    file_path.write_bytes(file_content)
                else: continue
            
        file_name = []
        file_content = []
        file_type = 0
        read_mode = 0


