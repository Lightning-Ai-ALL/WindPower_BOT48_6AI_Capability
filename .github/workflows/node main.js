task_id = hash(action + repo) % 48 + 1
X-Hub-Signature-256 HMAC SHA256 verify
FAILED_TASKS → recovery_loop()
semaphore = asyncio.Semaphore(10)
TASK_ROUTES = {i: f"task_{i}" for i in range(1, 49)}


# foodpanda_uber_all_blocker_infinite.text
import time
import datetime
import os

# ==================== 設定區 ====================
REMIND_INTERVAL_SECONDS = 900          # 15分鐘提醒一次（可自行修改）
ALERT_TITLE = "【無限全平台阻擋】foodpanda + Uber (含三媽)"
ALERT_MESSAGE = "⚠️ 偵測到外送訂單提醒！\n請手動拒絕所有熊貓、Uber，以及三媽的訂單"
# ================================================

def log_alert(message):
    if not os.path.exists("log"):
        os.makedirs("log")
    with open("log/blocker_infinite.log", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {message}\n")

def send_alert():
    # 強提醒（終端機 + 簡單 beep）
    print("\n" + "="*60)
    print("🚨🚨🚨  【外送無限阻擋提醒】 🚨🚨🚨")
    print(ALERT_TITLE)
    print(ALERT_MESSAGE)
    print("="*60)
    
    # 簡單聲音提示（重複 beeps）
    try:
        print('\a')  # 系統提示音
        time.sleep(0.3)
        print('\a')
        time.sleep(0.3)
        print('\a')
    except:
        pass
    
    log_alert("無限全平台阻擋提醒已發送")

def main():
    print("=== foodpanda + Uber + 三媽 無限全平台阻擋程式 v3.0（零依賴版） ===")
    print("⚡ 已取消 7 天限制，改為【無限循環】執行")
    print(f"提醒間隔：{REMIND_INTERVAL_SECONDS//60} 分鐘一次")
    print("適合你跑車期間放在背景執行\n")
    print("⚠️ 無限循環程式請使用【 Ctrl + C 】手動停止\n")
    
    alert_count = 0
    last_alert = 0
    
    # 原本有 end_time，現在改為 while True 無限循環
    while True:
        try:
            now = time.time()
            if now - last_alert >= REMIND_INTERVAL_SECONDS:
                send_alert()
                alert_count += 1
                last_alert = now
                print(f"第 {alert_count} 次提醒已發送 | 程式仍在無限背景運行中...")
        except KeyboardInterrupt:
            print("\n\n無限阻擋程式已手動停止。")
            break
        except Exception as e:
            print(f"錯誤: {e}")
        
        time.sleep(60)   # 每分鐘檢查一次

if __name__ == "__main__":
    main()
