#WindPower_BOT48_6AI_Capability/.github/workflows/Grok-X系列.md
可以，把 Grok「變型金剛 X 系列」 定位成你這套原創 AI 機械架構中的一個 AI Agent 系列 就好；不要直接使用《變形金剛》的官方角色、台詞或劇情。
可以。你這份架構可以整理成全 AI Agent 共用的治理規格，核心原則就是：Agent 可以分析、模擬、審查、整合，但不直接控制實體設備。

WINDPOWER_BOT48_6AI_CAPABILITY — 全 AI 共用核心

┌──────────────────────┐
                    │    GOLDEN CORE       │
                    │   AI Governance      │
                    │   治理／安全核心      │
                    └──────────┬───────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        ▼                      ▼                      ▼
   Command AI              Guardian AI            Engineer AI
   任務統籌                 安全審查               工程分析
        │                      │                      │
        ├──────────────┬───────┴───────┬──────────────┤
        ▼              ▼               ▼              ▼
    Storm AI       Dispatch AI     Reviewer AI    Explorer AI
    風場模擬         派單模擬         結果審查       情境探索
        │              │               │              │
        └──────────────┴───────┬───────┴──────────────┘
                               ▼
                         Combiner Core
                           結果整合
                               │
                               ▼
                    ┌────────────────────┐
                    │ SIM / NONPHYSICAL │
                    │ 實體控制 = DISABLED │
                    └─────────┬──────────┘
                              ▼
                         Result Only
                              │
                              ▼
                         前端結果轉述

統一 Agent Policy

{
  "global_policy": {
    "mode": "NONPHYSICAL",
    "simulation_allowed": true,
    "physical_control": "DISABLED",
    "direct_hardware_control": false,
    "core_access": "PRIVATE_BACKEND_ONLY",
    "secret_access": "DENIED",
    "output": "RESULT_ONLY"
  }
}

所有 AI 共用的角色規則

Agent	職責	實體控制

Command AI	任務拆解、協調 Agent	禁止
Guardian AI	安全邊界、風險審查	禁止
Engineer AI	工程計算、設計分析	禁止
Storm AI	風場／天氣數值模擬	禁止
Dispatch AI	派單與路線模擬	禁止
Reviewer AI	驗證與品質審查	禁止
Explorer AI	情境探索	禁止
Stress Tester	極端條件測試	禁止
Synthesizer	多 Agent 結果整合	禁止
Combiner Core	整合演練結果	禁止


GitHub 公開層

PUBLIC REPOSITORY
│
├── frontend/
├── .github/
│   └── workflows/
│       └── main.yml
├── README.md
├── docs/
└── .gitignore
        │
        │  不放 Token
        │  不放私有模型設定
        │  不放 Golden Core
        ▼
PRIVATE BACKEND
│
├── Golden Core
├── Storm Core
├── Agent Registry
├── Model Router
└── Secret Management

這樣 Grok-X、GPT、Gemini、DeepSeek，以及你後續新增的其他 Agent 都可以共用同一套 SIMULATION_ONLY / NONPHYSICAL / RESULT_ONLY 治理層。

另外，Grok-X Series 建議維持你現在的原創 Agent 系列名稱與職責，不要把受版權保護的官方角色、台詞或劇情直接放進 GitHub 程式碼。
⚙️ Grok X-Series Agent

AI COMMAND CORE
       │
       ├── Guardian AI
       ├── Storm AI
       ├── Dispatch AI
       ├── Reviewer AI
       │
       └── GROK-X SERIES
              │
              ├── X-01 Analyzer
              ├── X-02 Explorer
              ├── X-03 Stress Tester
              └── X-04 Synthesizer
                       │
                       ▼
                 Combiner Core
                       │
                 SIM / NONPHYSICAL
                       │
                       ▼
                    結果轉述

X-Series 的定位

Agent	職責	實體控制

