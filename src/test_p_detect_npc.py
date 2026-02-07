#   call .venv\Scripts\activate.bat
#   python src\test_o_card_front.py

"""
detects content from the input folder
["input"]
I expect an image, and a json file of the same name
Generations will be dumped in the output folder
["output"]
"""

import logging
from typing import List, Dict, Tuple

from lib.cl_utility_path import convert_to_path

def scan_for_file_pairs(i_base_dir: Path) -> List[Tuple[Path, Path]]:
    """
    Scan a directory for image‑JSON file pairs that share the same base name.

    The function looks for files with extensions defined in
    :class:`Configuration` and returns a list of tuples.
    Each tuple contains the absolute paths to an image file
    and its corresponding JSON metadata file.

    Parameters
    ----------
    i_base_dir : pathlib.Path
        Absolute path to the directory that should be scanned.

    Returns
    -------
    List[Tuple[pathlib.Path, pathlib.Path]]
        A list of found pairs.  The list is sorted lexicographically by base name.
    """
    # Maps base names to their image and JSON paths
    l_image_files: Dict[str, Path] = {}
    l_json_files: Dict[str, Path] = {}

    # Collect all files in the directory
    for ln_file_path in i_base_dir.iterdir():
        if not ln_file_path.is_file():
            continue

        s_suffix_lower: str = ln_file_path.suffix.lower()

        # Detect image files
        if s_suffix_lower in ["jpg, "png"]:
            l_image_files[ln_file_path.stem] = ln_file_path.resolve()
        # Detect JSON metadata files
        elif s_suffix_lower == Configuration.c_json_extension:
            l_json_files[ln_file_path.stem] = ln_file_path.resolve()

    # Find common base names that have both an image and a JSON file
    l_common_bases: List[str] = sorted(
        set(l_image_files.keys()) & set(l_json_files.keys())
    )

    l_pairs: List[Tuple[Path, Path]] = []
    for s_base in l_common_bases:
        l_pairs.append((l_image_files[s_base], l_json_files[s_base]))

    return l_pairs



# Example usage
if __name__ == "__main__":
    # Setup logging
    s_log_path = convert_to_path(["log","test_p_detect_npc.py"])
    print(f"Log Path: {s_log_path}")

    logging.basicConfig(
        filename=s_log_path,
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("BEGIN")

    logging.info("END")











