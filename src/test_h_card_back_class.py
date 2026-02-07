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
from lib.st_attribute_ability import St_attribute_ability
from lib.st_image import St_image


class Cl_npc_character_sheet_generator:
    """
    A class for generating NPC character sheet images from JSON layout definitions.
    
    This class encapsulates the functionality to load card layouts from JSON files
    and render them into PIL Images with proper positioning and font handling.
    """

    # Default colors for the generated images
    CN_DEFAULT_BACKGROUND_COLOR: Tuple[int, int, int] = (255, 255, 255)  # white
    CN_DEFAULT_BORDER_COLOR: Tuple[int, int, int] = (0, 0, 0)            # black
    CN_BORDER_WIDTH: int = 5

    def __init__(
        self,
        i_w_card_width_mm: float,
        i_h_card_height_mm: float,
        i_n_dots_per_inch : int,
        i_background_color: Optional[Tuple[int, int, int]] = None,
        i_border_color: Optional[Tuple[int, int, int]] = None
    ):
        """
        Initialize the character sheet generator with card dimensions and colors.
        
        Parameters
        ----------
        i_card_width : int
            Width of the card in pixels.
        i_card_height : int
            Height of the card in pixels.
        i_background_color : tuple[int, int, int] or None, default=None
            RGB background colour.  If ``None`` a default white is used.
        i_border_color : tuple[int, int, int] or None, default=None
            RGB border colour.  If ``None`` a default black is used.
        """

        self.g_w_card_width_mm: float = i_w_card_width_mm
        self.g_h_card_height_mm: float = i_h_card_height_mm
        self.g_n_dots_per_inch: int = i_n_dots_per_inch

        self.g_tn_background_color: Tuple[int, int, int] = (
            i_background_color or self.CN_DEFAULT_BACKGROUND_COLOR
        )

        self.g_tn_border_color: Tuple[int, int, int] = (
            i_border_color or self.CN_DEFAULT_BORDER_COLOR
        )

        self.g_cl_image_card_back : St_image = St_image(
            i_w_card_mm = self.g_w_card_width_mm,
            i_h_card_mm = self.g_h_card_height_mm,
            i_dot_per_inch = self.g_n_dots_per_inch
        )

        return

    def load_layout_from_json(
        self,
        i_file_path: str,
    ) -> List[Dict[str, Any]]:
        """
        Load the card layout specification from a JSON file.
        
        Parameters
        ----------
        i_file_path : str
            Path to the JSON file that contains the layout definition.

        Returns
        -------
        list[dict]
            A list where each element represents a single layout item.
            The dictionary keys are the ones used in the JSON
            (e.g. ``s_name``, ``w_pos`` …).
        """
        logging.info(f"Loading layout from: {i_file_path}")
        with open(i_file_path, "r", encoding="utf-8") as cl_file:
            ln_layout_data = json.load(cl_file)
        logging.info("Layout loaded successfully")
        return ln_layout_data

    def load_layout(
        self,
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
        l_layout_path = convert_to_path(i_ls_file_path)
        logging.info(f"Loading layout from: {l_layout_path}")
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

        logging.info(f"Successfully converted {len(l_result)} layout items")
        return l_result

    def draw_layout_to_image(
        self,
        i_ld_layout: List[Dict[str, Any]],
        i_cl_image : St_image
    ) -> bool:
        """
        Draw the layout described by *i_layout* onto a new PIL Image.
        
        Parameters
        ----------
        i_layout : list[dict]
            The list of layout items as returned by
            :func:`load_layout_from_json`.

        Returns
        -------
        PIL.Image.Image
            An image that contains the drawn layout.
        """
        logging.info("Drawing layout to image")
        # Create base image and drawing context
        cl_draw = draw.Draw(i_cl_image.g_cl_image)

        w_size_px = i_cl_image.g_w_card_px
        h_size_px = i_cl_image.g_h_card_px

        # Draw a simple rectangle border
        cl_draw.rectangle(
            [
                (self.CN_BORDER_WIDTH, self.CN_BORDER_WIDTH),
                (
                    w_size_px - self.CN_BORDER_WIDTH,
                    h_size_px - self.CN_BORDER_WIDTH,
                ),
            ],
            outline=self.g_tn_border_color,
            width=self.CN_BORDER_WIDTH,
        )

        # Default font – Pillow will fallback to a built‑in one if the path is wrong
        cl_default_font = font.load_default()

        try:
            ast_abilities = i_ld_layout["attributes_and_abilities"]
        except KeyError:
            logging.error("JSON layout missing 'attributes_and_abilities' key")
            print("ERR: field doesn't exist, json is wrong")
            return True #ERROR

        w_cursor = 0
        h_cursor = 0

        # Render each layout item; skip anything that isn't a dict
        for st_item in ast_abilities:
            
            # PPT part per thousand of the whole image
            # This way it's scale independent
            s_text: str = st_item.get("s_name", "")
            w_pos_ppt: int = st_item.get("w_pos_ppt", 0)
            h_pos_ppt: int = st_item.get("h_pos_ppt", 0)
            h_font_ppt: int = st_item.get("h_font_ppt", 0)
            
            # Convert PPT values to pixels
            w_pos_px = w_size_px * w_pos_ppt / 1000
            h_pos_px = h_size_px * h_pos_ppt / 1000
            h_font_px = h_size_px * h_font_ppt / 1000

            # Load a truetype font if possible, otherwise fall back to the default
            try:
                cl_item_font = font.truetype(
                    "verdana.ttf",
                    int(h_font_px),
                )
            except OSError:
                cl_item_font = cl_default_font
                logging.warning("Failed to load verdana.ttf, using default font")
                print("ERR: failed to load font")

            if (h_cursor <= 0):
                w_cursor = w_pos_px
                h_cursor = h_pos_px
            else:
                w_cursor += w_pos_px
                h_cursor += h_pos_px

            # Add the header for the attribute or ability 
            cl_draw.text((w_cursor, h_cursor), s_text, fill=(0, 0, 0), font=cl_item_font)
            # Fetch the numerical value of attribute or ability
            cl_draw.text((w_cursor, h_cursor), "+10", fill=(0, 0, 0), font=cl_item_font, anchor="ra")

        logging.info("Layout drawing completed successfully")
        return False #OK

    def generate_card_back(
        self,
        i_ls_layout_file_path: List[str],
        i_ls_output_file_path: List[str],
        i_background_color: Optional[Tuple[int, int, int]] = None,
        i_border_color: Optional[Tuple[int, int, int]] = None
    ) -> image.Image:
        """
        Generate a card back image from the specified JSON layout file.
        
        Parameters
        ----------
        i_layout_file_path : list[str]
            Path components to the JSON file that defines the layout.
        i_output_file_path : str
            Path where the generated image will be saved.
        i_background_color : tuple[int, int, int] or None, default=None
            RGB background colour.  If ``None`` a default white is used.
        i_border_color : tuple[int, int, int] or None, default=None
            RGB border colour.  If ``None`` a default black is used.

        Returns
        -------
        PIL.Image.Image
            The generated image object.
        """
        logging.info("Starting card back generation")
        
        # Load the layout from JSON
        st_layout = self.load_layout_from_json(convert_to_path(i_ls_layout_file_path))
        logging.info("Layout loaded successfully")


        # Draw the layout to an image
        cl_image = self.draw_layout_to_image(
            st_layout,
            self.g_cl_image_card_back
        )
        logging.info("Image drawn successfully")

        # Save the image
        logging.info(f"Saving image to: {i_ls_output_file_path}")
        self.g_cl_image_card_back.save_image(i_ls_output_file_path)
        logging.info("Image saved successfully")
        
        return cl_image

# Example usage
if __name__ == "__main__":
    # Setup logging
    s_log_path = convert_to_path(["log","test_h.log"])
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
    cl_generated_image = cl_generator.generate_card_back(
        i_ls_layout_file_path=["src", "json", "test_e_layout_back.json"],
        i_ls_output_file_path=["output","test_h_card_back.png"]
    )
    
    logging.info("END")
    print("Card back generated successfully!")