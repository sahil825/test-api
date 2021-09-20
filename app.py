from os import name
from flask import Flask, Response, request
import pymongo
import json
import bson.objectid
from pymongo.message import delete 

from werkzeug.wrappers import response
app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(
        host="localhost", 
        port =27017,
        serverSelectionTimeoutMs = 1000
        )
        db = mongo.Company 
        mongo.server_info() 
except:
    print("Error - Cannot connect to db")

#########################
@app.route("/users", methods=["GET"])
def get_some_users():
    try:
        data = list(db.users.find())
        for user in data:
            user ["_id"]= str(user["_id"])
        return response(response = json.dumps([{"id":1},{"id":2}]),
            status=500,
            mimetype="application/json"
            )

    except Exception as ex:
        print(ex)
        return response(response = json.dumps({"massage":"cannot read user"}),
            status=500,
            mimetype="application/json"
            )



#########################

@app.root("/user", method=["POST"])
def create_user():
    try:
        user = {
            "name":request.form["name"], 
            "LastName":request.form["last name"]
            }
        dbResponse = db.user.instert_one(user)
        print(dbResponse.insterted_id)
        #for attr in dir(dbResponse):
           # print(attr)
        return Response(
            response= json.dumps(
            response={"massage":"user created", 
            "id":f"{dbResponse.insert_id}"
            }),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print("**************")
        print(ex)
        print("**************")

#######################
@app.route("/user/<id>", method=["PATCH"])
def update_user(id):
    
    try:
        dbResponse = db.user.update_one(
            {"_id":bson.objectid.ObjectId(id)},
            {"$set":{"name":request.form["name"]}}
        )
            if dbResponse.modified_count == 1:
               return Response(
            response= json.dumps(
                {"massage":"user updated"}),
            status=200,
            mimetype="application/json"
        ) 
            else:
                return Response(
            response= json.dumps(
                {"massage":"nothing to updated"}),
            status=200,
            mimetype="application/json"

    except Exception as ex:
        print("***************************")
        print(ex)
        print("***************************")
        return Response(
            response= json.dumps(
                {"massage":"sorry cannot update user"}),
            status=500,
            mimetype="application/json"
        )



########################
@app.route("/user/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        dbResponse = db.user.delete_one({"_id:Objectid(id"})
        if dbResponse.deleted_count == 1:

        return Response(
            response= json.dumps(
                {"massage":"user delete","id":f"{id}"}),
            status=200,
            mimetype="application/json"
        )
            
        return Response(
            response= json.dumps(
                {"massage":"user not found",id":f"{id}"}),
            status=200,
            mimetype="application/json"
        )

    except Exception as ex:
        print("********")
        print(ex)
        print("********")
        return Response(
            response= json.dumps(
                {"massage":"sorry cannot delete user"}),
            status=500,
            mimetype="application/json"
        )




########################

if __name__ == "__main__":
    app.run(port=80, debug=True)