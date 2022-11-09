import pyodbc
import database

connectionString = database.getConnectionString()

conn = pyodbc.connect(connectionString)
cursor = conn.cursor()
# cursor.execute('SELECT * FROM RECORDS')

# parameters to prevent hack from SQL injection
query = "SELECT ARTIST, TITLE, GENRE, PLAY_LENGTH, CONDITION, STOCK, COST FROM RECORDS WHERE ARTIST = ?"

parameters = ['Bach']

for row in cursor.execute(query, parameters):
    print(row.ARTIST, row.TITLE, row.GENRE, row.PLAY_LENGTH, row.CONDITION, row.STOCK, row.COST)
print("Parameter found")