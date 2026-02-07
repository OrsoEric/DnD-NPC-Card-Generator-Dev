#!/usr/bin/env python3
"""
Image creation utility

This script creates an RGB image that is 67 mm wide and 88 mm high,
with a resolution of 10 pixels per millimetre.  
It then loads the SVG file located at ``/svg/symbol.svg``, scales it to
10 % of the resulting image size, places the rasterised SVG on the
bottom‑right corner of the background and finally writes the picture
to ``test.jpg``.
"""

# ----------------------------------------------------------------------
# Imports – no aliases are used.  All modules are referenced by their
# full names in accordance with the style guidelines.
# ----------------------------------------------------------------------
import io          # for BytesIO stream
import PIL.Image   # Pillow image handling
import cairosvg    # conversion from SVG to PNG


# ----------------------------------------------------------------------
# Constants – public class variables with a ``c`` prefix.
# ----------------------------------------------------------------------
class ImageParameters:
    """Container for image size and resolution constants."""
    c_mm_width: int = 67                # width of the image in millimetres
    c_mm_height: int = 88               # height of the image in millimetres
    c_pixels_per_mm: int = 10           # pixels per millimetre


# ----------------------------------------------------------------------
# Functions – all input variables are prefixed with ``i_``.
# ----------------------------------------------------------------------
def create_test_image() -> None:
    """
    Generates a JPEG image that contains a rasterised SVG placed at the
    bottom‑right corner.

    The background is created with Pillow, the SVG file is converted to a
    PNG using cairosvg and finally pasted onto the background.  The final
    image is written as ``test.jpg`` in the current working directory.
    """
    # ------------------------------------------------------------------
    # Image size calculation – everything expressed in pixels.
    # ------------------------------------------------------------------
    n_img_width_px: int = (
        ImageParameters.c_mm_width * ImageParameters.c_pixels_per_mm
    )
    n_img_height_px: int = (
        ImageParameters.c_mm_height * ImageParameters.c_pixels_per_mm
    )

    # ------------------------------------------------------------------
    # Create a white background image.
    # ------------------------------------------------------------------
    im_background: PIL.Image.Image = PIL.Image.new(
        mode="RGB",
        size=(n_img_width_px, n_img_height_px),
        color="white",
    )

    # ------------------------------------------------------------------
    # Determine SVG target size – 10 % of the background image.
    # ------------------------------------------------------------------
    n_svg_target_width_px: int = int(n_img_width_px * 0.1)
    n_svg_target_height_px: int = int(n_img_height_px * 0.1)

    # ------------------------------------------------------------------
    # Convert the SVG file to PNG in memory.
    # ------------------------------------------------------------------
    s_svg_path: str = "/svg/symbol.svg"
    b_png_bytes: bytes = cairosvg.svg2png(
        url=s_svg_path,
        output_width=n_svg_target_width_px,
        output_height=n_svg_target_height_px,
    )
    im_svg_pil: PIL.Image.Image = PIL.Image.open(
        io.BytesIO(b_png_bytes)
    )

    # ------------------------------------------------------------------
    # Compute the top‑left coordinate for bottom‑right placement.
    # ------------------------------------------------------------------
    n_pos_x: int = n_img_width_px - n_svg_target_width_px
    n_pos_y: int = n_img_height_px - n_svg_target_height_px

    # ------------------------------------------------------------------
    # Paste the rasterised SVG onto the background.  If the SVG has an
    # alpha channel it is respected by using ``mask``.
    # ------------------------------------------------------------------
    if im_svg_pil.mode == "RGBA":
        im_background.paste(im_svg_pil, (n_pos_x, n_pos_y), mask=im_svg_pil)
    else:
        im_background.paste(im_svg_pil, (n_pos_x, n_pos_y))

    # ------------------------------------------------------------------
    # Save the resulting image as JPEG.
    # ------------------------------------------------------------------
    s_output_path: str = "test.jpg"
    im_background.save(s_output_path, format="JPEG")


# ----------------------------------------------------------------------
# Entry point – executed when the script is run directly.
# ----------------------------------------------------------------------
if __name__ == "__main__":
    create_test_image()
