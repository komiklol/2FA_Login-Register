import pyotp
import json
import os
from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
from qrClassQR import qrCodeQR

# Initialize the Flask application
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'secretTest'


# Function to initialize user data for the application
def initialize_user_data():
    user_data_file = 'user_data.json'
    if not os.path.exists(user_data_file):  # Check if the user data file does not exist
        default_user = [
            {
                "name": "test",  # Default username
                "password": bcrypt.generate_password_hash("123").decode('utf-8'),  # Hashed default password
                "secret": "test",  # Placeholder 2FA secret
                "twofa-status": False  # 2FA disabled by default
            }
        ]
        with open(user_data_file, 'w') as file:
            json.dump(default_user, file)  # Write the default user data to the file


initialize_user_data()  # Ensure user data is initialized when the app starts


# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')  # Serve the homepage template


# Route to handle user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle form submission for user registration
        name = request.form['username']
        password = request.form['password']
        twofa_code = request.form['twofa_code']
        secret = session['twofa_secret']

        # Verify the provided 2FA code
        totp = pyotp.TOTP(secret)
        if not totp.verify(twofa_code):
            return render_template('ErrorPage.html', ErrorLog="Invalid 2FA code - 401")

        # Prepare user data for storage
        user_data_file = 'user_data.json'
        user_data = {
            "name": name,
            "password": bcrypt.generate_password_hash(password).decode('utf-8'),  # Hash the password
            "secret": secret,
            "twofa-status": True
        }

        # Update session variables for the registered user
        session['user'] = name
        session['twofa_secret'] = secret
        session['twofa_status'] = True

        # Load existing user data and add the new user
        if os.path.exists(user_data_file):
            with open(user_data_file, 'r') as file:
                all_users = json.load(file)
        else:
            all_users = []

        all_users.append(user_data)

        # Save updated user data to the file
        with open(user_data_file, 'w') as file:
            json.dump(all_users, file)

        return redirect("/account")  # Redirect to the account page

    # Generate a QR code for the TOTP secret (GET request)
    secret = pyotp.random_base32()  # Generate a random base32 secret for 2FA
    uri = f"otpauth://totp/2FAApp?secret={secret}&issuer=Login&algorithm=SHA1&digits=6&period=30"
    img = qrCodeQR(uri).generate_qr()  # Generate the QR code
    session['twofa_secret'] = secret  # Store the secret in the session

    return render_template("register.html", qr_code_image=img)  # Render the registration form with the QR code


# Route to handle user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle form submission for user login
        name = request.form['username']
        password = request.form['password']

        user_data_file = 'user_data.json'
        if os.path.exists(user_data_file):
            # Load user data from the JSON file
            with open(user_data_file, 'r') as file:
                all_users = json.load(file)

            # Find user by username
            user_data = next((user for user in all_users if user['name'] == name), None)

            # Verify username and password
            if user_data and bcrypt.check_password_hash(user_data['password'], password):
                # Set session variables for the logged-in user
                session['user'] = name
                twofa_secret = user_data['secret']
                twofa_status = user_data['twofa-status']
                session['twofa_secret'] = twofa_secret
                session['twofa_status'] = twofa_status
                totp = pyotp.TOTP(twofa_secret)

                # Verify 2FA code if 2FA is enabled
                if twofa_status:
                    if totp.verify(request.form['twofa_code']):
                        return redirect("/account")  # Redirect to the account page
                    else:
                        return render_template('ErrorPage.html', ErrorLog="Wrong code! - 401")
                return redirect("/account")
            else:
                return render_template('ErrorPage.html', ErrorLog="Invalid username or password - 401")
        else:
            return render_template('ErrorPage.html', ErrorLog="User data file not found - 500")

    return render_template('login.html')  # Render the login form


# Route to log out the user
@app.route('/logout')
def logout():
    # Clear the session variables related to the user
    session.pop('user', None)
    session.pop('twofa_secret', None)
    session.pop('twofa_status', None)
    return redirect("/")  # Redirect to the homepage


# Route for the account page
@app.route('/account', methods=['GET', 'POST'])
def account():
    secret = session['twofa_secret']
    uri = f"otpauth://totp/2FAApp?secret={secret}&issuer=Login&algorithm=SHA1&digits=6&period=30"
    img = qrCodeQR(uri).generate_qr()  # Generate the QR code
    return render_template('account.html', twoFA_STATUS=session['twofa_status'], qr_code_image=img)  # Render the account page


# Route to toggle 2FA status
@app.route('/change2fa', methods=['GET', 'POST'])
def change2fa():
    if request.method == 'GET':
        # Ensure the user is logged in
        if 'user' in session:
            name = session['user']
            user_data_file = 'user_data.json'
            if os.path.exists(user_data_file):
                # Load user data from the file
                with open(user_data_file, 'r') as file:
                    all_users = json.load(file)

                # Find user by username
                user_data = next((user for user in all_users if user['name'] == name), None)

                if user_data and user_data['name'] == name:
                    # Toggle the 2FA status
                    user_data['twofa-status'] = not user_data['twofa-status']
                    session['twofa_status'] = user_data['twofa-status']

                    # Update the specific user's data in the JSON file
                    for user in all_users:
                        if user['name'] == name:
                            user['twofa-status'] = user_data['twofa-status']
                            break

                    # Save the updated user data to the file
                    with open(user_data_file, 'w') as file:
                        json.dump(all_users, file)

                    return redirect("/account")
                else:
                    return render_template('ErrorPage.html', ErrorLog="Unauthorized access - 403")
            else:
                return render_template('ErrorPage.html', ErrorLog="User data file not found - 500")
        else:
            return render_template('ErrorPage.html', ErrorLog="User not logged in - 401")
    return redirect("/account")  # Redirect to the account page
