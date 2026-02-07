"""
python src\test_g_card_back_description.py


This is a stronger effort to get closer to the application
I start making the class
"""

"""
Utility for turning a JSON layout into a list of structured
attribute/ability descriptors.

This module intentionally keeps no Pillow imports – the data is purely
logical, making it suitable for further processing, validation,
or later rendering in any graphics library you choose.
"""

import logging

import json
from pathlib import Path
from typing import List
    
#This structure holds an attribute or an ability
from lib.st_attribute_ability import St_attribute_ability

def load_layout(
    i_ls_file_path: List[str],
    i_card_width: int,
    i_card_height: int,
) -> List[St_attribute_ability]:
    """
    Load a card layout from JSON and convert it into a list of
    :class:`St_attribute_ability` objects.

    The JSON file is expected to contain an ``attributes_and_abilities`` key
    whose value is an array.  Each element may use *percent‑per‑thousand*
    (`*_ppt`) values to describe positions and font sizes relative to the
    card dimensions – these are converted into pixel coordinates.

    Parameters
    ----------
    i_file_path : str
        Path to the JSON file that defines the layout.
    i_card_width : int
        Width of the card in pixels.  This value is used for scaling
        percent‑based positions.
    i_card_height : int
        Height of the card in pixels.

    Returns
    -------
    List[St_attribute_ability]
        A list, one entry per attribute/ability defined in the JSON,
        with all coordinates expressed in absolute pixel values.
    """
    # --------------------------------------------------------------------- #
    # 1. Read and parse the JSON file
    # --------------------------------------------------------------------- #
    l_layout_path: Path = Path(*i_ls_file_path).with_suffix(".json")
    if not l_layout_path.is_file():
        raise FileNotFoundError(f"Layout file does not exist: {i_ls_file_path}")

    with l_layout_path.open("r", encoding="utf-8") as cl_file:
        ln_json_data: dict[str, object] = json.load(cl_file)

    try:
        lv_abilities: List[dict[str, object]] = ln_json_data["attributes_and_abilities"]
    except KeyError as exc:
        raise ValueError("JSON layout must contain an 'attributes_and_abilities' key") from exc

    # --------------------------------------------------------------------- #
    # 2. Convert each entry to St_attribute_ability
    # --------------------------------------------------------------------- #
    l_result: List[St_attribute_ability] = []

    h_cursor = 0
    w_cursor = 0

    for st_item in lv_abilities:
        # ----------------------------------------------------------------- #
        #   Name
        # ----------------------------------------------------------------- #
        s_name: str = str(st_item.get("s_name", ""))

        n_w_pos_ppt: int | float = st_item.get("w_pos_ppt", 0)
        n_h_pos_ppt: int | float = st_item.get("h_pos_ppt", 0)

        w_name_px: int = int(i_card_width * n_w_pos_ppt / 1000)
        h_name_px: int = int(i_card_height * n_h_pos_ppt / 1000)

        if (h_cursor <= 0):
            w_cursor = w_name_px
            h_cursor = h_name_px
        else:
            w_cursor += w_name_px
            h_cursor += h_name_px

        # ----------------------------------------------------------------- #
        #   Font Size
        # ----------------------------------------------------------------- #

        h_font_ppt : int = st_item.get("h_font_ppt", 0)
        h_font_px = i_card_height * h_font_ppt / 1000

        # ----------------------------------------------------------------- #
        #   Modifier
        # ----------------------------------------------------------------- #
        s_modifier_value: str = str(st_item.get("s_modifier_value", ""))

        # The layout may provide a dedicated position for the modifier.
        # If it is missing we simply use the same X coordinate as the name.
        n_w_mod_pos_ppt: int | float = st_item.get("w_pos_modifier_ppt")
        if n_w_mod_pos_ppt is not None:
            w_mod_px: int = int(i_card_width * n_w_mod_pos_ppt / 1000)
        else:
            w_mod_px: int = w_name_px

        # ----------------------------------------------------------------- #
        #   Assemble the dataclass instance
        # ----------------------------------------------------------------- #
        cl_ability: St_attribute_ability = St_attribute_ability(
            s_name=s_name,
            w_name_pos_px = w_cursor,
            h_name_pos_px = h_cursor,
            h_name_font = h_font_px,

            s_modifier_value=s_modifier_value,
            w_modifier_pos_px=w_cursor -w_mod_px,
        )
        l_result.append(cl_ability)

    return l_result

if __name__ == "__main__":
    logging.basicConfig(
        filename="test_g.log",
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("BEGIN")

    lst_abilities_attributes = load_layout(
        i_ls_file_path= ["src", "json", "test_e_layout_back.json"],
        i_card_width= 750,
        i_card_height= 1000,
    )

    for st_temp in lst_abilities_attributes:
        logging.info(st_temp)

    logging.info("END")
    