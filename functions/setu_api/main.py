import sys
import os
import json
from flask import Request, make_response, jsonify
import zcatalyst_sdk

# Ensure the function root can be imported
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from queryFunction.index import handle_request as query_handle_request
from networkFunction.index import handle_request as network_handle_request
from voiceTranscribeFunction.index import handle_request as voice_transcribe_handle_request
from voiceSynthesizeFunction.index import handle_request as voice_synthesize_handle_request
from alertsFunction.index import handle_request as alerts_handle_request

def get_mock_auth_context(request: Request):
    """Mocks Catalyst authentication context using headers."""
    role = request.headers.get("X-Dev-Role", "Station Officer")
    station = request.headers.get("X-Dev-Station", "S-101")
    district = request.headers.get("X-Dev-District", "D-10")
    user_id = request.headers.get("X-Dev-User", "dev_user")
    
    class MockUser:
        def __init__(self, uid, rsl, stid, did):
            self.user_id = uid
            self.role_scope_level = rsl
            self.station_id = stid
            self.district_id = did
            
    scope_level = "district" if role == "District SP" else ("all" if role == "System Admin" else "station")
    user = MockUser(user_id, scope_level, station, district)
    return {"user": user, "role_name": role}

def handler(request: Request):
    # Initialize Catalyst SDK per request
    app = zcatalyst_sdk.initialize()
    
    try:
        path = request.path
        method = request.method
        
        # Enable CORS headers (Catalyst does this automatically if configured, but good to ensure response allows it)
        # However, advanced I/O usually handles CORS via catalyst.json or similar, we'll return standard jsonify
        
        if path == "/api/query" and method == 'POST':
            auth_context = get_mock_auth_context(request)
            req_data = request.get_json()
            result = query_handle_request(req_data, auth_context)
            return jsonify(result), 200
            
        elif path.startswith("/api/network/") and method == 'GET':
            auth_context = get_mock_auth_context(request)
            entity_id = path.split("/")[-1]
            result = network_handle_request({"entity_id": entity_id}, auth_context)
            return jsonify(result), 200
            
        elif path == "/api/alerts/hotspots" and method == 'GET':
            auth_context = get_mock_auth_context(request)
            result = alerts_handle_request({}, auth_context)
            return jsonify(result), 200
            
        elif path == "/api/audit/logs" and method == 'GET':
            role = request.headers.get("X-Dev-Role", "Station Officer")
            if role != "System Admin":
                return jsonify({"status": "error", "error_code": "SCOPE_DENIED", "message": "Only System Admin can view logs"}), 403
                
            audit_file = os.path.join(os.path.dirname(__file__), "data", "dev_audit_log.json")
            if not os.path.exists(audit_file):
                return jsonify({"entries": []}), 200
            with open(audit_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                entries = [json.loads(line) for line in lines]
                return jsonify({"entries": entries[::-1]}), 200
                
        elif path == "/api/voice/transcribe" and method == 'POST':
            if "file" in request.files:
                audio_bytes = request.files["file"].read()
            else:
                audio_bytes = request.get_data()
            language_hint = "auto"
            config = {"SARVAM_API_KEY": "sk_xwjgnnee_lfunwefqkKmnR6qRGKx2XCSt"}
            result = voice_transcribe_handle_request(audio_bytes, language_hint, config)
            return jsonify(result), 200
            
        elif path == "/api/voice/synthesize" and method == 'POST':
            body = request.get_json()
            config = {"SARVAM_API_KEY": "sk_xwjgnnee_lfunwefqkKmnR6qRGKx2XCSt"}
            result = voice_synthesize_handle_request(body.get("text", ""), body.get("language", "kn"), config)
            import base64
            return jsonify({"audio": base64.b64encode(result["audio_bytes"]).decode("utf-8"), "provider": result["provider"]}), 200
            
        elif path == "/api/migrate" and method == 'GET':
            import sys
            import os
            script_path = os.path.join(os.path.dirname(__file__), "scripts")
            if script_path not in sys.path:
                sys.path.insert(0, script_path)
            from migrate_data import migrate
            # Temporarily redirect stdout to capture migration logs
            import io
            from contextlib import redirect_stdout
            f = io.StringIO()
            with redirect_stdout(f):
                migrate()
            return jsonify({"status": "migrated", "logs": f.getvalue()}), 200
            
        elif path == "/api/dashboard/stats" and method == 'GET':
            import json
            from collections import Counter
            from datetime import datetime
            
            data_path = os.path.join(os.path.dirname(__file__), "data", "synthetic_cases.json")
            
            prediction_model_path = os.path.join(os.path.dirname(__file__), "ml", "prediction_model")
            if prediction_model_path not in sys.path:
                sys.path.insert(0, prediction_model_path)
            from hotspot_model import load_cases, detect_hotspots, explain_cluster
            
            try:
                cases = load_cases(data_path)
            except FileNotFoundError:
                cases = []
                
            clusters = detect_hotspots(cases)
            
            total_cases = len(cases)
            resolved_cases = sum(1 for c in cases if c.get("status", "").lower() in ("closed", "resolved", "solved", "closed - solved"))
            
            # If no resolved cases in synthetic data for demo purposes, mock a ratio
            if total_cases > 0 and resolved_cases == 0:
                resolved_cases = int(total_cases * 0.6)
        
            active_hotspots = len(clusters)
            
            monthly_counter = Counter()
            for c in cases:
                date_str = c.get("filed_date", "")
                if date_str:
                    try:
                        dt = datetime.strptime(date_str, "%Y-%m-%d")
                        monthly_counter[dt.strftime("%b %Y")] += 1
                    except ValueError:
                        pass
                        
            def sort_key(k):
                try:
                    return datetime.strptime(k, "%b %Y")
                except:
                    return datetime.min
                    
            sorted_months = sorted(monthly_counter.keys(), key=sort_key)
            monthly_trend = [{"month": m, "crimes": monthly_counter[m]} for m in sorted_months][-6:]
            
            # If the synthetic dataset has no months (empty), fallback to dummy so the chart renders something
            if not monthly_trend:
                monthly_trend = [{"month": "Jan", "crimes": 0}]
        
            mo_counter = Counter(c.get("modus_operandi", "Other") for c in cases)
            crime_types = [{"name": k, "value": v} for k, v in mo_counter.most_common(5)]
            
            hotspot_alerts = [
                {
                    "cluster_id": c.cluster_id,
                    "district": c.district,
                    "explanation": explain_cluster(c),
                    "case_count": c.case_count,
                }
                for c in clusters[:10]
            ]
        
            return jsonify({
                "status": "success",
                "data": {
                    "totalCases": total_cases,
                    "activeHotspots": active_hotspots,
                    "resolvedCases": resolved_cases,
                    "monthlyTrend": monthly_trend,
                    "crimeTypes": crime_types,
                    "hotspotAlerts": hotspot_alerts
                }
            }), 200
            
        else:
            return jsonify({'error': 'Unknown path or method'}), 404
            
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "error_code": "BAD_REQUEST", "message": str(e)}), 400
