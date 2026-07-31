import os
import sys
import sqlite3

# Ensure the parent directory is in Python's search path for Config import
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from config import Config

def get_connection():
    """
    Establishes and returns a connection to the SQLite database
    using the configured absolute database path, enabling foreign keys
    and configuring Row factory for dictionary-like access.
    """
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    # Explicitly enable foreign key support for SQLite
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# =====================================================================
# GENERIC QUERY EXECUTION HELPERS
# =====================================================================

def execute_write(query, params=()):
    """
    Executes a write query (INSERT, UPDATE, DELETE) and returns the lastrowid.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        last_id = cursor.lastrowid
        return last_id
    finally:
        conn.close()

def execute_read_all(query, params=()):
    """
    Executes a read query and returns all rows as a list of dictionaries.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def execute_read_one(query, params=()):
    """
    Executes a read query and returns a single row as a dictionary, or None.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

# =====================================================================
# USERS TABLE OPERATIONS
# =====================================================================

def db_create_user(full_name, email, password_hash, phone_number, age, gender,
                   state, district, education, occupation, annual_family_income,
                   category, is_disabled):
    """
    Inserts a new user record into the users table. Returns the newly created user_id.
    """
    query = """
        INSERT INTO users (
            full_name, email, password_hash, phone_number, age, gender,
            state, district, education, occupation, annual_family_income,
            category, is_disabled
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    params = (full_name, email, password_hash, phone_number, age, gender,
              state, district, education, occupation, annual_family_income,
              category, is_disabled)
    return execute_write(query, params)

def db_get_user_by_id(user_id):
    """
    Retrieves a user record by user_id. Returns a dictionary or None.
    """
    query = "SELECT * FROM users WHERE user_id = ?;"
    return execute_read_one(query, (user_id,))

def db_get_user_by_email(email):
    """
    Retrieves a user record by email. Returns a dictionary or None.
    """
    query = "SELECT * FROM users WHERE email = ?;"
    return execute_read_one(query, (email,))

def db_update_user(user_id, full_name, phone_number, age, gender, state,
                   district, education, occupation, annual_family_income,
                   category, is_disabled):
    """
    Updates an existing user record. Returns the number of affected rows.
    """
    query = """
        UPDATE users
        SET full_name = ?, phone_number = ?, age = ?, gender = ?,
            state = ?, district = ?, education = ?, occupation = ?,
            annual_family_income = ?, category = ?, is_disabled = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?;
    """
    params = (full_name, phone_number, age, gender, state, district,
              education, occupation, annual_family_income, category,
              is_disabled, user_id)
    # execute_write returns lastrowid, but we run raw connection execute to check rowcount
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()

# =====================================================================
# SCHEMES TABLE OPERATIONS
# =====================================================================

def db_create_scheme(title, description, category, eligibility_criteria,
                     benefits, deadline, required_documents, application_url, department):
    """
    Inserts a new scheme record. Returns the newly created scheme_id.
    """
    query = """
        INSERT INTO schemes (
            title, description, category, eligibility_criteria,
            benefits, deadline, required_documents, application_url, department
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    params = (title, description, category, eligibility_criteria,
              benefits, deadline, required_documents, application_url, department)
    return execute_write(query, params)

def db_get_scheme_by_id(scheme_id):
    """
    Retrieves a scheme record by scheme_id. Returns a dictionary or None.
    """
    query = "SELECT * FROM schemes WHERE scheme_id = ?;"
    return execute_read_one(query, (scheme_id,))

def db_get_all_schemes():
    """
    Retrieves all schemes ordered by creation date. Returns a list of dictionaries.
    """
    query = "SELECT * FROM schemes ORDER BY created_at DESC;"
    return execute_read_all(query)

def db_search_schemes(search_query, category=None):
    """
    Searches for schemes matching a keyword in title/description, optionally filtered by category.
    """
    if category:
        query = """
            SELECT * FROM schemes
            WHERE (title LIKE ? OR description LIKE ?) AND category = ?
            ORDER BY created_at DESC;
        """
        params = (f"%{search_query}%", f"%{search_query}%", category)
    else:
        query = """
            SELECT * FROM schemes
            WHERE title LIKE ? OR description LIKE ?
            ORDER BY created_at DESC;
        """
        params = (f"%{search_query}%", f"%{search_query}%")
    return execute_read_all(query, params)

# =====================================================================
# DOCUMENTS TABLE OPERATIONS
# =====================================================================

def db_create_document(user_id, document_type, original_filename, stored_file_path):
    """
    Inserts an uploaded document metadata record. Returns the newly created document_id.
    """
    query = """
        INSERT INTO documents (
            user_id, document_type, original_filename, stored_file_path, verification_status
        ) VALUES (?, ?, ?, ?, 'Pending');
    """
    params = (user_id, document_type, original_filename, stored_file_path)
    return execute_write(query, params)

def db_get_document_by_id(document_id):
    """
    Retrieves a document record by its ID. Returns a dictionary or None.
    """
    query = "SELECT * FROM documents WHERE document_id = ?;"
    return execute_read_one(query, (document_id,))

def db_get_documents_by_user(user_id):
    """
    Retrieves all document metadata records uploaded by a user.
    """
    query = "SELECT * FROM documents WHERE user_id = ? ORDER BY upload_timestamp DESC;"
    return execute_read_all(query, (user_id,))

def db_delete_document(document_id, user_id):
    """
    Deletes a document record belonging to a specific user. Returns number of affected rows.
    """
    query = "DELETE FROM documents WHERE document_id = ? AND user_id = ?;"
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, (document_id, user_id))
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()

def db_update_document_status(document_id, verification_status):
    """
    Updates the verification status of a document. Returns number of affected rows.
    """
    query = "UPDATE documents SET verification_status = ? WHERE document_id = ?;"
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, (verification_status, document_id))
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()

# =====================================================================
# NOTIFICATIONS TABLE OPERATIONS
# =====================================================================

def db_create_notification(user_id, title, message, notification_type):
    """
    Inserts a new notification record. Returns the newly created notification_id.
    """
    query = """
        INSERT INTO notifications (
            user_id, title, message, notification_type, is_read
        ) VALUES (?, ?, ?, ?, 0);
    """
    params = (user_id, title, message, notification_type)
    return execute_write(query, params)

def db_get_notifications_by_user(user_id):
    """
    Retrieves all notifications for a specific user.
    """
    query = "SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC;"
    return execute_read_all(query, (user_id,))

def db_mark_notification_as_read(notification_id, user_id):
    """
    Marks a single notification as read. Returns number of affected rows.
    """
    query = "UPDATE notifications SET is_read = 1 WHERE notification_id = ? AND user_id = ?;"
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, (notification_id, user_id))
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()

def db_mark_all_notifications_as_read(user_id):
    """
    Marks all notifications for a specific user as read. Returns number of affected rows.
    """
    query = "UPDATE notifications SET is_read = 1 WHERE user_id = ?;"
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, (user_id,))
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()

# =====================================================================
# ELIGIBILITY HISTORY TABLE OPERATIONS
# =====================================================================

def db_create_eligibility_history(user_id, scheme_id, eligibility_result,
                                  match_percentage, ai_explanation, missing_requirements):
    """
    Inserts an eligibility evaluation history record. Returns the newly created history_id.
    """
    query = """
        INSERT INTO eligibility_history (
            user_id, scheme_id, eligibility_result, match_percentage, ai_explanation, missing_requirements
        ) VALUES (?, ?, ?, ?, ?, ?);
    """
    params = (user_id, scheme_id, eligibility_result, match_percentage, ai_explanation, missing_requirements)
    return execute_write(query, params)

def db_get_eligibility_history_by_user(user_id):
    """
    Retrieves the complete eligibility checking history for a specific user.
    """
    query = """
        SELECT eh.*, s.title as scheme_title, s.category as scheme_category
        FROM eligibility_history eh
        JOIN schemes s ON eh.scheme_id = s.scheme_id
        WHERE eh.user_id = ?
        ORDER BY eh.checked_at DESC;
    """
    return execute_read_all(query, (user_id,))

def db_get_eligibility_history_by_user_and_scheme(user_id, scheme_id):
    """
    Retrieves the most recent eligibility evaluation for a specific user and scheme.
    """
    query = """
        SELECT * FROM eligibility_history
        WHERE user_id = ? AND scheme_id = ?
        ORDER BY checked_at DESC LIMIT 1;
    """
    return execute_read_one(query, (user_id, scheme_id))
