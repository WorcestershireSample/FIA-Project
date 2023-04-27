import requests
from b4 import BeautifulSoup

ing = input("Enter Ingredient")
r = requests.get('https://upcfoodsearch.com/food-ingredients/' + ing + '/')
soup = BeautifulSoup(r.content, 'html.parser')
s = soup.find('div', class_= 'table-responsive')
lines = s.find('tr')
for line in lines:
  print(line.text)
