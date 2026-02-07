
#   call .venv\Scripts\activate.bat
#   python src\test_o_card_front.py


"""
Class for generating NPC character sheet images from JSON layout definitions.

This module provides a class that combines the functionality of loading
card layouts from JSON and rendering them into PIL Images.
"""

import json
import logging
from typing import List, Dict, Any, Tuple, Optional

import PIL.Image as image
import PIL.ImageDraw as draw
import PIL.ImageFont as font

from lib.cl_utility_path import convert_to_path
from lib.st_image import St_image
#this utility allows to draw a multiline text box onto an image

from lib.cl_generator import Cl_npc_character_sheet_generator

# Example usage
if __name__ == "__main__":
    # Setup logging
    s_log_path = convert_to_path(["log","test_o_card_back_action.log"])
    print(f"Log Path: {s_log_path}")

    logging.basicConfig(
        filename=s_log_path,
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("BEGIN")

    cl_generator = Cl_npc_character_sheet_generator(
        i_w_card_width_mm=63.5,
        i_h_card_height_mm=88.9,
        i_n_dots_per_inch = 300,
        i_background_color=(255, 255, 255),
        i_border_color=(0, 0, 0)
    )

    # Generate the card back
    cl_generated_image = cl_generator.generate_card(
        i_ls_layout_file_path=["src", "json", "test_k_layout_back.json"],
        i_ls_npc_file_path = ["src", "json", "demo_npc_b.json"],
        i_ls_output_file_path=["output","test_o_card_back.png"]
    )
    
    logging.info("END")
    print("Card back generated successfully!")