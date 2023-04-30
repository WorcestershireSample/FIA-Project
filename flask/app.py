import os
import cv2
import re
import pytesseract
from PIL import Image
from flask import Flask, request, render_template, jsonify

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
    # preprocessed_image_path = f"_preprocessed.{image_format}"
    cv2.imwrite(preprocessed_image_path, img)
    

    # Load the preprocessed image using PIL
    pil_image = Image.open(preprocessed_image_path)

    # Set the image DPI
    pil_image = pil_image.resize((pil_image.width * image_dpi // 72, pil_image.height * image_dpi // 72))

    # Specify the language of the text
    pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR'

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
    #os.remove(preprocessed_image_path)

    # Remove the original image file
    #os.remove(image_path)

    return text


# Parse the ingredients into a list
def parse_ingredients(text): 

    # Remove parentheses and their contents
    text = re.sub(r'\([^)]*\)', '', text).lower()
    
    # Replace newline characters with spaces
    text = text.replace('\n', ' ')

    # Replace initial INGREDIENTS or CONTAINS with spaces
    text = text.replace('ingredients: ', '').replace('contains: ', '')

    # Remove paranthesis again in case any were left over
    text = text.replace('(','').replace(')','').replace('.','')

    # Split ingredients by commas
    ingredients = text.split(',')
    
    # Remove leading and trailing whitespace from each ingredient
    ingredients = [ingredient.strip() for ingredient in ingredients]
    
    # Remove any empty ingredients
    ingredients = [ingredient for ingredient in ingredients if ingredient]
    
    vegRead = open("veganIngredients.txt", "r")
    banRead = open("veganBanned.txt", "r")
    veganList = []
    banList = []

    for x in vegRead:
            veganList.append(x.rstrip())
    for x in banRead:
            banList.append(x.rstrip())
    ingredientReading = []
    for item in ingredients:
        if item in veganList:
            ingredientReading.append(item + " is vegan")
        elif item in banList:
            ingredientReading.append(item + " is not vegan")
        else:
            ingredientReading.append(item + " cannot be read")
    #print(ingredientReading)

    vegRead.close()
    banRead.close()
    return ingredientReading


app = Flask(__name__)
app.config["IMAGE_UPLOADS"] = "./upload/"

@app.route('/', methods=['POST', 'GET'])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            # filepath = "./" + os.path.join(app.config["IMAGE_UPLOADS"], image.filename)
            filepath = os.path.join(app.config["IMAGE_UPLOADS"], image.filename)
            image.save(filepath)
            ingredient_list = optimize_image_for_ocr(filepath, whitelist='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ()[],')
            parsed_list = parse_ingredients(ingredient_list)
            processed_filename = image.filename + "_preprocessed.png"
            processed_filepath = os.path.join(app.config["IMAGE_UPLOADS"], processed_filename)
            # return jsonify(parsed_list)
            return render_template("index.html", uploaded_image=filepath, processed_image=processed_filepath, results=parsed_list)
            # return jsonify(['bruh'])
    # return jsonify(['error'])
    return render_template("index.html")


@app.route('/upload/<filename>')
def send_uploaded_file(filename=''):
    from flask import send_from_directory
    return send_from_directory(app.config["IMAGE_UPLOADS"], filename)

if __name__ == "__main__":
    app.run()
