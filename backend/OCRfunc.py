import json
import cv2
# ^ Must be installed via pip
import os
import re
# ^ Should be there by default idk why it didnt work
import pytesseract
import requests
# ^ Another pip install
from PIL import Image
import numpy as np
# ^for deskewing

import numpy as np
from PIL import Image

def deskew_image(image_path):
    # Load the image and convert it to grayscale
    image = Image.open(image_path).convert('L')
    # Convert the image to a numpy array
    image_array = np.array(image)
    
    # Compute the moments of the image
    moments = cv2.moments(image_array)
    # Compute the angle of the major axis of the moments ellipse
    angle = np.degrees(np.arctan2(2 * moments['mu11'], moments['mu20'] - moments['mu02'])) / 2.0
    # Compute the rotation matrix
    rot_matrix = cv2.getRotationMatrix2D((image_array.shape[1] / 2, image_array.shape[0] / 2), -angle, 1.0)
    # Rotate the image
    rotated_image = Image.fromarray(cv2.warpAffine(image_array, rot_matrix, image_array.shape[::-1], flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=255))
    
    return rotated_image


# testing deskewing
# deskewed_image = deskew_image(r"tip377.png")
# deskewed_image = Image.fromarray(deskewed_image)
# deskewed_image.save(r"straight-4.png")

# Take in a png and convert it to text, make preprocessing its own function
def optimize_image_for_ocr(image_path, lang='eng', image_dpi=300, image_format='png', whitelist = None, blacklist = None):
    
    # Load the image
    img = cv2.imread(image_path)

    # Preprocess the image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(img, 1)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Save the preprocessed image
    preprocessed_image_path = f"{image_path}_preprocessed.{image_format}"
    cv2.imwrite(preprocessed_image_path, img)
    

    # Load the preprocessed image using PIL
    pil_image = Image.open(preprocessed_image_path)

    # Set the image DPI
    pil_image = pil_image.resize((pil_image.width * image_dpi // 72, pil_image.height * image_dpi // 72))

    # Specify the language of the text
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Specify whitelist + blacklist
    if whitelist is not None:
        whitelist_option = f"tessedit_char_whitelist={whitelist}"
    else:
        whitelist_option = ''
    
    if blacklist is not None:
        blacklist_option = f"tessedit_char_blacklist={blacklist}"
    else:
        blacklist_option = ''
    
    custom_config = f'-l {lang} --dpi {image_dpi} {whitelist_option} {blacklist_option}'

    # Extract text from the image
    text = pytesseract.image_to_string(pil_image, config=custom_config)

    # Remove the preprocessed image file
    os.remove(preprocessed_image_path)

    return text

# Parse the ingredients into a list
def parse_ingredients(text): 

    # Remove parentheses and their contents
    text = re.sub(r'\([^)]*\)', '', text)
    
    # Replace newline characters with spaces
    text = text.replace('\n', ' ')

    # Replace initial INGREDIENTS or CONTAINS with spaces
    text = text.replace('INGREDIENTS: ', '').replace('CONTAINS: ', '')

    # Remove paranthesis again in case any were left over
    text = text.replace('(','').replace(')','').replace('.','')

    # Split ingredients by commas
    ingredients = text.split(',')
    
    # Remove leading and trailing whitespace from each ingredient
    ingredients = [ingredient.strip() for ingredient in ingredients]
    
    # Remove any empty ingredients
    ingredients = [ingredient for ingredient in ingredients if ingredient]
    
    return ingredients

# convert list to JSON

# testing
# print(parse_ingredients(ingredient_list))

# Request Spoonacular API to see if ingredient is vegan

# def check_vegan(ingredient, diet):
#     url = 'https://api.spoonacular.com/recipes/complexSearch'
#     params = {
#         'apiKey': '9ff5fa8b2ad548e3948941754a464ec3',
#         'query': ingredient,
#         'diet': diet,
#         'number': 1  # Only need 1 result
#     }
#     response = requests.get(url, params=params)
#     if response.status_code == 200:
#         data = response.json()
#         if data['results']:
#             return data['results'][0]
#     else:
#         print(f'Error {response.status_code}: {response.reason}')
#     return None

# print(check_vegan('chocolate', 'vegan'))

# Convert list to JSON
def convert_JSON(ingredient_list):
    json_string = json.dumps(ingredient_list)
    return json_string

# Send information to web server, use JSON
def send_data_to_server(data):
    url = 'http://example.com/api'
    headers = {'Content-Type': 'application/json'}

    # Send the POST request with the JSON data
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print('Data sent successfully!')
    else:
        print('Error sending data:', response.status_code)


if __name__ == '__main__':
    # make image argv argument
    ingredient_list = optimize_image_for_ocr(r"sem2\brownine_mix.png", whitelist='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ()[],')
    parsed_list = parse_ingredients(ingredient_list)
    print(parsed_list)
    send_data_to_server(convert_JSON(parsed_list))