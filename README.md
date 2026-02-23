# NPC Character‑Sheet Generator  
*A command‑line friendly tool that turns JSON definitions + PNG art into a printable double‑sided card.*

---

## 1. Overview

The project is a small Python library / CLI that:

| Step | What happens |
|------|--------------|
| **Load an NPC** | Reads the JSON file that describes a single creature (name, stats, actions, language, etc.). |
| **Read a layout definition** | Loads a *localised* JSON file (`layout_en.json`, `layout_de.json` …) that contains all coordinates / sizes for every visual element. |
| **Compose two card halves** | Creates a **front** (illustration + mask + front text boxes) and a **back** (mask + back text boxes, attributes & actions). |
| **Merge into one image** | Concatenates the two halves side‑by‑side, draws a divider line, and writes a JPEG that can be printed or distributed. |

The result is a single JPEG that looks like:

```
+-----------------+-----------------+
|  Front (image)  |  Back (text)    |
+-----------------+-----------------+
```

---

## 2. Architecture

### 2.1 Core Class – `Cl_npc_character_sheet_generator`

All logic lives inside this class.

| Attribute / Method | Purpose |
|---------------------|---------|
| `g_cl_image_card`   | **Composite** image that will contain the final card (both halves). |
| `g_cl_image_card_front`, `g_cl_image_card_back` | Separate images for the front and back before merging. |
| `load_layout_from_json()` | Reads a localisation‑aware JSON layout file. |
| `draw_layout_front_to_image()` | Renders the *front* text boxes onto the illustration. |
| `draw_layout_back_to_image()` | Renders attributes, abilities, action blocks, etc. onto the back side. |
| `load_values_*_from_npc_dict()` | Populates the layout placeholders with real values from an NPC dictionary. |
| `generate_card()` | The orchestrator that calls all of the above and writes a JPEG. |
| `find_and_generate_cards()` | Static helper to scan a folder for matching image‑JSON pairs and produce cards in bulk. |

### 2.2 Supporting Utilities

| Utility | Responsibility |
|---------|----------------|
| `St_image` (from `lib/st_image.py`) | Simple wrapper around Pillow’s `Image`. Handles unit conversions (mm → pixels) and common operations like `draw_image`, `compose_image`, `save_image`. |
| `Cl_multiline_text` (from `lib/cl_multiline_text.py`) | Renders multiline text boxes with optional padding, border, centre‑alignment, automatic height calculation. |
| `find_file_pair_image_json()` & `build_path_output_jpg()` (from `lib/…`) | Helpers to find matching image / JSON files in an input directory and build a corresponding output path. |

### 2.3 Data Contracts

* **NPC JSON** – Must contain:
  * `language` (e.g., `"en"`)
  * Basic stats like `name`, `strength`, `dexterity`
  * `ACTIONS`: a list of dicts (`s_name`, `s_text`, `s_flavor`, …)
  * Any other keys referenced by the layout

* **Layout JSON** – Has at least:
  ```json
  {
      "FRONT_TEXT_BOXES": [...],
      "attributes_and_abilities": [...],
      "text_boxes": [...],
      "ACTIONS": { "h_font_title_ppt": ..., ... }
  }
  ```
  Each sub‑array contains dicts with pixel‑percentage (`*_ppt`) values, font sizes and colour tuples.

* **Mask Images** – PNG files that will be composited onto the front or back (e.g., a frame or bleed).

---

## 3. How It Works – Step by Step

1. **Instantiate the generator**
   ```python
   gen = Cl_npc_character_sheet_generator(
       i_w_card_width_mm=63.5,          # e.g. a standard playing card
       i_h_card_height_mm=88.9,
       i_n_dots_per_inch=300,
       i_s_font_path=["font","CormorantGaramond-BoldItalic.ttf"]
   )
   ```

2. **Load the NPC**
   ```python
   npc = Cl_npc()
   npc.load_from_file("npc_data.json")      # sets npc.g_d_npc dict
   ```

