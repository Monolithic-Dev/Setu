import sys
import os
import uuid
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "shared"))

import local_audit_store

_REPO_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")

def handle_request(request_body: dict, auth_context: dict) -> dict:
    """
    Implements POST /api/feedback.
    Accepts { audit_id, was_helpful }
    """
    audit_id = request_body.get("audit_id")
    was_helpful = request_body.get("was_helpful")
    
    if not audit_id or was_helpful is None:
        return {
            "status": "error",
            "error_code": "BAD_REQUEST",
            "message": "audit_id and was_helpful are required"
        }
        
    feedback_id = str(uuid.uuid4())
    
    # Store feedback in the local dev store
    local_audit_store.append_feedback(_REPO_ROOT, {
        "feedback_id": feedback_id,
        "audit_id": audit_id,
        "was_helpful": bool(was_helpful),
        "timestamp_": datetime.utcnow().isoformat()
    })
    
    return {
        "status": "recorded"
    }
