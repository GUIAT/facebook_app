# TO DO : VALIDATION - OK
# TO DO : GET JSON - PENDING
# facebook documentation to follow : 'check event notification' 
# https://developers.facebook.com/docs/graph-api/webhooks/getting-started?locale=en_US
# Sample app :https://developers.facebook.com/docs/graph-api/webhooks/sample-apps
# video taht might help : https://www.youtube.com/watch?v=82cpdEisqsA&t=246s
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# VARIABLES not sure if keep

token = '12345' #figure out a way to get this from heroku
verification_parameters = []
received_updates = []



class Verification(Resource): # Not Student anymore
    parser = reqparse.RequestParser()
    parser.add_argument('hub.mode')
    parser.add_argument('hub.challenge')
    parser.add_argument('hub.verify_token')

    
    def get (self):
        received_data = Verification.parser.parse_args()
        #verification_parameters.append(received_data)
       
        if token == received_data['hub.verify_token']:
            return int(received_data['hub.challenge'])

#    def post (self):
#        return verification_parameters

# PAYLOAD
#class Payload(Resource): 
    def post (self):
        update = request.get_json()
        received_updates.append(update)
        return update['field']

# APP NECESSITIES
api.add_resource(Verification, '/verification') # Not Student anymore
#api.add_resource(Payload, '/stories') # Not Student anymore

if __name__ == '__main__':
    app.run(debug=True, port=5000)