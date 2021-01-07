from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
 
 
@app.route('/')
def infer():
    return "Tested"
 
 
if __name__ == "__main__":
    app.run('0.0.0.0', 8081)