from flask import Flask
from flask import Response
from adal import AuthenticationContext
import flask
import uuid
import requests
import config
import json
from flask import render_template, Flask, request, redirect, url_for, session, flash, escape, send_file, jsonify, json, make_response

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'

SESSION = requests.Session()
PORT = 5000  # A flask app by default runs on PORT 5000
AUTHORITY_URL = config.AUTHORITY_HOST_URL + '/' + config.TENANT
REDIRECT_URI = 'http://localhost:{}/getAToken'.format(PORT)
TEMPLATE_AUTHZ_URL = ('https://login.microsoftonline.com/{}/oauth2/authorize?' + 
                      'response_type=code&client_id={}&redirect_uri={}&' + 
                      'state={}&resource={}')


@app.route("/")
def main():
    '''login_url = 'http://localhost:{}/login'.format(PORT)

    resp = Response(status=307)
    resp.headers['location'] = login_url'''
    return  main_logic()

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    # res = processRequest(req)
    
    res = jsonify({
                "fulfillmentText": "This is a text response",
                "fulfillmentMessages": [
                  {
                    "card": {
                      "title": "card title",
                      "subtitle": "card text",
                      "imageUri": "https://assistant.google.com/static/images/molecule/Molecule-Formation-stop.png",
                      "buttons": [
                        {
                          "text": "button text",
                          "postback": "https://assistant.google.com/"
                        }
                      ]
                    }
                  }
                ],
                "source": "example.com",
                "payload": {
                  "google": {
                    "expectUserResponse":"true",
                    "richResponse": {
                      "items": [
                        {
                          "simpleResponse": {
                            "textToSpeech": "this is a simple response"
                          }
                        }
                      ]
                    }
                  },
                  "facebook": {
                    "text": "Hello, Facebook!"
                  },
                  "slack": {
                    "text": "This is a text response for Slack."
                  }
                },
                "outputContexts": [
                  {
                    "name": "projects/${PROJECT_ID}/agent/sessions/${SESSION_ID}/contexts/context name",
                    "lifespanCount": 5,
                    "parameters": {
                      "param": "param value"
                    }
                  }
                ],
                "followupEventInput": {
                  "name": "event name",
                  "languageCode": "en-US",
                  "parameters": {
                    "param": "param value"
                  }
                }})
           
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def login():
 
    auth_state = str(uuid.uuid4())
    SESSION.auth_state = auth_state
   
    authorization_url = TEMPLATE_AUTHZ_URL.format(
        config.TENANT,
        config.CLIENT_ID,
        REDIRECT_URI,
        auth_state,
        config.RESOURCE)
        
    resp = Response(status=307)
    resp.headers['location'] = authorization_url
 
    return resp


@app.route("/getAToken")
def main_logic():
    
    

   
    # Need to install requests package for python
    # easy_install requests

    # Set the request parameters
    url = 'https://dev34640.service-now.com/api/now/v1/table/incident'

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'admin'
    pwd = 'Mohan@8391'

    # Set proper headers
    headers = {"Content-Type":"application/json", "Accept":"application/json"}
    # Do the HTTP request
    auth = (user,pwd)
    '''response = requests.post(url, auth=(user, pwd), headers=headers)'''
    response = make_api_call('POST',url,auth,"","")

    # Check for HTTP codes other than 200
    # Decode the JSON response into a dictionary and use the data
    
    data = response.json()
    print(data)
    print(str(response))
    return jsonify(data)
   

def createApiUrl(roomName, response):
    
    r = make_api_call('GET', 'https://outlook.office.com/api/v2.0/users/' + roomName + '/events' , str(response['access_token']), "", "").json()
    jsonString = json.dumps(r)
    valueArray = json.loads(jsonString)
    print(len(valueArray))
    '''for index in range(len(valueArray)):
     getValuesCal(index, valueArray)'''
    print('data is ' + str(r))
    
    return jsonify(r)


def getValuesCal(index, valueArray):
    valueArray = valueArray["meetingTimeSuggestions"][index]
    meetingTimeSlotData = valueArray["meetingTimeSlot"]
    '''roomLocationsName = meetingTimeSlotData["locations"]
    roomName = roomLocationsName["displayName"]'''
    locationValue = valueArray["locations"]
    for index in range(0, len(locationValue)):
     findMeetingRoom(index, locationValue, meetingTimeSlotData)
     
    print(len(locationValue))

     
def findMeetingRoom(index, locationValue, meetingTimeSlotData):
     address = locationValue[index]
     roomName = address["displayName"]
     roomEmailAddress = address["locationEmailAddress"]
     endData = meetingTimeSlotData["end"]
     endDateTime = endData["dateTime"]
     startData = meetingTimeSlotData["start"]
     startDateTime = startData["dateTime"]
     print('Meeting room name is ' + str(roomName))
     print('Meeting room email address ' + roomEmailAddress)
     print('Start Time is ' + startDateTime)
     print('End Time is ' + endDateTime)
     print ('Index is:', index)
     print (meetingTimeSlotData)
     print('**********************************End*********************************')


def getValues(index, valueArray):
    print('printing values')
    valueArray = valueArray["value"][index]
    ownerData = valueArray["Owner"]
    addressData = ownerData["Address"]
    print('email address of the owner is ' + addressData)
    print ('Owner data index is:', index)
    print (ownerData)


def make_api_call(method, url, auth,payload=None, parameters=None):
      # Send these headers with all API calls
      headers = { "Content-Type":"application/json", "Accept":"application/json"}
    
      # Use these headers to instrument calls. Makes it easier
      # to correlate requests and responses in case of problems
      # and is a recommended best practice.
      request_id = str(uuid.uuid4())
      instrumentation = { 'client-request-id' : request_id,
                          'return-client-request-id' : 'true' }
    
      headers.update(instrumentation)
    
      response = None
    
      if (method.upper() == 'GET'):
          response = requests.get(url, auth=auth, headers=headers)
      elif (method.upper() == 'DELETE'):
          response = requests.delete(url, auth=auth, headers=headers)
      elif (method.upper() == 'PATCH'):
          headers.update({ 'Content-Type' : 'application/json' })
          response = requests.patch(url, auth=auth, headers=headers)
      elif (method.upper() == 'POST'):
          headers.update({ 'Content-Type' : 'application/json' })
          response = requests.post(url, auth=auth, headers=headers)
    
      return response  


if __name__ == "__main__":
    app.run()
