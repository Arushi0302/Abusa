from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from Model.load_abuse import abuse
from Model.model import getData

app = Flask(__name__)
CORS(app)
 
 
@app.route('/')
def infer():
    return "Tested", 200
 
@app.route('/getAbusiveData')
def bad_words():
    return abuse, 200

@app.route('/modelData', methods = ['POST'])
@cross_origin()
def data_recieve():
    data = request.get_json()
    
    return jsonify(getData(data)), 200
 
if __name__ == "__main__":
    app.run()