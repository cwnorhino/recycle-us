from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('recycling.db')
    conn.row_factory = sqlite3.Row
    return conn

def update_user_streaks():
    print("Updating user streaks...")
    conn = get_db_connection()
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Get all users
    users = conn.execute('SELECT id FROM users').fetchall()
    
    for user in users:
        user_id = user['id']
        
        # Check if the user recycled yesterday
        recycled_yesterday = conn.execute('SELECT COUNT(*) FROM recycling_logs WHERE user_id = ? AND date = ?', 
                                          (user_id, yesterday)).fetchone()[0]
        
        if recycled_yesterday > 0:
            # User recycled yesterday, increase streak
            conn.execute('UPDATE users SET current_streak = current_streak + 1 WHERE id = ?', (user_id,))
        else:
            # User didn't recycle yesterday, reset streak to 0
            conn.execute('UPDATE users SET current_streak = 0 WHERE id = ?', (user_id,))
    
    conn.commit()
    conn.close()
    print("User streaks updated successfully.")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_user_streaks, CronTrigger(hour=0, minute=0))  # Run daily at midnight
    scheduler.start()