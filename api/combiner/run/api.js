// backend/src/api.js (擴充部分)

// --- 合體協議 (Combiner Protocol) ---
app.post('/api/combiner/run', async (req, res) => {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing token' });
  }

  const token = authHeader.split(' ')[1];
  if (token !== process.env.INTERNAL_API_KEY) {
    return res.status(403).json({ error: 'Invalid token' });
  }

  try {
    const { mode, wind_speed, agent_chain, combine } = req.body;

    // 1. 模擬各 Agent 的獨立計算 (實際情況會各自呼叫不同微服務)
    const guardianCheck = { status: 'ok', message: '安全邊界確認：無實體控制' };
    const stormResult = { simulated_power: wind_speed * 50, status: 'generating' };
    const dispatchSuggestion = { recommended_units: ['T-01', 'T-03'], eta: '15min' };
    const reviewResult = { passed: true, notes: '邏輯一致' };

    // 2. 合體聚合 (Combiner)
    let combinedReport = {};
    if (combine) {
      combinedReport = {
        command: '合體協議完成',
        mode: mode,
        agents: agent_chain || ['Guardian', 'Storm', 'Dispatch', 'Reviewer'],
        outputs: {
          guardian: guardianCheck,
          storm: stormResult,
          dispatch: dispatchSuggestion,
          reviewer: reviewResult
        },
        combined_summary: {
          overall_status: 'SIMULATION_ONLY',
          physical_control: 'DISABLED',
          requires_approval: true,
          timestamp: new Date().toISOString()
        },
        // 標記「飛外太空」的來源
        origin: 'Private Backend (Alien Planet)'
      };
    }

    // 3. 回傳合體結果
    res.json({
      status: 'success',
      data: combinedReport,
      message: '🤖 AI 機械派系合體完成。此結果僅為模擬轉述。'
    });

  } catch (err) {
    console.error('[Combiner] Error:', err);
    res.status(500).json({ error: err.message });
  }
});

# 加上 AI 绿能模拟引擎（GE Vernova / Tesla Megapack）
def simulate_weibull_wind_speed() -> float:
    import math
    shape = 2.0
    scale = 8.5
    return scale * (-math.log(1.0 - random.random())) ** (1.0 / shape)

def dispatch_smart_grid(power_generated: float, battery_stored: float) -> Dict:
    grid_demand = random.uniform(300.0, 1200.0)
    net_power = power_generated - grid_demand
    
    if net_power > 0:
        available_room = 50000.0 - battery_stored
        actual_charge = min(net_power, available_room)
        battery_stored += actual_charge
        charge_status = "CHARGING"
    else:
        actual_discharge = min(abs(net_power), battery_stored)
        battery_stored -= actual_discharge
        charge_status = "DISCHARGING"
        
    return {
        "grid_demand_kwh": round(grid_demand, 2),
        "megapack_soc_pct": round((battery_stored / 50000.0) * 100, 2),
        "megapack_status": charge_status
    }

@app.get("/grid/digital-twin")
async def get_digital_twin():
    v = simulate_weibull_wind_speed()
    power = calculate_power(v) # 复用您已有的功率公式
    grid_metrics = dispatch_smart_grid(power, 25000.0) # 初始电量 25000
    price = PricingEngine.get_price()
    revenue = round(power * price, 2)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "weather_station": {
            "wind_speed_ms": round(v, 2),
            "drone_inspection_status": "NORMAL" if v <= 25.0 else "WARNING_STORM_LOCK"
        },
        "ge_vernova_ai_turbine": {
            "power_output_kwh": power,
            "efficiency_optimized": "ACTIVE" if 3.0 <= v <= 12.0 else "STANDBY"
        },
        "tesla_megapack": grid_metrics,
        "pricing_engine": {
            "current_price_per_kwh": price,
            "billing_mode": "DYNAMIC_BILLING_ACTIVE" if price > 0 else "FREE_TRIAL",
            "revenue_generated": revenue
        }
      }
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
version: '3.8'

