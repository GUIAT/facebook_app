# TO DO : VALIDATION - OK check on how to get environnement valiable token working
# TO DO : GET JSON - OK
# TO DO : Check how to validate payload, SHA1 SIGNATURE not working
# TO DO : figure out a way to get every story id
# TO DO : store ids in DB + insights in db
# TO DO : match STORIES ID WITH ITS INSIGHTS

# facebook documentation to follow : 'check event notification' 
# https://developers.facebook.com/docs/graph-api/webhooks/getting-started?locale=en_US
# Sample app :https://developers.facebook.com/docs/graph-api/webhooks/sample-apps
# video taht might help : https://www.youtube.com/watch?v=82cpdEisqsA&t=246s
# Webhook Insta : https://developers.facebook.com/docs/graph-api/webhooks/reference/instagram/

# request to get all id necessary to request sotries : https://developers.facebook.com/docs/instagram-api/getting-started
# stories endpoint : https://developers.facebook.com/docs/instagram-api/reference/user/stories

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
#token = str(environ.get("TOKEN")) or 'token'        PUT BACK ONCE DONE/ CHEKC IF THIS WORKS IN HEROKU /make sure this is a striiiinngggg
received_updates = []

# ------------------------LINES 23 /26 == OK
class Updates(Resource): 
    #parser = reqparse.RequestParser()
    #parser.add_argument('field')
    #parser.add_argument('value')

    def get (self):
        #received_updates = Updates.parser.parse_args()                                  #DELETE ONCE DONE
        app.logger.info(received_updates)                                                #DELETE ONCE DONE
        return {'Received_updates' : received_updates}

# ------------------------LINES 28 /37 == OK
class Verification(Resource): 
    parser = reqparse.RequestParser()
    parser.add_argument('hub.mode')
    parser.add_argument('hub.challenge')
    parser.add_argument('hub.verify_token') #, location='form' does not workcd ..
    parser.add_argument('entry')
    #parser.add_argument('field') #, type=list, location='json'                             #DELETE ONCE DONE
    #parser.add_argument('value') #, type=list, location='json'                             #DELETE ONCE DONE
    

    def get (self):
        received_data = Verification.parser.parse_args()

        # Debugging logs
        app.logger.info(token)                                                                                      #DELETE ONCE DONE
        app.logger.info(received_data['hub.mode'] == 'subscribe' and received_data['hub.verify_token'] == token)    #DELETE ONCE DONE
        app.logger.info(received_data['hub.mode'] == 'subscribe')                                                   #DELETE ONCE DONE
        app.logger.info(received_data['hub.verify_token'] == token)                                                 #DELETE ONCE DONE

        if received_data['hub.mode'] == 'subscribe' and received_data['hub.verify_token'] == token :
            return int(received_data["hub.challenge"])

# ------------------------LINES 39 /52 == ?

    def post (self):
        '''
        Does not WOrk
        if "X-Hub-Signature" not in request.headers:
            abort (403)
            return {"nique" : "nique"}
        signature = request.headers.get("X-Hub-Signature", "").split(":")[1]
       
        # Generate our own signature based on the request payload
        secret = os.environ.get('APP_SECRET', '').encode("utf-8")
        mac = hmac.new(secret, msg=request.data, digestmod=sha1)

        # Ensure the two signatures match
        if not str(mac.hexdigest()) == str(signature):
            abort(403)
            return {"nique" : "nique"}
        '''

        received_data = Verification.parser.parse_args()
        isThereData = received_data['entry']
        
        if isThereData :
            received_updates.append(received_data['entry'])
            
            #received_updates.append(received_data['field'])           #DELETE ONCE DONE
            #received_updates.append(received_data['value'])          #DELETE ONCE DONE

        return {'Received_updates' : received_updates}, 200


# ROUTING
api.add_resource(Updates, '/') 
#api.add_resource(Verification, '/facebook')                        #DELETE ONCE DONE
api.add_resource(Verification, '/instagram')  


if __name__ == '__main__':
    app.run(debug=True, port=5000)