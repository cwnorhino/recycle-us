import sqlite3

def create_tables():
    conn = sqlite3.connect('recycling.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, email TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS guides
                 (id INTEGER PRIMARY KEY, material TEXT, instructions TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS centers
                 (id INTEGER PRIMARY KEY, name TEXT, latitude REAL, longitude REAL)''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()