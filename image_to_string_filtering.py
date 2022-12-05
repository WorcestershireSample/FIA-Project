import pytesseract
from PIL import Image


#  this line breaks the script for macOS because of differing file system
#  add tesseract to path variable on both operating systems to ignore this line
#  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

#  filter_image_string takes the string output of pytesseract.image_to_string()
#  and returns an array of strings. Each string in the array is 1 ingredient
def filter_image_string(pytesseract_string):
    #  buffer_to_string is a helper function for filter_image_string
    #  that takes an array of characters and converts it to a string
    #  to be appended to the array of strings returned in the outer function
    def buffer_to_string(a):
        new_string = ""
        for elt in a:
            if elt == '\n':  # pytesseract adds \n chars in the string for reason unknown to me - Chris
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

    for element in array:
        index = element.find("INGREDIENTS: ")
        if index != -1:
            array[index] = array[index].replace("INGREDIENTS: ", "")

    return array


file_name = 'ingredients.png'
image_string = (pytesseract.image_to_string(Image.open(file_name)))

processed_image_string = filter_image_string(image_string)

print(processed_image_string)
