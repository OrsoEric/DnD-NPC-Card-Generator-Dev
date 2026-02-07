"""
python src\test_e_layout_json.py
"""

# -*- coding: utf-8 -*-
"""
Utility functions and a small helper class for working with the card layout
definition that is stored in JSON format.
"""

import json
from typing import Any, Dict, List

from pathlib import Path

import PIL.Image as image
import PIL.ImageDraw as draw
import PIL.ImageFont as font

def load_layout_from_json(
    i_file_path: str,
) -> List[Dict[str, Any]]:
    """
    Load the card layout specification from a JSON file.

    Parameters:
        i_file_path (str): Path to the JSON file that contains the layout definition.

    Returns:
        list[dict]: A list where each element represents a single layout item.
                    The dictionary keys are the ones used in the JSON
                    (e.g. ``s_name``, ``w_pos`` …).
    """
    with open(i_file_path, "r", encoding="utf-8") as cl_file:
        ln_layout_data = json.load(cl_file)
    return ln_layout_data


def draw_layout_to_image(
    i_layout: List[Dict[str, Any]],
    i_card_width: int,
    i_card_height: int,
    i_background_color: tuple[int, int, int],
    i_border_color: tuple[int, int, int],
) -> image.Image:
    """
    Draw the layout described by *i_layout* onto a new PIL Image.

    Parameters:
        i_layout (list[dict]): The list of layout items as returned by
                               :func:`load_layout_from_json`.
        i_card_width (int):   Width of the card in pixels.
        i_card_height (int):  Height of the card in pixels.
        i_background_color (tuple[int, int, int]): RGB background color.
        i_border_color (tuple[int, int, int]): RGB border color.

    Returns:
        PIL.Image.Image: An image that contains the drawn layout.
    """
    # Create base image and drawing context
    cl_image = image.new("RGB", (i_card_width, i_card_height), i_background_color)
    cl_draw = draw.Draw(cl_image)

    # Draw a simple border
    n_border_width = 5
    cl_draw.rectangle(
        [
            (n_border_width, n_border_width),
            (
                i_card_width - n_border_width,
                i_card_height - n_border_width,
            ),
        ],
        outline=i_border_color,
        width=n_border_width,
    )

    # Default font – Pillow will fall back to a built‑in one if the path is empty
    cl_default_font = font.load_default()

    # Render each layout item
    for st_item in i_layout:
        s_text: str = st_item.get("s_name", "")
        n_x_pos: int = st_item.get("w_pos", 0)
        n_y_pos: int = st_item.get("h_pos", 0)
        n_font_size: int = st_item.get("h_font", 12)

        # Load a truetype font if possible, otherwise fall back to the default
        try:
            cl_item_font = font.truetype(
                "arial.ttf",
                n_font_size,
            )
        except OSError:
            cl_item_font = cl_default_font

        cl_draw.text((n_x_pos, n_y_pos), s_text, fill=(0, 0, 0), font=cl_item_font)

CN_DEFAULT_BACKGROUND_COLOR: tuple[int, int, int] = (255, 255, 255)  # white
CN_DEFAULT_BORDER_COLOR: tuple[int, int, int] = (0, 0, 0)            # black
CN_BORDER_WIDTH: int = 5

