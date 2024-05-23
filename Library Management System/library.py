 
# Kritagya Sharma




borrowedISBNs=[]
    

def printMenu():
    print('\n######################')
    print('1: (A)dd a new book.')
    print('2: Bo(R)row books.') 
    print('3: Re(t)urn a book.') 
    print('4: (L)ist all books.') 
    print('5: E(x)it.') 
    print('######################\n') 

# ADD BOOK PART

def addBook(allBooks):
        while True:

            bookName = input("Book name> ")
        
        # BOOKNAME PART

    # Checks if bookname is valid

            if "*" in bookName or "%" in bookName:


                print("Invalid book name!")

            else:

                break

        bookAuthor = input("Author Name> ")
    # BOOK EDITION PART
        while True:
            bookEdition = input("Edition> ")
            if not bookEdition.isdigit():  
                print("Invalid Book Edition") # If it's not a digit, then print this
            else:
                break
            
    # IBSN PART
        
        while True:
            bookISBN = input("ISBN> ")
            if not bookISBN.isdigit():
                print("Invalid ISBN!")
            else: 
                if (len(bookISBN)) == 13:
                    break
                else:
                    print("Invalid ISBN!")
        count = 0
        bookISBN = str(bookISBN) # Change this into a string momentarily so that when it checks for the range, it can actually perform the check as it is in string format.
        for isbnChar in range(len(bookISBN)):
                digit = int(bookISBN[isbnChar])
                if isbnChar % 2  == 0: 
                    count = count + digit * 1
                else:
                    count = count + digit * 3
        if count % 10 == 0: 
            for book in allBooks:
                if book [0] == str(bookISBN): # The [0] starts at the first position and scans everything in the allBooks list. If a duplicate is found, it will display an error message accordingly.
                    print("Dublicate ISBN Found! Cannot add the book") # So we want the parameter 'book' to inspect everything in the list, and if there are no duplicates, it should be added to the list.
                    break
                elif book [0] != str(bookISBN) and book == allBooks [-1]:
                    allBooks.append ([bookISBN, bookName, bookAuthor, bookEdition,[]]) # The empty list is for anyone who borrowed the book.
                    print("A new book is added successfully.")
                    break
        else:
            print("Invalid ISBN! ")


def borrowBook(allBooks, borrowedISBNs):
    borrowName = input("Enter the borrower name> ")
    searchBook = input("Search term> ")
    bookFound = False

    # Contains (*) 

    if searchBook.lower().endswith('*'):
        searchBook = searchBook.replace('*',"") # Removes astrix before entering the loop
        for book in allBooks:
            if searchBook.lower() in book[1].lower() and book[0] not in borrowedISBNs: 
                book[4].append(borrowName)
                borrowedISBNs.append(book[0]) 
                print(f' -"{book[1]}" is borrowed!')
                bookFound = True
            

        if not bookFound:
            print("No book is found!")
    
# Starts With (%)
    elif searchBook.lower().endswith('%'):
        searchBook = searchBook.replace('%',"")
        for book in allBooks:
            bookSplit = book[1].split () # It takes a sentence or phrase and divides it into smaller parts, creating a list. For example, if the original text is "Hi Hello," when we use split(), it becomes a list with two elements: ["Hi", "Hello"].
            if searchBook.lower() in book[1].lower() and book[0] not in borrowedISBNs:  # It checks if the search term is the same as the first word in the book name.
                book[4].append(borrowName)  
                borrowedISBNs.append(book[0])
                print(f' -"{book[1]}" is borrowed!')
                bookFound = True
            

        if not bookFound:
            print("No books found!")

     
     # Exact Part
       
    else:
        for book in allBooks:
            if searchBook.lower() == book[1].lower() and book[0] not in borrowedISBNs: 
                book[4].append(borrowName)
                borrowedISBNs.append(book[0])
                print(f' -"{book[1]}" is borrowed!')
                bookFound = True
        if not bookFound:
            print("No books found!")


# Returning A Book 

def bookReturn(allBooks, borrowedISBNs): 
    returnIsbn = input("ISBN> ")
    #print (returnIsbn)
    if returnIsbn in borrowedISBNs:
        borrowedISBNs.remove(returnIsbn) # When they enter the ISBN number, the system should detect if that number is already in the rented ISBNs list. If it is, the system will then remove that number from the list to indicate that the book has been returned.
        
        for book in allBooks:
            if returnIsbn == book[0]: # Looking at the 0 index in allBooks, which contains all the ISBN numbers, if we accessed allBooks[0], it would retrieve the data like this: "9780596007126", "The Earth Inside Out", "Mike B", 2, ['Ali'], which is not what we are looking for.
                #book[4].remove())    
                print(f'"{book[1]}" is returned') 
                break 
    else:
        print("No books is found!")
        
   
# Listing Book
def bookList(allBooks, borrowedISBNs):
    # Checks Availability and prints the details of all books
    for book in allBooks:
        print("---------------")
        if  book[0] in borrowedISBNs:
            status = "[Unavailaible]"
        else:
            status = "[Available]"

        print(status)
        print(f"{book[1]} - {book[2]}")
        print(f"E: {book[3]} ISBN: {book[0]}")
        print(f"borrowed by: {book[4]}")


# Exiting The Code

def bookExit(allBooks, borrowedISBNs):
    print("$$$$$$$$ FINAL LIST OF BOOKS $$$$$$$$")
    bookList(allBooks, borrowedISBNs)






# Start Function is defined here
def start():
    allBooks = [ ['9780596007126',"The Earth Inside Out","Mike B",2,['Ali']], 
                ['9780134494166',"The Human Body","Dave R",1,[]],
                ['9780321125217',"Human on Earth","Jordan P",1,['David','b1','user123']] ]

    borrowedISBNs=[]

    while True: # Loop that keeps asking for the valid input begins
        printMenu()

        selection = input("Your selection> ")


        if selection == "1" or selection.lower() == "a":

            addBook(allBooks)

        elif selection =="2" or selection.lower() == "r":

            borrowBook(allBooks, borrowedISBNs)

        elif selection == "3" or selection.lower() == "t":
            bookReturn(allBooks,borrowedISBNs)

        elif selection == "4" or selection.lower() == "l":
            
            bookList(allBooks, borrowedISBNs)

        elif selection == "5" or selection.lower() == "x":
            bookExit(allBooks, borrowedISBNs)
            break

        else: 

            print("Wrong selection! Please selection a valid option. ")

     
start()
