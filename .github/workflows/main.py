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
# 使用官方轻量级 Python 镜像 (纯本地无外部编译依赖)
FROM python:3.13-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装 (避免层级缓存问题)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制所有项目代码到容器内
COPY . .

# 配置容器启动命令
# --host 127.0.0.1 强制只能从容器内部访问，确保完全隔离
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
import os
from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="Lightning Empire - 閃電帝國 BOT 銀行系統")

# 從 GitHub Secrets 讀取環境變數
BOT_KEY = os.getenv("LIGHTNING_BOT_KEY", "DEV_BOT_KEY")
BANK_NAME = os.getenv("UNION_ACCOUNT_NAME", "主權帳戶803")
BANK_NUMBER = os.getenv("UNION_ACCOUNT_NUMBER", "061507123481")

@app.get("/")
def home():
    return {"status": "閃電帝國核心運作中", "bot_ready": True}

# 驗證 BOT_KEY 的端點
@app.get("/bot/verify")
def verify_bot_key(bot_key: str = Header(None)):
    if bot_key != BOT_KEY:
        raise HTTPException(status_code=401, detail="無效的 BOT_KEY！")
    return {"message": "身份驗證成功", "status": "authorized"}

# 專給 BOT 查詢銀行帳戶的端點（必須帶正確的 BOT_KEY）
@app.get("/bot/bank-info")
def get_bank_info(bot_key: str = Header(None)):
    if bot_key != BOT_KEY:
        raise HTTPException(status_code=401, detail="拒絕存取：未授權的 BOT")
    return {
        "bank_name": BANK_NAME,
        "bank_number": BANK_NUMBER,
        "note": "請轉帳至此帳號，完成後由系統自動開通店家 ID。"
    }

# 給客戶端直接顯示的簡易付款資訊（免驗證）
@app.get("/public/bank-info")
def public_bank_info():
    return {
        "bank_name": BANK_NAME,
        "bank_number": BANK_NUMBER
    }
from fastapi import FastAPI, Request, HTTPException
import re

app = FastAPI()

# 黑名單：直接封鎖的 IP 列表（從日誌中收集）
BLOCKED_IPS = {"203.0.113.5", "198.51.100.77"}  # 範例，請換成真實濫用 IP

# 黑名單：特定的 User-Agent 關鍵字（外送機器人、自動化工具）
BLOCKED_UA_PATTERNS = [
    r"python-requests",
    r"Go-http-client",
    r"Apache-HttpClient",
    r"okhttp",
    r"Scrapy",
    r"curl",
    r"wget",
    r"Uber",          # 外送相關
    r"Foodpanda",
    r"Deliveroo",
    r"DoorDash",
    r"Meituan",       # 美團
    r"Eleme",         # 餓了麼
    r"automatic",
    r"bot",
    r"spider",
]

@app.middleware("http")
async def block_abuse(request: Request, call_next):
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent", "")

    # IP 黑名單
    if client_ip in BLOCKED_IPS:
        raise HTTPException(status_code=403, detail="您的 IP 已被封鎖（濫用檢測）")

    # User-Agent 黑名單
    for pattern in BLOCKED_UA_PATTERNS:
        if re.search(pattern, user_agent, re.IGNORECASE):
            raise HTTPException(status_code=403, detail="自動化工具不被允許")

    # 可選：請求頻率限制（每 IP 每分鐘最多 10 次）
    # 需要用 slowapi 或自建計數器，這裡不展開

    return await call_next(request)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import date, timedelta
from typing import Dict, Optional

app = FastAPI(title="Lightning Restaurant Promotion System")

class MerchantCreate(BaseModel):
    name: str = Field(..., min_length=1, description="餐廳名稱")
    start_date: date = Field(..., description="試用開始日期 (YYYY-MM-DD)")

class MerchantStatus(BaseModel):
    merchant: str
    status: str
    days_left: Optional[int] = None
    end_date: str
    suggest_price: Optional[str] = None

db: Dict[str, dict] = {}  # 後續可替換為資料庫
FREE_DAYS = 7

@app.get("/")
def home():
    return {"system": "Lightning Promotion", "status": "running", "version": "0.1.0"}

