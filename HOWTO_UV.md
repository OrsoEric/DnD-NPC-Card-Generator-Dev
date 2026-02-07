# Create UV 

uv venv .venv --python 3.13

call .venv\Scripts\activate.bat

uv init

uv add pillow


# Use UV 

call .venv\Scripts\activate.bat

python src\test_f_text_box.py

python src\test_g_card_back_description.py

python src\test_h_card_back_class.py

python src\test_i_text_multiline.py