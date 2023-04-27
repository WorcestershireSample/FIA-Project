import webScraper

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
        ingredientReading.append(item + " cannot be found within database. Searching has found " + webScraper.scrapeInfoUPC(item))
print(ingredientReading)

vegRead.close()
banRead.close()
