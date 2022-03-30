from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from pprint import pprint
import os
import re

# For clearing terminal
if os.name == 'nt':
    clr = 'cls'
else:
    clr = 'clear'

# Aesthetics
divider = '_' * 40


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
    print("List of tasks\n" + divider)
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
def task_1(db, name_basics, title_basics, title_ratings):
    os.system(clr)

    # Get list of keywords
    keywords = list(input("Enter 1 or more keywords, separated by spaces (eg. cmput MaTh DAVOOD): ").split())

    # Adds all ints to year checker just incase someone decides a title has numbers and year
    keywords_ints=[]
    keywords_reg=""
    keyints_reg=""
    int_finder=[]
    
    if len(keywords) > 0:
        for x in range(0,len(keywords)):
            # Add regex statements so it gets each elements
            if keywords[x].isdigit():
                int_finder.append(x) 
                keywords_ints.append("%s"%(keywords[x]))
            else:
                keywords[x] = "(?=.*%s)"%(keywords[x])
        for x in range(len(int_finder)-1,-1,-1):
            keywords.pop(int_finder[x])
            
        # If there are items in the list then we do some regex magic and make it so any keyword will return a search results

        keywords_reg = ''.join(keywords)
        keyints_reg  = ''.join(keywords_ints)

        keywords_reg = "(?i)^" + keywords_reg + ".+"

        # Pipeline match the for both start year and primaryTitle

        agg_pipe_q1 = [
                {"$match" : {"primaryTitle" : {"$regex" : keywords_reg }}},
                {"$match" : {"startYear" : {"$regex" : keyints_reg}}}
                ]

        keywords_reg_yrt = keywords_reg[0:-2] + "(?=.*\\b%s\\b)"%keyints_reg+".+"

        agg_pipe_final = [
                {"$match" : {"primaryTitle" : {"$regex" : keywords_reg_yrt}}},
                {"$unionWith" : {"coll" : "title_basics","pipeline":agg_pipe_q1}},
                {"$group" : {
                    "_id" : "$tconst",
                    "tconst" :        {"$first":  "$tconst"},
                    "titleType" :     {"$first":  "$titleType"},
                    "primaryTitle" :  {"$first":  "$primaryTitle"},
                    "originalTitle" : {"$first":  "$originalTitle"},
                    "isAdult" :       {"$first":  "$isAdult"},
                    "startYear" :     {"$first":  "$startYear"},
                    "endYear" :       {"$first":  "$endYear"},
                    "runtimeMinutes" :{"$first":  "$runtimeMinutes"},
                    "genres" :        {"$first":  "$genres"}
                    }},
                {"$unset":"_id"}
                ]

        movie_matches = list(title_basics.aggregate(agg_pipe_final))
        # If there are movies in search
        if len(movie_matches):

            # Print movie matches table
            print("\nMovie matches")
            print("\n    {:^14}    {:^10}    {:^40}    {:^40}    {:^8}    {:^10}    {:^10}    {:^16}    {:^46}".format("tconst", 
            "titleType", "primaryTitle", "originalTitle", "isAdult", "startYear", "endYear", "runtimeMinutes", "genres"))
            print("    " + "-" * 14 + " " * 4 + "-" * 10 + " " * 4 + "-" * 40 + " " * 4 + "-" * 40 + " " * 4 + "-" * 8 + " " * 4 + "-" * 10 +
            " " * 4 + "-" * 10 + " " * 4 + "-" * 16 + " " * 4 + "-" * 46)
            
            # Paginate movie results
            i = 0
            end = False
            while not end:
                for x in range(50):
                    if i < len(movie_matches):
                        print("{:<3} {:^14}    {:^10}    {:<40}    {:<40}    {:^8}    {:^10}    {:^10}    {:^16}    {:<46}".format(i + 1, 
                        str(movie_matches[i]["tconst"][:14] or ''), str(movie_matches[i]["titleType"][:10] or ''), str(movie_matches[i]["primaryTitle"][:40] or ''), 
                        str(movie_matches[i]["originalTitle"][:40] or ''), str(movie_matches[i]["isAdult"[:8]] or '') , str(movie_matches[i]["startYear"] or ''), 
                        str(movie_matches[i]["endYear"] or ''), str(movie_matches[i]["runtimeMinutes"] or ''), ', '.join(movie_matches[i]["genres"])))
                        i += 1
                    else:
                        end = True
                        break
                if not end:
                    input("\n*ENTER to show next 50 results...*\n")

            print("\n" + divider + "\n")

            # Prompt for title select
            while True:
                try:
                    select = int(input("Select a movie: "))
                    if 1 <= select <= len(movie_matches):
                        break
                    print("Invalid option!")
                except ValueError:
                    print("Please enter an integer.")

            # Find rating and number votes from title_ratings
            stats = db.title_ratings.find_one({"tconst": movie_matches[select - 1]["tconst"]}, {"_id": 0, "tconst": 0})

            # Print rating and number votes
            rating = stats["averageRating"]
            votes = stats["numVotes"]
            print("\n" + movie_matches[select - 1]["primaryTitle"] + "\n-----------------\nRating:", rating, "\nNumber of Votes:", votes, "\n\nCast/crew members")

            # Find cast/crew members from title_principals and name_basics
            members = list(db.title_principals.aggregate([
                {"$match": {"tconst": movie_matches[select - 1]["tconst"]}},
                {"$lookup": {"from": "name_basics",
                        "localField": "nconst",
                        "foreignField": "nconst",
                        "as": "name"
                        }
                }
            ]))

            # Print list of cast/crew members, and associated characters
            print("\n{:^16}      {:^40}      {:^70} ".format("nconst", "Name", "Characters"))
            print("-" * 16 + " " * 6 + "-" * 40 + " " * 6 + "-" * 70)
            for member in members:
                if not member["characters"]:
                    member["characters"] = []
                print("{:^16}      {:^40}      {:^70} ".format(member["nconst"], member["name"][0]["primaryName"], ', '.join(member["characters"])))
        else:
            print("\nNo matches!")
    else: 
        print("\nNo matches!")

