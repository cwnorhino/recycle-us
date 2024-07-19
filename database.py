import sqlite3

def create_tables():
    conn = sqlite3.connect('recycling.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY,
                  username TEXT UNIQUE NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  join_date TEXT NOT NULL,
                  total_recycled REAL DEFAULT 0,
                  current_streak INTEGER DEFAULT 0,
                  co2_saved REAL DEFAULT 0)''')
    
    # Create recycling centers table
    c.execute('''CREATE TABLE IF NOT EXISTS centers
                 (id INTEGER PRIMARY KEY,
                  name TEXT NOT NULL,
                  latitude REAL NOT NULL,
                  longitude REAL NOT NULL)''')
    
    # Create achievements table
    c.execute('''CREATE TABLE IF NOT EXISTS achievements
                 (id INTEGER PRIMARY KEY,
                  user_id INTEGER,
                  achievement TEXT NOT NULL,
                  date_achieved TEXT NOT NULL,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # Create recycling goals table
    c.execute('''CREATE TABLE IF NOT EXISTS goals
                 (id INTEGER PRIMARY KEY,
                  user_id INTEGER,
                  goal TEXT NOT NULL,
                  target_date TEXT NOT NULL,
                  completed BOOLEAN DEFAULT 0,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # Create recycling logs table
    c.execute('''CREATE TABLE IF NOT EXISTS recycling_logs
                 (id INTEGER PRIMARY KEY,
                  user_id INTEGER,
                  material TEXT NOT NULL,
                  weight REAL NOT NULL,
                  date TEXT NOT NULL,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()