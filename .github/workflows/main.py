# 下載完整程式碼（我用 echo 方式建立）from fastapi import FastAPI, Request, HTTPException
import hmac, hashlib, os, asyncio
from typing import Dict

app = FastAPI(title="Lightning-Empire Storm Bot Core")

# =========================
# CONFIG
# =========================
GITHUB_SECRET = os.getenv("GITHUB_SECRET", "storm_secret")

# 48 task slots mapping
TASK_ROUTES = {i: f"task_{i}" for i in range(1, 49)}

# queue limiter (Storm Protection Core)
MAX_CONCURRENT_TASKS = 10
semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

# retry store
FAILED_TASKS = []


# =========================
# SECURITY (GitHub verify)
# =========================
def verify_signature(payload: bytes, signature: str):
    mac = hmac.new(
        GITHUB_SECRET.encode(),
        msg=payload,
        digestmod=hashlib.sha256
    )
    expected = "sha256=" + mac.hexdigest()
    return hmac.compare_digest(expected, signature)


# =========================
# STORM CORE ROUTER (1 → 48)
# =========================
def route_task(task_id: int, data: Dict):
    if task_id not in TASK_ROUTES:
        raise ValueError("Invalid task id")

    return {
        "route": TASK_ROUTES[task_id],
        "payload": data
    }


# =========================
# EXECUTION ENGINE
# =========================
async def execute_task(task):
    async with semaphore:
        try:
            # simulate processing
            await asyncio.sleep(0.2)

            print(f"[STORM CORE EXEC] {task}")

            return {"status": "ok", "task": task}

        except Exception as e:
            FAILED_TASKS.append(task)
            return {"status": "failed", "error": str(e)}


# =========================
# AUTO RECOVERY ENGINE
# =========================
async def recovery_loop():
    while True:
        if FAILED_TASKS:
            task = FAILED_TASKS.pop(0)
            print("[RECOVERY] retry:", task)
            await execute_task(task)

        await asyncio.sleep(5)


# =========================
# GITHUB WEBHOOK
# =========================
@app.post("/webhook/github")
async def github_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256")

    if not signature or not verify_signature(body, signature):
        raise HTTPException(status_code=403, detail="Invalid signature")

    payload = await request.json()

    # extract action
    action = payload.get("action", "unknown")
    repo = payload.get("repository", {}).get("full_name", "unknown")

    # convert GitHub event → task id (simple mapping)
    task_id = hash(action + repo) % 48 + 1

    task = route_task(task_id, {
        "repo": repo,
        "action": action,
        "raw": payload
    })

    result = await execute_task(task)

    return {
        "storm": "active",
        "task_id": task_id,
        "result": result
    }


# =========================
# STORM MONITOR
# =========================
@app.get("/storm/status")
def status():
    return {
        "active_tasks": MAX_CONCURRENT_TASKS,
        "failed_queue": len(FAILED_TASKS),
        "routes": len(TASK_ROUTES)
    }


# =========================
# START RECOVERY LOOP
# =========================
@app.on_event("startup")
async def startup():
    asyncio.create_task(recovery_loop())
    
echo 'from fastapi import FastAPI, HTTPException; from fastapi.responses import HTMLResponse; from pydantic import BaseModel; from datetime import datetime; from typing import Optional; import secrets; import sqlite3; import hashlib; from contextlib import contextmanager; app = FastAPI(); DB_PATH = "api_keys.db"; 
@contextmanager
def get_db(): conn = sqlite3.connect(DB_PATH); conn.row_factory = sqlite3.Row; yield conn; conn.commit(); conn.close()
def init_db():
    with get_db() as db:
        db.execute("CREATE TABLE IF NOT EXISTS api_keys (id INTEGER PRIMARY KEY, name TEXT, key_hash TEXT UNIQUE, key_prefix TEXT, target_user TEXT, created_at TEXT, is_active BOOLEAN DEFAULT 1)")
init_db()
class CreateRequest(BaseModel): name: str; to: Optional[str] = None
@app.post("/api/keys")
async def create(req: CreateRequest):
    raw = f"ak_{secrets.token_urlsafe(32)}"; hsh = hashlib.sha256(raw.encode()).hexdigest(); pre = raw[:12]
    with get_db() as db:
        cur = db.execute("INSERT INTO api_keys (name, key_hash, key_prefix, target_user, created_at, is_active) VALUES (?,?,?,?,?,1)", (req.name, hsh, pre, req.to, datetime.utcnow().isoformat()))
        return {"key": raw, "id": cur.lastrowid, "name": req.name}
@app.get("/api/keys")
async def list_keys():
    with get_db() as db:
        rows = db.execute("SELECT id, name, key_prefix, target_user, created_at, is_active FROM api_keys ORDER BY created_at DESC").fetchall()
        return {"keys": [dict(r) for r in rows]}
@app.delete("/api/keys/{kid}")
async def revoke(kid: int):
    with get_db() as db:
        db.execute("UPDATE api_keys SET is_active = 0 WHERE id = ?", (kid,))
        return {"ok": True}
@app.get("/", response_class=HTMLResponse)
async def ui():
    return "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>API Key Manager</title><style>body{font-family:system-ui;background:linear-gradient(135deg,#667eea,#764ba2);padding:40px}.container{max-width:800px;margin:0 auto}.card{background:white;border-radius:16px;padding:30px;margin-bottom:30px}h2{margin-bottom:20px}input,button{padding:12px;margin:5px;border-radius:8px;border:1px solid #ddd}button{background:#667eea;color:white;cursor:pointer}.key-item{border:1px solid #ddd;border-radius:12px;padding:15px;margin-bottom:10px}</style></head><body><div class=container><div class=card><h2>🔑 建立 API Key</h2><form id=f><input type=text id=name placeholder='名称' required><input type=text id=to placeholder='To (使用者/用途)'><button type=submit>✨ 建立</button><button type=button onclick=\"document.getElementById(\\\"f\\\").reset()\">取消</button></form></div><div class=card><h2>📋 API Key 列表</h2><div id=list></div></div></div><script>let lastKey='';async function load(){let r=await fetch('/api/keys'),d=await r.json();document.getElementById('list').innerHTML=(d.keys||[]).map(k=>`<div class=key-item><b>${escape(k.name)}</b> <code>${k.key_prefix}...</code> ${k.is_active?'✅啟用':'❌撤銷'}<br>To: ${escape(k.target_user||'-')} | ${new Date(k.created_at).toLocaleString()}<br>${k.is_active?`<button onclick=revoke(${k.id})>🔒 撤銷</button>`:''}</div>`).join('')||'<p>尚無 API Key</p>'}function escape(s){return s.replace(/[&<>]/g,function(m){return{'&':'&amp;','<':'&lt;','>':'&gt;'}[m]})}async function revoke(id){if(confirm('確定撤銷？')){await fetch(`/api/keys/${id}`,{method:'DELETE'});load()}}document.getElementById('f').onsubmit=async(e)=>{e.preventDefault();let name=document.getElementById('name').value,to=document.getElementById('to').value,r=await fetch('/api/keys',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,to})}),d=await r.json();if(d.key){alert(`✅ 已建立\n\n${d.key}\n\n這個 Key 不會再顯示`);document.getElementById('f').reset();load()}else alert('建立失敗')};load()</script></body></html>"' > api_key_manager.py && python3 -c "import uvicorn; from api_key_manager import app; uvicorn.run(app, host='0.0.0.0', port=8000)"