# Search for genres
def task_2(db, title_basics, title_ratings):
    os.system(clr)
    genre = "^" + input("Enter genre: ").strip() + "$"

    # Get valid votes of int
    while True:
        try:
            count = int(input("Enter minimum vote count: ").strip())
            break
        except ValueError:
            print("Please enter an integer.")

    # Aggregate pipeline to narrow down results
    titles = list(db.title_basics.aggregate([

        # All movies with matching category case insensitive
        {"$match": {"genres": re.compile(genre, re.IGNORECASE)}},

        # Join title_basics with title_ratings
        {"$lookup": {
                    "from": "title_ratings",
                    "localField": "tconst",
                    "foreignField": "tconst",
                    "as": "stats"}
        },

        # Convert votes and average rating to ints/floats
        {"$project": {"_id": 0, "tconst": 1,"primaryTitle": 1, 
                    "ratings": {"$toDouble": {"$arrayElemAt": ["$stats.averageRating", 0]}}, 
                    "numVotes": {"$toInt": {"$arrayElemAt": ["$stats.numVotes", 0]}}}
        }, 

        # Add votes constraint and sort
        {"$match": {"numVotes": {"$gt": count}}},
        {"$sort": {"ratings" : -1}}
    ]))

    # Print titles, ratings, votes
    if titles:
        print("\n{:^20}      {:60}      {:^10}      {:^14}".format("tconst", "Title", "Rating", "Votes"))
        print("-" * 20 + " " * 6 + "-" * 60 + " " * 6 + "-" * 10 + " " * 6 + "-" * 14)

        # Loop to paginate
        i = 0
        end = False
        while not end:
            for x in range(50):
                if i < len(titles):
                    print("{:^20}      {:60}      {:^10}      {:^14}".format(titles[i]["tconst"][:20], str(titles[i]["primaryTitle"][:60] or ''), 
                    str(titles[i]["ratings"] or ''), str(titles[i]["numVotes"] or '')))
                    i += 1
                else:
                    end = True
                    break
            if not end:
                input("\n*ENTER to show next 50 results...*\n")
            
    else:
        print("\nNo movies fit these constraints!")