@app.post("/merchant", response_model=Dict)
def create_merchant(data: MerchantCreate):
    if data.name in db:
        raise HTTPException(status_code=400, detail="該店家已存在")

    end_date = data.start_date + timedelta(days=FREE_DAYS)
    
    db[data.name] = {
        "start_date": data.start_date,
        "end_date": end_date
    }

    return {
        "message": "免費合作已啟動",
        "merchant": data.name,
        "end_date": end_date.strftime("%Y-%m-%d"),
        "free_days": FREE_DAYS
    }

@app.get("/merchant/{name}", response_model=MerchantStatus)
def merchant_status(name: str):
    if name not in db:
        raise HTTPException(status_code=404, detail="找不到店家")

    record = db[name]
    end_date = record["end_date"]
    today = date.today()
    
    days_left = (end_date - today).days

    if today < end_date:
        return MerchantStatus(
            merchant=name,
            status="免費試用中",
            days_left=max(days_left, 0),
            end_date=end_date.strftime("%Y-%m-%d")
        )
    else:
        return MerchantStatus(
            merchant=name,
            status="試用已結束，可開始月費合作",
            end_date=end_date.strftime("%Y-%m-%d"),
            suggest_price="NT$3,000 \~ 5,000 / 月"
        )
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional

app = FastAPI(title="Lightning AI Factory - 餐飲合作管理系統")

# ================= 資料模型定義 =================
class MerchantCreate(BaseModel):
    name: str = Field(..., description="餐廳名稱")
    address: str = Field(..., description="營業地址（例：國安國仔/逢甲商圈）")
    start_date: date = Field(..., description="試用開始日期 (YYYY-MM-DD)")

class DailyStats(BaseModel):
    date: date
    impressions: int = 0  # 曝光數
    clicks: int = 0       # 點擊數
    inquiries: int = 0    # 詢問數
    orders: int = 0       # 訂單數

class MerchantStatusResponse(BaseModel):
    merchant: str
    status: str
    end_date: str
    days_left: Optional[int] = None
    stats: Optional[List[DailyStats]] = None
    suggest_price: Optional[str] = None

# ================= 模擬資料庫 =================
# 實際應用時請改成 SQLite 或 PostgreSQL
db_merchants: Dict[str, dict] = {}
FREE_DAYS = 7

# ================= API 介面 =================

@app.get("/")
def home():
    return {
        "system": "Lightning AI Factory",
        "message": "歡迎使用 AI 餐飲合作管理系統",
        "version": "1.0.0"
    }

# 1. 新增合作店家
@app.post("/merchant", response_model=dict)
def create_merchant(data: MerchantCreate):
    if data.name in db_merchants:
        raise HTTPException(status_code=400, detail="該店家已註冊")
    
    end_date = data.start_date + timedelta(days=FREE_DAYS)
    
    db_merchants[data.name] = {
        "start_date": data.start_date,
        "end_date": end_date,
        "address": data.address,
        "stats": [] # 用來存放每日追蹤數據
    }

    return {
        "message": "免費合作已啟動！",
        "merchant": data.name,
        "end_date": end_date.strftime("%Y-%m-%d"),
        "free_days": FREE_DAYS,
        "secret_tip": "請務必在 7 天內透過 POST /merchant/{name}/stats 輸入數據！"
    }

# 2. 每日輸入成效數據（將你之前的 python tracker.py 整合進來）
@app.post("/merchant/{name}/stats")
def add_daily_stats(name: str, stats: DailyStats):
    if name not in db_merchants:
        raise HTTPException(status_code=404, detail="找不到店家")
    
    merchant = db_merchants[name]
    
    # 檢查今天是否已經記錄過
    for record in merchant["stats"]:
        if record["date"] == stats.date:
            raise HTTPException(status_code=400, detail=f"{stats.date} 已有數據，今日不可重複輸入")
    
    merchant["stats"].append(stats.dict())
    return {"message": f"已成功記錄 {stats.date} 的營運數據"}

