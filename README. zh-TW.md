# Public Repository Policy

**Version:** 1.0  
**Date:** 2026-08-20  
**Status:** DEVELOPMENT

## 1. 目的

本儲存庫為公開文件與 AI 記憶展示層。

公開內容僅用於：

- 專案概念說明
- 架構摘要
- 開發紀錄
- 可公開的測試與模擬結果
- AI 記憶索引

本儲存庫不作為私有核心程式碼儲存位置。

## 2. 公開層

公開層原則上只提供 Markdown 文件：

- `README.md`
- `README.zh-TW.md`
- `README.zh-CN.md`
- `README.en-US.md`
- `docs/*.md`
- 概念性圖表與公開說明

文件不得包含：

- 私有金鑰
- API Token
- 密碼
- 私有網域
- 私有 IP
- 模型權重
- 私有 Prompt
- 完整核心演算法
- 私有 Agent 路由規則
- 可直接部署的核心實作

## 3. 私有核心

完整開發環境應存放於受控的私有環境，包括：

- 原始程式碼
- 私有 Git Repository
- CI/CD
- 模型與權重
- 私有 AI / Agent 設定
- 私有記憶資料
- 備份檔案
- 內部測試資料

公開文件可以保留「索引」或「摘要」，但不應因此暴露私有實作。

## 4. AI Memory

公開 Markdown 可以作為開發記憶的摘要層。

記憶資料應明確區分：

`CLAIM` → 單方描述  
`SIMULATION` → 模擬資料  
`VERIFIED` → 已驗證資料  
`PRIVATE` → 私有開發資料

「AI 記得某項開發內容」不代表該內容就是現實世界已完成的事件。

## 5. 公開安全原則

公開 Repository 應避免提交：

- 壓縮檔
- 執行檔
- 機密設定
- 私有憑證
- CI/CD 工作流程
- 可還原核心實作的完整程式碼

真正的安全措施應依靠 Repository 權限、存取控制、Secrets 管理與私有環境，而不是單純將檔案內容轉成亂碼。

## 6. 狀態

```text
Repository: PUBLIC DOCUMENTATION
Core Implementation: PRIVATE
Status: DEVELOPMENT
