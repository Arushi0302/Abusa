from flask import Flask, request, jsonify
from flask_cors import CORS
from Model.load_abuse import abuse

app = Flask(__name__)
CORS(app)
 
 
@app.route('/')
def infer():
    return "Tested", 200
 
@app.route('/getAbusiveData', methods['POST'])
def bad_words():
    return abuse, 200
 
if __name__ == "__main__":
    app.run()