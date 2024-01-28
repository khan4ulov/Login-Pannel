from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

# Dictionary to store user credentials (username: {password: hashed_password})
user_credentials = {}

# File path for the user profiles CSV file
USER_PROFILES_FILE = 'user_profiles.csv'

# Create user_profiles.csv if it doesn't exist
def create_user_profiles_file():
    if not os.path.exists(USER_PROFILES_FILE):
        with open(USER_PROFILES_FILE, mode='w', newline='') as file:
            fieldnames = ['username', 'password', 'first_name', 'last_name', 'mobile_no', 'email']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

# Load user profiles from the CSV file into the user_credentials dictionary
def load_user_profiles():
    if os.path.exists(USER_PROFILES_FILE):
        with open(USER_PROFILES_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_credentials[row['username']] = {
                    'password': row['password'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'mobile_no': row['mobile_no'],
                    'email': row['email']
                }

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if the username exists and the password is correct
    if username in user_credentials and user_credentials[username]['password'] == password:
        return redirect(url_for('welcome'))
    else:
        return render_template('login.html', error='Invalid credentials. Please try again.')

@app.route('/create_profile')
def create_profile():
    return render_template('create_profile.html')

@app.route('/save_profile', methods=['POST'])
def save_profile():
    username = request.form['username']
    password = request.form['password']
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    mobile_no = request.form['mobileNo']
    email = request.form['email']

    # Check if the username already exists
    if username in user_credentials:
        return render_template('create_profile.html', error='Username already exists. Please choose a different one.')

    # Check password requirements
    if not (len(password) >= 8 and any(c.isupper() for c in password) and any(c.islower() for c in password) and any(c.isdigit() for c in password)):
        return render_template('create_profile.html', error='Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, and one digit.')

    # Store the new user's credentials (for demonstration purposes; in a real app, you would hash the password)
    user_credentials[username] = {'password': password, 'first_name': first_name, 'last_name': last_name, 'mobile_no': mobile_no, 'email': email}

    # Save the profile information to a CSV file
    with open(USER_PROFILES_FILE, mode='a', newline='') as file:
        fieldnames = ['username', 'password', 'first_name', 'last_name', 'mobile_no', 'email']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Check if the file is empty and write the header if needed
        if file.tell() == 0:
            writer.writeheader()

        # Write the user's profile information to the file
        writer.writerow({'username': username, 'password': password, 'first_name': first_name, 'last_name': last_name, 'mobile_no': mobile_no, 'email': email})

    # Redirect to the login page after successful profile creation
    return redirect(url_for('home'))

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    # Process subscription here (you can update user profile or store subscription info)
    return render_template('subscribe_success.html')

if __name__ == '__main__':
    create_user_profiles_file()  # Create user_profiles.csv if it doesn't exist
    load_user_profiles()  # Load user profiles from the CSV file
    app.run(debug=True)