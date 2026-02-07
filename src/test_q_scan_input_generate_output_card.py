#   call .venv\Scripts\activate.bat
#   python src\test_q_scan_input_generate_output_card.py


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

from lib.st_image import St_image
#this utility allows to draw a multiline text box onto an image

from lib.cl_generator import Cl_npc_character_sheet_generator

def generate_card() -> bool:
    #look at the input folder, and scan for image/json files with same name, our NPCs
    ltss_npc_input_path = find_file_pair_image_json("input")

    if (len(ltss_npc_input_path) < 0):
        logging.error("ERR: no valid file pair in the input folder")
        return True #FAIL

    for tss_npc_input_path in ltss_npc_input_path:
        
        #unpack
        s_image_path = tss_npc_input_path[0]
        s_json_path = tss_npc_input_path[1]
        logging.info(f"Processing NPC files {s_image_path} {s_json_path} ")

        
        # construct the output path
        logging.info(f"Processing NPC files {Path("output",f"{s_json_path.name}") } ")
        


        cl_generator = Cl_npc_character_sheet_generator(
            i_w_card_width_mm=63.5,
            i_h_card_height_mm=88.9,
            i_n_dots_per_inch = 300,
            i_background_color=(255, 255, 255),
            i_border_color=(0, 0, 0)
        )
        logging.info("Constructed NPC generator class...")

        # Generate the card back
        cl_generated_image = cl_generator.generate_card(
            i_ls_layout_file_path=["src", "json", "npc_layout.json"],
            #i_ls_mask_front_path=["mask", "front_mask_transparent.png"],
            i_ls_mask_front_path=["mask", "front_mask_d.png"],
            i_ls_npc_illustration_path= s_image_path,
            i_ls_npc_json_path = s_json_path,
            i_ls_output_file_path=["output","test_q_card_back.png"]
        )
        

    return False #OK

# Example usage
if __name__ == "__main__":
    # Setup logging
    s_log_path = convert_to_path(["log","test_q_card_back_action.log"])
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