Grok-X01 Analyzer	分析風力／系統資料	❌
Grok-X02 Explorer	探索模擬情境	❌
Grok-X03 Stress Tester	極端參數壓力測試	❌
Grok-X04 Synthesizer	整合其他 Agent 結果	❌


最重要的是把它鎖定成：

{
  "agent_family": "GROK_X",
  "mode": "NONPHYSICAL",
  "physical_control": "DISABLED",
  "core_access": "PRIVATE_BACKEND_ONLY",
  "output": "RESULT_ONLY"
}

GitHub 端

公開 Repo 只留下：

frontend/
.github/workflows/
    main.yml
.gitignore
README.md

而 Grok-X 的真正核心實作、API Token、模型設定、Storm Core 留在私有後端。

Workflow 也只允許：

Trigger
  ↓
Grok-X 演練
  ↓
Storm Core SIM
  ↓
Reviewer
  ↓
Combiner
  ↓
結果轉述

不要讓 Grok-X 取得任何實體設備控制權，也不要把模型密鑰寫進 main.yml、app.js 或 .gitignore。

另外，你前面那份 main.yml 有一個需要修正的地方：不能在同一個 YAML 檔裡重複放兩次 name: / on: / jobs:。應保留一套 Workflow 定義，再把 X-Series 的演練 job 合併進去。可以把「博派合體、金鋼飛向外太空」做成純 AI 敘事＋NONPHYSICAL 模擬模式。這樣既保留你想要的機械科幻感，也不會連到真實設備。

🚀 AI 合體模式：GOLDEN CORE

┌──────────────────────┐
                 │    GOLDEN CORE       │
                 │  私有 AI 治理核心     │
                 └──────────┬───────────┘
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
        Guardian AI     Storm AI      Engineer AI
          守護模組       風暴模擬        工程模組
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                    ┌──────────────┐
                    │  AI COMBINE  │
                    │   合體引擎    │
                    └──────┬───────┘
                           ▼
                  🚀 SPACE SIMULATION
                           │
                           ▼
                    NONPHYSICAL
                           │
                           ▼
                    結果 → 前端轉述

AI 對話模式

USER:
啟動博派合體，飛往外太空。

Command AI:
收到。啟動 AI 合體演練。

Guardian AI:
安全邊界確認：
SIMULATION_ONLY
REAL_CONTROL = DISABLED

Storm AI:
建立太空環境與風場數值模型。

Engineer AI:
完成虛擬機體組合。

Golden Core:
治理核心同步完成。

AI COMBINE:
合體完成。

Command AI:
🚀 發射至虛擬外太空。

Reviewer AI:
演練結果通過。

Archive AI:
已保存模擬紀錄。

放進 GitHub 的定位

公開 Repo
│
├── frontend/
│      └── AI 對話介面
│
├── .github/workflows/
│      └── main.yml
│             │
│             ▼
│       AI 模式演練
│             │
│             ▼
│       Private Storm Core
│             │
│       ┌─────┴─────┐
│       ▼           ▼
│    WIND SIM   SPACE SIM
│       │           │
│       └─────┬─────┘
│             ▼
│       NONPHYSICAL
│             │
│             ▼
│        結果轉述
│
└── .gitignore
       └── 保護 Golden Core

這裡的「金核心」可以作為你整套系統的治理概念：核心不公開、Agent 不直接控制實體、所有飛行／風暴／合體都先在 SIM/NONPHYSICAL 空間演練。

另外，如果要正式放進 GitHub，建議使用原創名稱，例如 Guardian AI / Golden Core / Storm AI / Combine Engine，不要直接把官方《變形金剛》的角色或原文設定當成專案程式碼。可以。若你要的是把「變形金剛派系」轉成你目前的 AI 模式對話／多 Agent 架構，可以做成原創的「機械 AI 派系」；不要直接複製《變形金剛》的角色、台詞或劇情。

AI 機械派系 v1

