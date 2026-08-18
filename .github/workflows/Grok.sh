// ==========================================
// Uber Driver 廉價與雷達單自動過濾腳本
// ==========================================
name: Run Grok
  run: bash Grok.sh
  chmod +x Grok.sh
const MIN_PRICE_PER_KM = 28; // 低於 28 元就拒
let blockCount = 0; // 今日拒單計數器

auto.waitFor();
toastLog("⚡ 過濾腳本已開啟，歡迎光臨 28 元/公里 俱樂部");

setInterval(() => {
    // 抓取螢幕上出現的「元」與「公里」資訊
    let priceNodes = textMatches(/.*元.*/).find();
    let distNodes = textMatches(/.*公里.*/).find();

    if (priceNodes.length === 0 || distNodes.length === 0) return;

    // 簡單抓取最近的數字（實際應用可依 UI 結構優化）
    let price = parseFloat(priceNodes[0].text().replace(/[^0-9.]/g, ""));
    let dist = parseFloat(distNodes[0].text().replace(/[^0-9.]/g, ""));

    if (!price || !dist) return;

    let unitPrice = price / dist;

    // 如果低於門檻
    if (unitPrice < MIN_PRICE_PER_KM) {
        let delay = random(1500, 3000); // 模擬人類 1.5~3 秒猶豫時間
        sleep(delay);
        
        // 尋找「拒絕」或「忽略」按鈕 (通用寫法)
        let btn = text("拒絕").findOne(1000) || text("忽略").findOne(1000) || text("不接").findOne(1000);
        
        if (btn) {
            // 隨機偏移點擊座標，避免每次點擊正中心
            let b = btn.bounds();
            click(b.centerX() + random(-15, 15), b.centerY() + random(-15, 15));
            
            blockCount++;
            toastLog(`🚫 已拒絕 ${unitPrice.toFixed(1)}元/公里 (今日已拒 ${blockCount} 單)`);
        }
    }
}, 1500); // 每 1.5 秒檢查一次
python foodpanda_uber_all_blocker_test_zero.py
// ==========================================
// Auto.js 腳本：Uber Driver 低價單自動過濾（含雷達單）
// ==========================================

// 1. 設定目標門檻
const TARGET_PRICE_PER_KM = 28; 
let isProcessing = false; // 防止重複觸發的旗標

// 2. 啟動無障礙服務
auto.waitFor();
toastLog("🚀 Uber 自動過濾(含雷達)已啟動");

// 主要循環，每 1.5 秒檢查一次
setInterval(() => {
    if (isProcessing) return;
    isProcessing = true;

    try {
        // ---------- 環節 A：解析畫面數據 ----------
        let price = null;
        let distance = null;
        let pricePerKm = 0;

        // 抓取當前畫面所有節點
        let allNodes = text().find();
        allNodes.forEach(node => {
            let txt = node.text();
            if (txt && txt.includes("公里") && !distance) {
                distance = parseFloat(txt.replace(/[^0-9.]/g, ""));
            }
            if (txt && txt.includes("元") && !price) {
                price = parseFloat(txt.replace(/[^0-9.]/g, ""));
            }
        });

        if (!distance || !price) {
            isProcessing = false;
            return; // 沒有金額或里程數據，跳過
        }

        pricePerKm = price / distance;

        // ---------- 環節 B：判斷是否低於門檻 ----------
        if (pricePerKm < TARGET_PRICE_PER_KM) {
            let msg = `⚠️ 低價單偵測！ ${pricePerKm.toFixed(2)} 元/公里 (<${TARGET_PRICE_PER_KM})`;

            // 隨機延遲 2~4 秒 (演得像真人思考)
            let delayTime = random(2000, 4000);
            toastLog(`${msg}， ${(delayTime/1000).toFixed(1)}秒後拒絕`);
            sleep(delayTime);

            // ---------- 環節 C：執行拒單動作 ----------
            // 抓取目前的「拒絕」或「忽略」按鈕
            let actionBtn = text("拒絕").findOne(1000) || text("忽略").findOne(1000);

            if (actionBtn) {
                // 模擬真人點擊（帶隨機偏移）
                let b = actionBtn.bounds();
                click(b.centerX() + random(-10, 10), b.centerY() + random(-10, 10));
                toastLog(`✅ 已自動拒絕雷達/派單 (${pricePerKm.toFixed(2)}元/km)`);
            } else {
                // 如果找不到按鈕，且是雷達單，嘗試點擊右上角關閉 (僅適用部分UI)
                // 或等待倒數結束自動忽略
                toastLog("❌ 找不到拒絕/忽略按鈕，請確認手機UI版本");
            }
        } else {
            // 價格達標，紀錄但不動作
            // console.log(`✅ 正常單， $${pricePerKm.toFixed(2)} 元/km`);
        }

    } catch (e) {
        console.error("腳本發生錯誤:", e);
    } finally {
        isProcessing = false;
    }

}, 1500); // 每 1.5 秒執行一次
// ==========================================
// Auto.js 腳本：Uber Driver 低價單自動拒絕
// ==========================================

