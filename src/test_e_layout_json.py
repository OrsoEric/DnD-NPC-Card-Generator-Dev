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

    return cl_image


# --------------------------------------------------------------------------- #
# Example class that uses the above helpers – demonstrates a minimal card
# generator. The style is kept intentionally simple so it can be extended.
# --------------------------------------------------------------------------- #
class Cl_card_generator:
    """
    Class that encapsulates constants and helper methods for generating
    card images based on an external layout definition file.
    """

    # Constants (public class variables)
    cn_card_width: int = 400
    cn_card_height: int = 600
    cn_background_color: tuple[int, int, int] = (255, 255, 255)  # white
    cn_border_color: tuple[int, int, int] = (0, 0, 0)  # black

    def __init__(self, i_layout_file_path: str):
        """
        Load the layout from *i_layout_file_path* and keep it for later use.

        Parameters:
            i_layout_file_path (str): Path to the JSON file containing the layout.
        """
        self.ln_loaded_layout = load_layout_from_json(i_layout_file_path)

    def generate_card_back(self) -> image.Image:
        """
        Generate a card back that contains only the border and background.

        Returns:
            PIL.Image.Image: The generated card back image.
        """
        cl_image = image.new(
            "RGB",
            (self.cn_card_width, self.cn_card_height),
            self.cn_background_color,
        )
        cl_draw = draw.Draw(cl_image)

        # Draw the border
        n_border_width = 5
        cl_draw.rectangle(
            [
                (n_border_width, n_border_width),
                (
                    self.cn_card_width - n_border_width,
                    self.cn_card_height - n_border_width,
                ),
            ],
            outline=self.cn_border_color,
            width=n_border_width,
        )
        return cl_image

    def generate_full_card(self) -> image.Image:
        """
        Generate a full card that contains the border, background and all layout
        items.

        Returns:
            PIL.Image.Image: The generated card image.
        """
        return draw_layout_to_image(
            self.ln_loaded_layout,
            self.cn_card_width,
            self.cn_card_height,
            self.cn_background_color,
            self.cn_border_color,
        )

# --------------------------------------------------------------------------- #
# Example class that uses the above helpers – demonstrates a minimal card
# generator. The style is kept intentionally simple so it can be extended.
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    s_path_json_layout : str = str(Path("src") / Path("json") / Path("layout_back.json"))
    # Create a 5 px/mm A‑4 sheet
    st_layout_back = load_layout_from_json( s_path_json_layout )

    print(st_layout_back)

    cl_card_generator = Cl_card_generator()
    cl_card_generator.d
