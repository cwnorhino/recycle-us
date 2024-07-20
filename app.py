from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from firebase_config import sign_up, sign_in, get_account_info
import sqlite3
import secrets
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.secret_key = secrets.token_hex(16)

def get_db_connection():
    conn = sqlite3.connect('recycling.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/guides')
def guides():
    return render_template('guides.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/userauthentication')
def userauthentication():
    return render_template('userauthentication.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.json['email']
    password = request.json['password']
    try:
        user = sign_up(email, password)
        if user:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (username, email, join_date) VALUES (?, ?, ?)',
                         (email.split('@')[0], email, datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            conn.close()
            return jsonify({"success": True}), 200
        else:
            print("Firebase signup failed")
            return jsonify({"success": False, "message": "Firebase signup failed"}), 400
    except Exception as e:
        print(f"Signup error: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 400
    
@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    try:
        user = sign_in(email, password)
        if user:
            session['user'] = {
                'email': email,
                'idToken': user['idToken']
            }
            print(f"User logged in: {email}")
            return jsonify({"success": True}), 200
        else:
            return jsonify({"success": False, "message": "Invalid credentials"}), 401
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 401
    
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    if 'user' not in session:
        print("User not in session, redirecting to signup")
        return redirect(url_for('getStarted'))
    
    user_email = session['user']['email']
    print(f"Fetching profile for user: {user_email}")
    
    conn = get_db_connection()
    user_data = conn.execute('SELECT * FROM users WHERE email = ?', (user_email,)).fetchone()
    conn.close()
    
    if user_data:
        print(f"User data found for: {user_email}")
        return render_template('profile.html', user=user_data)
    else:
        print(f"No user data found for: {user_email}")
        return redirect(url_for('home'))

@app.route('/get_recycling_centers')
def get_recycling_centers():
    conn = get_db_connection()
    centers = conn.execute('SELECT * FROM centers').fetchall()
    conn.close()
    return jsonify([dict(center) for center in centers])

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (username, email, join_date) VALUES (?, ?, ?)',
                     (data['username'], data['email'], datetime.now().strftime("%Y-%m-%d")))
        conn.commit()
        return jsonify({"success": True}), 200
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "Username or email already exists"}), 400
    finally:
        conn.close()

@app.route('/log_recycling', methods=['POST'])
def log_recycling():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    
    data = request.json
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO recycling_logs (user_id, material, weight, date) VALUES (?, ?, ?, ?)',
                     (session['user_id'], data['material'], data['weight'], datetime.now().strftime("%Y-%m-%d")))
        conn.commit()
        return jsonify({"success": True}), 200
    except:
        return jsonify({"success": False, "message": "Failed to log recycling"}), 400
    finally:
        conn.close()

def check_achievements(user_id):
    conn = get_db_connection()
    total_recycled = conn.execute('SELECT SUM(weight) FROM recycling_logs WHERE user_id = ?', (user_id,)).fetchone()[0]
    if total_recycled >= 100 and not conn.execute('SELECT * FROM achievements WHERE user_id = ? AND achievement = ?', (user_id, "100kg Recycled")).fetchone():
        conn.execute('INSERT INTO achievements (user_id, achievement, date_achieved) VALUES (?, ?, ?)',
                     (user_id, "100kg Recycled", datetime.now().strftime("%Y-%m-%d")))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)