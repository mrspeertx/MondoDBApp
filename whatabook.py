##  whatabook assignment 
##  Michael Speer
## Lines 4-29 govern the connection to the database
from asyncio.windows_events import NULL
from contextlib import nullcontext
from wsgiref import validate
import mysql.connector
from mysql.connector import errorcode

config = {
    "user": "whatabook_user",
    "password": "MySQL8IsGreat!",
    "host": "127.0.0.1",
    "database": "whatabook",
    "raise_on_warnings": True
}

try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)


def show_menu():
    """Displays main menu and returns a user response"""
    
    print("\n--Main Menu--")

    print("Please make a selection by typing the corresponding value: \n1: View Books \n2: View Store Locations \n3: My Account \n0: Exit Program\n\n")
    
    a = 1
    while a == 1:
        try:
            response = int(input('Your Choice:  '))

            return response

        except:
            print("That is an invalid response, please try again. \n <Example: If you want to view available books, simply type 1 and hit enter>\n")

def show_books(_cursor):
    """Queries database and prints all available books"""

    _cursor.execute("SELECT book_name, author FROM book")

    books = _cursor.fetchall()
    print("\n\nAvailable books are as follows")
    for book in books:
        print("'{}' by {}".format(book[0], book[1]))

    print("\n\n\n")

def show_locations(_cursor):
    """Queries database and prints all locations"""

    _cursor.execute("SELECT store_id, locale FROM store")

    stores = _cursor.fetchall()

    print("\n\nFind the book you're looking for at these fine locations:")
    
    for store in stores:
        print("   Store number {}, located in beautiful {}".format(store[0], store[1]))

def validate_user(_cursor):
    """Queries database and gets userid from use"""
    _cursor.execute("SELECT user_id FROM user")
    all_id = _cursor.fetchall()
    id_list = []
    for id in all_id:
        id_list.append(str(id[0]))


    user_input = None
    while user_input != 0:        
        user_input = input("\n\nPlease enter your user id or enter 0 to exit: ")

        if user_input in id_list:
            return user_input
        elif user_input == '0':
            close()
        else:
            print("\nThat is an invalid response. Please try again.\n")

def show_account_menu():
    """Shows customer menu and validates response"""
    while 1 == 1:
        print("\n\n== Customer Menu ==\n1. Wishlist\n2. Add Book\n3. Main Menu\n0. Close Program")
        try:
            account_option = int(input("\n\nPlease make your selection: "))
        except:
            print("That was not a valid response. Please try again or enter 0 to exit.")
        if account_option > 0 & account_option <= 3:
            return account_option
        elif account_option == 0:
            close()
        else:
            break



def show_wishlist(_cursor, _user_id):
    """Queries database and prints user's wishlist"""
    _cursor.execute("SELECT book.book_name, book.author FROM wishlist INNER JOIN book ON wishlist.book_id = book.book_id WHERE wishlist.user_id = {}".format(_user_id))
    wishlist = _cursor.fetchall()
    
    print("\n--Your Wishlist--")
    for book in wishlist:
        print("'{}' by {}".format(book[0], book[1]))

def select_book_to_add(_cursor, _user_id):
    """Queries database, prints all books not in user wishlist, verifies user input """
    _cursor.execute("SELECT book_id, book_name FROM book WHERE book_id NOT IN "
                    "(SELECT book_id FROM wishlist WHERE user_id = {})".format(_user_id))
    books = _cursor.fetchall()

    print("Books Available to add to your Wishlist:")
    book_id_list = []
    for book in books:
        print("\n Book ID: {}\n Book Title: {}".format(book[0],book[1]))
        book_id_list.append(book[0])
    try:
        book_to_add = int(input("\n\nPlease enter the ID of the book you would like to add: "))
        if book_to_add in book_id_list:
            return book_to_add
        else:
            print("That is an invalid selection.")
            return None

    except:
        return None

def add_book_to_wishlist(_cursor, _user_id, _book_id):
    """Adds selected book to user's wishlist"""
    _cursor.execute("INSERT INTO wishlist(user_id, book_id) VALUES({},{})".format(_user_id, _book_id))


def close():
    """Closes program and thanks user"""
    print("Thank  you for choosing What-a-Book\n\n")
    quit()




## Begin the user interface :D

## Show menu and record the user response to user_response (int) 
user_response = show_menu()

## If user_response is 0 it should close program, otherwise enter the if statement
while user_response != 0:

    ## If user selects View Books program calls show_books. Nothing is returned.
    if user_response == 1:
        show_books(cursor)

    ## If user selects View Store Locations program calls show_locations(). Nothing is returned.
    elif user_response == 2:
        show_locations(cursor)

    ## If user selects My Account program calls validate user
    elif user_response == 3:

        ## validate_user() verifies that user exists in database and records to id (str)
        id = validate_user(cursor)

        ## show_account_menu() displays the second menu and records the input to account_option (int)
        account_option = show_account_menu()

        ## while loop holds the user position in the cutomer menu until they exit
        while account_option != 3:

            ## If user selects wishlist, show_wishlist() queries database and prints all books in the user database 
            if account_option == 1:
                show_wishlist(cursor, id)
            
            ## If user selects Add Book select_book_to_add queries database to find all books NOT in the user's wishlist and records the user's decision to book_to_add
            if account_option == 2:
                book_to_add = select_book_to_add(cursor, id)

                ## select_book_to_add may return None if the user enters invalid data
                ## if select_book_to_add returned a value lines 191-196 writes the book to the user wishlist
                if book_to_add != None:
                    add_book_to_wishlist(cursor, id, book_to_add)
                    db.commit()
                    print("Book ID: {} was added to your wishlist!".format(book_to_add))
                else:
                    print('\nThat input was invalid. Please try again.\n')

            ## if a user inputs invalid data this catches it
            if account_option < 0 or account_option > 3:
                print("\n      Invalid option, please retry...")
           
            var = input('\n\nPress any key to continue...  ')

            ## this calls the customer menu and perpetuates the loop
            account_option = show_account_menu()

    ## if user chooses to close program this exits the program        
    elif user_response == 0:
        close()

    var = input('\n\nPress any key to continue...  ')
    ## this perpetuates the loop
    user_response = show_menu()

close()