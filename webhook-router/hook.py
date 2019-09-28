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

        message = json.dumps(request.json)
        
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
