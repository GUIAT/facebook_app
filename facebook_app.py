from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# VARIABLES
token = '12345'


class Verification(Resource): # Not Student anymore
    parser = reqparse.RequestParser()
    parser.add_argument('hub.mode', type=str)
    parser.add_argument('hub.challenge', type=str)
    parser.add_argument('hub.verify_token', type=str)
    
    def get (self):
        received_data = Verification.parser.parse_args()
        verification_data = {
                            'hub.mode' : received_data['hub.mode'],
                            'hub.challenge' : received_data['hub.challenge'],
                            'hub.verify_token' : received_data['hub.verify_token']

                            }

        return verification_data



api.add_resource(Verification, '/verification') # Not Student anymore

if __name__ == '__main__':
    app.run(debug=True, port=5000)