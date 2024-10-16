#!/usr/bin/python3
from gpt4all import GPT4All
from flask import Flask,render_template, redirect, session, request
import database_handler, jsonify
from flask_cors import CORS

application = Flask(__name__)
model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")
CORS(application)

@application.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    #Get the API key from the request
    api_key = request.args.get('api_token')
    #Check if the API key is valid
    if database_handler.check_api_key(api_key):
        #Return the jsonified response
        response_dict = {
            'status': 'success',
            'message': 'Authentication successful'
        }
        return jsonify(response_dict)
    else:
        #Return the jsonified response
        response_dict = {
            'status': 'error',
            'message': 'Authentication failed'
        }
        return jsonify(response_dict)
    

@application.route('/send_message', methods=['POST'])
def send_message():
    # Get the API key and message from the request
    data = request.get_json()  # Get the JSON data from the request
    api_key = data.get('api_key')  # Extract API key
    message = data.get('message')    # Extract message

    print("================================================")
    print(f"Received API Key: {api_key}")
    print(f"Received Message: {message}")

    with model.chat_session():
            bot_response = model.generate(message)
    print(f"Bot: {bot_response}")

    response_dict = {
        'status': 'success',
        'message': bot_response
    }
    return jsonify(response_dict)
    """
    # Check if the API key is valid
    if database_handler.check_api_key(api_key):
        # Send the message to the bot
        with model.chat_session():
            bot_response = model.generate(message)
        
        response_dict = {
            'status': 'success',
            'message': bot_response
        }
        return jsonify(response_dict), 200  # Return a 200 OK status
    else:
        response_dict = {
            'status': 'error',
            'message': 'Authentication failed'
        }
        return jsonify(response_dict), 401  # Return a 401 Unauthorized status
        """

if __name__ == '__main__':
    application.run(host='localhost', port=5000)