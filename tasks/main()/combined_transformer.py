# ====================== 靈神星每日位置監看（追加） ======================
import math
from datetime import datetime, timedelta

PSYCHE_DATA_FILE = RESULT_DIR / "psyche_daily_position.json"

def simulate_psyche_position(day_offset: int = 0) -> dict:
    """
    模擬靈神星 (16 Psyche) 每日位置變化
    使用簡化開普勒軌道模型（僅供模擬展示）
    """
    # 基準日期（模擬起始點）
    base_date = datetime(2026, 8, 18)
    current_date = base_date + timedelta(days=day_offset)
    
    # 簡化軌道參數（模擬用）
    semi_major_axis_au = 2.922   # 平均距離
    eccentricity = 0.134
    period_days = 1827           # 約 5 年
    inclination_deg = 3.1
    
    # 計算相位角（每天推進）
    mean_anomaly = (2 * math.pi * (day_offset % period_days)) / period_days
    true_anomaly = mean_anomaly + 2 * eccentricity * math.sin(mean_anomaly)  # 近似
    
    # 模擬日心黃道座標（AU）
    r = semi_major_axis_au * (1 - eccentricity**2) / (1 + eccentricity * math.cos(true_anomaly))
    x = r * math.cos(true_anomaly)
    y = r * math.sin(true_anomaly)
    z = r * math.sin(math.radians(inclination_deg)) * 0.1  # 簡化
    
    # 與地球距離近似（地球假設在 1 AU）
    earth_distance_au = math.sqrt((x - 1)**2 + y**2 + z**2)
    
    return {
        "date": current_date.strftime("%Y-%m-%d"),
        "asteroid": "靈神星 (16 Psyche)",
        "heliocentric": {
            "x_au": round(x, 4),
            "y_au": round(y, 4),
            "z_au": round(z, 4),
            "distance_from_sun_au": round(r, 4)
        },
        "earth_distance_au": round(earth_distance_au, 4),
        "phase_angle_deg": round(math.degrees(true_anomaly) % 360, 2),
        "status": "SIMULATION",
        "note": "簡化軌道模型，僅供任務模擬使用"
    }

def check_psyche_daily():
    """每天自動記錄靈神星位置變化"""
    log("📡 開始每日靈神星位置監看...")
    
    # 讀取既有資料
    history = []
    if PSYCHE_DATA_FILE.exists():
        try:
            with open(PSYCHE_DATA_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except:
            history = []
    
    # 計算今天偏移天數
    base = datetime(2026, 8, 18)
    today_offset = (datetime.now() - base).days
    
    # 產生今天資料
    today_pos = simulate_psyche_position(day_offset=today_offset)
    
    # 避免重複寫入同一天
    if not history or history[-1].get("date") != today_pos["date"]:
        history.append(today_pos)
        
        # 只保留最近 90 天
        history = history[-90:]
        
        with open(PSYCHE_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        
        log(f"✅ 靈神星位置已更新 → {today_pos['date']}")
        log(f"   日心距離: {today_pos['heliocentric']['distance_from_sun_au']} AU")
        log(f"   與地球距離: {today_pos['earth_distance_au']} AU")
        log(f"   相位角: {today_pos['phase_angle_deg']}°")
    else:
        log("ℹ️ 今日靈神星位置已存在，略過寫入")
    
    return today_pos
