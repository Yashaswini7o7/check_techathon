from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from orchestrator import master_handle_message
import shutil, os, uuid

app = FastAPI()
SESSIONS = {}  # session_id -> context

class Msg(BaseModel):
    session_id: str
    customer_id: str
    text: str

@app.post("/chat/send")
def chat_send(msg: Msg):
    ctx = SESSIONS.setdefault(msg.session_id, {"stage":"start"})
    resp, new_ctx = master_handle_message(msg.session_id, msg.customer_id, msg.text, ctx)
    SESSIONS[msg.session_id] = new_ctx
    return {"responses": resp["responses"], "context": new_ctx}

@app.post("/upload/salary")
def upload_salary(session_id: str = Form(...), file: UploadFile = File(...)):
    out_dir = "uploads"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    fname = os.path.join(out_dir, f"{session_id}_{uuid.uuid4().hex}_{file.filename}")
    with open(fname, "wb") as f:
        shutil.copyfileobj(file.file, f)
    # attach to session
    if session_id in SESSIONS:
        SESSIONS[session_id]["uploaded_salary_path"] = fname
        # optionally run OCR / simulation to extract salary
        SESSIONS[session_id]["mock_salary_amount"] = 60000
    return {"status":"ok","path":fname}
