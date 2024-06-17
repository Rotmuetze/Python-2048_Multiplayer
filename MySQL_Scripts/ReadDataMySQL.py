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

for item in result:
    i = [str(b) for b in item]
    a1 = 20 - len(i[1])
    a2 = 20 - len(i[2])
    a3 = 20 - len(i[3])
    a4 = 20 - len(i[4])
    a5 = 20 - len(i[5])
    spacei1i2 = ""
    spacei2i3 = ""
    spacei3i4 = ""
    spacei4i5 = ""
    spacei5i0 = ""
    print()
    while a1 != 0:
        spacei1i2 = spacei1i2 + " "
        a1 = a1-1
    while a2 != 0:
        spacei2i3 = spacei2i3 + " "
        a2 = a2-1
    while a3 != 0:
        spacei3i4 = spacei3i4 + " "
        a3 = a3-1
    while a4 != 0:
        spacei4i5 = spacei4i5 + " "
        a4 = a4-1
    while a5 != 0:
        spacei5i0 = spacei5i0 + " "
        a5 = a5-1
    print("SpielID:            Spieler 1:          Punkte:             Spieler 2:          Punkte:             Timestamp:")
    print( i[1] + spacei1i2 + i[2] +spacei2i3 + i[3] + spacei3i4+ i[4] + spacei4i5 + i[5] + spacei5i0 + i[0])


print()
print()
print("x zum schliessen.")
while(input() != "x"):
    time.sleep(1)


