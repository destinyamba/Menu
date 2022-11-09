import pyodbc
import database
import numpy as np
import matplotlib.pyplot as plt

connectionString = database.getConnectionString()

conn = pyodbc.connect(connectionString)
cursor = conn.cursor()

def menu():
    menu_details = 'Select option.' + '\n' + \
                   'BASIC FEATURES:' + '\n' + \
                   '1. Display list of record titles and their respective details.' + '\n' + \
                   '2. Display list of record titles and their respective details for user price threshold.' + '\n' + \
                   '3. Display report giving the number of records existing in each genre type.' + '\n' + \
                   'ADVANCED FEATURES:' + '\n' + \
                   '4. Add a new record and present a summary report.' + '\n' + \
                   '5. Search for record.' + '\n' + \
                   '(a) increase stock level.' + '\n' + \
                   '(b) decrease the stock level.' + '\n' + \
                   '6. Plot Bar Chart.' + '\n' + \
                   '7. Delete Record' + '\n' + \
                   '8. Quit.'
    print(menu_details)
menu()
options = int(input('Enter options 1-8: '))

def option1():
    # print all records and the total stock and value of the records.
    # parameters to prevent hack from SQL injection
    query = "SELECT ARTIST, TITLE, GENRE, PLAY_LENGTH, CONDITION, STOCK, COST FROM RECORDS"
    stock_sum = "SELECT STOCK FROM RECORDS"
    cost_sum = "SELECT COST FROM RECORDS"

    for row in cursor.execute(query):
        print(row.ARTIST, row.TITLE, row.GENRE, row.PLAY_LENGTH, row.CONDITION, row.STOCK, row.COST)

    # calculate total cost of records
    total_cost = 0
    for row in cursor.execute(cost_sum):
        total_cost += row[0]
    print("COST: £",total_cost)  
    # calculate total stock, get stock column values from database and add.
    total_stock = 0
    for row in cursor.execute(stock_sum):
        #print(row.STOCK)
        total_stock += row[0]
    print("STOCK: #",total_stock)  

def option2():
    # Prompt user input and return threshold value of records greater than input value.
    query = "SELECT ARTIST, TITLE, GENRE, PLAY_LENGTH, CONDITION, STOCK,COST FROM RECORDS WHERE COST > ?"
    threshold = float(input('Enter price threshold: '))

    parameters = [threshold]

    for row in cursor.execute(query, parameters):
        print(row.ARTIST, row.TITLE, row.GENRE, row.PLAY_LENGTH, row.CONDITION, row.STOCK, row.COST)

def option3():
    # group the genres of records and return the value for each genre.
    cursor.execute("SELECT GENRE, COUNT(*) AS VALUE FROM RECORDS GROUP BY GENRE") 
    data = list(cursor) 
    for row in data:
        print(row.GENRE,':',row.VALUE)
def option4(): 
    # parameters to prevent hack from SQL injection
    print('Enter the following record data:')
    artist = str(input('ARTIST: '))
    title = str(input('TITLE: '))
    genre = str(input('GENRE: '))
    play_length = str(input('PLAY LENGTH: '))
    condition = str(input('CONDITION: '))
    stock = int(input('STOCK: '))
    cost = float(input('COST: '))
    cursor.execute("""
    INSERT INTO RECORDS(ARTIST, TITLE, GENRE, PLAY_LENGTH, CONDITION, STOCK, COST)
    VALUES (?,?,?,?,?,?,?)
    """, (artist, title, genre, play_length, condition, stock, cost))
    conn.commit()
    cursor.commit()
    print('Commit Successful')

def option5():
    # change the stock of a record from user input.
    # Search by artist and update stock.
    search = input('Enter Artist: ')
    new_stock = input('Enter new stock: ')
    query = "UPDATE RECORDS SET STOCK = ? WHERE ARTIST = ?"

    parameters = [new_stock,search]

    cursor.execute(query, parameters)
    cursor.commit()
    option1()

def option6():
    cursor.execute("SELECT GENRE, COUNT(*) AS VALUE FROM RECORDS GROUP BY GENRE") 
    data = list(cursor) 
    for row in data:
        x = np.array([row.GENRE])
        y = np.array([row.VALUE])
        plt.bar(x, y)
    plt.show()

def option7():
    # this function deletes records from the database
    query = "DELETE FROM RECORDS WHERE ARTIST = ?"
    search = input('Enter Artist: ')

    parameters = [search]

    cursor.execute(query, parameters)
    cursor.commit()

def option8():
    print('Goodbye!' + '\U0001F917')

while options != 0:  # Validate user input to inspect data before computation.
    # Make options functional.
    if options == 1:
        option1()
    elif options == 2:
        option2()
    elif options == 3:
        option3()
    elif options == 4:
        option4()
    elif options == 5:
        option5()
    elif options == 6:
        option6()
    elif options == 7:
        option7()
    elif options == 8:
        option8()
        break
    else:
        print('Invalid option. Try again.')
        menu()
    options = int(input('Enter options 1-8: '))