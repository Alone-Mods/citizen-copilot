import json
from database.db import db_get_documents_by_user

def check_uploaded_documents(user_id, required_documents):
    """
    Compares a scheme's required documents against a citizen's uploaded files.
    
    Args:
        user_id (int): User ID.
        required_documents (list or str): List of required document type strings,
                                         or JSON-serialized string representation.
                                         
    Returns:
        dict: Summary containing:
            - has_all_documents (bool)
            - missing_documents (list of str)
            - uploaded_documents (list of str)
            - missing_count (int)
    """
    # Deserializes required_documents if passed as JSON string
    if isinstance(required_documents, str):
        try:
            req_list = json.loads(required_documents)
        except Exception:
            req_list = []
    elif isinstance(required_documents, list):
        req_list = required_documents
    else:
        req_list = []

    # Fetch user's uploaded documents metadata from database
    raw_user_docs = db_get_documents_by_user(user_id)
    
    # Extract unique uploaded document types
    uploaded_types = set()
    for doc in raw_user_docs:
        doc_type = doc.get("document_type")
        if doc_type:
            uploaded_types.add(doc_type.strip())

    missing_documents = []
    uploaded_matches = []

    for req in req_list:
        clean_req = str(req).strip()
        if not clean_req:
            continue
        
        # Check if the document type exists in uploaded set
        if clean_req in uploaded_types:
            uploaded_matches.append(clean_req)
        else:
            missing_documents.append(clean_req)

    has_all = len(missing_documents) == 0

    return {
        "has_all_documents": has_all,
        "missing_documents": missing_documents,
        "uploaded_documents": uploaded_matches,
        "missing_count": len(missing_documents)
    }