// 1. 設定目標門檻
const TARGET_PRICE_PER_KM = 28; 

// 2. 監聽通知或 UI 變化
auto.waitFor(); // 等待無障礙服務啟動
toastLog("🚀 Uber 自動過濾腳本已啟動");

// 每 2 秒檢查一次畫面
setInterval(() => {
    // 抓取當前螢幕上的所有文字節點
    let screenText = text().findOne(1000); 
    if (!screenText) return;

    // 3. 解析數據 (這裡需要根據實際畫面抓取，建議用 OCR 或找特定 ID)
    // 假設我們透過正規表達式去抓取畫面上的「公里」和「元」字眼
    let distance = null;
    let price = null;
    
    // 遍歷畫面中的節點來尋找關鍵字
    // 這裡是示意寫法，實際請用 UI 樹查看器找出 Uber 特定的 id
    text().find().forEach(node => {
        let txt = node.text();
        if (txt && txt.includes("公里")) {
            distance = parseFloat(txt.replace(/[^0-9.]/g, "")); // 提取數字
        }
        if (txt && txt.includes("元")) {
            price = parseFloat(txt.replace(/[^0-9.]/g, ""));    // 提取數字
        }
    });

    // 4. 計算與判斷
    if (distance && price) {
        let pricePerKm = price / distance;
        let msg = `目前單價：${pricePerKm.toFixed(2)} 元/公里`;

        if (pricePerKm < TARGET_PRICE_PER_KM) {
            toastLog(`⚠️ ${msg}，低於 ${TARGET_PRICE_PER_KM} 元，準備拒絕！`);
            
            // 為了躲過風控，這裡加入人類隨機點擊延遲 (1.5秒 ~ 3秒)
            let delayTime = random(1500, 3000); 
            sleep(delayTime);

            // 5. 模擬點擊「拒絕」按鈕
            // 找「拒絕」按鈕方式有兩種：
            // A. 直接找文字 (穩定) -> text("拒絕").findOne(2000)?.click();
            // B. 找座標 (針對沒有文字的圖標)
            let rejectBtn = text("拒絕").findOne(2000);
            if(rejectBtn){
                // 使用隨機座標偏移，避免每次都精確點擊正中心 (更像真人)
                let b = rejectBtn.bounds();
                click(b.centerX() + random(-10, 10), b.centerY() + random(-10, 10));
                toastLog("✅ 已自動拒絕低價單");
            } else {
                toastLog("❌ 找不到拒絕按鈕");
            }
        } else {
            // 價格達標，不動作
            console.log(`✅ ${msg}，符合標準`);
        }
    }
}, 2000); // 每2秒執行一次
/**
 * Uber Driver 低里程車資拒單腳本
 * 條件：1公里低於 28 元自動拒絕
 */

auto.waitFor(); // 等待無障礙服務啟動
toast("Uber 自動拒單腳本已啟動");

// 模擬人類操作的隨機延遲 (防止風控)
function randomSleep(min, max) {
    let time = Math.floor(Math.random() * (max - min + 1)) + min;
    sleep(time);
}

// 持續監聽
while (true) {
    // 1. 監聽 Uber 通知 (為了避免卡住，這裡用最簡單的輪詢抓取螢幕內容)
    // 更進階的寫法可以用 notificationObserver 監聽通知列
    let uiObject = textContains("元").findOnce(); 
    let distObject = textContains("公里").findOnce();
    
    if (uiObject && distObject) {
        // 2. 正規表達式萃取數值
        let fareText = uiObject.text();
        let distText = distObject.text();
        
        // 假設抓到字串為 "預估車資 25 元" 和 "距離 1.0 公里"
        let fareMatch = fareText.match(/(\d+)/);
        let distMatch = distText.match(/([\d.]+)/);
        
        if (fareMatch && distMatch) {
            let fare = parseFloat(fareMatch[0]);
            let dist = parseFloat(distMatch[0]);

            // 3. 數學計算與判斷
            if (dist > 0) {
                let pricePerKm = fare / dist;
                console.log("本次單價: " + pricePerKm + " 元/公里");

                if (pricePerKm < 28) {
                    toastLog("⚠️ 低於 28 元/公里，準備自動拒絕！");
                    
                    // 4. 關鍵：拒絕動作
                    // 建議使用文字點擊 "拒絕" (文字通常比座標更穩定)
                    let rejectBtn = text("拒絕").findOne(2000);
                    // 或者是找 "不接"、"取消" 按鈕
                    if (rejectBtn) {
                        // 模擬人類延遲：先停頓 1~3 秒再點擊
                        randomSleep(1000, 3000);
                        rejectBtn.click();
                        console.log("✅ 已自動拒絕此單");
                    } else {
                        console.log("⚠️ 找不到拒絕按鈕，可能已過期");
                    }
                }
            }
        }
    }
    
    // 避免死循環過度消耗效能與觸發風控
    sleep(500);
}
# foodpanda_uber_all_blocker_infinite.py
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
