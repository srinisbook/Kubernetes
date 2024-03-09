from waitress import serve
from flask import Flask, request, abort
import requests
import json
import os
import datetime

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])

def webhook():
    if request.method == 'POST':
        
        print(request.json)
       
        try:
            WEBHOOK_URI = os.environ['WEBHOOK_URI']
        except KeyError:
            print ("[ERROR] " + datetime.datetime.now().strftime("%Y %d %b %H:%M:%S") + " Please set the environment variable WEBHOOK_URI")

        try:
            SERVER_NAME = os.environ['SERVER_NAME']
        except KeyError:
            SERVER_NAME = ""
            print ("[ERROR] " + datetime.datetime.now().strftime("%Y %d %b %H:%M:%S") + " Please set the environment variable SERVER_NAME")
        
        try:
            CUSTOM_HEADER = os.environ['CUSTOM_HEADER']
            HEADER = CUSTOM_HEADER + "\n"

        except KeyError:
            HEADER = ""

        request_data = request.json
        alerts = request_data['alerts']
        no_of_alerts = len(alerts)
        
        message = HEADER +  "Alerts from \t: " + SERVER_NAME + "\n" + "===================================" + "\n"
        
        for i in range(no_of_alerts):
            try:
                message = message + 'Job Name \t: ' + alerts[i]['labels']['job'] + '\n'
            except:
                print ("Job field not found")
            try:
                message = message + 'Alert Name \t: ' + alerts[i]['labels']['alertname'] + '\n'    
            except:
                print ("Alert Name field not found")
            try:
                message = message + 'StartsAt \t\t: ' + alerts[i]['startsAt'] + '\n'
            except:
                print("StartsAt field not found" )
            try:
                message = message + 'Status \t\t: ' + alerts[i]['status'] + '\n'
            except:
                print("Status field not found" )
            try:
                message = message + 'Severity \t\t: ' + alerts[i]['labels']['severity'] + '\n'
            except:
                print("Severity field not found" )
            try:
                message = message + 'Message \t: ' + alerts[i]['annotations']['message'] + '\n\n'
            except:
                print ("Message field not found")
            
        response = "[ERROR] " + datetime.datetime.now().strftime("%Y %d %b %H:%M:%S") + " Error occured while sending message. Please check webhook url"
        
        try:
            response = requests.post(
                url=WEBHOOK_URI,
                json={"Content": message}) 
        except:
            return response
        
        return '', 200
    else:
        abort(400)

if __name__ == '__main__':
    
    print("[INFO] " + datetime.datetime.now().strftime("%Y %d %b %H:%M:%S") + " Webhook router stated." )

    serve(app, host='0.0.0.0', port=5000)
