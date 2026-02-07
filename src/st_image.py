"""
st_image.py

This module defines a structure that keeps an image together with its dimensional
information expressed in millimetres (mm), pixels (px) and dots per inch (dpi).
All configuration values are stored as **private instance attributes** – the
public API only exposes behaviour, not internal data.
"""

# --------------------------------------------------------------------------- #
# IMPORTS
# --------------------------------------------------------------------------- #

import pathlib
import PIL.Image

# --------------------------------------------------------------------------- #
# CLASS DEFINITION
# --------------------------------------------------------------------------- #


class St_image:
    """
    A container for an image together with its dimensional metadata.

    The configuration (card size, DPI, etc.) is stored in private instance
    variables that are initialised once when the object is created.  Users
    interact only through the public methods.
    """

    # ----------------------------------------------------------------------- #
    # CONSTRUCTOR
    # ----------------------------------------------------------------------- #

    def __init__(
        self,
        i_w_card_mm : float,
        i_h_card_mm : float,
        i_dot_per_inch : int
    ) -> None:
        """
        Initialise the structure and set all configuration values.

        All parameters are kept private; they are prefixed with an underscore to
        signal that they should not be accessed directly from user code.
        """
        self._w_card_mm: float = i_w_card_mm          #: Width of a standard card in millimetres.
        self._h_card_mm: float = i_h_card_mm          #: Height of a standard card in millimetres.
        self._dot_per_inch: int = i_dot_per_inch          #: DPI – dots (pixels) per inch.
        self._mm_per_inch: float = 25.4        #: Millimetres per inch.

        # The image itself is created lazily; ``None`` indicates that no
        # image exists yet.
        self._image: PIL.Image.Image | None = None

        self.create_image()

        return

    # ----------------------------------------------------------------------- #
    # PUBLIC API
    # ----------------------------------------------------------------------- #

    def compute_px(self) -> tuple[int, int]:
        """
        Compute the pixel width and height that correspond to the physical
        card dimensions at the configured DPI.

        Returns:
            A two‑tuple ``(width_px, height_px)`` containing the size in pixels.
        """
        n_width_px: int = int(
            self._w_card_mm / self._mm_per_inch * self._dot_per_inch
        )
        n_height_px: int = int(
            self._h_card_mm / self._mm_per_inch * self._dot_per_inch
        )
        return (n_width_px, n_height_px)

    def create_image(self, i_color: str = "white") -> None:
        """
        Create a new RGB image that matches the physical dimensions of the card.

        The created image is stored in :attr:`_image`.  If an image already
        exists it will be replaced.

        Parameters:
            i_color (str): The background colour of the blank image.
                Any colour recognised by Pillow can be used, e.g. "white",
                "#FF00FF" or a tuple ``(R, G, B)``.
        """
        n_width_px, n_height_px = self.compute_px()
        self._image: PIL.Image.Image = PIL.Image.new(
            mode="RGB", size=(n_width_px, n_height_px), color=i_color
        )

    def destroy_image(self) -> None:
        """
        Destroy the currently stored image.

        The method safely closes the Pillow image (if it implements the
        ``close`` protocol) and removes the reference so that Python's garbage
        collector can reclaim the memory.
        """
        if self._image is not None:
            try:  # pragma: no cover
                getattr(self._image, "close")()
            finally:
                del self._image
                self._image = None

    def save_image(self, i_path_parts: list[str]) -> None:
        """
        Persist the current image to disk as a PNG file.

        The list of strings is treated as successive components of a path
        (e.g. ``["output", "card.png"]``).  Any missing parent directories are
        created automatically.  If the supplied path does not have an extension,
        ``.png`` will be appended.

        Parameters:
            i_path_parts (list[str]): Components that together form the desired
                file path, e.g. a directory name and a filename without
                extension.

        Raises:
            ValueError: If no image has been created or loaded yet.
        """
        if self._image is None:
            raise ValueError(
                "No image available to save – call create_image() first."
            )

        # Build the destination path; ensure .png suffix.
        p_path = pathlib.Path(*i_path_parts).with_suffix(".png")

        # Ensure that all parent directories exist.
        p_path.parent.mkdir(parents=True, exist_ok=True)

        self._image.save(str(p_path), format="PNG")

    # ----------------------------------------------------------------------- #
    # REPRESENTATION HELPERS (optional)
    # ----------------------------------------------------------------------- #

    def __repr__(self) -> str:
        """
        Return a concise representation that includes the size of the stored
        image if it exists.
        """
        if self._image is not None:
            return (
                f"{self.__class__.__name__}(image={self._image.size[0]}x{self._image.size[1]})"
            )
        else:
            return f"{self.__class__.__name__}()"

# --------------------------------------------------------------------------- #
# TEST BENCH
# --------------------------------------------------------------------------- #

#from st_image import St_image

st = St_image(
    i_w_card_mm=63.5,
    i_h_card_mm = 88.9,
    i_dot_per_inch = 300
)

st.save_image(["output", "test_bench_st_image"])   # creates output/card.png
