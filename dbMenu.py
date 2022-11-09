# This program reads in data from the text file containing details of the records held in stock,
# then stores it into a list data structure and implements the following menu options.
# BASIC FEATURES:
# 1. Output a list of record titles and their respective details, including a summary report displaying
# (a) the total number of titles in stock and
# (b) the value of records in stock.
# 2. Output a list of record titles and their respective details which are above a user provided price threshold.
# 3. Output a report giving the number of records existing in each genre type.
# ADVANCED FEATURES:
# 4. Option to add a new record and present a summary report displaying
# (a) the new total number of titles in stock and
# (b) the new total value of records in stock.
# The record which you should add is one copy of the LP Radio Silence, by
# the Neil Cowley Trio at £12.99. The Neil Cowley Trio is a Jazz group.
# 5. Query if a record title is available and present option of
# (a) increasing stock level or
# (b) decreasing the stock level, due to a sale. If the stock level is decreased to zero indicate to the user that
# the record is currently out of stock.
# 6. Plot a labelled bar chart that presents the number of titles existing in each genre type.
# 7. Quit.
import numpy as np
import matplotlib.pyplot as plt
import os

print('...............START Program...............')


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
                   '7. Quit.'
    print(menu_details)


menu()
options = int(input('Enter options 1-7: '))


# This function counts the stock and value of stocks.
def option1():
    # open records.txt file, read and print details, total number of titles and value of stock.
    record_file = open('record_data.txt', 'r')
    next(record_file)  # skip line.
    next(record_file)
    # records = record_file.read()
    print('VINYL STORE RECORDS.' + '\n' + \
          '==========================')
    contents_split = record_file.readlines()  # read over each line.
    count = 0
    counter = 0
    for line in contents_split:
        lines = str(line.strip()).split(',')  # split lines into lists.
        print(','.join(lines))  # print without brackets
        stocks = int(lines[5])
        count += stocks
        each_value = float(lines[6])
        counter += each_value
    print()
    print(f'Stocks: #{count}')
    print(f'Value of Stocks: £{counter:,.2f}')
    record_file.close()
    menu()


# This function filters the records by cost of record.
def option2():
    record_file = open('record_data.txt', 'r')
    next(record_file)
    next(record_file)
    threshold = float(input('Enter price threshold: '))
    for line in record_file:
        lines = str(line.strip()).split(', ')
        each_number = float(lines[6])
        if threshold < each_number:
            print(line.rstrip('\n'))
    menu()


# This function groups the genre of the records.
def option3():
    # open records.txt file, read and print genres in groups.
    record_file = open('record_data.txt', 'r')
    next(record_file)
    next(record_file)
    genre = {}
    for genre_count in record_file:
        line = str(genre_count.strip()).split(', ')
        genre_group = line[2]
        if genre_group in genre.keys():
            genre[genre_group] = int(genre[genre_group]) + 1
        else:
            genre[genre_group] = 1
    for key, value in genre.items():
        print('{}: {}'.format(key, value))


# This function allows user append new records to the file and updates stocks and value of stocks.
def option4():
    # Open the coffee.txt file in append mode.
    record_file = open('record_data.txt', 'a')
    print('Enter the following record data:')
    artist = str(input('ARTIST: '))
    title = str(input('TITLE: '))
    genre = str(input('GENRE: '))
    play_length = str(input('PLAY LENGTH: '))
    condition = str(input('CONDITION: '))
    stock = int(input('STOCK: '))
    cost = float(input('COST: '))
    record_file.write('\n' + artist + ', ')
    record_file.write(title + ', ')
    record_file.write(genre + ', ')
    record_file.write(play_length + ', ')
    record_file.write(condition + ', ')
    record_file.write(str(stock) + ', ')
    record_file.write(str(cost))
    print('Data appended to record_data.txt.')
    record_file.close()
    option1()


# This function allows the user to change the stock of a record.
def option5():
    print('Increase or Decrease stock: ')
    record_file = open('record_data.txt', 'r')
    temp_file = open('temp.txt', 'w')  # open temporary file.
    search = input('Enter Artist: ')
    file_read = ' '
    while file_read:
        file_read = record_file.readline()
        lines = file_read.split(', ')
        if len(file_read) > 0:
            if lines[0] == search:
                new_stock = input('Enter new stock: ')
                temp_file.write(search + ', ' + lines[1] + ', ' + lines[2] + ', ' + lines[3] + ', ' + lines[
                    4] + ', ' + new_stock + ', ' + lines[6])
                print(search + ', ' + lines[1] + ', ' + lines[2] + ', ' + lines[3] + ', ' + lines[
                    4] + ', ' + new_stock + ', ' + lines[6])
            else:
                temp_file.write(file_read)
    temp_file.close()
    record_file.close()
    os.remove('record_data.txt')
    os.rename('temp.txt', 'record_data.txt')
    menu()


# This function displays a bar chart based on grouped genres.
def option6():
    record_file = open('record_data.txt', 'r')
    next(record_file)
    next(record_file)
    genre = {}
    for genre_count in record_file:
        line = str(genre_count.strip()).split(', ')
        genre_group = line[2]
        if genre_group in genre.keys():
            genre[genre_group] = int(genre[genre_group]) + 1
        else:
            genre[genre_group] = 1
    for key, value in genre.items():
        print('{}: {}'.format(key, value))
        x = np.array([key])
        y = np.array([value])
        plt.bar(x, y)
    plt.show()


# This function exits the program.
def option7():
    print('Goodbye!' + '\U0001F917')

    # Make sure user enters correct option.


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
        break
    else:
        print('Invalid option. Try again.')
        menu()
    options = int(input('Enter options 1-7: '))
