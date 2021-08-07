from flask import Flask
import pymongo

## To intialize the new client for our database we use MongoClient()
client = pymongo.MongoClient()

### To create a database client["databasename"]
mydb = client["Mydb"]

### To create a database in mongodatabase , unless we create a collection in given database
## to create a collection database['CollectionName']
mycol = mydb['People']

### Now we need to create a data in collection which is in Json format 
data = {'name':'abc','age':30}

### to insert the data into collection we can use single(by insert_one),multiple(insert_many)
mycol.insert_one(data)

### To insert the data with multiple elements into database
datalist = [{'name':'def','age':10},{'name':'john'}]

x=mycol.insert_many(datalist)

### to get the ids present in the database
print(x.inserted_ids)

### to get the databaselist names present in the database
print(client.list_database_names())

### To get the collection names 
print(mydb.collection_names())

### to print the everything in the document 
for i in mycol.find():
    print(i)
### to get particular data in collection we can use n no of conditions in the find()
for i in mycol.find({'name':'abc'}):
    print(i)