# Search for cast/crew members
def task_3(db, name_basics, title_basics, title_principals):
    os.system(clr)
    name = "^" + input("Enter cast/crew member name: ").strip() + "$"
    
    # Get list of persons with matching name
    persons = list(db.name_basics.find({"primaryName": re.compile(name, re.IGNORECASE)}, {"_id": 0, "primaryProfession": 1, "nconst": 1}))

    if not persons:
        print("\nNo names found!")

    else:

        # Print professions and movies of each member
        print(divider)
        for person in persons:
            print("\nProfession Info\n")
            print("{:^14}    {:^80}".format("nconst", "Professions"))
            print("-" * 14 + " " * 4 + "-" * 80)
            print("{:^14}    {:^80}".format(person["nconst"][:14], ', '.join(person["primaryProfession"])))
            print("\n")  

            # Find titles that cast member is in
            titles = (list(db.title_principals.aggregate([
                {"$match": {"nconst": person["nconst"]}},
                {"$lookup": {
                    "from": "title_basics",
                    "localField": "tconst",
                    "foreignField": "tconst",
                    "as": "primaryTitle"}
                    }
            ])))
            if titles:
                # Print movies of the member if any
                print("Movies\n")
                print("{:<70}      {:^14}      {:^30}      {:^40}".format("Primary Title", "tconst", "Job", "Characters"))
                print("-" * 70 + " " * 6 + "-" * 14 + " " * 6 + "-" * 30 + " " * 6 + "-" * 40)
                for title in titles:
                    if not title["characters"]:
                        title["characters"] = []
                    print("{:<70}      {:^14}      {:^30}      {:^40}".format(str(title["primaryTitle"][0]["primaryTitle"][:70] or ''), 
                    str(title["tconst"][:14] or ''), str(title["job"] or ''), str(', '.join(title["characters"]))))
            else: 
                print("\nNot in any movies!")

            print("\n")
            print(divider)


# Add a movie
def task_4(db, title_basics):
    os.system(clr)

    while True:
        mid = input("Enter unique tconst: ").strip()

        # Make sure unique MID
        if not db.title_basics.find_one({"tconst": mid}):
            break

        print(mid ,"already exists!")

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
    print("\n" + divider + "\nAdded to title_basics: ")
    pprint(db.title_basics.find_one({"tconst": mid}, {"_id": 0}), sort_dicts=False)
    print(divider)
                            

# Add a cast/crew member
def task_5(db, name_basics, title_basics, title_principals):
    os.system(clr)

    # Make sure cast ID exists
    while True:
        cid = input("Enter nconst: ").strip()

        if db.name_basics.find_one({"nconst": cid}):
            break

        print(cid, "does not exist!")
    
    # Make sure title ID exists
    while True:
        mid = input("Enter tconst: ").strip()

        if db.title_basics.find_one({"tconst": mid}):
            break

        print(mid, "does not exist!")
    
    category = input("Enter category: ").strip()

    # Find largest ordering listed
    ordering = list(db.title_principals.aggregate([
        {"$match": {"tconst": mid}},
        {"$group": {"_id": "$tconst", 
                    "max": {"$max": {"$toInt": "$ordering"}}}},
        {"$project": {"_id": 0}}
    ]))

    # Set the new insert's ordering to 1, or largest ordering + 1
    if ordering:
        ordering = str((ordering[0]["max"]) + 1)
    else:
        ordering = '1'

    # Insert the cast/crew member
    db.title_principals.insert_one({"tconst": mid,
                                    "ordering": ordering,
                                    "nconst": cid,
                                    "category": category,
                                    "job": None,
                                    "characters": None
    })

    # Confirm cast/crew member added
    print("\n" + divider + "\nAdded to title_principals: ")
    pprint(db.title_principals.find_one({"$and": [
            {"tconst": mid},
            {"ordering": ordering}
        ]},
        {"_id": 0}), sort_dicts=False
    )
    print(divider)


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
            task_1(db, name_basics, title_basics, title_ratings)
            input("\n*ENTER key to go back*")
        elif task == 2:
            task_2(db, title_basics, title_ratings)
            input("\n*ENTER key to go back*")
        elif task == 3:
            task_3(db, name_basics, title_basics, title_principals)
            input("\n*ENTER key to go back*")
        elif task == 4:
            task_4(db, title_basics)
            input("\n*ENTER key to go back*")
        elif task == 5:
            task_5(db, name_basics, title_basics, title_principals)
            input("\n*ENTER key to go back*")


if __name__ == "__main__":
    main()
