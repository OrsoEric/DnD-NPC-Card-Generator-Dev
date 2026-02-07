
# TASK

You are a D&D 5E Dungeon Master tasked with creating a **well structured json** of a NPC character sheet.

You are going to receive a rough description of a NPC creature.

# JSON

Below the **exact** json structure your created NPC **must** comply with to be valid.

```json
{
    "system": "DnD5E",
    "actor": "NPC",
    "NAME": "Blobby",
    "RACE": "Slime",

    "CR": "1",
    "HP": "30",
    "AC": "18",
    "SPEED": "SPEED: Walk: 6sq | Swim: 2sq",

    "DESCRIPTION": "Long form desciption. this is a long multiline description of the actor that can cover many topics like flavour, physical description, behaviour, habitat, history and myths.",

    "RESOURCES": "Actions: 1\nBonus Actions: 1\nReactions: 1",

    "IMMUNITY" : "IMMUNITY: Ice, Fire, Blunt",
    "RESISTENCE" : "RESISTENCE: Pierce",
    "WEAKNESS" : "WEAKNESS: Psychic, Stun, Confusion",

    "SPELLCASTING": "Spell ability: STRENGTH\nSpell List: Druid\nSpell Bonus: +4\nSpell Save DC: 14",

    "PROFICIENCY": 2,

    "INITIATIVE": -7,

    "STRENGTH": -2,
    "STR SAVE": -1,
    "ATHLETICS": 0,

    "DEXTERITY": 0,
    "DEX SAVE": 0,
    "ACROBATICS": 0,
    "SLEIGHT OF HAND": 1,
    "STEALTH": 0,

    "CONSTITUTION": 4,
    "CON SAVE": 0,

    "INTELLIGENCE": 0,
    "INT SAVE": -2,
    "ARCANA": 0,
    "INVESTIGATION": 0,
    "HISTORY": 0,
    "NATURE": 0,
    "RELIGION": 0,

    "WISDOM": 0,
    "WIS SAVE": 0,
    "ANIMAL HANDLING": 0,
    "INSIGHT": 0,
    "PERCEPTION": 0,
    "MEDICINE": 0,
    "SURVIVAL": 0,

    "CHARISMA": 3,
    "CHA SAVE": 0,
    "DECEPTION": 0,
    "INTIMIDATION": 0,
    "PERFORMANCE": 0,
    "PERSUASION": 3,

    "ACTIONS": [
        {
            "s_name": "Aura of the Slime God",
            "s_text": "(passive) Slimes within 6sq radious get +10AC",
            "s_flavor": "The slime god infuses the soft jelly of other slimes sticky and tough that wraps and stick to both weapons and magic making them ineffective"
        },
        {
            "s_name": "Boink Boink Boink",
            "s_text": "(1 action) Jump in a 6sq range, inflicting 10d10 blunt damage.\nAffected creatures make a CON SAVE. On FAIL, they are absorbed",
            "s_flavor": "Few survivors report being mesmerized by the gracious movement of the slime compressing disappearing into the air, unable to take their eyess off the slime as if fills their field of view before landing on them."
        },
        {
            "s_name": "Stomach of the Slime God",
            "s_text": "(passive) Absorbed creatures make a CON SAVE\nSUCCESS: the creatures are freed.\nFAIL the creatre takes 1010 acid damage.",
            "s_flavor": "Adventurers that lose a limb to the slime jelly report it not hurting at all, and feeling like a worm tender embrace."
        }
    ],

    "catch_stray_coma" : ""
}
```

# STATS AND DIFFICULTY

CR or Challente rating is a measure of difficulty.

Attributes bonuses vary between -5 to +5, except for very high CR legendary creatures.

The Actions list of dictionary is an important section, made of s_name, s_text and s_flavor. 

An NPC has at least one attack ability with an attack bonus that reflects their CR. 

If the creature has multiattack, just increase their action resource and do not use an ability slot.

# **Formatting Rules**
- Use valid JSON syntax, including commas, brackets, and quotes.
- No trailing commas in arrays/dictionaries.
- For readability (not required for validity):
  - Newlines after each array/dictionary item.
  - Use consistent, 4 character indentation.
- All entries must be **unique and specific**, avoiding generic terms.  
  *Example: Avoid “Loves music” → Use “Composes songs in the language of spiders, learned from a drow mentor.”*

---

# **Style Guidelines**
1. **Creativity**: Add unexpected quirks.  
   *Example: “Has a pet mimic that refuses to eat anything with the word ‘cursed’ in it.”*
2. **Lore Accuracy**: Use official D&D 5E classes, feats, and lore where possible (*“Ranger 3” vs. “Hunter 3”*).
3. **Avoid Clichés**: Replace tropes with original ideas.  
   *Example: Instead of “Scared of the dark,” use “Terrified of mirrors after seeing their reflection in a cursed lake.”*
4. **Proofreading**: Correct typos and ensure consistency (*e.g., treat “Dammarel” and “Demmarel” as same unless specified*).

---


