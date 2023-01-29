from models import (Base,session,
Book,engine)
import datetime
import csv
import time


def menu():
    while True:
        print('''
        
          \nPROGRAMMING BOOKS: 

          \r1) Add Book
          \r2) View all books
          \r3) Search for book
          \r4) Book Analysis
          \r5) Exit''')

        choice = input('What would you like to do? ')  
        if choice in ['1', '2', '3', '4', '5']:
            return choice

        else:
            input('''
            \rPlease choose one of the options above.
            \rA number from 1 - 5
            \rPress enter to try again!
            ''')


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            #add book
            title = input('Title: ')
            author = input('Author: ')
            date_error = True

            while date_error:
                date = input('Published Date (Ex: January 10, 1986): ')
                date = clean_date(date)
                if type(date) == datetime.date:
                    date_error = False

            price_error = True
            while price_error:        
                price = input('Price (Ex: 25.64): ')
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            new_book = Book(title=title, author=author, published_date=date, price=price)
            session.add(new_book)     
            session.commit()   
            print('Book added successfully!')
            time.sleep(1.5)

        elif choice == '2':
            #view all book
            pass

        elif choice == '3':
            #search book
            pass

        elif choice == '4':
            #book analysis
            pass

        else:
            print('Goodbye!!!')
            app_running = False

def clean_date(date_str):
    months = ['January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    split_date = date_str.split(' ')

    try:
        month = months.index(split_date[0]) + 1
        day = int(split_date[1].split(',')[0])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)

    except ValueError:
        input('''
        \n********* Date Error ***********
        \rThe date format should include a valid Month, Day, year from the past.
        \rEx: january 11, 2014.
        \rPress ENTER to try again
        *********************************''')

        return
    else:
        return return_date


def clean_price(price_str):

    try:
        price_float = float(price_str)
    except ValueError:
        input('''
        \n********* Price Error ***********
        \rThe price should be a number without the currency symbol.
        \rEx: 35.23.
        \rPress ENTER to try again
        *********************************''')

    else:
        return int(price_float * 100)

def add_csv():
    with open('suggested_book.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            book_in_db = session.query(Book).filter(Book.title==row[0]).one_or_none()

            if book_in_db == None:
                title = row[0]
                author = row[1]
                date = clean_date(row[2])
                price = clean_price(row[3])
                new_book = Book(title=title, author=author, published_date=date, price=price)
                session.add(new_book)
        session.commit()


if __name__=='__main__':
    Base.metadata.create_all(engine)
    app()
 