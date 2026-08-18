import requests
import json
import time
import os
from datetime import datetime

# ====================== 設定區 ======================
MAIN_SERVER_URL = os.getenv("MAIN_SERVER_URL", "http://127.0.0.1:8000")
GATEWAY_PASSPHRASE = os.getenv("GATEWAY_PASSPHRASE", "Wshao777opscenter_Transformer")
POLL_INTERVAL = 15  # 秒

# 風速觸發閾值
STORM_THRESHOLD = 20.0   # m/s → Grok-X 風暴模式
LOW_WIND_THRESHOLD = 4.0 # m/s → DeepSeek-Z 儲能校準模式


def activate_combination(mission_type: str, current_wind_data: dict):
    """
    Grok-X / DeepSeek-Z 變型金剛合體運算模擬
    """
    print(f"🚀 [{datetime.now().strftime('%H:%M:%S')}] 合體初始化 | 任務模式: {mission_type}")

    action_plan = {}

    if mission_type == "storm_safety":
        print("⚡ Grok-X 啟動：分析 48 個節點雷達掃描數據...")
        action_plan = {
            "command": "降低切入風速保護",
            "area": "全風場",
            "ai_partner": "grok-x",
            "priority": "HIGH",
            "reason": f"風速過高 ({current_wind_data.get('weather_station', {}).get('wind_speed_ms', 'N/A')} m/s)"
        }

    elif mission_type == "grid_balance":
        print("🌀 DeepSeek-Z 啟動：校準 Megapack 儲能極限...")
        action_plan = {
            "command": "開啟 20% 額外儲能緩衝",
            "model_recalc": True,
            "ai_partner": "deepseek-z",
            "priority": "MEDIUM",
            "reason": f"風速過低 ({current_wind_data.get('weather_station', {}).get('wind_speed_ms', 'N/A')} m/s)"
        }

    else:
        print(f"⚠️ 未知任務模式: {mission_type}")
        return

    # 發送合體指令至 8000 主機
    try:
        response = requests.post(
            f"{MAIN_SERVER_URL}/admin/transformer-bridge",
            json={
                "task_plan": action_plan,
                "auth": GATEWAY_PASSPHRASE,
                "timestamp": datetime.now().isoformat()
            },
            timeout=10
        )
        print(f"✅ 合體指令已發送 | HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ 發送失敗: {e}")


def main():
    print("=" * 60)
    print("🤖 Grok-X 系列變型金剛 已啟動")
    print(f"📡 監聽主機: {MAIN_SERVER_URL}")
    print(f"⏱️  輪詢間隔: {POLL_INTERVAL} 秒")
    print("=" * 60)

    while True:
        try:
            grid_resp = requests.get(f"{MAIN_SERVER_URL}/grid/digital-twin", timeout=8)
            data = grid_resp.json()
            wind = data.get("weather_station", {}).get("wind_speed_ms", 0.0)

            print(f"🌬️  當前風速: {wind:.2f} m/s", end=" | ")

            if wind > STORM_THRESHOLD:
                print("→ 觸發 Grok-X 風暴合體")
                activate_combination("storm_safety", data)
            elif wind < LOW_WIND_THRESHOLD:
                print("→ 觸發 DeepSeek-Z 儲能合體")
                activate_combination("grid_balance", data)
            else:
                print("⏸️ 平穩，合體金剛待命中...")

        except Exception as e:
            print(f"⚠️ 主機 8000 未回應: {e}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
