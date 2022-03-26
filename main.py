from pymongo import MongoClient
import json
import os

# For clearing terminal
if os.name == 'nt':
    clr = 'cls'
else:
    clr = 'clear'


# Get port number
def get_port():
    while True:
        try:
            port = int(input("Enter port number: "))
            return port
        except ValueError:
            print("Invalid input!")


# Main menu prompt
def print_main_menu():
    os.system(clr)
    print("List of tasks\n------------------------------")
    print("1. Search for titles\n2. Search for genres\n3. Search for cast/crew members\n4. Add a movie\n5. Add a "
          "cast/crew member\n6. Exit\n")


# Get task number
def get_task():
    while True:
        try:
            inp = int(input("Execute task: "))
            if inp in (1, 2, 3, 4, 5, 6):
                return inp
            else:
                print("Please enter a valid task number! (1, 2, 3, 4, 5, 6)")
        except ValueError:
            print("Invalid input!")


# Search for titles
def task_1():
    os.system(clr)
    keywords = list(input("Enter 1 or more keywords, separated by spaces (eg. cmput MaTh DAVOOD): ").split())
    print('pog')


# Search for genres
def task_2():
    os.system(clr)
    genre = input("Enter genre: ")
    while True:
        try:
            count = int(input("Enter minimum vote count: "))
            break
        except ValueError:
            print("Please enter an integer.")


# Search for cast/crew members
def task_3():
    os.system(clr)
    name = input("Enter cast/crew member name: ")


# Add a movie
def task_4(db):
    os.system(clr)
    mid = input("Enter unique MID: ")
    title = input("Enter title: ")
    while True:
        try:
            year = int(input("Enter start year: "))
            break
        except ValueError:
            print("Invalid input!")
    while True:
        try:
            running_time = int(input("Enter running time: "))
            break
        except ValueError:
            print("Invalid input!")
    genres = list(input("Enter genre(s), separated by spaces (eg. action cOmEdy HORROR): ").split())
    db.title_basics.insert({"_id": mid,
                            "titleType": "movie",
                            "primaryTitle": title,
                            "originalTitle": title,
                            "isAdult": "\N",
                            "startYear": year,
                            "endYear": "\N",
                            "runtimeMinutes": running_time,
                            "genres": genres})
                            

# Add a cast/crew member
def task_5():
    os.system(clr)
    cid = input("Enter CID: ")
    title = input("Enter title id: ")
    category = input("Enter category: ")


# Main program
def main():
    port = get_port()
    client = MongoClient("localhost", port)

    # Open database
    db = client["291db"]

    # Open all the collections
    name_basics = db["name_basics"]
    title_basics = db["title_basics"]
    title_principals = db["title_principals"]
    title_ratings = db["title_ratings"]
    while True:
        print_main_menu()
        task = get_task()
        if task == 6:
            quit("Goodbye!")
        elif task == 1:
            task_1()
            input("\n*Enter key to go back*")
        elif task == 2:
            task_2()
            input("\n*Enter key to go back*")
        elif task == 3:
            task_3()
            input("\n*Enter key to go back*")
        elif task == 4:
            task_4(db)
            input("\n*Enter key to go back*")
        elif task == 5:
            task_5()
            input("\n*Enter key to go back*")


if __name__ == "__main__":
    main()
