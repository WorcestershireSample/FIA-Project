import os

import pytesseract
from PIL import Image

#  need this if tesseract is not found in PATH variable
#  os.path.join utilizes file system of the operating system running the program
#  and joins the tesseract folder

pytesseract.pytesseract.tesseract_cmd = os.path.join("tesseract")


def filter_image_string(pytesseract_string):
    def buffer_to_string(a):
        new_string = ""
        for elt in a:
            if elt == '\n':  # pytesseract adds \n chars in the string for reason unknown to me
                new_string += " "
            else:
                new_string += elt
        return new_string

    buffer = []
    array = []
    sub_ingredient = 0
    for character in pytesseract_string:
        if character == '(':
            sub_ingredient = 1
        if character == ')':
            sub_ingredient = 0
        if character == ',' and sub_ingredient == 1:
            continue
        if character == ',' and sub_ingredient == 0:
            array.append(buffer_to_string(buffer))
            buffer.clear()
        else:
            buffer.append(character)

    return array


file_name = 'ingredients.png'
image_string = (pytesseract.image_to_string(Image.open(file_name)))

processed_image_string = filter_image_string(image_string)

print(processed_image_string)
