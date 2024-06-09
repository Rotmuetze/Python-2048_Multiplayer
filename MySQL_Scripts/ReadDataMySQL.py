import mysql.connector
import time

db = mysql.connector.connect(
    port="3308",
    host="localhost",
    user="root",
    password="sadsklghasiujgbhafjw4z689wrkldftßq0(§LJSDAS",
    database="2048_DB"
)

cursor = db.cursor()


cursor.execute("SELECT * FROM spielsessions")
result = cursor.fetchall()

print("SpielID:       Spieler 1:          Punkte:         Spieler 2:                Punkte:        Timestamp:")

for item in result:
    i = [str(b) for b in item]
    print()
    print( i[1] + "              " + i[2] + "     " + i[3] + "               " + i[4] + "           " + i[5] + "             "  + i[0])

print()
print()
print("x zum schliessen.")
while(input() != "x"):
    time.sleep(1)