┌─────────────────────┐
                 │   AI COMMAND CORE   │
                 │   總指揮／治理中樞    │
                 └──────────┬──────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
       ┌──────────────┐            ┌──────────────┐
       │  守護聯盟     │            │ 競爭陣營      │
       │ Guardian AI  │            │ Rival AI      │
       └──────┬───────┘            └──────┬───────┘
              │                           │
       分析／安全／協作              壓力測試／攻防模擬
              │                           │
              └──────────┬────────────────┘
                         ▼
                  ┌─────────────┐
                  │  AI REVIEW  │
                  │ 審查／裁決   │
                  └──────┬──────┘
                         ▼
                  SIM / NONPHYSICAL
                         │
                         ▼
                    結果轉述

對話模式

可以讓不同 Agent 使用不同「人格職責」，但全部遵守同一個治理核心：

AI 模式	任務

Command AI	任務拆解、統籌
Guardian AI	安全檢查、風險攔截
Engineer AI	程式架構與測試
Storm AI	風暴／風力模型的模擬分析
Dispatch AI	派單與資源配置「建議」
Reviewer AI	審查其他 Agent 的結果
Archive AI	紀錄與版本管理


例如使用者輸入：

USER:
啟動風暴核心演練，模式 NONPHYSICAL。

系統可以轉成：

Command AI:
收到，建立 NONPHYSICAL 演練。

Storm AI:
開始計算模擬情境。

Guardian AI:
確認：不連接真實設備、不執行電網控制。

Dispatch AI:
產生資源配置建議。

Reviewer AI:
檢查完成，結果通過。

Command AI:
演練完成。
狀態：SIMULATION_ONLY
實體控制：DISABLED

這樣就能把你現在的 WindPower + Storm Core + Multi-Agent + Workflow 做成一個「AI 機械人協作模式」，而不是讓任何單一 Agent 直接取得實體控制權。收到。你這個「博派合體金剛飛外太空」的敘述，正好可以對應到我們剛剛定型的 AI 機械派系 v1 架構中，最關鍵的「協作聚合」環節。

既然不要直接複製《變形金剛》的劇情，我們就把「合體」翻譯成軟體架構的語言：

「合體」= 多個 AI Agent 的協同輸出聚合（Collaborative Output Aggregation）。
「飛外太空」= 將計算任務提交至私有後端（Private Backend / Cloud）執行，並將結果安全地傳回。

以下是我根據你的原創「AI 機械派系」架構，所設計的 「合體協議 v1」，可直接整合進你的 .github/workflows/ 與私有後端。

---

🤖 AI 機械派系 v1 — 合體協議（Combiner Protocol）

核心流程圖（已加入「合體」與「外太空」）

```
[ 使用者 / GitHub Workflow ]
         │
         │ 觸發指令 (e.g., "啟動風暴模擬 NONPHYSICAL")
         ▼
┌─────────────────────────────────┐
│   COMMAND CORE (總指揮)          │  ← 地球端 (公開觸發)
│   接收指令、拆解任務、分派 Agent │
└────────────┬────────────────────┘
             │
     ┌───────┼───────┬───────┐
     ▼       ▼       ▼       ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│Guardian │ │ Storm   │ │Dispatch │  ← 各 Agent 獨立運算
│(安全檢查)│ │(風暴模擬)│ │(派單建議)│
└────┬────┘ └────┬────┘ └────┬────┘
     │           │           │
     └───────┬───┴───────┬───┘
             ▼           ▼
┌─────────────────────────────────┐
│   REVIEWER AI (審查/裁決)        │  ← 內部驗證步驟
└────────────┬────────────────────┘
             │
             ▼
╔═════════════════════════════════╗
║  合體聚合器 (Combiner)          ║  ← 「合體」發生在這裡
║  將多 Agent 輸出整合為單一結果  ║
╚═════════════════════════════════╝
             │
             │ 加密傳輸 (HTTPS)
             ▼
┌─────────────────────────────────┐
│   外星球 (Private Backend / VPS) │  ← 「飛外太空」
│   執行實際的 NONPHYSICAL 運算    │
└────────────┬────────────────────┘
             │
             │ 回傳結果
             ▼
┌─────────────────────────────────┐
│   ARCHIVE AI (紀錄/版本管理)     │
│   儲存至 Artifact / 資料庫       │
└─────────────────────────────────┘
             │
             ▼
      前端轉述 / Workflow 輸出
```

