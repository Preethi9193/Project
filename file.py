from flask import Flask ,Response ,request
import pymongo
import json
from bson.objectid import ObjectId
from pymongo.message import _do_bulk_write_command
app = Flask(__name__)


### to connect the database 
try:
    mongo = pymongo.MongoClient(host="localhost",
    port = 27017)
    db = mongo.company
    mongo.server_info()  # it triggers exception if cannot connect to db

except:
    print("ERROR - Cannot Connect to db")
#######################

#(Creating the database)

@app.route("/users",methods = ['POST'])
def create_user():
    try:
       # user = {"name":"A","lastname":"AA"}   ### To send the data manually to database
        user = {"name":request.form["name"],   ## to send the data from postman using post method
        "lastname":request.form["lastname"]}
        dbResponse = db.users.insert_one(user)
        print(dbResponse.inserted_id)
        return Response(
            response=json.dumps({"message":"user created","id":f"{dbResponse.inserted_id}"}),
            status =200,
            mimetype="application/json"
        )
    except Exception as ex:
        print("******")
        print(ex)
        print("*****")
########################
### To read the data from the database[get]method

@app.route("/users",methods = ["GET"])
def get_some_users():
    try:
        data = list(db.users.find()) ## find is the command which gives all the users in th database 
        for user in data:
            user["_id"] = str(user["_id"])
        return Response( response=json.dumps(data),
            status =500,
            mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response( response=json.dumps({"message":"cannot read users"}),
            status =500,
            mimetype="application/json")

############################################
### To update the data in the database using method[put]  --- Here we give the <id> which we need to update

@app.route("/users/<id>",methods = ["PUT"])
def update_user(id):
    try:
        dbRespone = db.users.update_one(
            {"_id":ObjectId(id)},
            {"$set":{"name":request.form["name"]}},
            {"$set":{"lastname":request.form["name"]}}
        )
        #for attr in dir(dbRespone):   ## to get the methods which can be performed in REsponse using it
        #   print(f"****{attr}*****")
        ## to check weather data is modified or not
        if dbRespone.modified_count == 1:
            return Response( response=json.dumps({"message":"User updated"}),
            status = 200,
            mimetype="application/json")  
        else:
            return Response( response=json.dumps({"message":"Nothing to updated"}),
            status = 200,
            mimetype="application/json") 

    except Exception as ex:
        print("***********")
        print(ex)
        print("************")
        return Response( response=json.dumps({"message":"Sorry cannot update user"}),
            status = 500,
            mimetype="application/json")
########################################
### To Delete the data from the database we use method[DELETE]
@app.route("/users/<id>",methods = ["DELETE"])
def delete_user(id):
    try:
        dbResponse = db.users.delete_one({"_id":ObjectId(id)})
        ## to check whether user is correctly deleted or not
        if dbResponse.deleted_count == 1:
            return Response( response=json.dumps({"message":"User Deleted","id":f"{id}"}),
            status = 200,
            mimetype="application/json")
        ## to return the response after deleting the particular user and returing the id 
        return Response( response=json.dumps({"message":"User not found","id":f"{id}"}),
            status = 200,
            mimetype="application/json")
    except Exception as ex:
        print("******")
        print(ex)
        print("*******")
        return Response( response=json.dumps({"message":"Sorry cannot delete a user"}),
            status = 500,
            mimetype="application/json")


#######################
if __name__ == "__main__":
    app.run(port = 80,debug = True)