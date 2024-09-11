from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from firebase_config import sign_up, sign_in, get_account_info
import sqlite3
import secrets
from flask_cors import CORS
from datetime import datetime
import googlemaps
from datetime import datetime
import os
from dotenv import load_dotenv, dotenv_values 
from scheduled_tasks import start_scheduler

# env
load_dotenv() 

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_API_KEY")
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

app = Flask(__name__)
CORS(app)
app.secret_key = secrets.token_hex(16)

def get_db_connection():
    conn = sqlite3.connect('recycling.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    user = None
    if 'user' in session:
        user = session['user']
    return render_template('home.html', user=user)

@app.route('/guides')
def guides():
    return render_template('guides.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/get_recycling_centers')
def get_recycling_centers():
    latitude = float(request.args.get('lat'))
    longitude = float(request.args.get('lng'))
    
    conn = get_db_connection()
    centers = conn.execute('''
        SELECT * FROM recycling_centers 
        WHERE (latitude BETWEEN ? AND ?) 
        AND (longitude BETWEEN ? AND ?)
    ''', (latitude - 0.1, latitude + 0.1, longitude - 0.1, longitude + 0.1)).fetchall()
    conn.close()

    if not centers:
        print("No centers found in database, fetching from Google Maps API")
        centers = fetch_recycling_centers(latitude, longitude)
        store_recycling_centers(centers)
    else:
        print(f"Found {len(centers)} centers in database")

    centers_list = [dict(center) for center in centers]
    return jsonify(centers_list)

def fetch_recycling_centers(latitude, longitude, radius=5000):
    print(f"Fetching recycling centers from Google Maps API for lat:{latitude}, lng:{longitude}")
    places_result = gmaps.places_nearby(
        location=(latitude, longitude),
        radius=radius,
        keyword='recycling center'
    )

    centers = []
    for place in places_result['results']:
        center = {
            'name': place['name'],
            'latitude': place['geometry']['location']['lat'],
            'longitude': place['geometry']['location']['lng']
        }
        centers.append(center)

    return centers

def store_recycling_centers(centers):
    conn = get_db_connection()
    for center in centers:
        conn.execute('''INSERT OR REPLACE INTO recycling_centers 
                        (name, latitude, longitude) 
                        VALUES (?, ?, ?)''',
                     (center['name'], center['latitude'], center['longitude']))
    conn.commit()
    conn.close()
    print(f"Stored {len(centers)} centers in database")
    

@app.route('/userauthentication')
def userauthentication():
    return render_template('userauthentication.html')

def initialize_achievements(user_id):
    conn = get_db_connection()
    achievements = [
        ("🌱 Recycling Rookie", "Recycle 10kg of waste", 10),
        ("♻️ Paper Saver", "Recycle 20kg of paper", 20),
        ("💧 Water Bottle Warrior", "Recycle 15kg of water bottles", 15)
    ]
    for achievement, description, required_amount in achievements:
        conn.execute('''INSERT INTO achievements 
                        (user_id, achievement, description, required_amount, completed) 
                        VALUES (?, ?, ?, ?, 0)''',
                     (user_id, achievement, description, required_amount))
    conn.commit()
    conn.close()

@app.route('/signup', methods=['POST'])
def signup():
    email = request.json['email']
    password = request.json['password']
    
    conn = get_db_connection()
    existing_user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    
    if existing_user:
        conn.close()
        return jsonify({"success": False, "message": "An account with this email already exists"}), 400
    
    try:
        user = sign_up(email, password)
        if user:
            cursor = conn.execute('INSERT INTO users (username, email, join_date) VALUES (?, ?, ?)',
                         (email.split('@')[0], email, datetime.now().strftime("%Y-%m-%d")))
            user_id = cursor.lastrowid
            conn.commit()
            initialize_achievements(user_id)
            conn.close()
            return jsonify({"success": True}), 200
        else:
            conn.close()
            return jsonify({"success": False, "message": "Firebase signup failed"}), 400
    except Exception as e:
        conn.close()
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
        return redirect(url_for('userauthentication'))
    
    user_email = session['user']['email']
    
    conn = get_db_connection()
    user_data = conn.execute('SELECT * FROM users WHERE email = ?', (user_email,)).fetchone()
    
    if user_data:
        user_id = user_data['id']
        # Fetch achievements
        completed_achievements = conn.execute('SELECT * FROM achievements WHERE user_id = ? AND completed = 1', (user_id,)).fetchall()
        incomplete_achievements = conn.execute('SELECT * FROM achievements WHERE user_id = ? AND completed = 0', (user_id,)).fetchall()
        # Fetch goals (challenges)
        goals = conn.execute('SELECT * FROM goals WHERE user_id = ?', (user_id,)).fetchall()
        
        # Fetch the current streak
        current_streak = user_data['current_streak']
        
        conn.close()
        return render_template('profile.html', user=user_data, completed_achievements=completed_achievements, 
                               incomplete_achievements=incomplete_achievements, goals=goals, current_streak=current_streak)
    else:
        conn.close()
        return redirect(url_for('home'))

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

@app.route('/recycling_log')
def recycling_log():
    if 'user' not in session:
        return redirect(url_for('userauthentication'))
    
    user_email = session['user']['email']
    
    conn = get_db_connection()
    try:
        user = conn.execute('SELECT id FROM users WHERE email = ?', (user_email,)).fetchone()
        if not user:
            return redirect(url_for('home'))
        
        user_id = user['id']
        
        # Fetch user's recycling logs
        logs = conn.execute('''
            SELECT material, weight, date 
            FROM recycling_logs 
            WHERE user_id = ? 
            ORDER BY date DESC
            LIMIT 10
        ''', (user_id,)).fetchall()
        
        return render_template('recycling_log.html', logs=logs)
    finally:
        conn.close()

@app.route('/log_recycling', methods=['POST'])
def log_recycling():
    if 'user' not in session:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    
    data = request.json
    user_email = session['user']['email']
    
    conn = get_db_connection()
    try:
        # Get user_id
        user = conn.execute('SELECT id FROM users WHERE email = ?', (user_email,)).fetchone()
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        user_id = user['id']
        
        # Insert recycling log
        conn.execute('INSERT INTO recycling_logs (user_id, material, weight, date) VALUES (?, ?, ?, ?)',
                     (user_id, data['material'], data['weight'], datetime.now().strftime("%Y-%m-%d")))
        
        # Update user stats
        total_recycled = conn.execute('SELECT SUM(weight) FROM recycling_logs WHERE user_id = ?', (user_id,)).fetchone()[0]
        co2_saved = total_recycled * 0.700
        
        conn.execute('UPDATE users SET total_recycled = ?, co2_saved = ? WHERE id = ?',
                     (total_recycled, co2_saved, user_id))
        
        # Check achievements
        check_achievements(conn, user_id, data['material'], data['weight'])
        
        conn.commit()
        return jsonify({"success": True, "message": "Recycling logged successfully"}), 200
    except Exception as e:
        print(f"Error logging recycling: {str(e)}")
        return jsonify({"success": False, "message": "Failed to log recycling"}), 400
    finally:
        conn.close()

def check_achievements(conn, user_id, material, weight):
    achievements = conn.execute('SELECT * FROM achievements WHERE user_id = ? AND completed = 0', (user_id,)).fetchall()
    
    for achievement in achievements:
        if achievement['achievement'] == "🌱 Recycling Rookie":
            total_recycled = conn.execute('SELECT SUM(weight) FROM recycling_logs WHERE user_id = ?', (user_id,)).fetchone()[0] or 0
            if total_recycled >= achievement['required_amount']:
                conn.execute('UPDATE achievements SET completed = 1, date_achieved = ? WHERE id = ?',
                             (datetime.now().strftime("%Y-%m-%d"), achievement['id']))
        
        elif achievement['achievement'] == "♻️ Paper Saver" and material.lower() == "paper":
            total_paper = conn.execute('SELECT SUM(weight) FROM recycling_logs WHERE user_id = ? AND material LIKE ?',
                                       (user_id, '%paper%')).fetchone()[0] or 0
            if total_paper >= achievement['required_amount']:
                conn.execute('UPDATE achievements SET completed = 1, date_achieved = ? WHERE id = ?',
                             (datetime.now().strftime("%Y-%m-%d"), achievement['id']))
        
        elif achievement['achievement'] == "💧 Water Bottle Warrior" and material.lower() == "plastic":
            total_bottles = conn.execute('SELECT SUM(weight) FROM recycling_logs WHERE user_id = ? AND material LIKE ?',
                                         (user_id, '%bottle%')).fetchone()[0] or 0
            if total_bottles >= achievement['required_amount']:
                conn.execute('UPDATE achievements SET completed = 1, date_achieved = ? WHERE id = ?',
                             (datetime.now().strftime("%Y-%m-%d"), achievement['id']))
                
if __name__ == '__main__':
    start_scheduler()
    app.run(debug=True)