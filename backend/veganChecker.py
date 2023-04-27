import requests
from bs4 import BeautifulSoup

vegRead = open("veganIngredients.txt", "r")
banRead = open("veganBanned.txt", "r")
veganList = []
banList = []

for x in vegRead:
    veganList.append(x.rstrip())
for x in banRead:
    banList.append(x.rstrip())
ingredientReading = []
ingredients = ["apple", "corn", "acetate", "adrenaline", "fat", "bowling Ball"]
for item in ingredients:
    if item in veganList:
        ingredientReading.append(item + " is vegan")
    elif item in banList:
        ingredientReading.append(item + " is not vegan")
    else:
        ingredientReading.append(item + " cannot be found within database. Try " + webScrape(item))
print(ingredientReading)

vegRead.close()
banRead.close()

def webScrape(ing):
    r = requests.get('https://upcfoodsearch.com/food-ingredients/' + ing + '/')
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('div', id= 'main')
    leftbar = s.find('ul', class_='leftBarList')
    lines = leftbar.find_all('li')
 
    for line in lines:
        print(line.text)
    return('https://upcfoodsearch.com/food-ingredients/' + ing + '/')
