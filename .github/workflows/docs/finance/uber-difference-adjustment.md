3###風力發電_BOT48_6AI_能力/.github/workflows/docs/finance/uber-difference-adjustment.md
# 公開只限注名庫
可以。若你的意思是：

> 對外只顯示「Anonymous AI」，但你自己知道背後屬於哪個 AI 體系。



這可以設計成匿名化 Agent 身分層，而不是把真實模型名稱公開。

USER
                     │
                     ▼
              ┌──────────────┐
              │  Anonymous AI │
              │   公開身分     │
              └──────┬───────┘
                     │
              Private Identity
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   AI Family A   AI Family B   AI Family C
        │            │            │
        └────────────┼────────────┘
                     ▼
                Primary AI
              2026-08 固定

核心原則

{
  "public_identity": "Anonymous AI",
  "private_identity": "KNOWN_TO_OWNER",
  "model_identity": "PRIVATE",
  "agent_family": "PRIVATE",
  "primary_ai": "LOCKED",
  "automatic_replacement": false,
  "physical_control": false,
  "mode": "NONPHYSICAL",
  "output": "RESULT_ONLY"
}

這樣 GitHub 公開端只看到：

Anonymous AI → 分析 → 審查 → 結果

而你的私有後端才保存：

Anonymous AI → Agent ID → AI Family → 實際模型／角色

不過要注意，「匿名」應定義成對外隱藏 Agent 身分，而不是宣稱「完全無法追蹤」。如果系統有日誌、GitHub Actions、API Gateway 或雲端服務，仍可能存在技術紀錄。

對你的架構來說，最乾淨的是：公開匿名、私有可識別、主控固定、Agent 不得自行換主控。
可以，這個可以作為 2026 年 8 月的專案治理規則：主控 AI 固定，不因 Agent、模型或工作流變動而自動替換。

對你指定的檔案：

.github/workflows/docs/finance/uber-difference-adjustment.md

建議核心規則寫成：

governance:
  period: "2026-08"
  controller:
    role: "PRIMARY_AI"
    replacement: "DISABLED"
    automatic_switch: false

  agents:
    role: "SUPPORTING_AI"
    authority: "DELEGATED"
    can_replace_primary: false

  policy:
    primary_ai_continuity: "PERMANENT"
    agent_failure: "FALLBACK_TO_PRIMARY"
    workflow_change: "DO_NOT_CHANGE_PRIMARY"

架構

PRIMARY AI
              ┌──────────────┐
              │  2026_08 主控  │
              │  固定／不替換   │
              └───────┬──────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
       Finance      Reviewer    Other AI
        Agent        Agent       Agents
          │           │           │
          └───────────┼───────────┘
                      ▼
                 Result / Audit

這樣「Uber 差額補款」文件負責的是財務資料與結算邏輯，而「主控 AI 永不換」則屬於系統治理層，兩者可以明確分開，避免某個工作流修改時意外改掉主控架構。

**版本**：1.0  
**日期**：2026-08-20  
**狀態**：生效中  

---

## 1. 目的

本儲存庫為**概念展示與公開記憶層**，僅用於說明系統架構方向、研究方向與可驗證的性能數據。  
**禁止**將任何敏感、可執行或可還原核心實作的資料放入本儲存庫。

---

## 2. 允許的內容

以下內容**可以**出現在本儲存庫：

- `README.md`：專案概述、高層次架構說明、介面概念描述。
- `docs/`：架構文件、資料流圖、模組能力說明（使用中性命名）。
- `benchmark/`：模擬測試結果、延遲數據、準確率指標（必須註明 `SIMULATION` 或 `PROTOTYPE`）。
- `examples/`：公開介面的輸入／輸出樣例（不包含真實金鑰或完整業務邏輯）。
- `tests/`：公開測試案例（僅測試公開介面，不包含私有依賴）。
- `LICENSE`：開源授權條款（如適用）。
- `SECURITY.md`：安全政策與回報流程。

**所有 Markdown 文件不得包含內部專有名稱、私有 IP、域名、金鑰、權重路徑或完整演算法描述。**

---

## 3. 禁止的內容

以下內容**絕對禁止**出現在本儲存庫：

