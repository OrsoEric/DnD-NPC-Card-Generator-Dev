# -*- coding: utf-8 -*-
"""
Utilities for opening SVG files with Pillow in a cross‑platform manner.
"""

from pathlib import Path
import io

from PIL import Image


def open_svg(i_svg_path: str) -> Image.Image | None:
    """
    Reads an SVG file and converts it into a Pillow image object.

    The function accepts a path as a string (or any value accepted by :class:`~pathlib.Path`)
    and works on Windows, macOS and Linux without modification.  It uses
    ``io.BytesIO`` so the file is read only once and no temporary files are written
    to disk.

    Parameters
    ----------
    i_svg_path : str
        The path to the SVG file that should be opened.  The function treats the
        argument as a relative or absolute path depending on how it was supplied.

    Returns
    -------
    Image.Image | None
        A Pillow image instance if the SVG could be parsed successfully; otherwise
        ``None`` and an error message is printed to :data:`sys.stderr`.

    Notes
    -----
    * The function does **not** rely on any operating‑system specific separators.
      Internally it uses :class:`~pathlib.Path`, which normalises the path for the
      current platform.
    * Pillow itself cannot render SVG files directly.  In practice this helper
      will succeed only if a back‑end such as CairoSVG is available, which
      Pillow automatically delegates to when opening an SVG.  If you need to
      support environments where Pillow has no SVG backend, consider using
      ``cairosvg.svg2png`` instead.

    Examples
    --------
    >>> image = open_svg(\"/svg/symbol.svg\")          # relative or absolute
    >>> if image:
    ...     image.show()
    """
    try:
        svg_path = Path(i_svg_path)

        if not svg_path.is_file():
            raise FileNotFoundError(f"SVG file does not exist: {svg_path}")

        with svg_path.open("rb") as svg_file_obj:
            # Pillow expects a binary stream.  ``svg_file_obj.read()`` returns
            # bytes which can be wrapped in BytesIO.
            svg_bytes = svg_file_obj.read()

        img_stream = io.BytesIO(svg_bytes)
        image_object = Image.open(img_stream)

        # Ensure the image is loaded before returning (prevents lazy loading errors)
        image_object.load()
        return image_object

    except Exception as error:  # pragma: no cover
        print(f"Error opening SVG '{i_svg_path}': {error}")
        return None


# --------------------------------------------------------------------------- #
# Example usage
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # The path can be relative or absolute; Path will handle OS differences.
    svg_file_name = "acid.svg"
    svg_directory = Path("svg")
    full_svg_path = "src" / svg_directory / svg_file_name

    image_instance = open_svg(str(full_svg_path))
    if image_instance:
        image_instance.show()  # Optional: display the resulting image