def draw_layout_to_image(
    i_layout: List[Dict[str, Any]],
    i_card_width: int,
    i_card_height: int,
    i_background_color: tuple[int, int, int] | None = None,
    i_border_color: tuple[int, int, int] | None = None,
) -> image.Image:
    """
    Render the supplied layout into a new PIL Image.

    Parameters
    ----------
    i_layout : list[dict]
        Layout data returned by :func:`load_layout_from_json`.
    i_card_width : int
        Width of the output card in pixels.
    i_card_height : int
        Height of the output card in pixels.
    i_background_color : tuple[int, int, int] or None, default=None
        RGB background colour.  If ``None`` a default white is used.
    i_border_color : tuple[int, int, int] or None, default=None
        RGB border colour.  If ``None`` a default black is used.

    Returns
    -------
    PIL.Image.Image
        An image object that contains the drawn layout.
    """
    tn_background_color: tuple[int, int, int] = (
        i_background_color or CN_DEFAULT_BACKGROUND_COLOR
    )
    tn_border_color: tuple[int, int, int] = (
        i_border_color or CN_DEFAULT_BORDER_COLOR
    )

    # Create base image and drawing context
    cl_image: image.Image = image.new(
        "RGB",
        (i_card_width, i_card_height),
        tn_background_color,
    )
    cl_draw: draw.Draw = draw.Draw(cl_image)

    # Draw a simple rectangle border
    cl_draw.rectangle(
        [
            (CN_BORDER_WIDTH, CN_BORDER_WIDTH),
            (
                i_card_width - CN_BORDER_WIDTH,
                i_card_height - CN_BORDER_WIDTH,
            ),
        ],
        outline=tn_border_color,
        width=CN_BORDER_WIDTH,
    )

    # Default font – Pillow will fallback to a built‑in one if the path is wrong
    cl_default_font: font.FreeTypeFont = font.load_default()

    try:
        ast_abilities = i_layout["attributes_and_abilities"]
    except:
        print("ERR: field doesn't exist, json is wrong")
        return cl_draw

    cursor_w = 0
    cursor_h = 0

    # Render each layout item; skip anything that isn’t a dict
    for st_item in ast_abilities:
        
        #PPT part per thousand of the whole image
        #This way it's scale independent
        s_text : str = st_item.get("s_name", "")
        w_pos_ppt : int = st_item.get("w_pos_ppt", 0)
        h_pos_ppt : int = st_item.get("h_pos_ppt", 0)
        h_font_ppt : int = st_item.get("h_font_ppt", 0)
        #PX
        w_pos_px = i_card_width * w_pos_ppt / 1000
        h_pos_px = i_card_height * h_pos_ppt / 1000
        h_font_px = i_card_height * h_font_ppt / 1000

        try:
            cl_item_font: font.FreeTypeFont = font.truetype(
                "verdana.ttf",
                h_font_px,
            )
        except OSError:
            cl_item_font = cl_default_font
            print("ERR: failed to load font")

        if (cursor_h <= 0):
            cursor_w = w_pos_px
            cursor_h = h_pos_px
        else:
            cursor_w += w_pos_px
            cursor_h += h_pos_px

        #add the header for the attribute or ability 
        cl_draw.text((cursor_w, cursor_h), s_text, fill=(0, 0, 0), font=cl_item_font)
        #fetch the numerical value of attribute or ability
        cl_draw.text((cursor_w, cursor_h), "+10", fill=(0, 0, 0), font=cl_item_font, anchor="ra")

        

    return cl_image

# --------------------------------------------------------------------------- #
# Example class that uses the above helpers – demonstrates a minimal card
# generator. The style is kept intentionally simple so it can be extended.
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    s_path_json_layout : str = str(Path("src") / Path("json") / Path("test_e_layout_back.json"))
    # Create a 5 px/mm A‑4 sheet
    st_layout_back = load_layout_from_json( s_path_json_layout )

    print(st_layout_back)

    w_card_mm = 63.5
    h_card_mm = 88.9
    dot_per_inch = 300
    mm_per_inch = 25.4

    w_card_px : int = int(w_card_mm / mm_per_inch * dot_per_inch)
    h_card_px : int = int(h_card_mm / mm_per_inch * dot_per_inch)
    print(f"Image size: W: {w_card_px} H: {h_card_px}")

    # Create an image from that data
    cl_card_image: image.Image = draw_layout_to_image(
        st_layout_back,
        i_card_width = w_card_px,
        i_card_height = h_card_px,
        i_background_color=(255, 255, 255),
        i_border_color=(0, 0, 0),
    )

    # Persist the result
    c_s_output_path: Path = Path("output") / "test_e_back_json.png"

    cl_card_image.save(c_s_output_path)