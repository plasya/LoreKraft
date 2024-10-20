from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from collections import deque
import random
import string
from libs.MapStruct import Map, generate_random_numbers
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson import json_util, ObjectId
import numpy as np 
from image_gen import image_gen 
# Configure MongoDB connection (example with MongoDB Atlas)
# Initialize PyMongo

# def create_new_map(d, start, end):
#     n_common, n_triggers, n_friendly, n_delayed, delayed_numbers = generate_random_numbers(len(d))
#     return Map(d, start, end, n_common, n_triggers, n_friendly, n_delayed, delayed_numbers)

guilds = {}



app = Flask(__name__)
app.secret_key = 'I_am_upto_no_good'  # Required for session management and flashing messages
app.config["MONGO_URI"] = "mongodb+srv://joy:lol.java@website.fn5zw.mongodb.net/Hackathon?retryWrites=true&w=majority"
CORS(app)
mongo = PyMongo(app)

users = {
    "testuser": "password123",
    "surya": 'qwerty123',
    "lasya":'lol',
    "joy": '1121'
}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/test')
def sometest():
    try:
        # Hardcoded MongoDB query similar to SQL:
        # SELECT * FROM collection_name WHERE image_id IS NOT NULL
        query = { }

        # Query MongoDB (assuming 'collection_name' is the name of your collection)
        documents = mongo.db.characters.find(query)
        # Convert MongoDB cursor to list and then to JSON format
        data = eval(json_util.dumps(documents))
        data = [i for i in data if i["image_ids"]]

        return jsonify({"status": "success", "data": data}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if the username exists and the password is correct
    if username in users and users[username] == password:
        session['username'] = username  # Save the username in the session
        flash('Login successful!', 'success')
        return render_template('guild.html') #redirect(url_for('guild_create_join'))  # Redirect to welcome page
    else:
        flash('Invalid username or password. Please try again.', 'error')
        return redirect(url_for('home'))


@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/guild_create_joinpage', methods=['POST'])
def guild_create_joi():
    data = request.get_json()
    gcode = data['guildCode']
    task = data['task']
    if task == 'join':
        if gcode not in guilds:
            return jsonify({'success':0})
        session['guildcode'] = gcode  
    if task == 'create':  
        if gcode not in guilds:
            guilds[gcode] = 1
            session['guildcode'] = gcode  
        else:
            return jsonify({'success':0})
    return jsonify({'success':1}) #redirect(url_for('game'))

@app.route('/imagen', methods = ['POST'])
def imag_gen():
    data = request.get_json()
    p = data["prompt"]
    str1 = imag_gen(p)
    return str1

@app.route('/narato')
def ttpts():
    
    return jsonify({'data': "lasya is cutie pie"})

@app.route('/create_new_map', methods=['POST'])
def create_new_map():
    try:
        # Get JSON data from the POST request
        data = request.get_json()

        # Extract 'd', 'start', and 'end' from the JSON data
        d = data.get('d')
        start = data.get('start')
        end = data.get('end')

        if d is None or start is None or end is None:
            return jsonify({'error': 'Missing data in request'}), 400

        # Generate random numbers and create the map
        n_common, n_triggers, n_friendly, n_delayed, delayed_numbers = generate_random_numbers(len(d))
        new_map = Map(d, start, end, n_common, n_triggers, n_friendly, n_delayed, delayed_numbers)

        # Return a success response (customize the response data as needed)
        return jsonify({'message': 'Map created successfully', 'map': str(new_map)}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from the session
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
