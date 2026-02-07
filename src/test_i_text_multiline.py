# ------------------------------------------------------------------
#  Imports
# ------------------------------------------------------------------
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
from typing import List


# ------------------------------------------------------------------
#  Multiline Text Utility Class
# ------------------------------------------------------------------
class Cl_multiline_text:

    # --------------------------------------------------------------
    #  Font handling
    # --------------------------------------------------------------
    @staticmethod
    def load_font(
            i_font_path: str,
            i_font_size: int) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(i_font_path, i_font_size)

    # --------------------------------------------------------------
    #  Measurement helpers
    # --------------------------------------------------------------
    @staticmethod
    def measure_text_width(
            i_draw: ImageDraw.Draw,
            i_string: str,
            i_font: ImageFont.FreeTypeFont) -> int:
        return i_draw.textlength(i_string, font=i_font)

    # --------------------------------------------------------------
    #  Text wrapping
    # --------------------------------------------------------------
    @staticmethod
    def wrap_text_into_lines(
            i_text: str,
            i_max_width: int,
            i_draw: ImageDraw.Draw,
            i_font: ImageFont.FreeTypeFont) -> List[str]:

        words: List[str] = i_text.split()
        wrapped_lines: List[str] = []
        current_line: str = ""

        for word in words:
            tentative_line: str = f"{current_line} {word}".strip()

            if (Cl_multiline_text.measure_text_width(
                    i_draw, tentative_line, i_font) <= i_max_width):
                current_line = tentative_line
            else:
                if current_line:
                    wrapped_lines.append(current_line)
                current_line = word

        if current_line:
            wrapped_lines.append(current_line)

        return wrapped_lines

    # --------------------------------------------------------------
    #  Rendering
    # --------------------------------------------------------------
    @staticmethod
    def draw_wrapped_text(
            i_draw: ImageDraw.Draw,
            i_x: int,
            i_y: int,
            i_lines: List[str],
            i_font: ImageFont.FreeTypeFont,
            i_text_color: tuple[int, int, int],
            i_line_spacing: int = 0) -> None:

        line_height: int = i_draw.textbbox(
            (0, 0), "A", font=i_font
        )[3]

        y_offset: int = 0

        for line in i_lines:
            i_draw.text(
                (i_x, i_y + y_offset),
                line,
                fill=i_text_color,
                font=i_font
            )
            y_offset += line_height + i_line_spacing

    # --------------------------------------------------------------
    #  Public API: render into an existing image
    # --------------------------------------------------------------
    @staticmethod
    def render_fixed_size_text_box(
            i_img: Image.Image,
            i_text: str,
            i_box_x: int,
            i_box_y: int,
            i_box_width: int,
            i_box_height: int,
            i_font: ImageFont.FreeTypeFont,
            i_text_color: tuple[int, int, int] = (0, 0, 0),
            i_padding: int = 5,
            i_draw_border: bool = False,
            i_border_color: tuple[int, int, int] = (0, 0, 0)
            ) -> None:
        """
        Render wrapped text into a fixed-size rectangle on an existing image.
        """

        cl_draw: ImageDraw.Draw = ImageDraw.Draw(i_img)

        if i_draw_border:
            cl_draw.rectangle(
                [
                    i_box_x,
                    i_box_y,
                    i_box_x + i_box_width,
                    i_box_y + i_box_height
                ],
                outline=i_border_color
            )

        # Wrap text to inner width
        inner_width: int = i_box_width - (2 * i_padding)

        wrapped_lines: List[str] = (
            Cl_multiline_text.wrap_text_into_lines(
                i_text=i_text,
                i_max_width=inner_width,
                i_draw=cl_draw,
                i_font=i_font
            )
        )

        # Render
        Cl_multiline_text.draw_wrapped_text(
            i_draw=cl_draw,
            i_x=i_box_x + i_padding,
            i_y=i_box_y + i_padding,
            i_lines=wrapped_lines,
            i_font=i_font,
            i_text_color=i_text_color
        )

if __name__ == "__main__":
    img = Image.new("RGB", (400, 300), (255, 255, 255))
    font = Cl_multiline_text.load_font("arial.ttf", 18)

    Cl_multiline_text.render_fixed_size_text_box(
        i_img=img,
        i_text="This is a reusable multiline text box renderer This is a reusable multiline text box renderer . . ..",
        i_box_x=20,
        i_box_y=20,
        i_box_width=250,
        i_box_height=120,
        i_font=font,
        i_draw_border=True
    )

    img.save("outest_i_multiline_text.png")
