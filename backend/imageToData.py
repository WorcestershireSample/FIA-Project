from PIL import Image
import pytesseract

word = (pytesseract.image_to_string(Image.open('../res/brownine_mix2.png')))
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