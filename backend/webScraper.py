
import requests
from b4 import BeautifulSoup

def scrapeInfoUPC(ing):
  r = requests.get('https://upcfoodsearch.com/food-ingredients/' + ing + '/')
  soup = BeautifulSoup(r.content, 'html.parser')
  s = soup.find('div', class_= 'table-responsive')
  lines = s.find('tr')
  result = ""
  for line in lines:
    result += line.text.strip()
  return result
