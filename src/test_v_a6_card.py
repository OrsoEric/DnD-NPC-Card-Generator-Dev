# python src/test_v_a6_card.py

# ────────────────────────────────────────────────────────────────────────────── #
#   File:  src/test_w_card_composition.py                                  #
#   Purpose: Create an A4 page that contains a centered red A6 rectangle,     #
#            then duplicate the same page to form a two‑page PDF.           #
#   Author: <your name>                                                    #
# ────────────────────────────────────────────────────────────────────────────── #

from PIL import Image, ImageDraw
import typing

# ────────────────────────────────────────────────────────────────────────────── #
#   Constants & type aliases                                                      #
# ────────────────────────────────────────────────────────────────────────────── #
MM_TO_INCH: float = 1 / 25.4                    # Millimetres → inches
DPI: int = 300                                  # Desired resolution (dots per inch)

A4_W_MM: int = 210                              # A4 width in millimetres
A4_H_MM: int = 297                              # A4 height in millimetres

A6_W_MM: int = 105                              # A6 width in millimetres
A6_H_MM: int = 148                              # A6 height in millimetres


# ────────────────────────────────────────────────────────────────────────────── #
#   Utility helpers                                                               #
# ────────────────────────────────────────────────────────────────────────────── #
def mm_to_px(i_mm: int) -> int:
    """
    Convert a measurement from millimetres to pixels at the current DPI.

    Parameters
    ----------
    i_mm : int
        The value in millimetres that should be converted.

    Returns
    -------
    int
        Equivalent pixel count for the specified DPI.
    """
    return int(i_mm * MM_TO_INCH * DPI)


# ────────────────────────────────────────────────────────────────────────────── #
#   Build one page (A4 with centered A6)                                         #
# ────────────────────────────────────────────────────────────────────────────── #
def build_a4_with_centered_a6(
    i_s_fill_color : str = "red"
) -> Image.Image:
    """
    Create a single PDF page: an A4 sheet containing a red centred A6 rectangle.

    Returns
    -------
    PIL.Image.Image
        The resulting canvas that can be written to a PDF.
    """
    # Convert the physical dimensions to pixels
    a4_px_width: int = mm_to_px(A4_W_MM)
    a4_px_height: int = mm_to_px(A4_H_MM)

    a6_px_width: int = mm_to_px(A6_W_MM)
    a6_px_height: int = mm_to_px(A6_H_MM)

    # -------------------------------------------------------------------------- #
    #   Canvas
    # -------------------------------------------------------------------------- #
    cl_canvas: Image.Image = Image.new("RGB", (a4_px_width, a4_px_height), "white")
    draw_obj: ImageDraw.ImageDraw = ImageDraw.Draw(cl_canvas)

    # -------------------------------------------------------------------------- #
    #   Compute the top‑left corner of the centred A6 rectangle
    # -------------------------------------------------------------------------- #
    x0: int = (a4_px_width - a6_px_width) // 2
    y0: int = (a4_px_height - a6_px_height) // 2

    # Bottom‑right corner
    x1: int = x0 + a6_px_width
    y1: int = y0 + a6_px_height

    # -------------------------------------------------------------------------- #
    #   Draw the red rectangle
    # -------------------------------------------------------------------------- #
    draw_obj.rectangle([x0, y0, x1, y1], fill=i_s_fill_color)

    return cl_canvas



# ────────────────────────────────────────────────────────────────────────────── #
#   Demo / entry point                                                            #
# ────────────────────────────────────────────────────────────────────────────── #

if __name__ == "__main__":
    s_output_pdf_path: str = "output/a4_with_a6_centered_two_pages.pdf"
    
    cl_first_page = build_a4_with_centered_a6("red")

    cl_second_page = build_a4_with_centered_a6("blue")


    cl_first_page.save(
        s_output_pdf_path,
        format="PDF",
        resolution=DPI,
        save_all=True,                    # Enables multi‑page mode
        append_images=[cl_second_page],      # Pages that follow the first one
    )