3. **Read the layout (auto‑localised)**
   ```python
   base_layout = Path("layout.json")
   layout = gen.load_layout_from_json(base_layout, npc.language)
   ```

4. **Populate placeholders with real data**  
   *Front:* `load_values_front_from_npc_dict()` copies fields such as `name`, `race` into the front text boxes.  
   *Back:* `load_values_back_from_npc_dict()` does the same for attributes, abilities and actions – it even clones a template box to create one per action.

5. **Create the card halves**  
   * Front: draw illustration → apply mask → render front text boxes.  
   * Back : apply mask → render back content (attributes & action blocks).

6. **Merge halves side‑by‑side**  
   ```python
   self.g_cl_image_card.draw_image(front, (0,0), size_front)
   self.g_cl_image_card.draw_image(back,  (size_front[0],0), size_back)
   ```
   A black vertical line is added at the seam.

7. **Save JPEG**
   ```python
   self.g_cl_image_card.save_image(output_path, i_s_format="JPEG")
   ```

8. **Batch mode**  
   `find_and_generate_cards()` scans an input folder for every pair of image/JSON files, builds output paths in a target directory and calls `generate_card()` on each.

---

## 4. Running the Tool

```bash
# Ensure dependencies are installed
pip install pillow tqdm

# Create directories
mkdir -p data/cards input_images npc_data

# Place your NPC JSONs & illustration PNGs in `input_images/`
# Place the layout file(s) in `data/layout.json`

# Run batch generation (example paths)
python -m lib.cl_npc_character_sheet_generator \
    --layout_path=data/layout.json \
    --mask_front=mask/front.png \
    --mask_back=mask/back.png \
    --input_folder=input_images \
    --output_folder=cards
```

> **Tip** – The static `find_and_generate_cards()` is already wired into the script; just call it from a small driver or your CI pipeline.

---

## 5. Customisation & Extending

| What you might want to tweak | Where |
|-----------------------------|-------|
| Font paths / sizes | Constructor (`i_s_font_path`) and layout JSON `h_font_ppt` values |
| Colour scheme | `CN_DEFAULT_BACKGROUND_COLOR`, `g_tn_border_color`, or per‑box `t_text_color` |
| Layout geometry | Edit the layout JSON – all coordinates are *per‑thousand* of the card size, making it resolution‑independent. |
| Additional content blocks | Add more keys to the layout JSON and implement a rendering method in `Cl_npc_character_sheet_generator`. |

---

## 6. Summary

The **NPC Character‑Sheet Generator** is a small but complete pipeline that:

1. Loads NPC data and localisation.
2. Parses a flexible, unit‑independent layout definition.
3. Renders a double‑sided card using Pillow.
4. Supports batch processing of many NPCs.

Because everything is driven by JSON files and simple image masks, you can easily swap in new fonts, colours or even an entirely different card shape – the only hard part that stays constant is the Python core logic.

# Paper Size

What is the correct size of a D&D card?

![](/paper/Standard%20Paper%20Size.jpg)

TODO: I need to find much bigger sleeves

# 2026-02-22 FEEDBACK

I made NPCs for a test campaign, including italian localization.


![](/Examples/NPC%20-%20Olivia%20Prezzo%20-%20Alchemist%20sheet.jpg)

### Positives

- It's convenient to cut and fold, and use the magic sleeves

- The front works really well, I like it's a wall art with minimal information.

- I also like the back layout. I did a good job the way it's organized

- It's really convenient that I have a standard sleeve to put the card in

### Negatives

- The text is waaaaay too small for the card, even if I had a good printer.

- but there is waaaaay too much text for that card size.

- I lack the roleplay information on the card

### TODO

- I need to vastly increase the card size.

- I should add the behaviour information in the front, this way I should have everything to make PCs as well as NPs

- I need a json preprocessor. The source json should list the proficiencies, expertise and compute the stat itself, and have a nudge to adjust the final value, it makes easier to estimate.

- I need a difficulty estimation so that I can estimate CR.