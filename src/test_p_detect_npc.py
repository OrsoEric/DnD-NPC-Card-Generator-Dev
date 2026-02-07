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
from lib.cl_utility_path import find_file_pair_image_json
from lib.cl_utility_path import build_path_output_jpg

# -*- coding: utf-8 -*-



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

    s_output_image = build_path_output_jpg( "output", lts_pair[0][0] )
    logging.info(f"Output image path {s_output_image}")

    logging.info("END")











