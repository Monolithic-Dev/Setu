import sys
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(title="Setu Local Dev Server")

# Add CORS middleware to match Catalyst's frontend-backend bridge
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure Catalyst functions can be imported
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import the Catalyst functions
from functions.queryFunction.index import handle_request as query_handle_request
from functions.networkFunction.index import handle_request as network_handle_request
from functions.voiceTranscribeFunction.index import handle_request as voice_transcribe_handle_request
from functions.voiceSynthesizeFunction.index import handle_request as voice_synthesize_handle_request

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

@app.post("/server/api/query")
async def api_query(request: Request):
    auth_context = get_mock_auth_context(request)
    try:
        body = await request.json()
        result = query_handle_request(body, auth_context)
        return result
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail={"status": "error", "error_code": "BAD_REQUEST", "message": str(e)})

@app.get("/server/api/network/{entity_id}")
async def api_network(entity_id: str, request: Request):
    auth_context = get_mock_auth_context(request)
    try:
        result = network_handle_request({"entity_id": entity_id}, auth_context)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "error_code": "BAD_REQUEST", "message": str(e)})

@app.get("/server/api/audit/logs")
async def api_audit_logs(request: Request):
    role = request.headers.get("X-Dev-Role", "Station Officer")
    if role != "System Admin":
        raise HTTPException(status_code=403, detail={"status": "error", "error_code": "SCOPE_DENIED", "message": "Only System Admin can view logs"})
        
    try:
        import json
        audit_file = os.path.join(os.path.dirname(__file__), "data", "dev_audit_log.json")
        if not os.path.exists(audit_file):
            return {"entries": []}
        with open(audit_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            entries = [json.loads(line) for line in lines]
            return {"entries": entries[::-1]} # Return newest first
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "error_code": "BAD_REQUEST", "message": str(e)})

@app.post("/server/api/voice/transcribe")
async def api_voice_transcribe(request: Request):
    try:
        # Assuming audio bytes are sent in the body or form
        form = await request.form()
        audio_bytes = await form["file"].read() if "file" in form else await request.body()
        language_hint = "auto"
        config = {"SARVAM_API_KEY": "sk_xwjgnnee_lfunwefqkKmnR6qRGKx2XCSt"}
        result = voice_transcribe_handle_request(audio_bytes, language_hint, config)
        return result
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail={"status": "error", "error_code": "BAD_REQUEST", "message": str(e)})

@app.post("/server/api/voice/synthesize")
async def api_voice_synthesize(request: Request):
    try:
        body = await request.json()
        config = {"SARVAM_API_KEY": "sk_xwjgnnee_lfunwefqkKmnR6qRGKx2XCSt"}
        result = voice_synthesize_handle_request(body.get("text", ""), body.get("language", "kn"), config)
        
        # We need to return audio bytes (or base64) to the client.
        import base64
        return {"audio": base64.b64encode(result["audio_bytes"]).decode("utf-8"), "provider": result["provider"]}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail={"status": "error", "error_code": "BAD_REQUEST", "message": str(e)})

if __name__ == "__main__":
    import uvicorn
    print("Starting Catalyst local dev mock server on port 3000 using FastAPI...")
    uvicorn.run("server:app", host="127.0.0.1", port=3000, reload=True)
