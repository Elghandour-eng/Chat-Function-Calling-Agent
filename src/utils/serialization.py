from bson import ObjectId

def serialize_document(doc):
    """Convert MongoDB document to a JSON-serializable dictionary."""
    if isinstance(doc, dict):
        return {key: (str(value) if isinstance(value, ObjectId) else value) for key, value in doc.items()}
    return doc