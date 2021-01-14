from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from Model.load_abuse import abuse
from Model.model import getData

app = Flask(__name__)
CORS(app)
 
data = []
 
@app.route('/')
def infer():
    return "Tested", 200
 
@app.route('/getAbusiveData')
def bad_words():
    return abuse, 200

@app.route('/getModelData')
def model_data():
    return jsonify(data), 200

@app.route('/modelData', methods = ['POST'])
def data_recieve():
    global data
    data = request.get_json()
    data = getData(data)
    response = jsonify({"data": "OK"})
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Origin", "*")
    
    return response, 200
 
if __name__ == "__main__":
    app.run()