#
#   python src\test_i_text_multiline.py

# ------------------------------------------------------------------
#  Imports
# ------------------------------------------------------------------

import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
from typing import List
from lib.cl_utility_path import convert_to_path
from lib.cl_multiline_text import Cl_multiline_text


if __name__ == "__main__":
    cl_image = Image.new("RGB", (800, 600), (255, 255, 255))

    s_font_path = convert_to_path(["font","fantasy.ttf"])

    h_box = Cl_multiline_text.render_fixed_size_text_box(
        i_cl_imgage = cl_image,
        i_s_text = "This is a reusable multiline text box renderer This is a reusable multiline text box renderer . . ..",
        i_w_margin = 20,
        i_h_margin = 20,
        i_w_border = 250,
        i_h_border = 0,
        i_s_font_name = s_font_path,
        i_n_font_size = 25,
        i_tn_color = (127, 127, 127),
        i_n_padding = 5,
        i_x_draw_border = True,
        i_tn_border_color = (255,0,0)
    )

    print(f"W: {h_box}")
    s_output_path = convert_to_path(["output","outest_i_multiline_text.png"])
    cl_image.save(s_output_path)
