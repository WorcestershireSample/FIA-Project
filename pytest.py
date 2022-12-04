# tessseract stuff
from PIL import Image
import pytesseract

# SQL stuff
import mysql.connector
from mysql.connector import Error
import pandas as pd

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

word = (pytesseract.image_to_string(Image.open('brownine_mix2.png')))
# word = 'Testing 1, testing 2, testing 3, testing 4(testing 6, testing 7)'
print(word)
word = word.replace('\n',' ')
word = word.replace('INGREDIENTS: ','')
word = word.replace('),',')\n')
word = word.replace(', ',',')
word = word.replace('.','')
word = word.replace(' OR ','\n')
word = word.replace(' (','(')
# print(word)
# for some reason, there is an extra linespace at the end of the word
# print(word)
print("hello!\n")
balance = 0
counter=-1
for i in word:
    counter +=1
    if (i=='('):
        balance += 1
    if (i == ')'):
        balance -= 1
    if balance == 0 and i == ',' and word[counter-1] != ')':
        word = word[:counter] + '\n' + word[counter+1:]


words = word.split("\n")
ingredients = [item.strip() for item in words]

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
            print(value + ' may be vegan.')
        else:
            print(value + ' is not vegan.')
    else:
        print(value + ' is not in the database!')
    return row

for i in ingredients:
    if (i.find('(')):
        x =i.partition('(')
        # print(x[0])
    # print(i)
    has_value(mycursor, x[0])
cnx.close()