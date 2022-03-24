# Connect to 291db.db
# Should be able to run the 5 tasks

from pymongo import MongoClient
import json

while True:
   try:
        port = int(input("Enter port number: "))
        break
   except ValueError:
        print("Invalid input!")
