from pymongo import MongoClient
from flask import Flask, request, jsonify
import os


url = "mongodb+srv://bgserl65:kXEVKPfCMuVYZ7B2@bagasbabiganas.jcvvr.mongodb.net/?retryWrites=true&w=majority&appName=bagasbabiganas"



client = MongoClient(url)
db = client["SMCP"]
collection = db["SIC6"] 

app = Flask(__name__)


@app.route('/save', methods=['POST'])
def save_item():
    try:
        data = request.get_json()
        
        if not data or "temperature" not in data or "humidity" not in data:
            return jsonify({"error": "Missing required fields"}), 400

        temperature= data.get("temperature")
        humidity= data.get("humidity")
        data= {"temperature":temperature,"humidity":humidity}

        
        if not data:
            return jsonify({"error": "No data provided"})
        
        result=collection.insert_one(data)  
        return jsonify({"message": "Item added", "id": str(result.inserted_id)})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=9090, host='0.0.0.0')