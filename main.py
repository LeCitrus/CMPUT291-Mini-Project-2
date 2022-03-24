# Connect to 291db.db
# Should be able to run the 5 tasks

from pymongo import MongoClient
import json

# Get port number
def get_port():
   while True:
      try:
           port = int(input("Enter port number: "))
           return port
      except ValueError:
           print("Invalid input!")

            
def main():
   port = get_port()
   
if __name__ == "__main__":
    main()
