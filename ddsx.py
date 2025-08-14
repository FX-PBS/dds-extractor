###################
##               ##
##    ddsx.py    ##
##               ##
###################

import sys
import os
import struct

extractor_data = {"cat_name": "", "cat_file_ref": "", "dds_entries": {}}

min_args = {
    "-l": 0,
    "-e": 2,
    "-E": 1,
    "-i": 2,
    "-I": 2,
}

# ---------------------------------------------------------------------------------


def determine_action(arg_i, args):
    match args[arg_i]:
        case "-l":
            list_dds_entries()
        case "-e":
            extract_dds(args[arg_i + 1], args[arg_i + 2])
        case "-E":
            extract_dds_all(args[arg_i + 1])
        case "-i":
            insert_dds(args[arg_i + 1], args[arg_i + 2])
        case "-I":
            insert_dds_all(args[arg_i + 1], args[arg_i + 2])


def list_dds_entries():
    img_renamed = extractor_data["cat_name"]
    for _, index in enumerate(extractor_data["dds_entries"]):
        print(f"{img_renamed}_{index:<10} : {extractor_data['dds_entries'][index]}")
    print()


def extract_dds(texture_index, path):
    texture_index = int(texture_index)
    dds_addr = extractor_data["dds_entries"][texture_index]
    filename = extractor_data["cat_name"].rsplit(".", 1)[0]
    print(f"{path}\\{filename}_{texture_index}.dds")

    with open(f"{path}\\{filename}_{texture_index}.dds", "wb") as a:

        # Determine content size
        extractor_data["cat_file_ref"].seek(dds_addr + 20)
        size = struct.unpack("<i", extractor_data["cat_file_ref"].read(4))[0]

        # Minmap check
        extractor_data["cat_file_ref"].seek(dds_addr + 28)
        minmap_count = struct.unpack("<i", extractor_data["cat_file_ref"].read(4))[0]

        # Check for cubemap
        extractor_data["cat_file_ref"].seek(dds_addr + 113)
        cubemap_texture_count = _calc_cubemap_tex_count(
            struct.unpack("<B", extractor_data["cat_file_ref"].read(1))[0]
        )

        # Extraction
        extractor_data["cat_file_ref"].seek(dds_addr)
        a.write(extractor_data["cat_file_ref"].read(size + 128))

        if cubemap_texture_count > 0:
            for i in range(cubemap_texture_count - 1):
                a.write(extractor_data["cat_file_ref"].read(size))

        if minmap_count > 0:
            temp_size = size
            for i in range(minmap_count - 1):
                temp_size //= 2
                a.write(extractor_data["cat_file_ref"].read(temp_size))


def extract_dds_all(path):
    for _, index in enumerate(extractor_data["dds_entries"]):
        extract_dds(index, path)


def insert_dds(texture_index, new_texture_path):
    texture_index = int(texture_index)
    dds_addr = extractor_data["dds_entries"][texture_index]

    print(f"Writing {new_texture_path} to cat file...")
    with open(new_texture_path, "rb") as a:
        extractor_data["cat_file_ref"].seek(dds_addr)
        extractor_data["cat_file_ref"].write(a.read())


def insert_dds_all(new_texture_path, cat_ref):
    print(cat_ref)
    full_path = os.path.abspath(new_texture_path)
    textures = [x for x in os.scandir(full_path) if x.name.count(cat_ref) > 0]
    for t in textures:
        for _, index in enumerate(extractor_data["dds_entries"]):
            if t.name.count(f"{cat_ref}_{index}.dds") > 0:
                insert_dds(index, t.path)


def _find_dds_entries(cat_path):
    count = 0
    pos = 0

    dump = extractor_data["cat_file_ref"].read()

    pos = dump.find(b"\x44\x53\x20")
    while pos != -1:
        count += 1
        extractor_data["dds_entries"][count] = pos - 1
        pos = dump.find(b"\x44\x53\x20", pos + 1)


def _list_parsed_files(filenames: os.DirEntry):
    print("Parsed files:")
    for i in filenames:
        print(f"- {i.name}")


def _calc_cubemap_tex_count(cubemap_value):
    if cubemap_value == 0:
        return 0

    flag = 128
    count = 0
    while cubemap_value != 0 or flag >= 1:
        if cubemap_value - flag >= 0:
            cubemap_value -= flag
            count += 1

        flag //= 2

    if count > 0:
        count -= 1

    return count


# ---------------------------------------------------------------------------------


if __name__ == "__main__":

    # Prepare stuff
    args = sys.argv[1:]
    valid_options = list(min_args.keys())

    full_path = os.path.abspath(args[0])
    path = full_path.rsplit("\\", 1)[0]
    wildcard = full_path.rsplit("\\", 1)[1]

    # Search files
    dir_entries = [
        f
        for f in os.scandir(path)
        if (f.name.count(wildcard) >= 1 and f.name.count(".cat") >= 1)
    ]

    if len(dir_entries) > 0:
        _list_parsed_files(dir_entries)
        print("________________________\n")
    else:
        print("No .cat files found")

    for f in dir_entries:
        with open(f.path, "r+b") as cat_file:

            # Initialisation
            extractor_data["cat_name"] = f.name
            extractor_data["cat_file_ref"] = cat_file
            _find_dds_entries(f)

            # Argument parsing
            for arg_i, arg in enumerate(args):
                if arg in valid_options:
                    try:
                        determine_action(arg_i, args)
                    except Exception as e:
                        print(f"Uh oh ({e})")