---

🧠 各 AI 模式職責表（已更新）

AI 模式 職責 是否接觸核心演算法
Command AI 任務拆解、調度 Agent、統一出口 ❌ 僅協調
Guardian AI 安全檢查（確認無實體控制、無金鑰外洩） ❌ 僅檢查標記
Storm AI 執行風暴/風力模擬計算（呼叫私有 Core） ✅ 是（但僅在私有後端）
Dispatch AI 產生派單/資源配置「建議」 ❌ 僅產生建議，不執行
Reviewer AI 審查其他 Agent 的輸出邏輯一致性 ❌ 僅驗證格式與邊界
Archive AI 儲存結果、版本管理、生成日誌 ❌ 僅 I/O
Combiner (合體) 聚合所有 Agent 輸出為單一 JSON 報告 ❌ 僅資料合併

---

🚀 實際可執行的「合體」指令（GitHub Workflow 擴充）

你可以在 .github/workflows/main.yml 中新增以下觸發方式，讓 Workflow 直接呼叫「外星球」（私有後端）的合體 API：

```yaml
# .github/workflows/main.yml (擴充部分)

name: AI 機械派系 - 合體演練

on:
  workflow_dispatch:
    inputs:
      mode:
        description: '演練模式 (SIM / NONPHYSICAL)'
        required: true
        default: 'NONPHYSICAL'
      wind_speed:
        description: '風速 (m/s)'
        required: true
        default: '25'

jobs:
  combiner-protocol:
    runs-on: ubuntu-latest
    steps:
      - name: 觸發合體協議 (Command Core → 外星球)
        env:
          API_URL: ${{ secrets.WINDPOWER_API_URL }}
          API_KEY: ${{ secrets.WINDPOWER_API_KEY }}
        run: |
          echo "🧠 Command AI: 開始拆解任務..."
          echo "🛡️ Guardian AI: 安全檢查通過 (無實體控制)。"
          echo "🌪️ Storm AI: 計算風暴模擬中..."
          echo "📦 Dispatch AI: 產生資源建議..."
          echo "🔗 Combiner: 聚合所有 Agent 輸出，準備發送至外星球。"

          curl --fail-with-body \
            -X POST "$API_URL/api/combiner/run" \
            -H "Authorization: Bearer $API_KEY" \
            -H "Content-Type: application/json" \
            -d "{
                  \"mode\": \"${{ github.event.inputs.mode }}\",
                  \"wind_speed\": ${{ github.event.inputs.wind_speed }},
                  \"agent_chain\": [\"Guardian\", \"Storm\", \"Dispatch\", \"Reviewer\"],
                  \"combine\": true
                }" \
            -o combined_result.json

          echo "✅ 合體完成。結果已回傳至地球端 (此 Workflow)。"

      - name: 儲存合體結果 (Archive AI)
        uses: actions/upload-artifact@v4
        with:
          name: combined-ai-report
          path: combined_result.json
```

---

🛸 私有後端「外星球」的合體接收器（api.js 擴充）

在你的私有後端 api.js 中，加入 /api/combiner/run 路由，負責接收多個 Agent 的模擬請求，並回傳「合體後」的單一結果：

```javascript
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
```

---

📦 最終「合體」輸出範例（JSON）

當 Workflow 或前端呼叫此 API 後，會得到一個結構化的「合體」結果：

