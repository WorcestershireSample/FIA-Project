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
