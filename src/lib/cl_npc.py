# I want to load the NPC information
#   call .venv\Scripts\activate.bat
#   python src\test_l_load_npc.py     


# no shorthands – fully qualified names are used

import logging
import json
from typing import Any, Dict

from lib.cl_utility_path import convert_to_path


class Cl_npc:
    

    def __init__(self) -> None:
        """
        dictionary with the npc definition
        """

        g_d_npc : dict = dict()

        return

    def load_from_file( self, i_ls_path: list[str]) -> bool: 
        """
        """
        
        s_path = convert_to_path(i_ls_path)

        logging.info(f"Json Path {s_path}")

        with open(s_path, "r", encoding="utf-8") as file_obj:
            json_data: Dict[str, Any] = json.load(file_obj)

        return False #OK

if __name__ == "__main__":
    # Setup logging
    s_log_path = convert_to_path(["log","test_l_load_npc.log"])
    print(f"Log Path: {s_log_path}")

    logging.basicConfig(
        filename=s_log_path,
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("BEGIN")

    cl_npx = Cl_npc.from_file(["src", "json", "demo_npc_b.json"])
    logging.info(f"NPC: {cl_npx.__dict__}" )

    logging.info("END")