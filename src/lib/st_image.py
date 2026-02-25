# ────────────────────────────────────────────────────────────────────────────── #
#   File:  st_image.py                                                      #
#   Purpose: Image container + helper methods for manipulation and saving.    #
#            Adds `save_pdf` – creates one PDF from many A4 images.          
#   Author: Orso Eric
# ────────────────────────────────────────────────────────────────────────────── 

import logging
from pathlib import Path

#import PIL.Image

from PIL import Image

from lib.cl_utility_path import convert_to_path


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
        i_w_card_mm: float,
        i_h_card_mm: float,
        i_dot_per_inch: int,
    ) -> None:
        """
        Initialise the structure and set all configuration values.

        All parameters are kept private; they are prefixed with an underscore to
        signal that they should not be accessed directly from user code.
        """
        self.g_w_card_mm: float = i_w_card_mm          #: Width of a standard card in millimetres.
        self.g_h_card_mm: float = i_h_card_mm          #: Height of a standard card in millimetres.
        self.g_n_dot_per_inch: int = i_dot_per_inch    #: DPI – dots (pixels) per inch.
        self.g_n_mm_per_inch: float = 25.4            #: Millimetres per inch.

        # Image size in pixels will be calculated next
        self.g_w_card_px: int = int(0)
        self.g_h_card_px: int = int(0)

        self.g_cl_image : Image.Image = None


        x_fail = self.compute_px()
        if x_fail:
            logging.error("ERR: invalid image size")
            return

        self.create_image(self.g_w_card_px, self.g_h_card_px)

    # ----------------------------------------------------------------------- #
    # PUBLIC API
    # ----------------------------------------------------------------------- #

    def compute_px(self) -> bool:
        """
        Compute the pixel width and height that correspond to the physical
        card dimensions at the configured DPI.

        Returns:
            A two‑tuple ``(width_px, height_px)`` containing the size in pixels.
        """
        logging.debug(f"W mm: {self.g_w_card_mm} | H mm {self.g_h_card_mm}")

        self.g_w_card_px = int(
            self.g_w_card_mm / self.g_n_mm_per_inch * self.g_n_dot_per_inch
        )
        self.g_h_card_px = int(
            self.g_h_card_mm / self.g_n_mm_per_inch * self.g_n_dot_per_inch
        )

        logging.debug(f"W px: {self.g_w_card_px} | H px {self.g_h_card_px}")

        if self.g_w_card_px <= 0 or self.g_h_card_px <= 0:
            logging.error("ERR: invalid image size")
            return True

        return False

    def get_size(self) -> tuple[int, int]:
        """
        Return the image dimensions in pixels.
        """
        return (self.g_w_card_px, self.g_h_card_px)

    # ----------------------------------------------------------------------- #
    # Drawing / Compositing
    # ----------------------------------------------------------------------- #

    def draw_image(
        self,
        i_source_st_image: "St_image",
        i_offset_px: tuple[int, int],
        i_size_px: tuple[int, int],
    ) -> bool:
        """
        Draw a portion of *i_source_st_image* onto the current image.
        """
        if getattr(self, "g_cl_image", None) is None:
            logging.error("No destination image available for drawing.")
            return True

        if getattr(i_source_st_image, "g_cl_image", None) is None:
            logging.error("Source St_image has no image to draw.")
            return True

        lcl_source_img: Image.Image = i_source_st_image.g_cl_image

        # Resize source if requested size differs from its native resolution
        if (i_size_px[0] != lcl_source_img.width or
                i_size_px[1] != lcl_source_img.height):
            lcl_source_img = lcl_source_img.resize(
                (i_size_px[0], i_size_px[1]),
                resample=PIL.Image.Resampling.LANCZOS,
            )

        # Paste the processed source image onto the destination at the given offset.
        try:
            self.g_cl_image.paste(lcl_source_img, i_offset_px)
        except Exception as exc:  # pragma: no cover
            logging.exception("Failed to paste image: %s", exc)
            return True

        logging.debug(
            "Pasted source image (%sx%s) at offset (%d,%d) onto destination "
            "(%dx%d).",
            lcl_source_img.width,
            lcl_source_img.height,
            i_offset_px[0],
            i_offset_px[1],
            self.g_cl_image.width,
            self.g_cl_image.height,
        )

        return False

    def create_image(
        self,
        i_w_size_px: int,
        i_h_size_px: int,
        i_color: str = "white",
    ) -> bool:
        """
        Create a new RGB image that matches the physical dimensions of the card.
        """
        self.g_cl_image = Image.new("RGB", (i_w_size_px, i_h_size_px), color=i_color)
        return False

    def destroy_image(self) -> None:
        """Destroy the currently stored image."""
        if getattr(self, "g_cl_image", None) is not None:
            try:  # pragma: no cover
                getattr(self.g_cl_image, "close")()
            finally:
                del self.g_cl_image
                self.g_cl_image = None

    def apply_global_opacity_to_image(
        self,
        i_desired_opacity: float,
    ) -> bool:
        """
        Applies a uniform opacity factor to every pixel of an RGBA image.
        """
        ln_pixels = self.g_cl_image.load()
        n_width, n_height = self.g_cl_image.size

        for i_x in range(n_width):
            for j_y in range(n_height):
                r_value, g_value, b_value, a_value = ln_pixels[i_x, j_y]
                n_new_alpha: int = int(round(a_value * i_desired_opacity))
                n_new_alpha = max(0, min(255, n_new_alpha))  # clamp to [0,255]
                ln_pixels[i_x, j_y] = (r_value, g_value, b_value, n_new_alpha)

        return False

    def compose_image(
        self,
        i_st_mask_with_transparency: "St_image",
        i_n_opacity: float,
    ) -> bool:
        """Composite a mask onto the current image."""
        i_st_mask_with_transparency.apply_global_opacity_to_image(i_n_opacity)

        self.g_cl_image = Image.alpha_composite(
            self.g_cl_image.convert("RGBA"),
            i_st_mask_with_transparency.g_cl_image.convert("RGBA"),
        )
        return False

    # ----------------------------------------------------------------------- #
    # File I/O
    # ----------------------------------------------------------------------- #

    def load_image(
        self,
        i_ls_path: list[str] | Path,
    ) -> bool:
        """
        Load an image from the supplied path components and store it in this
        instance.
        """
        if isinstance(i_ls_path, list):
            s_image_path = convert_to_path(i_ls_path)
        else:
            s_image_path = i_ls_path

        try:
            cl_image_loaded: Image.Image = Image.open(s_image_path)
        except Exception as exc:  # pragma: no cover
            logging.exception("Failed to load image from %s: %s", s_image_path, exc)
            return True

        # Resize to the card size using LANCZOS for high quality.
        cl_image_resized = cl_image_loaded.resize(
            (self.g_w_card_px, self.g_h_card_px), resample=Image.LANCZOS
        )

        self.g_cl_image = cl_image_resized
        return False

    def save_image(
        self,
        i_ls_path: list[str] | Path,
        i_s_format="PNG",
    ) -> bool:
        """
        Persist the current image to disk.
        """
        if getattr(self, "g_cl_image", None) is None:
            return True  # error

        if isinstance(i_ls_path, list):
            s_image_path = convert_to_path(i_ls_path)
        else:
            s_image_path = i_ls_path

        logging.debug(f"input: {i_ls_path} path: {s_image_path}")

        self.g_cl_image.save(
            str(s_image_path),
            format=i_s_format,
            dpi=(self.g_n_dot_per_inch, self.g_n_dot_per_inch),
        )
        return False

    # ----------------------------------------------------------------------- #
    # NEW METHOD – SAVE A LIST OF A4 IMAGES AS ONE PDF
    # ----------------------------------------------------------------------- #

    @classmethod
    def save_pdf(
        cls,
        i_ls_st_images: list["St_image"],
        i_ls_path: list[str] | Path,
    ) -> bool:
        """
        Save a sequence of ``St_image`` objects as one multi‑page PDF.

        The method expects all images in *i_ls_st_images* to be A4‑sized
        (or at least the same size).  It uses Pillow's ``save`` with
        ``save_all=True`` and passes the remaining images via
        ``append_images``.  The DPI is taken from the first image, which should
        match all others.

        Parameters
        ----------
        i_ls_st_images : list[St_image]
            A list of already‑initialised ``St_image`` instances that each hold
            a Pillow image.
        i_ls_path : list[str] | Path
            File system path components (or a single ``Path``) where the PDF
            should be written.

        Returns
        -------
        bool
            ``False`` if the PDF was created successfully, ``True`` otherwise.
        """
        if not i_ls_st_images:
            logging.error("No images supplied for PDF generation.")
            return True

        # Build a list of Pillow Image objects, validating that each has data.
        lcl_pil_imgs: list[Image.Image] = []
        for idx, st_img in enumerate(i_ls_st_images):
            if getattr(st_img, "g_cl_image", None) is None:
                logging.error(
                    f"Image at index {idx} does not contain image data."
                )
                return True
            lcl_pil_imgs.append(st_img.g_cl_image)

        # Resolve the output path.
        if isinstance(i_ls_path, list):
            s_pdf_path: Path = convert_to_path(i_ls_path)
        else:
            s_pdf_path = i_ls_path

        try:
            dpi_tuple = (
                i_ls_st_images[0].g_n_dot_per_inch,
                i_ls_st_images[0].g_n_dot_per_inch,
            )
            lcl_pil_imgs[0].save(
                str(s_pdf_path),
                format="PDF",
                dpi=dpi_tuple,
                save_all=True,
                append_images=lcl_pil_imgs[1:],
            )
        except Exception as exc:  # pragma: no cover
            logging.exception("Failed to write PDF file %s: %s", s_pdf_path, exc)
            return True

        return False

    # ----------------------------------------------------------------------- #
    # REPRESENTATION HELPERS (optional)
    # ----------------------------------------------------------------------- #

    def __repr__(self) -> str:
        """
        Return a concise representation that includes the size of the stored
        image if it exists.
        """
        if getattr(self, "g_cl_image", None) is not None:
            return (
                f"{self.__class__.__name__}(image="
                f"{self.g_cl_image.size[0]}x{self.g_cl_image.size[1]})"
            )
        else:
            return f"{self.__class__.__name__}()"


# ────────────────────────────────────────────────────────────────────────────── #
#   TEST BENCH
# ────────────────────────────────────────────────────────────────────────────── #

if __name__ == "__main__":
    # Create a single instance and save it as PNG.
    st = St_image(
        i_w_card_mm=210, i_h_card_mm=297, i_dot_per_inch=300
    )
    st.save_image(["output", "test_bench_st_image"])

    # Example of writing two instances into one PDF (uncomment to test):
    # st2 = St_image(i_w_card_mm=210, i_h_card_mm=297, i_dot_per_inch=300)
    # St_image.save_pdf([st, st2], ["output", "cards.pdf"])
