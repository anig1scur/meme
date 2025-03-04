import os

input_folder = os.path.join(os.path.dirname(__file__), "../src/assets/imgs/intro")
output_folder = os.path.join(os.path.dirname(__file__), "../src/assets/imgs/intro")

os.makedirs(output_folder, exist_ok=True)

from PIL import Image


def trim_transparency(image_path, output_path):
    img = Image.open(image_path).convert("RGBA")
    bbox = img.getbbox()

    if bbox:
        img_cropped = img.crop(bbox)
        img_cropped.save(output_path)


for filename in os.listdir(input_folder):
    if filename.endswith(".png"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        trim_transparency(input_path, output_path)