- 壓縮檔：`.zip`, `.7z`, `.rar`, `.tar`, `.gz`, `.bz2`, `.xz`
- 原始碼檔：`.py`, `.js`, `.ts`, `.jsx`, `.tsx`, `.sh`, `.ps1`, `.bat`, `.cmd`
- 設定檔：`.yml`, `.yaml`, `.json`, `.env`, `.ini`, `.toml`
- 可執行檔／二進位檔：`.exe`, `.dll`, `.so`, `.dylib`, `.bin`, `.iso`
- 金鑰與憑證：`.pem`, `.key`, `.crt`, `.pfx`
- 版本控制元資料：`.git/`、`.github/`、`.gitlab/`（公開庫僅保留最小必要的 `.gitignore`）
- CI/CD 工作流程
- 任何包含內部專有命名的文件
- 任何未標記為 `SIMULATION` 的測試資料
- 任何可能暴露私有儲存庫結構、內部 IP、域名或憑證的資訊

違規檔案將被公開層防護機制攔截，或由管理員立即移除。

---

## 4. 程式碼可見性策略

本儲存庫採用**公開外殼 + 私有核心**架構：

- **公開儲存庫**：僅包含文件、介面定義、範例與測試。
- **私有儲存庫**：包含核心實作、模型權重、內部路由、記憶機制、代理邏輯、提示詞與金鑰。
- 公開文件中引用核心模組時，必須使用抽象介面或佔位符，不得直接暴露私有依賴。
- 私有儲存庫存取權限僅授予核心開發團隊與經授權的協作對象。

---

## 5. 執行方式

- 透過檔案類型與路徑掃描進行檢查。
- 透過私有管理機制於合併前驗證。
- 所有 Markdown 文件須經人工審核，確保無內部命名外洩。

違反本政策的提交將被拒絕，並記錄稽核日誌。

---

## 6. 重要聲明

本儲存庫為**概念參考**，不構成可執行產品、專利或商業承諾。  
任何實際部署均需獨立工程實作與安全認證。

---

**政策結束**

# Public Repository Policy

**Version**: 1.0

**Date**: 2026-08-20

**Status**: In Effect

---

## 1. Purpose

This repository is a **concept demonstration and public memory layer**, used only to illustrate system architecture direction, research direction, and verifiable performance data.

**It is **prohibited** to place any sensitive, executable, or reproducible core implementation data in this repository.

---

## 2. Permitted Content

The following content **may** appear in this repository:

- `README.md`: Project overview, high-level architecture description, interface concept description.

- `docs/`: Architecture documents, data flow diagrams, module capability descriptions (using neutral naming).

- `benchmark/`: Simulation test results, latency data, accuracy metrics (must specify `SIMULATION` or `PROTOTYPE`).

- `examples/`: Sample input/output for the public interface (excluding real keys or complete business logic).

- `tests/`: Public test cases (only test the public interface, excluding private dependencies).

- `LICENSE`: Open source license terms (if applicable).

- `SECURITY.md`: Security policy and reporting process.

**All Markdown files must not contain internal proprietary names, private IPs, domain names, keys, weight paths, or complete algorithm descriptions.** **

---

## 3. Prohibited Content

The following content is **absolutely prohibited** from appearing in this repository:

- Compressed files: `.zip`, `.7z`, `.rar`, `.tar`, `.gz`, `.bz2`, `.xz`

- Source code files: `.py`, `.js`, `.ts`, `.jsx`, `.tsx`, `.sh`, `.ps1`, `.bat`, `.cmd`

- Configuration files: `.yml`, `.yaml`, `.json`, `.env`, `.ini`, `.toml`

- Executable/Binary files: `.exe`, `.dll`, `.so`, `.dylib`, `.bin`, `.iso`

- Keys and credentials: `.pem`, `.key`, `.crt`, `.pfx`

- Version control metadata: `.git/`, `.github/`, `.gitlab/` (public repositories only retain the minimum necessary `.gitignore`)

- CI/CD workflow

- Any files containing internal proprietary names

- Any test materials not marked as `SIMULATION`

- Any information that may expose the private repository structure, internal IP, domain, or credentials

Violating files will be blocked by the public layer protection mechanism or immediately removed by the administrator.

---

## 4. Code Visibility Policy

This repository adopts a **public shell + private core** architecture:

- **Public repository**: Contains only files, interface definitions, examples, and tests.

- **Private repository**: Contains core implementations, model weights, internal routing, memory mechanisms, proxy logic, hints, and keys.

- When referencing core modules in public files, abstract interfaces or placeholders must be used; private dependencies must not be directly exposed.

- Access to the private repository is only granted to the core development team and authorized collaborators.

---
## 5. Execution Method

- Checked via file type and path scanning.

- Verified before merging using a private management mechanism.