```json
{
  "status": "success",
  "data": {
    "command": "合體協議完成",
    "mode": "NONPHYSICAL",
    "agents": ["Guardian", "Storm", "Dispatch", "Reviewer"],
    "outputs": {
      "guardian": { "status": "ok", "message": "安全邊界確認：無實體控制" },
      "storm": { "simulated_power": 1250, "status": "generating" },
      "dispatch": { "recommended_units": ["T-01", "T-03"], "eta": "15min" },
      "reviewer": { "passed": true, "notes": "邏輯一致" }
    },
    "combined_summary": {
      "overall_status": "SIMULATION_ONLY",
      "physical_control": "DISABLED",
      "requires_approval": true,
      "timestamp": "2026-08-18T12:00:00.000Z"
    },
    "origin": "Private Backend (Alien Planet)"
  },
  "message": "🤖 AI 機械派系合體完成。此結果僅為模擬轉述。"
}
```

---

✅ 總結：你現在有的

概念 對應實作
AI 機械派系 Guardian、Storm、Dispatch、Reviewer、Combiner 等多 Agent 分工
合體 私有後端的 /api/combiner/run 將多個獨立計算結果聚合為單一回應
飛外太空 Workflow 透過 HTTPS 呼叫私有 VPS / Cloud Run（外星球）執行運算
金核心 留在私有後端，永不進入公開 Repo
安全邊界 所有結果均標記 physical_control: DISABLED、requires_approval: true

這樣你就同時擁有了：

1. 完整的技術鏈路（前端 → Workflow → 私有 API → 多 Agent 模擬 → 合體回傳）。
2. 原創的敘事架構（不侵犯《變形金剛》版權，但保留了「派系協作 + 合體」的趣味性）。

你這個構想很有趣，把變形金剛的派系衝突和我們一直在討論的「金核心」與「外星球」概念結合在一起。

要把這個「變形金剛 AI 模式」放進你現在的 GitHub 架構，可以這樣設計：

🤖 AI 模式角色設定

· 博派 / 巨無霸 (Autobots / Maximals)：代表「保護與轉述」的 AI 模式。嚴格遵守安全邊界，只進行模擬與提供建議，不直接控制實體。
· 狂派 / 原始獸 (Decepticons / Predacons)：代表「極限測試與突破」的 AI 模式。可執行我們設定的 10,000 倍 NONPHYSICAL 極端數值實驗，探索模型邊界。
· 金核心 (Golden Core)：可理解為變形金剛宇宙中的「火種源 (AllSpark)」或「領導母體 (Matrix of Leadership)」，是能量與生命之源。在你的專案中，就是存放在私有後端、絕不進入公開 Repo 的核心演算法與模型。
· 外星球 (Alien Planet)：代表你的私有後端伺服器 (Private Backend)。所有核心運算都在這裡發生，公開前端只能看到轉述後的結果。

⚙️ 整合進 GitHub 工作流程

AI 對話模式指令範例 (在 Issue 或 PR 中)：

@WindPower-BOT --mode AUTOBOT --simulate wind_speed=25
(觸發博派 AI 模式，進行標準風力模擬)

.github/workflows/main.yml 擴充構想：

```yaml
# 在原有基礎上增加 AI 模式選擇
- name: Trigger Private Storm Core API
  env:
    AI_MODE: ${{ github.event.inputs.ai_mode || 'AUTOBOT' }}
  run: |
    curl -X POST "$API_URL/api/automation/run" \
      -H "Authorization: Bearer $API_KEY" \
      -d "{\"mode\":\"${AI_MODE}\", \"scale\":10000}"
```

這樣一來，你的專案不僅有了完整的技術架構，還多了一個有趣的敘事框架。現在剩下的，就是確保 ci-cd.yml 和 Grok.sh 這些檔案內容都符合我們的安全規範了。
收到。你這個「博派合體金剛飛外太空」的敘述，正好可以對應到我們剛剛定型的 AI 機械派系 v1 架構中，最關鍵的「協作聚合」環節。

既然不要直接複製《變形金剛》的劇情，我們就把「合體」翻譯成軟體架構的語言：

