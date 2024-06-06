import mysql.connector
import time

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sadsklghasiujgbhafjw4z689wrkldftßq0(§LJSDAS",
    database="2048_DB"
)

cursor = db.cursor()


print("Möchtest du wirklich alle Daten löschen? (y/n): ")
if input() == "y":
    cursor.execute("DELETE FROM spielsessions")
    db.commit()
    print("Daten gelöscht!")
    db.commit()

print()
print()
print("x zum schliessen.")
while(input() != "x"):
    time.sleep(1)
