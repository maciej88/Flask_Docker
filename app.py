from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


def check_data(postedData, functionName):
    if (functionName == "add"):
        if "x" not in postedData or "y" not in postedData:
            return 301
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


class Substract(Resource):
    pass


class Multiply(Resource):
    pass


class Divide(Resource):
    pass


api.add_resource(Add, "/add")


@app.route('/')
def hello_world():
    return "Hello World!"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80)
