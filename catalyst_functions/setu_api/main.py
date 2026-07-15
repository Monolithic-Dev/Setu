import sys
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Ensure the function root can be imported
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

app = FastAPI(title="Setu Catalyst API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# pyrefly: ignore [missing-import]
from queryFunction.index import handle_request as query_handle_request
# pyrefly: ignore [missing-import]
from networkFunction.index import handle_request as network_handle_request
# pyrefly: ignore [missing-import]
from voiceTranscribeFunction.index import handle_request as voice_transcribe_handle_request
# pyrefly: ignore [missing-import]
from voiceSynthesizeFunction.index import handle_request as voice_synthesize_handle_request
# pyrefly: ignore [missing-import]
from alertsFunction.index import handle_request as alerts_handle_request
# pyrefly: ignore [missing-import]
from exportFunction.index import handle_request as export_handle_request
from fastapi.responses import FileResponse

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

@app.post("/api/query")
async def api_query(request: Request):
    auth_context = get_mock_auth_context(request)
    try:
        body = await request.json()
        result = query_handle_request(body, auth_context)
        return result
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail={"status": "error", "error_code": "BAD_REQUEST", "message": str(e)})

@app.get("/api/network/{entity_id}")
async def api_network(entity_id: str, request: Request):
    auth_context = get_mock_auth_context(request)
    try:
        result = network_handle_request({"entity_id": entity_id}, auth_context)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "error_code": "BAD_REQUEST", "message": str(e)})

@app.get("/api/alerts/hotspots")
async def api_alerts_hotspots(request: Request):
    auth_context = get_mock_auth_context(request)
    try:
        result = alerts_handle_request({}, auth_context)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "error_code": "BAD_REQUEST", "message": str(e)})

@app.get("/api/audit/logs")
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

@app.post("/api/voice/transcribe")
async def api_voice_transcribe(request: Request):
    try:
        form = await request.form()
        audio_bytes = await form["file"].read() if "file" in form else await request.body()
        language_hint = "auto"
        config = {"SARVAM_API_KEY": "sk_xwjgnnee_lfunwefqkKmnR6qRGKx2XCSt"}
        result = voice_transcribe_handle_request(audio_bytes, language_hint, config)
        return result
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail={"status": "error", "error_code": "BAD_REQUEST", "message": str(e)})

@app.post("/api/voice/synthesize")
async def api_voice_synthesize(request: Request):
    try:
        body = await request.json()
        config = {"SARVAM_API_KEY": "sk_xwjgnnee_lfunwefqkKmnR6qRGKx2XCSt"}
        result = voice_synthesize_handle_request(body.get("text", ""), body.get("language", "kn"), config)
        
        import base64
        return {"audio": base64.b64encode(result["audio_bytes"]).decode("utf-8"), "provider": result["provider"]}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail={"status": "error", "error_code": "BAD_REQUEST", "message": str(e)})

@app.post("/api/export/pdf")
async def api_export_pdf(request: Request):
    auth_context = get_mock_auth_context(request)
    try:
        body = await request.json()
        result = export_handle_request(body.get("session_id"), body.get("conversation", {}), auth_context)
        return FileResponse(result["path"], filename=f"export_{body.get('session_id')}.pdf", media_type="application/pdf")
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail={"status": "error", "error_code": "BAD_REQUEST", "message": str(e)})

if __name__ == "__main__":
    import uvicorn
    print("Starting Catalyst local dev mock server on port 3000 using FastAPI...")
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)