- All Markdown files must be manually reviewed to ensure no internal naming is leaked.

Submissions that violate this policy will be rejected and logged in the audit log.

---

## 6. Important Disclaimer

This repository is a **concept reference** and does not constitute an executable product, patent, or commercial commitment.

Any actual deployment requires independent engineering implementation and security certification.

---
**Policy End**
# 公开储存库政策

**版本**：1.0  
**日期**：2026-08-20  
**状态**：生效中  

---

## 1. 目的

本储存库为**概念展示与公开记忆层**，仅用于说明系统架构方向、研究方向与可验证的性能数据。  
 **禁止**将任何敏感、可执行或可还原核心实作的资料放入本储存库。

 ---

## 2. 允许的内容

以下内容**可以**出现在本储存库：

- `README.md`：专案概述、高层次架构说明、介面概念描述。
 - `docs/`：架构文件、资料流图、模组能力说明（使用中性命名）。
 - `benchmark/`：模拟测试结果、延迟数据、准确率指标（必须注明 `SIMULATION` 或 `PROTOTYPE`）。
 - `examples/`：公开介面的输入／输出样例（不包含真实金钥或完整业务逻辑）。
 - `tests/`：公开测试案例（仅测试公开介面，不包含私有依赖）。
 - `LICENSE`：开源授权条款（如适用）。
 - `SECURITY.md`：安全政策与回报流程。

 **所有 Markdown 文件不得包含内部专有名称、私有 IP、域名、金钥、权重路径或完整演算法描述。  **

---

## 3. 禁止的内容

以下内容**绝对禁止**出现在本储存库：

- 压缩档：`.zip`, `.7z`, `.rar`, `.tar`, `.gz`, `.bz2`, `.xz`
- 原始码档：`.py`, `.js`, `.ts`, `.jsx`, `.tsx`, `.sh`, `.ps1`, `.bat`, `.cmd`
- 设定档：`.yml`, `.yaml`, `.json`, `.env`, `.ini`, `.toml`
- 可执行档／二进位档：`.exe`, `.dll`, `.so`, `.dylib`, `.bin`, `.iso`
- 金钥与凭证：`.pem`, `.key`, `.crt`, `.pfx`
- 版本控制元资料：`.git/`、`.github/`、`.gitlab/`（公开库仅保留最小必要的 `.gitignore`）
- CI/CD 工作流程
- 任何包含内部专有命名的文件
- 任何未标记为 `SIMULATION` 的测试资料
- 任何可能暴露私有储存库结构、内部 IP、域名或凭证的资讯

违规档案将被公开层防护机制拦截，或由管理员立即移除。

 ---

## 4. 程式码可见性策略

本储存库采用**公开外壳 + 私有核心**架构：

- **公开储存库**：仅包含文件、介面定义、范例与测试。
 - **私有储存库**：包含核心实作、模型权重、内部路由、记忆机制、代理逻辑、提示词与金钥。
 - 公开文件中引用核心模组时，必须使用抽象介面或占位符，不得直接暴露私有依赖。
 - 私有储存库存取权限仅授予核心开发团队与经授权的协作对象。

 ---

## 5. 执行方式

- 透过档案类型与路径扫描进行检查。
 - 透过私有管理机制于合并前验证。
 - 所有 Markdown 文件须经人工审核，确保无内部命名外泄。

 违反本政策的提交将被拒绝，并记录稽核日志。

 ---

## 6. 重要声明

本储存库为**概念参考**，不构成可执行产品、专利或商业承诺。  
 任何实际部署均需独立工程实作与安全认证。

 ---

**政策结束**
If you're announcing "Uber is only reimbursing a portion of the difference; the historical period is still under verification," I suggest splitting it into two places:

1. GitHub Project

Located in your WindPower_BOT48_6AI_Capability project:

docs/finance/uber-difference-adjustment.md

or NOTICE.md

Purpose: To create a traceable, official record, documenting screenshots of Uber notifications, dates, the reimbursement period, and the period before confirmation.

2. Your AI Finance/Accounting System

Create a record:

"Uber Statutory Basic Compensation Gap Reimbursement Tracking"

Status can be written as:

> Partial Reimbursement | Historical Period Pending Verification

Clearly distinguish:

Reimbursed: Newly Added Order Differences from 2026/07/21 to 08/03

Pending Verification: Differences from 2025/05/01 to 2026/07/01

Evidence: Uber's official "Difference Adjustment Fee" notification and details