# 3. 查看試用進度與 7 天成效總結 (讓店家一目了然)
@app.get("/merchant/{name}", response_model=MerchantStatusResponse)
def merchant_status(name: str):
    if name not in db_merchants:
        raise HTTPException(status_code=404, detail="找不到店家")

    record = db_merchants[name]
    end_date = record["end_date"]
    today = date.today()
    
    days_left = (end_date - today).days
    
    # 計算過去 7 天總訂單
    total_orders = sum(item["orders"] for item in record["stats"])
    avg_orders = total_orders / len(record["stats"]) if record["stats"] else 0
    
    status_msg = ""
    suggest_price = None
    
    if today < end_date:
        status_msg = "免費試用中"
    else:
        status_msg = "試用期已結束"
        if total_orders >= 50: # 如果 7 天達成 50 單，可以更有底氣開高價
            suggest_price = "NT$5,000 / 月 (達標爆單價)"
        else:
            suggest_price = "NT$3,000 ~ 5,000 / 月 (試用完成價)"

    return MerchantStatusResponse(
        merchant=name,
        status=status_msg,
        end_date=end_date.strftime("%Y-%m-%d"),
        days_left=max(days_left, 0),
        stats=record["stats"],
        suggest_price=suggest_price
    )

# 4. 爆單時間模擬器 (針對 17:30 ~ 21:30 的 50 單策略)
@app.get("/merchant/{name}/simulate")
def simulate_orders(name: str, target_orders: int = 50, start_str: str = "17:30", end_str: str = "21:30"):
    if name not in db_merchants:
        raise HTTPException(status_code=404, detail="找不到店家")

    start_time = datetime.strptime(start_str, "%H:%M")
    end_time = datetime.strptime(end_str, "%H:%M")
    total_seconds = (end_time - start_time).total_seconds()
    
    if target_orders <= 1:
        interval_seconds = 0
    else:
        interval_seconds = total_seconds / (target_orders - 1)
        
    interval_min = int(interval_seconds // 60)
    interval_sec = int(interval_seconds % 60)
    
    # 直接給你秀給老闆看的具體數據
    return {
        "merchant": name,
        "analysis_title": f"目標：{start_str} 到 {end_str} 達成 {target_orders} 單",
        "critical_metric": f"平均每 {interval_min} 分 {interval_sec} 秒需接一單",
        "actionable_advice": f"如果中間超過 {interval_min+1} 分鐘沒單，廚房需有準備瞬間出 2 單的彈性！",
        "raw_seconds_per_order": f"{interval_seconds:.2f} 秒"
    }
# -*- coding: utf-8 -*-
"""
專案名稱：Lightning_AI_Full
模組名稱：main.py
描述：對標 NVIDIA Omniverse / Tesla Megapack 的本地免認證智慧綠能調度與定價系統
語言：Python 3.11+
"""

import random
import math
from datetime import datetime, timezone, timedelta
from typing import Dict, Any
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Wshao777 Wind Pricing & Digital Twin Sandbox",
    description="對標 NVIDIA Omniverse / Tesla Megapack 的本地免認證智慧綠能調度系統",
    version="2.0.0"
)

# ==========================================
# 📊 系統核心內部狀態（純內存，重啟即重設，完全免費）
# ==========================================
SUPER_ADMIN_EMAIL = "Wshao777opscenter@gmail.com"
SYSTEM_START_TIME = datetime.now(timezone.utc)
TRIAL_DAYS = 7
PRICE_PER_KWH = 2.0

# 模擬 Tesla Megapack 儲能系統狀態
BATTERY_CAPACITY_KWH = 50000.0  # 總容量 50 MWh
battery_stored_kwh = 25000.0    # 當前儲電量 (預設 50%)

# 超級管理員干預標記
admin_force_free = False

# ==========================================
# 🌪️ AI 物理與發電最佳化引擎 (GE Vernova / Siemens Energy 模擬)
# ==========================================
def simulate_weibull_wind_speed() -> float:
    """使用韋伯分佈 (Weibull Distribution) 模擬真實沿海風速，比隨機數更符合氣象學"""
    shape = 2.0  # 沿海典型風速分佈參數
    scale = 8.5  # 平均風速約 7.5 m/s
    return scale * (-math.log(1.0 - random.random())) ** (1.0 / shape)

def calculate_ai_optimized_power(v: float) -> float:
    """
    智慧發電最佳化曲線：
    - 切入風速 (Cut-in): 3 m/s
    - 額定風速 (Rated): 12 m/s (達到最大功率)
    - 切出風速 (Cut-out): 25 m/s (無人機巡檢並強制鎖定葉片保護)
    """
    if v < 3.0 or v > 25.0:
        return 0.0
    if v >= 12.0:
        return 1500.0  # 單一大型海上風機額定發電 1500 kWh
    # 3m/s ~ 12m/s 之間依據風能公式與 AI 最佳化效率係數計算
    ai_efficiency_factor = 0.45 
    return round(0.5 * 1.225 * ai_efficiency_factor * (v ** 3), 2)

