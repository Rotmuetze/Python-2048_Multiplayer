import mysql.connector

my_db = mysql.connector.connect(
    port="3308",
    host="localhost",
    user="root",
    password="sadsklghasiujgbhafjw4z689wrkldftßq0(§LJSDAS",
    database="2048_DB"
)

my_cursor = my_db.cursor()


sql = """
    CREATE TABLE spielsessions(
    timestamp TIME,
    sessionid SMALLINT,
    spieler1 TEXT,
    spieler1pkt TINYINT,
    spieler2 TEXT,
    spieler2pkt TINYINT
    )
"""

#my_cursor.execute(sql)
#my_cursor.execute("CREATE DATABASE 2048_DB")
#my_cursor.execute("DROP TABLE spielsessions")
my_db.commit()