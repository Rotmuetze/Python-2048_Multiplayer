import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sadsklghasiujgbhafjw4z689wrkldftßq0(§LJSDAS",
    database="2048_DB"
)

cursor = db.cursor()


cursor.execute("SELECT * FROM spielsessions")
result = cursor.fetchall()

for _ in result:
    print(_)