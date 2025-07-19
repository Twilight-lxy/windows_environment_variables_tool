"""ico图标"""
import base64


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


icon_png = """
base64 code
"""

if __name__ == "__main__":
    print(image_to_base64("./icon.png"))
