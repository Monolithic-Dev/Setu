import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import the Catalyst functions
from functions.queryFunction.index import handle_request as query_handle_request
from functions.networkFunction.index import handle_request as network_handle_request
from functions.voiceTranscribeFunction.index import handle_request as voice_transcribe_handle_request
from functions.voiceSynthesizeFunction.index import handle_request as voice_synthesize_handle_request

@app.route('/server/api/query', methods=['POST'])
def api_query():
    # Construct the mock auth context from headers
    role = request.headers.get("X-Dev-Role", "Station Officer")
    station = request.headers.get("X-Dev-Station", "S-101")
    district = request.headers.get("X-Dev-District", "D-10")
    user_id = request.headers.get("X-Dev-User", "dev_user")
    
    # Simple User class mock
    class MockUser:
        def __init__(self, uid, rsl, stid, did):
            self.user_id = uid
            self.role_scope_level = rsl
            self.station_id = stid
            self.district_id = did
            
    scope_level = "district" if role == "District SP" else ("all" if role == "System Admin" else "station")
    user = MockUser(user_id, scope_level, station, district)
    auth_context = {"user": user, "role_name": role}

    try:
        body = request.get_json()
        result = query_handle_request(body, auth_context)
        return jsonify(result)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "error_code": "BAD_REQUEST", "message": str(e)}), 400

@app.route('/server/api/network/<entity_id>', methods=['GET'])
def api_network(entity_id):
    role = request.headers.get("X-Dev-Role", "Station Officer")
    station = request.headers.get("X-Dev-Station", "S-101")
    district = request.headers.get("X-Dev-District", "D-10")
    
    class MockUser:
        def __init__(self, uid, rsl, stid, did):
            self.user_id = uid
            self.role_scope_level = rsl
            self.station_id = stid
            self.district_id = did
            
    scope_level = "district" if role == "District SP" else ("all" if role == "System Admin" else "station")
    user = MockUser("dev", scope_level, station, district)
    auth_context = {"user": user, "role_name": role}

    try:
        result = network_handle_request({"entity_id": entity_id}, auth_context)
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "error_code": "BAD_REQUEST", "message": str(e)}), 400

@app.route('/server/api/audit/logs', methods=['GET'])
def api_audit_logs():
    role = request.headers.get("X-Dev-Role", "Station Officer")
    
    if role != "System Admin":
        return jsonify({"status": "error", "error_code": "SCOPE_DENIED", "message": "Only System Admin can view logs"}), 403
        
    try:
        import json
        audit_file = os.path.join(os.path.dirname(__file__), "data", "dev_audit_log.json")
        if not os.path.exists(audit_file):
            return jsonify({"entries": []})
        with open(audit_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            entries = [json.loads(line) for line in lines]
            return jsonify({"entries": entries[::-1]}) # Return newest first
    except Exception as e:
        return jsonify({"status": "error", "error_code": "BAD_REQUEST", "message": str(e)}), 400

if __name__ == '__main__':
    print("Starting Catalyst local dev mock server on port 3000...")
    app.run(port=3000, debug=True)