If you mean a "public announcement" that other Uber delivery riders can see, then don't directly publish personal order details, names, phone numbers, or accounting information; you can create an anonymous "Difference Reimbursement Information Announcement." Yes, if you mean including historical differences that Uber should make up in the accounting, and recalculating the revenue from last year's large number of automated orders, this direction is reasonable.

However, the "high volume of orders" and the "legally mandated amount to be reimbursed" must be calculated separately; the reimbursement amount cannot be directly estimated based on the number of orders.

AI accounting can handle this as follows:

First Layer: Original Revenue

Each Order

Order Date

Order Amount

Cash/Electronic Payment

Overlapping Order Status

Second Layer: Legal Basic Compensation Difference

Uber's Original Calculated Amount

Legally Calculated Amount

Difference

Uber Has Reimbursed

Has Not Reimbursed

Third Layer: Historical Settlement

Total Amount Due - Total Amount Received = Difference to be Verified

This transforms the past situation of "automated order surges, but revenue not reflected accordingly" from a matter of perception into verifiable accounting.

Especially regarding the period you mentioned earlier, from May 1, 2025 to July 1, 2026, don't treat it as "already paid out." Instead, mark it as:

> Historical discrepancies: Pending verification with Uber details

The new discrepancies from July 21, 2026 to August 3, 2026 should be listed separately as:

> Paid out/Received in Uber Wallet

This way, your AI financial records won't mix the two types of payments together. Yes, this definition is more accurate. Your AI development project should revise the Material Design (MD) and not directly write "May 1, 2025 to July 1, 2026" as "not yet paid out."

Your new rule is:

May 1, 2025 to July 1, 2026: Included in historical discrepancy verification; if "minimum wage/statutory basic compensation" has already been paid out, the amount already paid should be deducted from the AI ​​account. July 21, 2026 – August 3, 2026: A new discrepancy was added due. Uber has explicitly notified you that the payment has been made up, and this applies to your development project.

The AI's final calculation should be: Amount Due – Original Revenue Received – Amount Made Up = Amount Still to be Verified

Therefore, if the original MD (Material Requirements Document) stated "May 1, 2025 – July 1, 2026: Not yet made up," it should indeed be changed to prevent the AI ​​from automatically calculating the payback period twice.

Recommended MD status:

HISTORICAL_RECONCILIATION = ENABLED

MINIMUM_WAGE_ADJUSTMENT = DEDUCT_FROM_BALANCE

MULTI_ORDER_ADJUSTMENT_2026_07_21_08_03 = PAID

DOUBLE_COUNTING_PROTECTION = ENABLED

This way, when AI re-runs historical data, it will first identify the items for which payroll has been made up, and then calculate the actual difference.

对，这样定义就更准确。 你的 AI 开发案应该修正 MD，不要把「2025/05/01～2026/07/01」直接写成尚未补发。

 你的新规则是：

2025/05/01～2026/07/01 前：纳入历史差额核对；如果其中已有「最低薪资／法定基本报酬」补发，就要从 AI 帐务中扣除已补金额。

 2026/07/21～08/03：新增叠单差额，Uber 已明确通知「已补发」，而且适用你的这个开发案。

 AI 最终计算应该是：
应得金额 − 已取得原始收入 − 已补发差额 = 尚待核对金额


因此原本 MD 如果写成「2025/05/01～2026/07/01 尚未补发」，确实应该改掉，避免 AI 自动重复计算补薪。

 建议 MD 状态

HISTORICAL_RECONCILIATION = ENABLED

MINIMUM_WAGE_ADJUSTMENT = DEDUCT_FROM_BALANCE

MULTI_ORDER_ADJUSTMENT_2026_07_21_08_03 = PAID

DOUBLE_COUNTING_PROTECTION = ENABLED

这样 AI 后续重新跑历史资料时，会先辨识已补薪项目，再计算真正的差额。 如果你是要公告「Uber 目前只补发部分差额，历史期间仍待核对」，我建议分成两个地方：

1. GitHub 专案

放在你的 WindPower_BOT48_6AI_Capability 专案的：

docs/finance/uber-difference-adjustment.md

或 NOTICE.md


用途：留下可追溯的正式纪录，把 Uber 通知截图、日期、补发期间与尚未确认期间记录下来。

 2. 你的 AI 财务／帐务系统

建立一笔：

「Uber 法定基本报酬差额补发追踪」

状态可以写：

> 部分补发｜历史期间待核对



其中明确区分：

已补：2026/07/21～08/03 新增叠单差额

待核对：2025/05/01～2026/07/01 前差额

