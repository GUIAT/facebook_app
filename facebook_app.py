# TO DO : VALIDATION - OK
# TO DO : GET JSON - PENDING
# facebook documentation to follow : 'check event notification' 
# https://developers.facebook.com/docs/graph-api/webhooks/getting-started?locale=en_US
# Sample app :https://developers.facebook.com/docs/graph-api/webhooks/sample-apps
# video taht might help : https://www.youtube.com/watch?v=82cpdEisqsA&t=246s

from flask import Flask, request,  jsonify, abort
from flask_restful import Resource, Api, reqparse
from os import environ
import hmac
from hashlib import sha1

app = Flask(__name__)
api = Api(app)


# ------------------------LINES 9 /18 == ?


# ------------------------LINES 20 /21 == OK
token = str(12345)                            #DELETE ONCE DONE / We will use CONFIG VARS from Heroku once done      
#token = environ.get("TOKEN") or 'token'       PUT BACK ONCE DONE/ CHEKC IF THIS WORKS IN HEROKU /make sure this is a striiiinngggg
received_updates = []

# ------------------------LINES 23 /26 == OK
class Updates(Resource): 
    parser = reqparse.RequestParser()
    parser.add_argument('field')
    parser.add_argument('value')

    def get (self):
        received_updates = Updates.parser.parse_args()
        app.logger.info('All good so far')                #DELETE ONCE DONE
        return received_updates

# ------------------------LINES 28 /37 == OK
class Verification(Resource): 
    parser = reqparse.RequestParser()
    parser.add_argument('hub.mode')
    parser.add_argument('hub.challenge')
    parser.add_argument('hub.verify_token') #, location='form' does not workcd ..
    parser.add_argument('field') #, type=list, location='json'
    parser.add_argument('value') #, type=list, location='json'
    

    def get (self):
        received_data = Verification.parser.parse_args()

        # Debugging logs
        app.logger.info(token)  
        app.logger.info(received_data['hub.mode'] == 'subscribe' and received_data['hub.verify_token'] == token) 
        app.logger.info(received_data['hub.mode'] == 'subscribe') 
        app.logger.info(received_data['hub.verify_token'] == token) 

        if received_data['hub.mode'] == 'subscribe' and received_data['hub.verify_token'] == token :
            return int(received_data["hub.challenge"])

# ------------------------LINES 39 /52 == ?

    def post (self):
        received_data = Verification.parser.parse_args()
        received_updates.append(received_data['field'])
        received_updates.append(received_data['value'])          #DELETE ONCE DONE

        app.logger.info(received_data['field'])  
        app.logger.info(received_data['value'])  
        return received_updates

    

'''
        if ""
        app.logger.info ('Facebook request body:')
'''

# ROUTING
api.add_resource(Updates, '/') 
api.add_resource(Verification, '/facebook') 


if __name__ == '__main__':
    app.run(debug=True, port=5000)