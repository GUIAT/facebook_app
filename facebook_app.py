from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# VARIABLES
token = '12345'


class Verification(Resource): # Not Student anymore
    def get (self):
        parser = reqparse.RequestParser()
        parser.add_argument('hub.mode', type=str)
        parser.add_argument('hub.challenge', type=str)
        parser.add_argument('hub.verify_token', type=str)
        return parser.parse_args()



api.add_resource(Verification, '/verification') # Not Student anymore

if __name__ == '__main__':
    app.run(debug=True, port=5000)