# ==========================================
# ⚡ Tesla Megapack 智慧儲能與電網調度
# ==========================================
def dispatch_smart_grid(power_generated: float) -> Dict[str, float]:
    """
    智慧儲能調度算法：
    - 模擬電網基礎負載 (Base Load)
    - 發電大於負載：將多餘電力充入 Megapack
    - 發電小於負載：由 Megapack 放電補足電網
    """
    global battery_stored_kwh
    grid_demand = random.uniform(300.0, 1200.0) # 模擬城市動態用電需求
    net_power = power_generated - grid_demand
    
    charge_status = "BALANCE"
    if net_power > 0:
        # 充電邏輯
        available_room = BATTERY_CAPACITY_KWH - battery_stored_kwh
        actual_charge = min(net_power, available_room)
        battery_stored_kwh += actual_charge
        charge_status = "CHARGING"
    else:
        # 放電邏輯
        actual_discharge = min(abs(net_power), battery_stored_kwh)
        battery_stored_kwh -= actual_discharge
        charge_status = "DISCHARGING"
        
    return {
        "grid_demand_kwh": round(grid_demand, 2),
        "megapack_soc_pct": round((battery_stored_kwh / BATTERY_CAPACITY_KWH) * 100, 2),
        "megapack_status": charge_status
    }

# ==========================================
# 💰 延遲動態激活定價邏輯
# ==========================================
def get_current_pricing_rule() -> Dict[str, Any]:
    if admin_force_free:
        return {"price": 0.0, "mode": "SUPER_ADMIN_BYPASS_FREE"}
        
    now = datetime.now(timezone.utc)
    activation_date = SYSTEM_START_TIME + timedelta(days=TRIAL_DAYS)
    
    if now >= activation_date:
        return {"price": PRICE_PER_KWH, "mode": "DYNAMIC_BILLING_ACTIVE"}
    return {"price": 0.0, "mode": "SIMULATION_FREE_TRIAL"}

# ==========================================
# 🔌 FastAPI 路由端點 (純本地公開演練)
# ==========================================
@app.get("/health", tags=["Infrastructure"])
def local_health():
    return {"status": "Omniverse Twin Local Engine Operational"}

@app.get("/grid/digital-twin", tags=["Smart Grid Core"])
def get_digital_twin_metrics():
    """整合風速、AI發電最佳化與 Tesla Megapack 儲能調度的數位雙生端點"""
    v = simulate_weibull_wind_speed()
    p = calculate_ai_optimized_power(v)
    grid_metrics = dispatch_smart_grid(p)
    price_info = get_current_pricing_rule()
    
    # 動態營收計算
    revenue = round(p * price_info["price"], 2)
    
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "weather_station": {
            "wind_speed_ms": round(v, 2),
            "drone_inspection_status": "NORMAL" if v <= 25.0 else "WARNING_STORM_LOCK"
        },
        "ge_vernova_ai_turbine": {
            "power_output_kwh": p,
            "efficiency_optimized": "OPTIMAL_ON" if 3.0 <= v <= 12.0 else "STANDBY"
        },
        "tesla_megapack": grid_metrics,
        "pricing_engine": {
            "current_price_per_kwh": price_info["price"],
            "billing_mode": price_info["mode"],
            "revenue_generated": revenue
        }
    }

# ==========================================
# 👑 Wshao777 超級管理員本地控制端點 (免認證安全密鑰)
# ==========================================
@app.post("/admin/reset-grid-free", tags=["Super Admin Overrides"])
def super_admin_reset_free(admin_email: str = Header(...)):
    """
    不需透過任何第三方支付與 Google Cloud 憑證，
    直接比對 Header 內的管理員信箱。如果是 Wshao777opscenter@gmail.com 則強制切換為永久免費模式。
    """
    global admin_force_free
    if admin_email != SUPER_ADMIN_EMAIL:
        raise HTTPException(status_code=403, detail="拒絕存取：您不具備超級管理員權限")
        
    admin_force_free = True
    return {
        "status": "SUCCESS",
        "operator": SUPER_ADMIN_EMAIL,
        "action": "OVERRIDE_TO_PERMANENT_FREE",
        "message": "合作開發模式已啟動，超級管理員已將全系統能源交易判定重設為：完全免費演練模式。"
    }
