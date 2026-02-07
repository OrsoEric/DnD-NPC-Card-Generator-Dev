"""
python src\test_f_text_box.py
"""


# ------------------------------------------------------------------
#  Imports (full module names only, no aliases)
# ------------------------------------------------------------------
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
from typing import List, Tuple
from pathlib import Path

# ------------------------------------------------------------------
#  Constants (public class variables with a “c” prefix)
# ------------------------------------------------------------------
class TextBoxConstants:
    # Colors
    c_text_color: tuple[int, int, int] = (0, 0, 0)          # black

    # Font settings
    c_font_path: str   = "arial.ttf"
    c_font_size: int   = 18

    # Box dimensions
    c_box_width:  int  = 250      # pixels
    c_box_height: int  = 150     # pixels

# ------------------------------------------------------------------
#  Helper Functions
# ------------------------------------------------------------------
def load_main_font() -> ImageFont.FreeTypeFont:
    """
    Load the font that will be used for all text rendering.

    Returns:
        PIL.ImageFont.FreeTypeFont – a loaded True‑type font.
    """
    return ImageFont.truetype(TextBoxConstants.c_font_path,
                               TextBoxConstants.c_font_size)


def measure_text_width(i_draw: ImageDraw.Draw,
                       i_string: str,
                       i_font: ImageFont.FreeTypeFont) -> int:
    """
    Return the width, in pixels, of a single line of text.

    Parameters:
        i_draw (ImageDraw.Draw): The drawing context used for measurement.
        i_string (str): Text to measure.
        i_font (ImageFont.FreeTypeFont): Font used for measuring.

    Returns:
        int – pixel width of the rendered string.
    """
    return i_draw.textlength(i_string, font=i_font)


def wrap_text_into_lines(
        i_text: str,
        i_max_width: int,
        i_draw: ImageDraw.Draw,
        i_font: ImageFont.FreeTypeFont) -> List[str]:
    """
    Split a paragraph into a list of lines such that each line fits within
    the specified maximum width.

    The algorithm is simple:
    1. Tokenise the text by whitespace.
    2. Build a candidate line word‑by‑word until adding another word would
       exceed i_max_width.
    3. Commit the current line and start a new one.

    Parameters:
        i_text (str): The paragraph to wrap.
        i_max_width (int): Maximum allowed pixel width for a line.
        i_draw (ImageDraw.Draw): Drawing context used for measurement.
        i_font (ImageFont.FreeTypeFont): Font used for measurement.

    Returns:
        List[str] – ordered list of wrapped lines.
    """
    words: List[str] = i_text.split()
    wrapped_lines: List[str] = []
    current_line: str = ""

    for word in words:
        # Try adding the next word to the current line
        tentative_line: str = f"{current_line} {word}".strip()

        if measure_text_width(i_draw, tentative_line, i_font) <= i_max_width:
            current_line = tentative_line
        else:
            # Current line is full – commit it
            wrapped_lines.append(current_line)
            current_line = word

    # Append the last line (might be empty if text ended with whitespace)
    if current_line:
        wrapped_lines.append(current_line)

    return wrapped_lines


def draw_wrapped_text(
        i_draw: ImageDraw.Draw,
        i_position_x: int,
        i_position_y: int,
        i_lines: List[str],
        i_font: ImageFont.FreeTypeFont) -> None:
    """
    Render a list of pre‑wrapped lines onto the image.

    Parameters:
        i_draw (ImageDraw.Draw): Drawing context.
        i_position_x (int): X coordinate of the top‑left corner of the box.
        i_position_y (int): Y coordinate of the top‑left corner of the box.
        i_lines (List[str]): Lines to render, already wrapped.
        i_font (ImageFont.FreeTypeFont): Font used for rendering.

    Returns:
        None
    """
    line_height: int = i_draw.textbbox((0, 0), "A", font=i_font)[3]
    y_offset: int   = 0

    for line in i_lines:
        i_draw.text(
            (i_position_x, i_position_y + y_offset),
            line,
            fill=TextBoxConstants.c_text_color,
            font=i_font
        )
        y_offset += line_height


# ------------------------------------------------------------------
#  Main rendering logic
# ------------------------------------------------------------------
def render_fixed_size_text_box() -> None:
    """
    Create an image that contains a fixed‑size rectangular box with wrapped
    text inside it. The resulting file is written to the current directory.
    """
    # 1. Create canvas and drawing context
    img_width: int  = TextBoxConstants.c_box_width + 20
    img_height: int = TextBoxConstants.c_box_height + 20
    background_color: tuple[int, int, int] = (255, 255, 255)   # white
    img: Image.Image = Image.new("RGB", (img_width, img_height),
                                 background_color)
    cl_draw: ImageDraw.Draw = ImageDraw.Draw(img)

    # 2. Load font
    main_font: ImageFont.FreeTypeFont = load_main_font()

    # 3. Define the rectangle position (top‑left corner inside the image)
    rect_x: int = 10
    rect_y: int = 10

    # 4. Draw a simple border to visualise the box
    cl_draw.rectangle(
        [rect_x, rect_y,
         rect_x + TextBoxConstants.c_box_width,
         rect_y + TextBoxConstants.c_box_height],
        outline=(0, 0, 0)   # black border
    )

    # 5. Paragraph to render
    paragraph_text: str = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        "Integer nec odio. Praesent libero. Sed cursus ante dapibus diam."
    )

    # 6. Wrap the paragraph into lines that fit inside the box width
    wrapped_lines: List[str] = wrap_text_into_lines(
        i_text=paragraph_text,
        i_max_width=TextBoxConstants.c_box_width,
        i_draw=cl_draw,
        i_font=main_font
    )

    # 7. Render the wrapped text starting a few pixels inside the border
    draw_wrapped_text(
        i_draw=cl_draw,
        i_position_x=rect_x + 5,          # padding from left edge
        i_position_y=rect_y + 5,          # padding from top edge
        i_lines=wrapped_lines,
        i_font=main_font
    )

    # 8. Save the image
    c_s_output_path: Path = Path("output") / "test_f_text_box.png"
    img.save(c_s_output_path)
    print("Image written to fixed_box_example.png")


# ------------------------------------------------------------------
#  Execute demo
# ------------------------------------------------------------------
if __name__ == "__main__":
    render_fixed_size_text_box()
