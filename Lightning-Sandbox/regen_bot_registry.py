import json
import os

# ==================== 1. 原有的 4 個核心 Bot ====================
existing_bots = [
    { "name": "LightningEmperor_Bot", "role": "Control Tower", "status": "active" },
    { "name": "Grok_Analyzer_bot", "role": "Analysis", "status": "active" },
    { "name": "RedRabbit", "role": "Task Execution", "status": "active" },
    { "name": "AutoRainDispatch", "role": "Weather Dispatch", "status": "active" }
]

# ==================== 2. 補齊原本的 996 個 DeepSeek_Bot ====================
roles = [
    "Control Tower", "Analysis", "Task Execution", "Weather Dispatch",
    "Monitoring", "Data Sync", "Security", "Reporting", "Backup", "Scheduler"
]
total_existing_needed = 1000
for i in range(1, total_existing_needed - len(existing_bots) + 1):
    name = f"DeepSeek_Bot_{i:04d}"
    role = roles[(i - 1) % len(roles)]
    existing_bots.append({ "name": name, "role": role, "status": "active" })

# ==================== 3. 召喚並補充「48 戰術節點 + AI合體金剛」 ====================
# 新增 Grok-X 與 DeepSeek-Z 的專屬合體 Bot
special_ai_bots = [
    { "name": "Grok-X_Tank_Bot", "role": "合體先鋒裝甲", "status": "active", "ai_partner": "grok-x" },
    { "name": "DeepSeek-Z_Drill_Bot", "role": "合體能量鑽頭", "status": "active", "ai_partner": "deepseek-z" },
    { "name": "Task_Bot_01", "role": "葉片巡檢合體", "status": "active", "ai_partner": "grok-x" },
    { "name": "Task_Bot_48", "role": "緊急儲能切換合體", "status": "active", "ai_partner": "deepseek-z" }
]

# 補上剩下的 44 個一般風電任務節點
task_bots = []
for i in range(1, 49):
    if i not in [1, 48]:
        task_bots.append({ "name": f"WindTask_Bot_{i:02d}", "role": "風場節點監控", "status": "active" })

# 合併陣列：原有的1000個 + 新的48個 = 總共 1048 個 Bot
all_bots = existing_bots + special_ai_bots + task_bots

# ==================== 4. 寫入檔案 ====================
os.makedirs("governance", exist_ok=True)
filename = "governance/bot_registry.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump({"bots": all_bots}, f, indent=2, ensure_ascii=False)

print(f"✅ 補充完成！")
print(f"👉 已成功將 48 個『合體戰術節點』寫入 {filename}")
print(f"👉 檔案總數：原有 1000 個 + 新增 48 個 = 共 {len(all_bots)} 個 Bot (包含 Grok-X 與 DeepSeek-Z 的專屬部隊)")
