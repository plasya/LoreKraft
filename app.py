from flask import Flask, render_template, request, redirect, url_for, flash, session
from collections import deque
import random
import string
from libs.MapStruct import Map, generate_random_numbers

def create_new_map(d, start, end):
    n_common, n_triggers, n_friendly, n_delayed, delayed_numbers = generate_random_numbers(len(d))
    return Map(d, start, end, n_common, n_triggers, n_friendly, n_delayed, delayed_numbers)

app = Flask(__name__)
app.secret_key = 'I_am_upto_no_good'  # Required for session management and flashing messages

# Dummy user data (in real cases, this should come from a database)
users = {
    "testuser": "password123"
}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if the username exists and the password is correct
    if username in users and users[username] == password:
        session['username'] = username  # Save the username in the session
        flash('Login successful!', 'success')
        return redirect(url_for('welcome'))  # Redirect to welcome page
    else:
        flash('Invalid username or password. Please try again.', 'error')
        return redirect(url_for('home'))

@app.route('/welcome')
def welcome():
    if 'username' in session:
        username = session['username']
        return render_template('welcome.html', username=username)
    else:
        flash('You are not logged in!', 'error')
        return redirect(url_for('home'))
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
