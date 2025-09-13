from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import numpy as np
import requests

from keras.applications import InceptionV3
from keras.applications.inception_v3 import preprocess_input
from keras.applications import imagenet_utils
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
from io import BytesIO
import os

app = Flask(__name__)
api = Api(app)
# Load the pretrained model
pretrained_model = InceptionV3(weights="imagenet")


# Initialize MongoDB client
client = MongoClient("mongodb://db:27017/")
db = client.ImageRecognition
users = db["Users"]

def user_exists(username):
    return users.count_documents({"Username": username}) > 0


def verify_password(username, password):
    if not user_exists(username):
        return False
    hashed_password = users.find_one({"Username": username})["Password"]
    if bcrypt.checkpw(password.encode('utf8'), hashed_password):
        return True
    return False

def verify_credentials(username, password):
    if not user_exists(username):
        return {"status": 301, "message": "Invalid Username"}, True
    correct_password = verify_password(username, password)
    if not correct_password:
        return {"status": 302, "message": "Invalid Password"}, True
    
    return None, False

def generate_return_dictionary(status, message):
    return {
        "status": status,
        "message": message
    }

class Register(Resource):
    def post(self):
        # Get the data from the POST request
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        # Check if the username already exists
        if user_exists(username):
            return jsonify({
                "status": 301,
                "message": "Username already exists"
            })
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        # Insert the user into the database
        users.insert_one({"Username": username, "Password": hashed_password, "Tokens": 6})
        return jsonify({
            "status": 200,
            "message": "You successfully signed up for the API"
        })

class Classify(Resource):
    def post(self):
        # Get Posted Data
        postedData = request.get_json()
        # We get credentials and url from the posted data
        username = postedData["username"]
        password = postedData["password"]
        url = postedData["url"]        
        # verify credentials
        ret_json, error = verify_credentials(username, password)
        if error:
            return jsonify(ret_json)
        
        # check if user has enough tokens
        tokens = users.find_one({"Username": username})["Tokens"]
        if tokens <= 0:
            return jsonify(generate_return_dictionary(303, "You are out of tokens, please refill"))
        # classify the image
        if not url:
            return jsonify(({"error": "No url provided"}), 400)
        # Load the image from the url
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        # Pre process the image
        img = img.resize((299, 299))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        # Make prediction
        prediction = pretrained_model.predict(img_array)
        actual_prediction = imagenet_utils.decode_predictions(prediction,top=3)
        
        # return the classification
        ret_json = {}
        
        for pred in actual_prediction[0]:
            ret_json[pred[1]] = float(pred[2]*100)
        
            
        # update the user's tokens
        users.update_one({
            "Username": username
        }, {
            "$set": {
                "Tokens": tokens - 1
            }
        })
        return jsonify(ret_json)

class Refill(Resource):
    def post(self):
        # get the posted data
        postedData = request.get_json()
        # get credentials
        username = postedData["username"]
        password = postedData["admin_pw"]
        amount = postedData["amount"]
        # check if the user exists
        if not user_exists(username):
            return jsonify(generate_return_dictionary(301, "Invalid Username"))
        # check if the password is correct
        correct_pw = "abc123"
        if password != correct_pw:
            return jsonify(generate_return_dictionary(302, "Invalid Admin Password"))
        # update the user's tokens
        users.update_one({
            "Username": username
        }, {
            "$set": {
                "Tokens": tokens + amount
            }
        })
        return jsonify(generate_return_dictionary(200, "Tokens refilled successfully"))

class ClassifyImage(Resource):
    def post(self):
        # Get credentials from form data (since we're uploading files)
        username = request.form.get("username")
        password = request.form.get("password")  
        
        # verify credentials
        ret_json, error = verify_credentials(username, password)
        if error:
            return jsonify(ret_json)
        
        # check if user has enough tokens
        tokens = users.find_one({"Username": username})["Tokens"]
        if tokens <= 0:
            return jsonify(generate_return_dictionary(303, "You are out of tokens, please refill"))
        
        # Check if image file is provided
        if 'image' not in request.files:
            return jsonify(generate_return_dictionary(301, "No image file provided"))
        
        image_file = request.files['image']
        
        # Check if file is selected
        if image_file.filename == '':
            return jsonify(generate_return_dictionary(301, "No image file selected"))
        
        try:
            # Read the image file
            img = Image.open(image_file.stream)
            
            # Convert to RGB if necessary (handles RGBA, P mode images)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Pre process the image
            img = img.resize((299, 299))
            img_array = img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            
            # Make prediction
            prediction = pretrained_model.predict(img_array)
            actual_prediction = imagenet_utils.decode_predictions(prediction, top=3)
            
            # return the classification
            ret_json = {}
            
            for pred in actual_prediction[0]:
                ret_json[pred[1]] = float(pred[2]*100)
            
            # update the user's tokens
            users.update_one({
                "Username": username
            }, {
                "$set": {
                    "Tokens": tokens - 1
                }
            })
            
            return jsonify(ret_json)
            
        except Exception as e:
            return jsonify(generate_return_dictionary(301, f"Error processing image: {str(e)}"))

class GetAllUsers(Resource):
    def get(self):
        try:
            # Get all users from the database
            all_users = list(users.find({}, {"Username": 1, "Tokens": 1, "_id": 0}))
            
            # Format the response
            users_list = []
            for user in all_users:
                users_list.append({
                    "username": user["Username"],
                    "tokens": user["Tokens"]
                })
            
            return jsonify({
                "status": 200,
                "message": "Users retrieved successfully",
                "users": users_list,
                "total_users": len(users_list)
            })
            
        except Exception as e:
            return jsonify(generate_return_dictionary(301, f"Error retrieving users: {str(e)}"))


api.add_resource(Register, "/register")
api.add_resource(Classify, "/classify")
api.add_resource(ClassifyImage, "/classify-image")
api.add_resource(Refill, "/refill")
api.add_resource(GetAllUsers, "/users")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)