services:
  wind-pricing-twin:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: wshao777_wind_pricing_sandbox
    # 🚨 安全重點：鎖定 127.0.0.1。這確保外部區域網路 (LAN) 無法連入，僅手機/本機可訪問
    ports:
      - "127.0.0.1:8000:8000"
    environment:
      # 系統模式
      - ENV_MODE=LOCAL_SANDBOX_DEVELOPMENT
      # 明確聲明斷開外部網路與金流，請勿依賴真實雲端 API
      - DISABLE_EXTERNAL_NETWORK=true
      # 超級管理員信箱 (對齊治理層的帳號 ID)
      - SUPER_ADMIN_EMAIL=Wshao777opscenter@gmail.com
      # 系統基礎定價參數
      - PRICE_PER_KWH=2.0
      - TRIAL_DAYS=7
    # 設定為不自動重啟，完全交由您手動控制
    restart: "no"
    # 健康檢查，確保服務正常運行
    healthcheck:
      test: ["CMD", "curl", "-f", "http://127.0.0.1:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    logging:
      driver: "json-file"
      options:
        max-size: "5m"
        max-file: "1"
from datetime import datetime, timedelta
from fastapi import FastAPI, Header, HTTPException
import random
import math
from typing import Dict
import os

app = FastAPI(title="Wshao777 Green Energy Sandbox (V2)", version="2.0.0")

# ==================== 核心私有狀態與環境變數 ====================
# 讀取 Docker 環境變數，給予預設值確保本地也能跑
SUPER_ADMIN_EMAIL = os.getenv("SUPER_ADMIN_EMAIL", "Wshao777opscenter@gmail.com")
SYSTEM_START = datetime.now()
TRIAL_DAYS = int(os.getenv("TRIAL_DAYS", 7))
ACTIVATION_DATE = SYSTEM_START + timedelta(days=TRIAL_DAYS)
PRICE_PER_KWH = float(os.getenv("PRICE_PER_KWH", 2.0))

# ==================== 儲能與 AI 物理引擎 (GE/Tesla 模擬) ====================
BATTERY_CAPACITY_KWH = 50000.0
battery_stored_kwh = 25000.0

def simulate_weibull_wind_speed() -> float:
    """韋伯分佈模擬真實沿海風速"""
    shape = 2.0
    scale = 8.5
    return scale * (-math.log(1.0 - random.random())) ** (1.0 / shape)

def calculate_ai_optimized_power(v: float) -> float:
    """最佳化功率曲線 (含安全保護)"""
    if v < 3.0 or v > 25.0:
        return 0.0
    if v >= 12.0:
        return 1500.0
    ai_efficiency_factor = 0.45
    return round(0.5 * 1.225 * ai_efficiency_factor * (v ** 3), 2)

def dispatch_smart_grid(power_generated: float) -> Dict[str, float]:
    """Tesla Megapack 智慧充放電調度"""
    global battery_stored_kwh
    grid_demand = random.uniform(300.0, 1200.0)
    net_power = power_generated - grid_demand

    charge_status = "BALANCE"
    if net_power > 0:
        available_room = BATTERY_CAPACITY_KWH - battery_stored_kwh
        actual_charge = min(net_power, available_room)
        battery_stored_kwh += actual_charge
        charge_status = "CHARGING"
    else:
        actual_discharge = min(abs(net_power), battery_stored_kwh)
        battery_stored_kwh -= actual_discharge
        charge_status = "DISCHARGING"

    return {
        "grid_demand_kwh": round(grid_demand, 2),
        "megapack_soc_pct": round((battery_stored_kwh / BATTERY_CAPACITY_KWH) * 100, 2),
        "megapack_status": charge_status
    }

# ==================== 定價引擎 ====================
def get_current_pricing():
    now = datetime.now()
    if now >= ACTIVATION_DATE:
        return {"price": PRICE_PER_KWH, "mode": "BILLING_ACTIVE"}
    return {"price": 0.0, "mode": "FREE_TRIAL"}

# ==================== FastAPI 端點與權限治理 ====================

@app.get("/health", tags=["Infrastructure"])
async def health():
    return {
        "status": "healthy",
        "service": "Wshao777 Green Energy V2 Docker",
        "env_mode": os.getenv("ENV_MODE", "UNKNOWN"),
        "external_network_blocked": True,
        "current_admin": SUPER_ADMIN_EMAIL
    }

@app.get("/grid/digital-twin", tags=["Smart Grid Core"])
async def get_digital_twin():
    v = simulate_weibull_wind_speed()
    p = calculate_ai_optimized_power(v)
    grid_metrics = dispatch_smart_grid(p)
    price_info = get_current_pricing()
    revenue = round(p * price_info["price"], 2)

    return {
        "timestamp": datetime.now().isoformat(),
        "weather_station": {
            "wind_speed_ms": round(v, 2),
            "drone_inspection_status": "NORMAL" if v <= 25.0 else "WARNING_STORM_LOCK"
        },
        "ge_vernova_ai_turbine": {
            "power_output_kwh": p,
            "efficiency_optimized": "ACTIVE" if 3.0 <= v <= 12.0 else "STANDBY"
        },
        "tesla_megapack": grid_metrics,
        "pricing_engine": {
            "current_price_per_kwh": price_info["price"],
            "billing_mode": price_info["mode"],
            "revenue_generated": revenue
        }
    }

# 👑 超級管理員幹預端點：權限與零信任控制
@app.post("/admin/reset-grid-free", tags=["Super Admin Overrides"])
async def super_admin_reset_free(admin_email: str = Header(...)):
    """
    權限工作內容：
    僅有帶上 Header: `admin-email: Wshao777opscenter@gmail.com` 的請求能觸發此端點。
    觸發後強制切換為永久免費演練模式。
    """
    global ACTIVATION_DATE
    if admin_email != SUPER_ADMIN_EMAIL:
        raise HTTPException(status_code=403, detail="拒絕存取：Header 驗證失敗，您不具備超級管理員權限。")

    # 將激活日期無限期往後推到 9999 年，實現永久免費
    ACTIVATION_DATE = datetime(9999, 12, 31)
    return {
        "status": "SUCCESS",
        "operator": SUPER_ADMIN_EMAIL,
        "action": "OVERRIDE_TO_PERMANENT_FREE",
        "message": "超級管理員已判定系統進入永久免費演練模式，拒絕對外與計費行為。"
  }
name: 🚀 Wshao777 部署

on:
  push:
    branches:
      - main
      - bot-main
      - Ai-main
    paths:
      - 'wshao777/Lightning-Empire-Taichung-AI/.github/workflows/**'
      - 'wshao777/entry.sh'
      - 'MEMORY_CARD_AI_BOT.py'
      - 'MEMORY_CARD_AI_BOT.yml'
  workflow_dispatch:

# 定义全局环境变量，供所有 Job 使用
env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # --- 1. 代码检查与风格测试 ---
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: 安装检查工具并执行
        run: |
          pip install flake8 black
          black --check .
          flake8 .

  # --- 2. 单元测试 ---
  unit-test:
    runs-on: ubuntu-latest
    needs: lint # 确保 lint 通过后才执行单元测试
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: testpass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - name: 安装依赖并执行测试
        run: |
          pip install -r requirements.txt
          # 如果您的项目里没有 requirements.txt，请替换为相应的安装命令
          pytest --cov=app --cov-report=xml

  # --- 3. 构建并推送到 GitHub Container Registry (GHCR) ---
  build-push:
    needs: [lint, unit-test]
    if: github.ref == 'refs/heads/main' # 只有主分支推送到 main 才构建镜像
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - name: 登录 GHCR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - name: 构建并推送镜像
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

  # --- 4. 部署到 K8s 集群 ---
  deploy-staging:
    needs: build-push
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: 安装 Kubectl
        uses: azure/setup-kubectl@v4
        with:
          version: 'latest'
          
      # 关键：配置 kubeconfig 以连接您的 K8s 集群
      - name: 配置 K8s 集群凭证
        uses: azure/k8s-set-context@v4
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG_DATA }} 
          # ⚠️ 注意：您需要先在 GitHub Secrets 里配置 KUBE_CONFIG_DATA

      - name: 更新 K8s 部署清单
        run: |
          kubectl set image deployment/wind-pricing \
            app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            -n staging
