from flask import Blueprint, jsonify, session
from database.db import (
    db_get_notifications_by_user,
    db_mark_notification_as_read,
    db_mark_all_notifications_as_read
)
from models.notification import Notification

# Create the notifications Blueprint
notifications_bp = Blueprint("notifications", __name__)

@notifications_bp.route("/api/notifications", methods=["GET"])
def list_notifications():
    """
    Returns a list of all notifications for the authenticated user.
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "Unauthorized. No active session."
        }), 401

    try:
        raw_notifications = db_get_notifications_by_user(user_id)
        serialized_notifications = []
        
        for row in raw_notifications:
            notification = Notification.from_dict(row)
            if notification:
                serialized_notifications.append(notification.to_dict())

        return jsonify({
            "status": "success",
            "count": len(serialized_notifications),
            "notifications": serialized_notifications
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to retrieve notifications: {str(e)}"
        }), 500

@notifications_bp.route("/api/notifications/<int:notification_id>/read", methods=["PUT"])
def mark_as_read(notification_id):
    """
    Marks a single notification as read after confirming user ownership.
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "Unauthorized. No active session."
        }), 401

    try:
        # Update read status in database directly using notification_id and user_id
        affected_rows = db_mark_notification_as_read(notification_id, user_id)
        if affected_rows == 0:
            return jsonify({
                "status": "error",
                "message": "Notification not found or access denied."
            }), 404

        return jsonify({
            "status": "success",
            "message": "Notification marked as read."
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to mark notification as read: {str(e)}"
        }), 500

@notifications_bp.route("/api/notifications/read-all", methods=["PUT"])
def mark_all_read():
    """
    Marks all notifications for the authenticated user as read.
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "Unauthorized. No active session."
        }), 401

    try:
        db_mark_all_notifications_as_read(user_id)
        return jsonify({
            "status": "success",
            "message": "All notifications marked as read."
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to mark all notifications as read: {str(e)}"
        }), 500
