import os
import time
from flask import Blueprint, request, jsonify, session
from werkzeug.utils import secure_filename
from config import Config
from database.db import (
    db_create_document,
    db_get_document_by_id,
    db_get_documents_by_user,
    db_delete_document
)
from models.document import Document

# Create the documents Blueprint
documents_bp = Blueprint("documents", __name__)

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}

def allowed_file(filename):
    """
    Validates if the file suffix matches allowed document formats.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@documents_bp.route("/api/documents/upload", methods=["POST"])
def upload_document():
    """
    Handles secure multipart document uploads, committing file objects to disk and db metadata logs.
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "Unauthorized. No active session."
        }), 401

    # Check if file field exists in request payload
    if "file" not in request.files:
        return jsonify({
            "status": "error",
            "message": "No file part in the request."
        }), 400

    file = request.files["file"]
    document_type = request.form.get("document_type", "").strip()

    if not document_type:
        return jsonify({
            "status": "error",
            "message": "Field 'document_type' is required."
        }), 400

    # Ensure document_type matches supported categories
    valid_doc_types = ["Aadhaar Card", "Caste Certificate", "Income Certificate", "Educational Marksheet", "Domicile Certificate", "PAN Card", "Other"]
    if document_type not in valid_doc_types:
        return jsonify({
            "status": "error",
            "message": f"Document type must be one of: {', '.join(valid_doc_types)}"
        }), 400

    if file.filename == "":
        return jsonify({
            "status": "error",
            "message": "No file selected for upload."
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "status": "error",
            "message": "Unsupported file format. Allowed extensions are: .pdf, .png, .jpg, .jpeg"
        }), 400

    try:
        # Guarantee presence of uploads directory
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

        original_filename = file.filename
        safe_name = secure_filename(original_filename)
        
        # Create timestamped filename to prevent conflicts
        file_basename, file_ext = os.path.splitext(safe_name)
        unique_name = f"{user_id}_{int(time.time())}_{file_basename}{file_ext}"
        stored_file_path = os.path.abspath(os.path.join(Config.UPLOAD_FOLDER, unique_name))

        # Save file to host disk
        file.save(stored_file_path)

        # Write metadata entry into SQLite
        new_doc_id = db_create_document(
            user_id=user_id,
            document_type=document_type,
            original_filename=original_filename,
            stored_file_path=stored_file_path,
            verification_status="Pending"
        )

        return jsonify({
            "status": "success",
            "message": "Document uploaded successfully.",
            "document": {
                "document_id": new_doc_id,
                "document_type": document_type,
                "original_filename": original_filename,
                "verification_status": "Pending"
            }
        }), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to upload document: {str(e)}"
        }), 500

@documents_bp.route("/api/documents", methods=["GET"])
def list_documents():
    """
    Returns metadata list of all files uploaded by the active authenticated user.
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "Unauthorized. No active session."
        }), 401

    try:
        raw_docs = db_get_documents_by_user(user_id)
        serialized_docs = []
        
        for row in raw_docs:
            doc = Document.from_dict(row)
            if doc:
                serialized_docs.append(doc.to_dict())

        return jsonify({
            "status": "success",
            "count": len(serialized_docs),
            "documents": serialized_docs
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to list documents: {str(e)}"
        }), 500

@documents_bp.route("/api/documents/<int:document_id>", methods=["DELETE"])
def delete_document(document_id):
    """
    Removes uploaded file objects from the storage system and db metadata tables.
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "Unauthorized. No active session."
        }), 401

    try:
        # Check if the document exists
        raw_doc = db_get_document_by_id(document_id)
        if not raw_doc:
            return jsonify({
                "status": "error",
                "message": "Document not found."
            }), 404

        doc = Document.from_dict(raw_doc)
        
        # Verify ownership
        if doc.user_id != user_id:
            return jsonify({
                "status": "error",
                "message": "Forbidden. You do not own this document."
            }), 403

        # Remove physical file from host disk if present
        if doc.stored_file_path and os.path.exists(doc.stored_file_path):
            try:
                os.remove(doc.stored_file_path)
            except OSError as e:
                # Log error, but proceed with DB cleanup
                print(f"Warning: Failed to delete file {doc.stored_file_path}: {str(e)}")

        # Delete metadata record from sqlite
        db_delete_document(document_id, user_id)

        return jsonify({
            "status": "success",
            "message": "Document deleted successfully."
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to delete document: {str(e)}"
        }), 500
