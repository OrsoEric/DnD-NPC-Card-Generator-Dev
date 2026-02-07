#   call .venv\Scripts\activate.bat
#   python src\test_p_detect_npc.py

"""
detects content from the input folder
["input"]
I expect an image, and a json file of the same name
Generations will be dumped in the output folder
["output"]
"""

import logging
from typing import List, Dict, Tuple
from pathlib import Path

from lib.cl_utility_path import convert_to_path

# -*- coding: utf-8 -*-


def find_file_pair_image_json(i_s_folder : str) -> List[Tuple[Path, Path]]:
    """
    Locate pairs of JPEG/PNG images and a JSON file that share the same stem in the given directory.

    Parameters:
        i_cl_path (pathlib.Path): Path to the input directory containing image and JSON files.

    Returns:
        List[Tuple[pathlib.Path, pathlib.Path, pathlib.Path]]: A list where each tuple contains
            the paths of a JPEG file, its matching PNG counterpart, and the associated JSON file.
            Only complete triplets (all three files present) are returned.

    Raises:
        FileNotFoundError: If the supplied path does not exist.
        NotADirectoryError: If the supplied path is not a directory.
    """

    i_cl_path : Path = Path(i_s_folder)

    # ---- Validation ----------------------------------------------------
    if not i_cl_path.exists():
        raise FileNotFoundError(f"Folder not found: {i_cl_path}")

    if not i_cl_path.is_dir():
        raise NotADirectoryError(f"Provided path is not a directory: {i_cl_path}")

    # ---- Gather files -----------------------------------------------
    # Mapping from file stem to the paths of jpg, png and json files
    d_stem_to_files = dict()

    for d_paths in i_cl_path.iterdir():
        
        if not d_paths.is_file():
            continue  # Skip directories or non‑files

        s_extension_lower: str = d_paths.suffix.lower()
        logging.debug(f"{d_paths} | {s_extension_lower}")
        s_file_without_extension: str = d_paths.stem

        # Ensure we have an entry for this stem
        d_entry = d_stem_to_files.setdefault(s_file_without_extension, {"jpg": None, "png": None, "json": None})

        if s_extension_lower == ".jpg":
            d_entry["jpg"] = d_paths.resolve()
        elif s_extension_lower == ".png":
            d_entry["png"] = d_paths.resolve()
        elif s_extension_lower == ".json":
            d_entry["json"] = d_paths.resolve()

    # ---- Build result -----------------------------------------------
    ltss_image_json: List[Tuple[Path, Path]] = []

    for s_file_without_extension, d_paths in d_stem_to_files.items():
        logging.debug(f" ENTRY {s_file_without_extension} | {d_paths}")
        #if I have a jpg, and a json
        if (d_paths["jpg"] and d_paths["json"]):
            ltss_image_json.append( (d_paths["jpg"], d_paths["json"]) )
        elif (d_paths["png"] and d_paths["json"]):
            ltss_image_json.append( (d_paths["png"], d_paths["json"]) )
        else:
            pass

    return ltss_image_json


# --------------------------------------------------------------------
# Example usage (uncomment to run as a script)
#
# if __name__ == "__main__":
#     input_dir = pathlib.Path("input")
#     triplets = i_find_image_json_pairs(input_dir)
#     for jpg, png, json_file in triplets:
#         print(f"JPEG: {jpg}\nPNG:  {png}\nJSON: {json_file}\n---")



# Example usage
if __name__ == "__main__":
    # Setup logging
    s_log_path = convert_to_path(["log","test_p_detect_npc.log"])
    print(f"Log Path: {s_log_path}")

    logging.basicConfig(
        filename=s_log_path,
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("BEGIN")

    lts_pair = find_file_pair_image_json("input")
    logging.info(f"{len(lts_pair)} | {lts_pair}")

    logging.info("END")