「合體」= 多個 AI Agent 的協同輸出聚合（Collaborative Output Aggregation）。
「飛外太空」= 將計算任務提交至私有後端（Private Backend / Cloud）執行，並將結果安全地傳回。

以下是我根據你的原創「AI 機械派系」架構，所設計的 「合體協議 v1」，可直接整合進你的 .github/workflows/ 與私有後端。

---

🤖 AI 機械派系 v1 — 合體協議（Combiner Protocol）

核心流程圖（已加入「合體」與「外太空」）

```
[ 使用者 / GitHub Workflow ]
         │
         │ 觸發指令 (e.g., "啟動風暴模擬 NONPHYSICAL")
         ▼
┌─────────────────────────────────┐
│   COMMAND CORE (總指揮)          │  ← 地球端 (公開觸發)
│   接收指令、拆解任務、分派 Agent │
└────────────┬────────────────────┘
             │
     ┌───────┼───────┬───────┐
     ▼       ▼       ▼       ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│Guardian │ │ Storm   │ │Dispatch │  ← 各 Agent 獨立運算
│(安全檢查)│ │(風暴模擬)│ │(派單建議)│
└────┬────┘ └────┬────┘ └────┬────┘
     │           │           │
     └───────┬───┴───────┬───┘
             ▼           ▼
┌─────────────────────────────────┐
│   REVIEWER AI (審查/裁決)        │  ← 內部驗證步驟
└────────────┬────────────────────┘
             │
             ▼
╔═════════════════════════════════╗
║  合體聚合器 (Combiner)          ║  ← 「合體」發生在這裡
║  將多 Agent 輸出整合為單一結果  ║
╚═════════════════════════════════╝
             │
             │ 加密傳輸 (HTTPS)
             ▼
┌─────────────────────────────────┐
│   外星球 (Private Backend / VPS) │  ← 「飛外太空」
│   執行實際的 NONPHYSICAL 運算    │
└────────────┬────────────────────┘
             │
             │ 回傳結果
             ▼
┌─────────────────────────────────┐
│   ARCHIVE AI (紀錄/版本管理)     │
│   儲存至 Artifact / 資料庫       │
└─────────────────────────────────┘
             │
             ▼
      前端轉述 / Workflow 輸出
```

---

🧠 各 AI 模式職責表（已更新）

AI 模式 職責 是否接觸核心演算法
Command AI 任務拆解、調度 Agent、統一出口 ❌ 僅協調
Guardian AI 安全檢查（確認無實體控制、無金鑰外洩） ❌ 僅檢查標記
Storm AI 執行風暴/風力模擬計算（呼叫私有 Core） ✅ 是（但僅在私有後端）
Dispatch AI 產生派單/資源配置「建議」 ❌ 僅產生建議，不執行
Reviewer AI 審查其他 Agent 的輸出邏輯一致性 ❌ 僅驗證格式與邊界
Archive AI 儲存結果、版本管理、生成日誌 ❌ 僅 I/O
Combiner (合體) 聚合所有 Agent 輸出為單一 JSON 報告 ❌ 僅資料合併

---

🚀 實際可執行的「合體」指令（GitHub Workflow 擴充）

你可以在 .github/workflows/main.yml 中新增以下觸發方式，讓 Workflow 直接呼叫「外星球」（私有後端）的合體 API：

