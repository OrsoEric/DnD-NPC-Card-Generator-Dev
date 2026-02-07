# I want to load the NPC information
# python src\test_l_load_npc.py     


# no shorthands – fully qualified names are used

import logging
import json
from typing import Any, Dict

from lib.cl_utility_path import convert_to_path


class Cl_npc:
    """
    A simple container for an NPC’s D&D 5E data.
    Every attribute follows the “type‑prefix + description” convention.

    Attributes
    ----------
    s_name : str
        The NPC’s name.
    s_race : str
        The NPC’s race.
    s_description : str
        Long form description of the NPC.
    n_proficiency : int
        Proficiency bonus (numeric).
    n_strength : int
        Strength score.
    n_str_save : int
        Strength saving throw modifier.
    n_athletics : int
        Athletics skill modifier.
    n_dexterity : int
        Dexterity score.
    n_dex_save : int
        Dexterity saving throw modifier.
    n_acrobatics : int
        Acrobatics skill modifier.
    n_sleight_of_hand : int
        Sleight of Hand skill modifier.
    n_stealth : int
        Stealth skill modifier.
    n_constitution : int
        Constitution score.
    n_con_save : int
        Constitution saving throw modifier.
    n_intelligence : int
        Intelligence score.
    n_int_save : int
        Intelligence saving throw modifier.
    n_arcana : int
        Arcana skill modifier.
    n_investigation : int
        Investigation skill modifier.
    n_history : int
        History skill modifier.
    n_nature : int
        Nature skill modifier.
    n_religion : int
        Religion skill modifier.
    n_wisdom : int
        Wisdom score.
    n_wis_save : int
        Wisdom saving throw modifier.
    n_animal_handling : int
        Animal Handling skill modifier.
    n_insight : int
        Insight skill modifier.
    n_perception : int
        Perception skill modifier.
    n_medicine : int
        Medicine skill modifier.
    n_survival : int
        Survival skill modifier.
    n_charisma : int
        Charisma score.
    n_cha_save : int
        Charisma saving throw modifier.
    n_deception : int
        Deception skill modifier.
    n_intimidation : int
        Intimidation skill modifier.
    n_performance : int
        Performance skill modifier.
    n_persuasion : int
        Persuasion skill modifier.
    """

    def __init__(self) -> None:
        # Basic information --------------------------------------------------
        self.s_name: str = ""
        self.s_race: str = ""
        self.s_description: str = ""

        # Proficiency / stats -----------------------------------------------
        self.n_proficiency: int = 0
        self.n_strength: int = 0
        self.n_str_save: int = 0
        self.n_athletics: int = 0

        self.n_dexterity: int = 0
        self.n_dex_save: int = 0
        self.n_acrobatics: int = 0
        self.n_sleight_of_hand: int = 0
        self.n_stealth: int = 0

        self.n_constitution: int = 0
        self.n_con_save: int = 0

        self.n_intelligence: int = 0
        self.n_int_save: int = 0
        self.n_arcana: int = 0
        self.n_investigation: int = 0
        self.n_history: int = 0
        self.n_nature: int = 0
        self.n_religion: int = 0

        self.n_wisdom: int = 0
        self.n_wis_save: int = 0
        self.n_animal_handling: int = 0
        self.n_insight: int = 0
        self.n_perception: int = 0
        self.n_medicine: int = 0
        self.n_survival: int = 0

        self.n_charisma: int = 0
        self.n_cha_save: int = 0
        self.n_deception: int = 0
        self.n_intimidation: int = 0
        self.n_performance: int = 0
        self.n_persuasion: int = 0

    # --------------------------------------------------------------------- #
    def load_from_dict(self, i_data: Dict[str, Any]) -> bool:
        """
        Populate the NPC instance from a dictionary.

        Parameters
        ----------
        i_data : dict
            A mapping that contains keys matching the JSON field names.
        """
        self.s_name = i_data.get("name", "")
        self.s_race = i_data.get("race", "")
        self.s_description = i_data.get("description", "")

        # Proficiency and stats ---------------------------------------------
        self.n_proficiency = i_data.get("PROFICIENCY", 0)
        self.n_strength = i_data.get("STRENGTH", 0)
        self.n_str_save = i_data.get("STR SAVE", 0)
        self.n_athletics = i_data.get("ATHLETICS", 0)

        self.n_dexterity = i_data.get("DEXTERITY", 0)
        self.n_dex_save = i_data.get("DEX SAVE", 0)
        self.n_acrobatics = i_data.get("ACROBATICS", 0)
        self.n_sleight_of_hand = i_data.get("SLEIGHT OF HAND", 0)
        self.n_stealth = i_data.get("STEALTH", 0)

        self.n_constitution = i_data.get("CONSTITUTION", 0)
        self.n_con_save = i_data.get("CON SAVE", 0)

        self.n_intelligence = i_data.get("INTELLIGENCE", 0)
        self.n_int_save = i_data.get("INT SAVE", 0)
        self.n_arcana = i_data.get("ARCANA", 0)
        self.n_investigation = i_data.get("INVESTIGATION", 0)
        self.n_history = i_data.get("HISTORY", 0)
        self.n_nature = i_data.get("NATURE", 0)
        self.n_religion = i_data.get("RELIGION", 0)

        self.n_wisdom = i_data.get("WISDOM", 0)
        self.n_wis_save = i_data.get("WIS SAVE", 0)
        self.n_animal_handling = i_data.get("ANIMAL HANDLING", 0)
        self.n_insight = i_data.get("INSIGHT", 0)
        self.n_perception = i_data.get("PERCEPTION", 0)
        self.n_medicine = i_data.get("MEDICINE", 0)
        self.n_survival = i_data.get("SURVIVAL", 0)

        self.n_charisma = i_data.get("CHARISMA", 0)
        self.n_cha_save = i_data.get("CHA SAVE", 0)
        self.n_deception = i_data.get("DECEPTION", 0)
        self.n_intimidation = i_data.get("INTIMIDATION", 0)
        self.n_performance = i_data.get("PERFORMANCE", 0)
        self.n_persuasion = i_data.get("PERSUASION", 0)

        return False

    # --------------------------------------------------------------------- #
    @classmethod
    def from_file(cls, i_ls_path: list[str]) -> "Cl_npc":
        """
        Load an NPC definition from a JSON file.

        Parameters
        ----------
        i_path : str
            Path to the JSON file that contains the NPC data.

        Returns
        -------
        Npc
            An instance populated with the information from the file.
        """

        s_path = st_path = convert_to_path(i_ls_path)

        logging.info(f"Json Path {s_path}")

        with open(s_path, "r", encoding="utf-8") as file_obj:
            json_data: Dict[str, Any] = json.load(file_obj)

        npc_instance = cls()
        npc_instance.load_from_dict(json_data)
        return npc_instance



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