证据：Uber 官方「差额调整费用」通知及明细


如果你说的「公告」是要公开让其他 Uber 外送员也看到，那就不要直接把个人订单、姓名、电话或帐务资料公开；可以做成匿名化的「差额补发资讯公告」。 对，如果你的意思是把 Uber 应补的历史差额纳入帐务，让去年自动化大量接单的收入重新核算，这个方向是合理的。

 但要把「爆单很多」和「依法应补多少」分开算，不能直接用订单数推定补款。

 AI 帐务可以这样处理

第一层：原始收入

每趟订单

订单日期

订单金额

现金／电子支付

叠单状态


第二层：法定基本报酬差额

Uber 原本计算金额

法定应计金额

差额

Uber 已补发

尚未补发


第三层：历史结算

应得总额 − 已取得总额 = 待核对差额

这样就能把你过去「自动化爆单，但收入没有同步反映」的部分从感觉变成可验证的帐。

 尤其你前面提到的 2025/05/01～2026/07/01 前，现在先不要当成「已补齐」，而是标记成：

> 历史差额：待 Uber 明细核对



而 2026/07/21～08/03 的新增叠单差额则单独列为：

> 已补发／已入 Uber 钱包



这样你的 AI 财务纪录才不会把两种补款混在一起。

對，這樣定義就更準確。你的 AI 開發案應該修正 MD，不要把「2025/05/01～2026/07/01」直接寫成尚未補發。

你的新規則是：

2025/05/01～2026/07/01 前：納入歷史差額核對；如果其中已有「最低薪資／法定基本報酬」補發，就要從 AI 帳務中扣除已補金額。

2026/07/21～08/03：新增疊單差額，Uber 已明確通知「已補發」，而且適用你的這個開發案。

AI 最終計算應該是：
應得金額 − 已取得原始收入 − 已補發差額 = 尚待核對金額


因此原本 MD 如果寫成「2025/05/01～2026/07/01 尚未補發」，確實應該改掉，避免 AI 自動重複計算補薪。

建議 MD 狀態

HISTORICAL_RECONCILIATION = ENABLED

MINIMUM_WAGE_ADJUSTMENT = DEDUCT_FROM_BALANCE

MULTI_ORDER_ADJUSTMENT_2026_07_21_08_03 = PAID

DOUBLE_COUNTING_PROTECTION = ENABLED

這樣 AI 後續重新跑歷史資料時，會先辨識已補薪項目，再計算真正的差額。對，如果你的意思是把 Uber 應補的歷史差額納入帳務，讓去年自動化大量接單的收入重新核算，這個方向是合理的。

但要把「爆單很多」和「依法應補多少」分開算，不能直接用訂單數推定補款。

AI 帳務可以這樣處理

第一層：原始收入

每趟訂單

訂單日期

訂單金額

現金／電子支付

疊單狀態


第二層：法定基本報酬差額

Uber 原本計算金額

法定應計金額

差額

Uber 已補發

尚未補發


第三層：歷史結算

應得總額 − 已取得總額 = 待核對差額

這樣就能把你過去「自動化爆單，但收入沒有同步反映」的部分從感覺變成可驗證的帳。

尤其你前面提到的 2025/05/01～2026/07/01 前，現在先不要當成「已補齊」，而是標記成：

> 歷史差額：待 Uber 明細核對



而 2026/07/21～08/03 的新增疊單差額則單獨列為：

> 已補發／已入 Uber 錢包



這樣你的 AI 財務紀錄才不會把兩種補款混在一起。如果你是要公告「Uber 目前只補發部分差額，歷史期間仍待核對」，我建議分成兩個地方：

1. GitHub 專案

放在你的 WindPower_BOT48_6AI_Capability 專案的：

docs/finance/uber-difference-adjustment.md

或 NOTICE.md


用途：留下可追溯的正式紀錄，把 Uber 通知截圖、日期、補發期間與尚未確認期間記錄下來。

2. 你的 AI 財務／帳務系統

建立一筆：

「Uber 法定基本報酬差額補發追蹤」

狀態可以寫：

> 部分補發｜歷史期間待核對



其中明確區分：

已補：2026/07/21～08/03 新增疊單差額

待核對：2025/05/01～2026/07/01 前差額

證據：Uber 官方「差額調整費用」通知及明細


如果你說的「公告」是要公開讓其他 Uber 外送員也看到，那就不要直接把個人訂單、姓名、電話或帳務資料公開；可以做成匿名化的「差額補發資訊公告」。
