from waitress import serve
from flask import Flask, request, abort
import requests
import json
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])

def webhook():
    if request.method == 'POST':
        
        print(request.json)
       
        try:
            WEBHOOK_URI = os.environ['WEBHOOK_URI']
        except KeyError:
            print ("Please set the environment variable WEBHOOK_URI")

        message = json.dumps(request.json)
        
        response = "Error occured while sending message. Please check webhook url"
        
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
    serve(app, host='0.0.0.0', port=5000)