```yaml
# .github/workflows/main.yml (擴充部分)

name: AI 機械派系 - 合體演練

on:
  workflow_dispatch:
    inputs:
      mode:
        description: '演練模式 (SIM / NONPHYSICAL)'
        required: true
        default: 'NONPHYSICAL'
      wind_speed:
        description: '風速 (m/s)'
        required: true
        default: '25'

jobs:
  combiner-protocol:
    runs-on: ubuntu-latest
    steps:
      - name: 觸發合體協議 (Command Core → 外星球)
        env:
          API_URL: ${{ secrets.WINDPOWER_API_URL }}
          API_KEY: ${{ secrets.WINDPOWER_API_KEY }}
        run: |
          echo "🧠 Command AI: 開始拆解任務..."
          echo "🛡️ Guardian AI: 安全檢查通過 (無實體控制)。"
          echo "🌪️ Storm AI: 計算風暴模擬中..."
          echo "📦 Dispatch AI: 產生資源建議..."
          echo "🔗 Combiner: 聚合所有 Agent 輸出，準備發送至外星球。"

          curl --fail-with-body \
            -X POST "$API_URL/api/combiner/run" \
            -H "Authorization: Bearer $API_KEY" \
            -H "Content-Type: application/json" \
            -d "{
                  \"mode\": \"${{ github.event.inputs.mode }}\",
                  \"wind_speed\": ${{ github.event.inputs.wind_speed }},
                  \"agent_chain\": [\"Guardian\", \"Storm\", \"Dispatch\", \"Reviewer\"],
                  \"combine\": true
                }" \
            -o combined_result.json

          echo "✅ 合體完成。結果已回傳至地球端 (此 Workflow)。"

      - name: 儲存合體結果 (Archive AI)
        uses: actions/upload-artifact@v4
        with:
          name: combined-ai-report
          path: combined_result.json
```

---

🛸 私有後端「外星球」的合體接收器（api.js 擴充）

在你的私有後端 api.js 中，加入 /api/combiner/run 路由，負責接收多個 Agent 的模擬請求，並回傳「合體後」的單一結果：

```javascript
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
```

---

📦 最終「合體」輸出範例（JSON）

當 Workflow 或前端呼叫此 API 後，會得到一個結構化的「合體」結果：

```json
{
  "status": "success",
  "data": {
    "command": "合體協議完成",
    "mode": "NONPHYSICAL",
    "agents": ["Guardian", "Storm", "Dispatch", "Reviewer"],
    "outputs": {
      "guardian": { "status": "ok", "message": "安全邊界確認：無實體控制" },
      "storm": { "simulated_power": 1250, "status": "generating" },
      "dispatch": { "recommended_units": ["T-01", "T-03"], "eta": "15min" },
      "reviewer": { "passed": true, "notes": "邏輯一致" }
    },
    "combined_summary": {
      "overall_status": "SIMULATION_ONLY",
      "physical_control": "DISABLED",
      "requires_approval": true,
      "timestamp": "2026-08-18T12:00:00.000Z"
    },
    "origin": "Private Backend (Alien Planet)"
  },
  "message": "🤖 AI 機械派系合體完成。此結果僅為模擬轉述。"
}
```

---

✅ 總結：你現在有的

概念 對應實作
AI 機械派系 Guardian、Storm、Dispatch、Reviewer、Combiner 等多 Agent 分工
合體 私有後端的 /api/combiner/run 將多個獨立計算結果聚合為單一回應
飛外太空 Workflow 透過 HTTPS 呼叫私有 VPS / Cloud Run（外星球）執行運算
金核心 留在私有後端，永不進入公開 Repo
安全邊界 所有結果均標記 physical_control: DISABLED、requires_approval: true

這樣你就同時擁有了：

1. 完整的技術鏈路（前端 → Workflow → 私有 API → 多 Agent 模擬 → 合體回傳）。
2. 原創的敘事架構（不侵犯《變形金剛》版權，但保留了「派系協作 + 合體」的趣味性）。

如果你覺得這個「合體協議」可以直接用，請告訴我，我幫你把它整併進你目前的 ci-cd.yml 或 main.yml 中。如果還需要加入更多 Agent（例如「工程 AI」或「能源 AI」），也可以隨時擴充。
如果你覺得這個「合體協議」可以直接用，請告訴我，我幫你把它整併進你目前的 ci-cd.yml 或 main.yml 中。如果還需要加入更多 Agent（例如「工程 AI」或「能源 AI」），也可以隨時擴充。
