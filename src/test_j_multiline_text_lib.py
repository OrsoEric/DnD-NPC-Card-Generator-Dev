# r>python src\test_j_multiline_text_lib.py

import logging



from lib.st_image import St_image
from lib.cl_utility_path import convert_to_path
from lib.cl_multiline_text import Cl_multiline_text



# Example usage
if __name__ == "__main__":
    # Setup logging
    s_log_path = convert_to_path(["log","test_j_multiline_text_library.log"])
    print(f"Log Path: {s_log_path}")

    st_font = Cl_multiline_text.load_font("arial.ttf", 18)

    logging.basicConfig(
        filename=s_log_path,
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("BEGIN")

    cl_image_card_back : St_image = St_image(
        i_w_card_mm = 63.5,
        i_h_card_mm = 88.9,
        i_dot_per_inch = 300
    )

    Cl_multiline_text.render_fixed_size_text_box(
        i_cl_imgage = cl_image_card_back.g_cl_image,
        i_s_text = "This is a reusable multiline text box renderer This is a reusable multiline text box renderer . . ..",
        i_w_margin = 20,
        i_h_margin = 20,
        i_w_border = 250,
        i_h_border = 120,
        i_s_font_name = "arial.ttf",
        i_n_font_size = 18,
        i_tn_color = (127, 127, 127),
        i_n_padding = 5,
        i_x_draw_border = True,
        i_tn_border_color = (255,0,0)
    )

    cl_image_card_back.save_image( ["output","test_j_card_multiline_library.jpg"] )
    
    logging.info("END")
    print("Card back generated successfully!")