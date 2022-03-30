from pymongo import MongoClient 
import json
import os

# Creating File path
dir_path = os.path.dirname(os.path.realpath(__file__))
   
while True:
   try:
        port = input("Enter port number: ")
        break
   except ValueError:
        print("Invalid input!")

# Making Connection
def connector(port):
    # connects to db
    if port == None:
        return -1
    else:
        myclient = MongoClient("mongodb://localhost:"+port+'/') 
        return myclient
   

def clear_collections(name_basics, title_basics, title_principals, title_ratings):
    # drops all collections
    # for demo
    name_basics.drop()
    title_basics.drop()
    title_principals.drop()
    title_ratings.drop()
   
def main(myclient):  
    # database 
    db = myclient["291db"]   
    # Created or Switched to collection 
    # names: GeeksForGeeks
    name_basics = db["name_basics"]
    title_basics = db["title_basics"]
    title_principals = db["title_principals"]
    title_ratings = db["title_ratings"]
    
    clear_collections(name_basics, title_basics, title_principals, title_ratings)

    # Loading / Opening the json file
    print("Loading name.basics.json...")
    with open(dir_path+'/name.basics.json') as file:
        file_data = json.load(file)
    name_basics.insert_many(file_data) 
    print("file opened") 
    file.close()

    print("Loading title.basics.json...")
    with open(dir_path+'/title.basics.json') as file:
        file_data = json.load(file)
    title_basics.insert_many(file_data) 
    print("file opened") 
    file.close()

    print("Loading title.principals.json...")
    with open(dir_path+'/title.principals.json') as file:
        file_data = json.load(file)
    title_principals.insert_many(file_data)  
    print("file opened")
    file.close()

    print("Loading title.ratings.json...")
    with open(dir_path+'/title.ratings.json') as file:
        file_data = json.load(file)
    title_ratings.insert_many(file_data)  
    print("file opened")
    file.close()

    # create indexing
    db['title_basics'].create_index('tconst')
    db['title_ratings'].create_index('tconst')
    db['name_basics'].create_index('nconst')
    db['title_principals'].create_index('nconst')
    db['title_principals'].create_index('tconst')

if __name__ == "__main__":
    myclient = connector(port)
    main(myclient)
 
