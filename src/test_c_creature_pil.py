from PIL import Image, ImageDraw, ImageFont


class CreatureCardGenerator:
    """
    This class generates creature cards using the Pillow library.
    """

    cn_default_font = "arial.ttf"  # Default font for text rendering
    cn_default_font_size = 20  # Default font size
    cn_card_width = 600  # Width of the card in pixels
    cn_card_height = 800  # Height of the card in pixels
    cn_background_color = (240, 240, 240)  # Light gray background color
    cn_border_color = (0, 0, 0)  # Black border color
    cn_text_color = (0, 0, 0)  # Black text color

    def __init__(self):
        """
        Initializes the CreatureCardGenerator with default values.
        """
        pass

    def generate_card(self, i_creature_name: str, i_race_class: str, i_armor_class: int, i_initiative: int, i_speed: int, i_health: int, i_challenge_rating: int) -> Image.Image:
        """
        Generates a creature card image with the provided information.

        Parameters:
        i_creature_name (str): The name of the creature.
        i_race_class (str): The race and class of the creature.
        i_armor_class (int): The armor class of the creature.
        i_initiative (int): The initiative score of the creature.
        i_speed (int): The speed of the creature in feet per round.
        i_health (int): The health points of the creature.
        i_challenge_rating (int): The challenge rating of the creature.

        Returns:
        Image.Image: A PIL Image object representing the generated card.
        """

        # Create a new image with specified dimensions and background color
        ln_image = Image.new("RGB", (self.cn_card_width, self.cn_card_height), self.cn_background_color)
        ln_draw = ImageDraw.Draw(ln_image)

        # Define font settings
        ln_font = ImageFont.truetype(self.cn_default_font, self.cn_default_font_size)

        # Draw the border
        ln_border_width = 5
        ln_draw.rectangle([(ln_border_width, ln_border_width), (self.cn_card_width - ln_border_width, self.cn_card_height - ln_border_width)], outline=self.cn_border_color, width=ln_border_width)

        # Calculate positions for text elements
        n_name_x = 50
        n_name_y = 50
        n_race_class_x = 50
        n_race_class_y = 100
        n_ac_x = 50
        n_ac_y = 300
        n_initiative_x = 200
        n_initiative_y = 300
        n_speed_x = 400
        n_speed_y = 300
        n_health_x = 50
        n_health_y = 400
        n_cr_x = self.cn_card_width - 100
        n_cr_y = 50

        # Write the creature name and challenge rating
        ln_draw.text((n_name_x, n_name_y), i_creature_name, fill=self.cn_text_color, font=ln_font)
        ln_draw.text((n_cr_x, n_cr_y), "CR", fill=self.cn_text_color, font=ln_font)

        # Write the race and class
        ln_draw.text((n_race_class_x, n_race_class_y), i_race_class, fill=self.cn_text_color, font=ln_font)

        # Write the stats
        ln_draw.text((n_ac_x, n_ac_y), "AC", fill=self.cn_text_color, font=ln_font)
        ln_draw.text((n_initiative_x, n_initiative_y), str(i_initiative), fill=self.cn_text_color, font=ln_font)
        ln_draw.text((n_speed_x, n_speed_y), str(i_speed), fill=self.cn_text_color, font=ln_font)
        ln_draw.text((n_health_x, n_health_y), str(i_health), fill=self.cn_text_color, font=ln_font)

        return ln_image


# Example usage:
if __name__ == "__main__":
    generator = CreatureCardGenerator()
    ln_card_image = generator.generate_card(
        i_creature_name="Orc",
        i_race_class="Humanoid",
        i_armor_class=13,
        i_initiative=2,
        i_speed=30,
        i_health=15,
        i_challenge_rating=1
    )

    ln_card_image.save("creature_card.png")  # Save the image to a file
    print("Creature card generated and saved as creature_card.png")
