# pylint: disable=missing-docstring

#python src/test_d_a4.py

import PIL.Image

from pathlib import Path


class Cl_Sheet:
    """
    Representation of a printable A‑4 sheet image with embedded DPI information.
    """

    # --- Class constants -------------------------------------------------
    c_a4_width_mm: float = 210.0   #: width of an A‑4 sheet in millimetres
    c_a4_height_mm: float = 297.0  #: height of an A‑4 sheet in millimetres
    c_mm_per_inch: float = 25.4     #: conversion factor from millimetres to inches

    def __init__(self, i_pixels_per_mm: float) -> None:
        """
        Initialise a new sheet image.

        Parameters
        ----------
        i_pixels_per_mm : float
            Desired pixel density expressed in pixels per millimetre.
            The resulting image will have a DPI value that corresponds to this
            density.

        Notes
        -----
        * The physical dimensions of an A‑4 paper are fixed at 210 mm × 297 mm.
          They are converted to pixel units by multiplying with the supplied
          resolution.
        * DPI is calculated as ``pixels_per_mm * mm_per_inch`` and rounded to the
          nearest integer so it can be written into common image formats
          (PNG, JPEG, TIFF).
        """
        # Compute pixel dimensions from millimetres and the target resolution.
        n_width_px: int = round(self.c_a4_width_mm * i_pixels_per_mm)
        n_height_px: int = round(self.c_a4_height_mm * i_pixels_per_mm)

        # Create a white RGB image of the calculated size.
        self.l_image: PIL.Image.Image = PIL.Image.new(
            mode="RGB",
            size=(n_width_px, n_height_px),
            color=(255, 255, 255)
        )

        # DPI (dots per inch) that matches the requested pixels‑per‑mm
        self.c_dpi_x: int = round(i_pixels_per_mm * self.c_mm_per_inch)
        self.c_dpi_y: int = self.c_dpi_x

    def save_to_file(self, i_filepath: str) -> None:
        """
        Persist the image to disk while embedding its DPI metadata.

        Parameters
        ----------
        i_filepath : str
            Full path (including extension) where the file should be written.
            The chosen format will automatically receive a ``dpi`` tag with
            the values stored in ``c_dpi_x`` / ``c_dpi_y``.

        Notes
        -----
        * Pillow supports writing DPI metadata for PNG, JPEG and TIFF formats
          when the ``dpi`` keyword argument is supplied.  This method does not
          perform any format‑specific checks; it simply passes the value.
        """
        self.l_image.save(i_filepath, dpi=(self.c_dpi_x, self.c_dpi_y))

    @property
    def image_size_mm(self) -> tuple[float, float]:
        """
        Return the physical dimensions of the sheet in millimetres.

        Returns
        -------
        (float, float)
            Tuple containing width and height in millimetres.
        """
        return self.c_a4_width_mm, self.c_a4_height_mm

    @property
    def image_pixel_size(self) -> tuple[int, int]:
        """
        Return the pixel dimensions of the sheet image.

        Returns
        -------
        (int, int)
            Tuple containing width and height in pixels.
        """
        return self.l_image.size


# ---------------------------------------------------------------------------

# Example usage --------------------------------------------------------------
if __name__ == "__main__":
    c_s_save_path : str = str(Path("output") / Path("test_d_a4.png"))
    # Create a 5 px/mm A‑4 sheet
    sheet: Cl_Sheet = Cl_Sheet(i_pixels_per_mm=5.0)

    # Save to PNG; DPI information will be embedded automatically.
    sheet.save_to_file(c_s_save_path)

    print(f"Image size (px): {sheet.image_pixel_size}")
    print(f"DPI: ({sheet.c_dpi_x}, {sheet.c_dpi_y})")
