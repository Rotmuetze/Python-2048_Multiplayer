import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sadsklghasiujgbhafjw4z689wrkldftßq0(§LJSDAS",
    database="2048_DB"
)

cursor = db.cursor()


print("Möchtest du wirklich alle Daten löschen? (y/n): ")
if input() == "y":
#    cursor.execute("DELETE FROM spielsessions WHERE spieler1pkt = 64 or spieler2pkt = 64")
#    db.commit()
#    print("Daten gelöscht!")

    cursor.execute("DROP TABLE spielsessions")
    db.commit()
exit()
