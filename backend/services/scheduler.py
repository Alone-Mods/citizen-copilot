import time
import threading
from datetime import datetime, timedelta
from database.db import db_get_all_schemes, get_connection
from services.notification_service import send_user_notification

def check_upcoming_deadlines():
    """
    Scans schemes in SQLite database for upcoming application deadlines (within 30 days)
    and dispatches reminder notifications to registered citizens.
    """
    try:
        schemes = db_get_all_schemes()
        now = datetime.now()
        thirty_days_later = now + timedelta(days=30)

        # Get list of registered user IDs
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users;")
        user_ids = [row["user_id"] for row in cursor.fetchall()]
        conn.close()

        if not user_ids:
            return

        for scheme in schemes:
            deadline_str = scheme.get("deadline")
            if not deadline_str:
                continue

            try:
                # Parse deadline date string (YYYY-MM-DD)
                deadline_dt = datetime.strptime(deadline_str, "%Y-%m-%d")
                
                # Check if deadline falls within the next 30 days
                if now <= deadline_dt <= thirty_days_later:
                    title = f"Deadline Alert: {scheme.get('title')}"
                    message = f"The application deadline for {scheme.get('title')} is approaching ({deadline_str}). Check your eligibility today!"
                    
                    for uid in user_ids:
                        try:
                            send_user_notification(uid, title, message, notification_type="Warning")
                        except Exception as ne:
                            print(f"Warning: Failed to dispatch deadline notification to user {uid}: {str(ne)}")

            except ValueError:
                # Ignore non-standard date string formats
                continue

    except Exception as e:
        print(f"Error in scheduler check_upcoming_deadlines: {str(e)}")

def _scheduler_loop(interval_seconds):
    """
    Internal daemon loop that periodically triggers deadline checks.
    """
    while True:
        check_upcoming_deadlines()
        time.sleep(interval_seconds)

def start_scheduler(interval_seconds=3600):
    """
    Launches the background daemon thread for periodic deadline monitoring.
    
    Args:
        interval_seconds (int): Polling interval in seconds (default: 3600 / 1 hour).
    """
    thread = threading.Thread(target=_scheduler_loop, args=(interval_seconds,), daemon=True)
    thread.start()
    print(f"Background task scheduler initiated (interval: {interval_seconds}s).")
    return thread
