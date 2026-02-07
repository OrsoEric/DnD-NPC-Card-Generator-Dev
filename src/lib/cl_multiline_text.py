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
            i_cl_imgage: Image.Image,
            i_s_text: str,
            i_w_margin: int,
            i_h_margin: int,
            i_w_border: int,
            i_h_border: int,
            i_s_font_name: str,
            i_n_font_size: int,
            i_tn_color: tuple[int, int, int] = (0, 0, 0),
            i_n_padding: int = 5,
            i_x_draw_border: bool = False,
            i_tn_border_color: tuple[int, int, int] = (0, 0, 0)
            ) -> bool:
        """
        Render wrapped text into a fixed-size rectangle on an existing image.
        """

        cl_draw: ImageDraw.Draw = ImageDraw.Draw(i_cl_imgage)

        st_font = ImageFont.truetype(i_s_font_name, i_n_font_size)

        if i_n_font_size <= 0:
            print(f"ERR: invalid font size: {i_n_font_size}")
            return True 

        if i_x_draw_border:
            cl_draw.rectangle(
                [
                    i_w_margin,
                    i_h_margin,
                    i_w_margin + i_w_border,
                    i_h_margin + i_h_border
                ],
                outline=i_tn_border_color
            )

        # Wrap text to inner width
        inner_width: int = i_w_border - (2 * i_n_padding)

        wrapped_lines: List[str] = (
            Cl_multiline_text.wrap_text_into_lines(
                i_text=i_s_text,
                i_max_width=inner_width,
                i_draw=cl_draw,
                i_font=st_font
            )
        )

        # Render
        Cl_multiline_text.draw_wrapped_text(
            i_draw=cl_draw,
            i_x=i_w_margin + i_n_padding,
            i_y=i_h_margin + i_n_padding,
            i_lines=wrapped_lines,
            i_font=st_font,
            i_text_color=i_tn_color
        )
        return False #OK

if __name__ == "__main__":
    cl_image = Image.new("RGB", (400, 300), (255, 255, 255))

    Cl_multiline_text.render_fixed_size_text_box(
        i_cl_imgage = cl_image,
        i_s_text = "This is a reusable multiline text box renderer This is a reusable multiline text box renderer . . ..",
        i_w_margin = 20,
        i_h_margin = 20,
        i_w_border = 250,
        i_h_border = 120,
        i_s_font_name = "arial.ttf",
        i_n_font_size = 18,
        i_tn_color = (127, 127, 127),
        i_n_padding = 5,
        i_x_draw_border = True,
        i_tn_border_color = (255,0,0)
    )

    cl_image.save("outest_i_multiline_text.png")