練結果。: command not found                    ~ $
~ $ 這個版本先定位成純軟體、純本地、無真實設備控 制權限的 Sandbox，是最穩妥的。
這個版本先定位成純軟體、純本地、無真實設備控制權 限的: command not found                          ~ $ python -m uvicorn main:app --host 127.0.0.1 --port 8000
/data/data/com.termux/files/usr/bin/python: No module named uvicorn
~ $ http://127.0.0.1:8000/health                 bash: http://127.0.0.1:8000/health: No such file or directory
~ $ http://127.0.0.1:8000/ai/registry
bash: http://127.0.0.1:8000/ai/registry: No such file or directory
~ $ http://127.0.0.1:8000/grid/digital-twin
bash: http://127.0.0.1:8000/grid/digital-twin: No such file or directorypython -m pip install "uvicorn[standard]" fastapipython -m pip install fastapi "uvicorn[standard]"python --version
python -m pip --version
python -m pip install fastapi "uvicorn[standard]"er the canonical location of the 'bdist_wheel' command, and will be removed in a future release. Please update to setuptools v70.1 or later which contains an integrated version of this command.                 warn(
            Python reports SOABI: cpython-313-aarch64-linux-android
            Computed rustc target triple: aarch64-unknown-linux-android
            Target triple not supported by rustup: aarch64-unknown-linux-android
            Rust not found, installing into a temporary directory                                             [end of output]

        note: This error originates from a subprocess, and is likely not a problem with pip.
      error: metadata-generation-failed

      × Encountered error while generating package metadata.
      ╰─> maturin

      note: This is an issue with the package mentioned above, not pip.
      hint: See above for details.
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
ERROR: Failed to build 'watchfiles' when installing build dependencies for watchfilespython -m pip install fastapi uvicorn --no-depspython -m pip install starlette pydantic typing-extensionspython -m uvicorn main:app --host 127.0.0.1 --port 8000
# 存檔位置：WindPower_BOT48_6AI_Capability/combined_transformer.py
import requests
import json
import time

# 連接 8000 主機的合體 API
MAIN_SERVER_URL = "http://127.0.0.1:8000"
GATEWAY_PASSPHRASE = "Wshao777opscenter_Transformer" # 合體驗證碼

def activate_combination(mission_type: str, current_wind_data: dict):
    """此函數模擬 Grok-X 與 DeepSeek-Z 的變型金剛合體運算"""
    print(f"🚀 [合體初始化] 接收到任務模式: {mission_type}")
    
    # 簡單模擬 Grok-X 即時運算
    if mission_type == "storm_safety":
        print("⚡ Grok-X 啟動：分析 48 個節點的雷達掃描數據...")
        action_plan = {"command": "降低切入風速保護", "area": "全風場"}
    
    # 簡單模擬 DeepSeek-Z 底層校準
    if mission_type == "grid_balance":
        print("🌀 DeepSeek-Z 啟動：校準 Megapack 儲能極限...")
        action_plan = {"command": "開啟 20% 額外儲能緩衝", "model_recalc": "True"}

    # 回傳指令給 8000 主機
    response = requests.post(
        f"{MAIN_SERVER_URL}/admin/transformer-bridge",
        json={"task_plan": action_plan, "auth": GATEWAY_PASSPHRASE}
    )
    print(f"✅ 合體指令已發送給主機: {response.status_code}")

if __name__ == "__main__":
    # 模擬持續監聽 48 個任務節點的狀態
    while True:
        # 模擬取得當前風電數據 (從 main.py 取得)
        try:
            grid_resp = requests.get(f"{MAIN_SERVER_URL}/grid/digital-twin")
            data = grid_resp.json()
            wind = data["weather_station"]["wind_speed_ms"]
            
            if wind > 20.0: # 風速過大，觸發 Grok-X 合體
                activate_combination("storm_safety", data)
            elif wind < 4.0: # 風速過小，觸發 DeepSeek-Z 合體
                activate_combination("grid_balance", data)
            else:
                print("⏸️ 當前平穩，合體金剛待命中...")
                
        except Exception as e:
            print(f"⚠️ 主機 8000 未回應: {e}")
            
        time.sleep(15) # 每 15 秒掃描一次任務環境
