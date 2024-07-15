from flask import Flask, request, jsonify
from flask_cors import CORS
from nlpa_python.spacy_kbqa import generate_response

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/nlpa/qa', methods=['POST'])
def chat():
    print(f'Input: {request}')
    user_question = request.json.get('message')
    bot_response = generate_response(user_question) 
    return jsonify(bot_response)

if __name__ == '__main__':
    app.run(port=5000)
