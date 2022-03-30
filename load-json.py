# Make MongoDB collection from the 4 .jsons
# Port number input, connect to server, create 291db.db
import json
from pymongo import MongoClient 
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

while True:
   try:
        port = input("Enter port number: ")
        break
   except ValueError:
        print("Invalid input!")

# Making Connection
myclient = MongoClient("mongodb://localhost:"+port+'/') 
   
def main():  

    # database 
    db = myclient["291db"]   
    # Created or Switched to collection 
    # names: GeeksForGeeks
    name_basics = db["name_basics"]
    title_basics = db["title_basics"]
    title_principals = db["title_principals"]
    title_ratings = db["title_ratings"]

    name_basics.drop()
    title_basics.drop()
    title_principals.drop()
    title_ratings.drop()

    # Loading or Opening the json file
    with open(dir_path+'/name.basics.json') as file:
        file_data = json.load(file)
    name_basics.insert_many(file_data)  
    file.close()

    with open(dir_path+'/title.basics.json') as file:
        file_data = json.load(file)
    title_basics.insert_many(file_data)  
    file.close()

    with open(dir_path+'/title.principals.json') as file:
        file_data = json.load(file)
    title_principals.insert_many(file_data)  
    file.close()

    with open(dir_path+'/title.ratings.json') as file:
        file_data = json.load(file)
    title_ratings.insert_many(file_data)  
    file.close()

if __name__ == "__main__":
    main()
