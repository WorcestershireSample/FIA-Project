import mysql.connector

mydb = mysql.connector.connect(
  host="4.246.191.213",
  user="VegAnalyzer2023",
  password="DramaDadHearingClient1"
  # database="veganDB"
)

# Run the first time and then quit to create a database.
# mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE veganDB")
# mycursor.execute("CREATE TABLE veganListing (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), vegan INT, tags VARCHAR(255))")

sql = "INSERT INTO veganDB (name, vegan, tags) VALUES (%s, %s, %s)"
val = ("Milk", "0", "V")
mycursor.execute(sql, val)

veganDB.commit()

print(veganDB)
