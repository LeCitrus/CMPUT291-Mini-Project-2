from pymongo import MongoClient
import json

client = MongoClient("localhost", 27012)

db = client["291db"]

name_basics = db["name_basics"]
title_basics = db["title_basics"]
title_principals = db["title_principals"]
title_ratings = db["title_ratings"]

def clear_collections():
    name_basics.drop()
    title_basics.drop()
    title_principals.drop()
    title_ratings.drop()