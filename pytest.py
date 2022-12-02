# tessseract stuff
from PIL import Image
import pytesseract

# SQL stuff
import mysql.connector
from mysql.connector import Error
import pandas as pd

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

word = (pytesseract.image_to_string(Image.open('test.png')))
print(word)
# for some reason, there is an extra linespace at the end of the word
word = word.strip()

cnx = mysql.connector.connect(user='salle142', password='',
                              host='localhost', database = 'fia')

mycursor = cnx.cursor()

# run sql commands
mycursor.execute("")

def has_value(cursor, value):
    query = 'SELECT * from foodlistvegan WHERE itemName = %s'
    cursor.execute(query, (value,))
    row = cursor.fetchone()
    if (row):
        if (row[1] == 1):
            print(word + ' is in the database and is vegan.')
        else:
            print(word + ' is in the database and is not vegan.')
    else:
        print(word + ' is not in the database!')
    return row

has_value(mycursor, word)
cnx.close()