from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentenceDatabase
users = db["Users"]


def verify_password(username, password):
    hashed_p = users.find({
        "Username": username
    })[0]["Password"]
    if bcrypt.hashpw(password.encode('utf8'), hashed_p) == hashed_p:
        return True
    else:
        return False


def count_tokens(username):
    tokens = users.find({
        "Username": username
    })[0]["Tokens"]
    return tokens


class Register(Resource):
    def post(self):
        # get posted data from user:
        postedData = request.get_json()

        # data grab:
        username = postedData["username"]
        password = postedData["password"]

        # hashing password by bcrypt
        hashed_p = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        # store user log and pass in db:
        users.insert_one({
            "Username": username,
            "Password": password,
            "Sentence": "",
            "Tokens": 6
        })

        retJson = {
            "status": 200,
            "msg": "Success signed in API"
        }
        return jsonify(retJson)


class Store(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]

        correct_p = verify_password(username, password)

        if not correct_p:
            retJson = {
                "status": 302
            }
            return jsonify(retJson)

        num_token = count_tokens(username)
        if num_token <= 0:
            retJson = {
                "status": 301
            }
            return jsonify(retJson)

        users.update_one({
            "Username": username
        },
            {"$set":
                {
                    "Sentence": sentence,
                    "Tokens": num_token - 1
                }})

        retJson = {
            "status": 200,
            "msg": "sentence saved"
        }
        return jsonify(retJson)

class Get(Resource):
    def get(self):
        postedData = request.get_json()

        username = postedData["Username"]
        password = postedData["Password"]

        correct_p = verify_password(username, password)

        if not correct_p:
            retJson = {
                "status": 302
            }
            return jsonify(retJson)

        num_token = count_tokens(username)
        if num_token <= 0:
            retJson = {
                "status": 301
            }
            return jsonify(retJson)

        sentence = users.find({
            "Username": username
        })[0]["Sentence"]

        retJson = {
            "status": 200,
            "sentence": sentence
        }
        return jsonify(retJson)

api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource((Get, '/get'))

"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.aNewDB
UserNum = db["UserNum"]

UserNum.insert_one({
    "num_users":0
})


class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]["num_users"]
        new_num = prev_num + 1
        UserNum.update_one({}, { "$set": {"num_users": new_num}})
        return str(f"Hello user {str(new_num)}")


def check_data(postedData, functionName):
    if (functionName == "add" or functionName == "subtract" or functionName == "multiply"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        else:
            return 200
    elif (functionName == 'divide'):
        if "x" not in postedData or "y" not in postedData:
            return 301
        elif int(postedData["y"]) == 0:
            return 302
        else:
            return 200


class Add(Resource):
    def post(self):
        postedData = request.get_json()

        status_code = check_data(postedData, "add")
        if (status_code != 200):
            retJson = {
                "Message": "An error",
                "Status Code": status_code
            }
            return jsonify(retJson)

        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        ret = x + y
        retMap = {
            'Sum': ret,
            'Status Code': 200,
        }
        return jsonify(retMap)


class Subtract(Resource):
    def post(self):
        postedData = request.get_json()

        status_code = check_data(postedData, "subtract")
        if (status_code != 200):
            retJson = {
                "Message": "An error",
                "Status Code": status_code
            }
            return jsonify(retJson)

        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        ret = x - y
        retMap = {
            'Subtract': ret,
            'Status Code': 200,
        }
        return jsonify(retMap)


class Multiply(Resource):
    def post(self):
        postedData = request.get_json()

        status_code = check_data(postedData, "multiply")
        if (status_code != 200):
            retJson = {
                "Message": "An error",
                "Status Code": status_code
            }
            return jsonify(retJson)

        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        ret = x * y
        retMap = {
            'Multiply': ret,
            'Status Code': 200,
        }
        return jsonify(retMap)


class Divide(Resource):
    def post(self):
        postedData = request.get_json()

        status_code = check_data(postedData, "divide")
        if (status_code != 200):
            retJson = {
                "Message": "An error",
                "Status Code": status_code
            }
            return jsonify(retJson)

        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        ret = (x * 1.0) / y
        retMap = {
            'Divide': ret,
            'Status Code': 200,
        }
        return jsonify(retMap)


api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/divide")
api.add_resource(Visit, "/hello")


@app.route('/')
def hello_world():
    return "Hello World!"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
"""
