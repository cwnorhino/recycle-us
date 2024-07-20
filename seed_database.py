import sqlite3
from datetime import datetime, timedelta
import random

def seed_database():
    conn = sqlite3.connect('recycling.db')
    c = conn.cursor()

    # Sample users
    users = [
        ('user1', 'user1@example.com', '2024-07-01'),
        ('user2', 'user2@example.com', '2024-07-05'),
        ('user3', 'user3@example.com', '2024-07-10'),
    ]

    c.executemany('INSERT OR IGNORE INTO users (username, email, join_date) VALUES (?, ?, ?)', users)

    # Sample recycling centers
    centers = [
        ('Green Recycling Center', 40.7128, -74.0060),
        ('EcoFriendly Recycling', 34.0522, -118.2437),
        ('Sustainable Solutions', 41.8781, -87.6298),
    ]

    c.executemany('INSERT OR IGNORE INTO centers (name, latitude, longitude) VALUES (?, ?, ?)', centers)

    # Sample achievements
    achievements = [
        (1, 'Recycling Rookie', '2024-07-15'),
        (2, 'Paper Saver', '2024-07-18'),
        (3, 'Water Bottle Warrior', '2024-07-20'),
    ]

    c.executemany('INSERT OR IGNORE INTO achievements (user_id, achievement, date_achieved) VALUES (?, ?, ?)', achievements)

    # Sample goals
    goals = [
        (1, 'Recycle 10 kg this week', '2024-07-27', 0),
        (2, 'Use a reusable water bottle for 30 days', '2024-08-20', 0),
        (3, 'Compost food waste for a month', '2024-08-31', 0),
    ]

    c.executemany('INSERT OR IGNORE INTO goals (user_id, goal, target_date, completed) VALUES (?, ?, ?, ?)', goals)

    # Sample recycling logs
    start_date = datetime(2024, 7, 1)
    end_date = datetime(2024, 7, 20)
    materials = ['Paper', 'Plastic', 'Glass', 'Metal']

    recycling_logs = []
    for user_id in range(1, 4):  # For each user
        current_date = start_date
        while current_date <= end_date:
            if random.random() < 0.7:  # 70% chance of recycling each day
                material = random.choice(materials)
                weight = round(random.uniform(0.5, 5.0), 2)
                recycling_logs.append((user_id, material, weight, current_date.strftime('%Y-%m-%d')))
            current_date += timedelta(days=1)

    c.executemany('INSERT OR IGNORE INTO recycling_logs (user_id, material, weight, date) VALUES (?, ?, ?, ?)', recycling_logs)

    # Update user stats
    for user_id in range(1, 4):
        total_recycled = c.execute('SELECT SUM(weight) FROM recycling_logs WHERE user_id = ?', (user_id,)).fetchone()[0]
        if total_recycled is None:
            total_recycled = 0
        streak = c.execute('''
            SELECT COUNT(*) FROM (
                SELECT DISTINCT date FROM recycling_logs 
                WHERE user_id = ? 
                ORDER BY date DESC 
                LIMIT 30
            )
        ''', (user_id,)).fetchone()[0]
        co2_saved = total_recycled * 2.5  # Simplified calculation

        c.execute('UPDATE users SET total_recycled = ?, current_streak = ?, co2_saved = ? WHERE id = ?',
                  (total_recycled, streak, co2_saved, user_id))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    seed_database()
    print("Database seeded successfully!")