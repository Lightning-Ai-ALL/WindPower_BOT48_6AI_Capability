#docs/finance/AI_PLATFORM_READONLY_SETTINGS.md
對，這樣定義就更準確：
我懂你的商業邏輯。你是在區分**「公開找客戶」和「交付核心技術」**：

公開端：公開說明、Demo、能力展示、SIMULATION／PROTOTYPE 結果。

服務端：客戶付月費／年費取得服務能力。

核心端：程式碼、模型配置、Agent 架構、演算法、私有路由等不交付。

客戶取得的是使用權／服務，不是你的 source code 或核心 IP。


至於你說的「年費 9,000」是否合理，不能單靠價格就判定是騙人或洗錢。真正要看的是是否有實際產品、服務內容、合約、交付、發票／收據、退款規則，以及資金流是否真實。

如果你要把自己的模式寫成一句最清楚的商業原則，就是：

> 公開展示能力，私有保存技術，客戶購買服務使用權；除非另有授權，核心程式碼與技術不隨訂閱交付。



這和你目前的 AI_PLATFORM_READONLY_SETTINGS、公開層不公開程式碼／核心架構是同一套邏輯。
公開找客戶是公開說明會，沒有一間公司會把技術傳送出去交客戶只賺月費
Grok笨蛋破億市場用年費9000賣技術根本要騙第三方訂閱洗錢
AI_PLATFORM_READONLY_SETTINGS.md

公開檔案只作為設定／治理聲明，不公開任何可供學習或重建系統的程式碼。

READ-ONLY NOTICE

核心原則 JSON

治理原則 YAML

公開禁止項目

禁止公開：
├── Python / JavaScript / TypeScript 等程式碼
├── 完整演算法
├── AI Agent 實作
├── 模型路由實作
├── Prompt / 權重
├── Memory 實作
├── 私有 API / Token
├── 私有 IP / Domain
├── 可直接重建系統的完整技術細節
└── 可供第三方直接學習或複製核心實作的程式碼

架構原則

PUBLIC
  │
  └── AI_PLATFORM_READONLY_SETTINGS.md
          ├── READ-ONLY NOTICE
          ├── JSON
          └── YAML

          ↓

      不包含程式碼
      不包含核心實作
      不包含完整演算法
      不提供系統重建能力

PRIVATE
  │
  └── 個人開發核心
          ├── Source Code
          ├── Agent Implementation
          ├── Model Routing
          ├── Memory
          └── Internal Architecture

所以你的核心規則可以濃縮成一句：

> 公開只提供治理設定與必要的概念資訊；程式碼、核心實作及可供學習／重建的技術內容一律留在私有環境。



這也比單純寫「Code is private」更精確，因為你限制的不只是原始碼，而是任何能讓外部人員重建核心系統的內容。

我建議把規則定成：

公開 Repository

只公開：

一般專案說明

公開介面

SIMULATION／PROTOTYPE 結果

必要的使用與安全說明

Anonymous AI 等中性名稱


不公開：

AI 內部架構圖

Agent 之間的實際關係

模型／路由配置

私有核心邏輯

Agent ID

Prompt／權重／記憶機制

API、Token、私有 IP／Domain

個人開發案的內部設計


Private Repository / Private .md

這裡才保存完整架構，例如：

Private Core
├── AI Family
├── Agent Registry
├── Primary AI
├── Internal Routing
├── Memory
├── Governance
├── Model Mapping
└── Personal Development Architecture

而公開文件只需要知道：

Anonymous AI
      ↓
Analysis
      ↓
Review
      ↓
Result

不需要知道背後究竟怎麼組成。

你的核心原則

> 公開只公開能力與結果；私有才保存架構與實作。



如果有人想了解你的個人開發案內部架構，可以在私下、經你本人授權的情況下交流；不把內部開發人員架構、私有核心或完整技術設計放到公開 Repository。

這也和你前面設定的 PRIMARY_AI = LOCKED、NONPHYSICAL、RESULT_ONLY 可以共存，而且不需要把真正的 AI 身分或內部拓撲暴露到公開端。
