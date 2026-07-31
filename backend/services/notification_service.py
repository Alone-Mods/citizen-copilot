from database.db import (
    db_create_notification,
    db_get_notifications_by_user,
    db_mark_notification_as_read,
    db_mark_all_notifications_as_read
)
from models.notification import Notification

def send_user_notification(user_id, title, message, notification_type="Info"):
    """
    Dispatches a new notification to a specific user and records it in SQLite.
    
    Args:
        user_id (int): Target user ID.
        title (str): Notification title.
        message (str): Body text of the notification.
        notification_type (str): Notification category ('Info', 'Success', 'Warning').
        
    Returns:
        int: Newly created notification_id.
    """
    return db_create_notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type=notification_type
    )

def get_user_notifications(user_id):
    """
    Retrieves all notification records for a user, mapped to serialized dictionaries.
    
    Args:
        user_id (int): Target user ID.
        
    Returns:
        list: List of notification dictionaries.
    """
    raw_notifications = db_get_notifications_by_user(user_id)
    serialized = []
    
    for row in raw_notifications:
        notif = Notification.from_dict(row)
        if notif:
            serialized.append(notif.to_dict())

    return serialized

def mark_notification_read(notification_id, user_id):
    """
    Marks a single notification as read after confirming user ownership.
    
    Args:
        notification_id (int): Target notification ID.
        user_id (int): Requesting user ID.
        
    Returns:
        bool: True if notification was found and updated, False otherwise.
    """
    affected_rows = db_mark_notification_as_read(notification_id, user_id)
    return affected_rows > 0

def mark_all_notifications_read(user_id):
    """
    Marks all notifications belonging to a user as read.
    
    Args:
        user_id (int): Target user ID.
        
    Returns:
        int: Number of affected records.
    """
    return db_mark_all_notifications_as_read(user_id)
