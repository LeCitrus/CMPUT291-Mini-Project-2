from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from pprint import pprint
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
            port = int(input("Enter port number: ").strip())
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
            inp = int(input("Execute task: ").strip())
            if inp in (1, 2, 3, 4, 5, 6):
                return inp
            else:
                print("Please enter a valid task number! (1, 2, 3, 4, 5, 6)")
        except ValueError:
            print("Invalid input!")


# Search for titles
def task_1(db):
    os.system(clr)
    keywords = list(input("Enter 1 or more keywords, separated by spaces (eg. cmput MaTh DAVOOD): ").split())
    print('pog')


# Search for genres
def task_2(db, title_ratings):
    os.system(clr)
    genre = input("Enter genre: ").strip()
    while True:
        try:
            count = int(input("Enter minimum vote count: ").strip())
            break
        except ValueError:
            print("Please enter an integer.")


# Search for cast/crew members
def task_3(db):
    os.system(clr)
    name = input("Enter cast/crew member name: ").strip()


# Add a movie
def task_4(db, title_basics):
    os.system(clr)
    while True:
        mid = input("Enter unique MID: ").strip()

        # Make sure unique MID
        if not db.title_basics.find_one({"tconst": mid}):
            break

        print("Movie ID already exists!")

    title = input("Enter title: ").strip()

    # Make sure year is int
    while True:
        try:
            year = int(input("Enter start year: ").strip())
            break
        except ValueError:
            print("Invalid input!")

    # Make sure running time is int
    while True:
        try:
            running_time = int(input("Enter running time: ").strip())
            break
        except ValueError:
            print("Invalid input!")
        
    genres = list(input("Enter genre(s), separated by spaces (eg. action cOmEdy HORROR): ").split())

    # Add movie to title_basics
    db.title_basics.insert_one({"tconst": mid,
                            "titleType": "movie",
                            "primaryTitle": title,
                            "originalTitle": title,
                            "isAdult": None,
                            "startYear": year,
                            "endYear": None,
                            "runtimeMinutes": running_time,
                            "genres": genres
    })

    # Confirm movie has been added
    print("\n----------------------------\nAdded to title_basics: ")
    pprint(db.title_basics.find_one({"tconst": mid}, {"_id": 0}), sort_dicts=False)
    print("----------------------------")
                            

# Add a cast/crew member
def task_5(db, name_basics, title_basics, title_principals):
    os.system(clr)

    # Make sure cast ID exists
    while True:
        cid = input("Enter CID: ").strip()
        if db.name_basics.find_one({"nconst": cid}):
            break
        print("Cast ID does not exist!")
    
    # Make sure title ID exists
    while True:
        mid = input("Enter MID: ").strip()
        if db.title_basics.find_one({"tconst": mid}):
            break
        print("Movie ID does not exist!")
    
    category = input("Enter category: ").strip()

    # Find largest ordering listed
    ordering = list(db.title_principals.aggregate([
        {"$match": {"tconst": mid}},
        {"$group": {"_id": "$tconst", "max": {"$max": "$ordering"}}},
        {"$project": {"_id": 0}}
    ]))

    # Set the new insert's ordering to 1, or largest ordering + 1
    if ordering:
        ordering = int(ordering[0]["max"]) + 1
    else:
        ordering = 1

    # Insert the cast/crew member
    db.title_principals.insert_one({"tconst": mid,
                                    "ordering": ordering,
                                    "nconst": cid,
                                    "category": category,
                                    "job": None,
                                    "characters": None
    })

    # Confirm cast/crew member added
    print("\n----------------------------\nAdded to title_principals: ")
    pprint(db.title_principals.find_one({"$and": [
            {"tconst": mid},
            {"ordering": ordering}
        ]},
        {"_id": 0}), sort_dicts=False
    )
    print("----------------------------")


# Main program
def main():
    while True:
        port_num = get_port()
        try:
            client = MongoClient(host = "localhost", port = port_num, serverSelectionTimeoutMS = 1)
            client.server_info()
            break
        except ServerSelectionTimeoutError:
            print("Invalid port number!")

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
            task_1(db)
            input("\n*Enter key to go back*")
        elif task == 2:
            task_2(db, title_ratings)
            input("\n*Enter key to go back*")
        elif task == 3:
            task_3(db)
            input("\n*Enter key to go back*")
        elif task == 4:
            task_4(db, title_basics)
            input("\n*Enter key to go back*")
        elif task == 5:
            task_5(db, name_basics, title_basics, title_principals)
            input("\n*Enter key to go back*")


if __name__ == "__main__":
    main()
