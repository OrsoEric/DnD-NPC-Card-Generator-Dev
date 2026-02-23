# I should not have localization in the layout json
# instead the layout should specify size and dpi
# and I unload all s_text in the NPC json
# so I have a dimensional file that is text independent
# and a npc file that is layout independent


#   call .venv\Scripts\activate.bat
#   python src\test_t_layout_dimension.py


"""
Class for generating NPC character sheet images from JSON layout definitions.

This module provides a class that combines the functionality of loading
card layouts from JSON and rendering them into PIL Images.
"""

import json
import logging
from typing import List, Dict, Any, Tuple, Optional
from pathlib import Path
import PIL.Image as image
import PIL.ImageDraw as draw
import PIL.ImageFont as font

from lib.cl_utility_path import convert_to_path

from lib.cl_utility_path import find_file_pair_image_json

from lib.cl_utility_path import build_path_output_jpg

from lib.st_image import St_image
#this utility allows to draw a multiline text box onto an image

from lib.cl_generator import Cl_npc_character_sheet_generator

def generate_card() -> bool:
    x_fail = Cl_npc_character_sheet_generator.find_and_generate_cards(
        #card layout descriptor
        i_ls_layout_file_path  = ["src", "json", "npc_layout.json"],
        #card image frame overlay
        i_ls_mask_front_path = ["mask", "front_mask.png"],
        i_ls_mask_back_path =["mask", "back_mask.png"] ,
        #pair of image and json
        i_s_input_folder = "input",
        #where save output
        i_s_output_folder ="output"
    )

    return x_fail

# Example usage
if __name__ == "__main__":
    # Setup logging
    s_log_path = convert_to_path(["log","test_t_localization.log"])
    print(f"Log Path: {s_log_path}")

    logging.basicConfig(
        filename=s_log_path,
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("BEGIN")

    generate_card()

    logging.info("END")
    print("Card back generated successfully!")