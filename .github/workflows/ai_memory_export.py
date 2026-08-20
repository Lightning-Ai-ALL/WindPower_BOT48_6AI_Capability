# ai_memory_export.py
# Public AI Memory Layer
#
# 公開層 = AI 記憶摘要
# 私有層 = 真正程式碼
#
# 原則：
# Memory != Source Code
# Summary != Implementation
# Claim != Verified Fact

from pathlib import Path
from datetime import datetime
import json
import hashlib


ROOT = Path(__file__).resolve().parent
MEMORY_DIR = ROOT / "ai_memory"

PUBLIC_MEMORY = MEMORY_DIR / "PUBLIC_MEMORY.md"
MEMORY_INDEX = MEMORY_DIR / "memory_index.json"


def sha256(text: str) -> str:
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def create_memory(
    project: str,
    purpose: str,
    architecture: str,
    decisions: list[str],
    status: str = "DEVELOPMENT",
):
    timestamp = datetime.now().isoformat()

    memory = {
        "project": project,
        "purpose": purpose,
        "architecture": architecture,
        "decisions": decisions,
        "status": status,
        "updated_at": timestamp,
    }

    MEMORY_DIR.mkdir(exist_ok=True)

    markdown = f"""# AI Project Memory

## Project

{project}

## Purpose

{purpose}

## Architecture Summary

{architecture}

## Development Decisions

"""

    for decision in decisions:
        markdown += f"- {decision}\n"

    markdown += f"""
## Status

`{status}`

## Memory Metadata

- Updated: `{timestamp}`
- Memory Hash: `{sha256(json.dumps(memory, ensure_ascii=False))}`

---

> This document is an AI memory record.
> It is not source code.
> It does not contain credentials, private keys,
> executable workflows, or private implementation details.
"""

    PUBLIC_MEMORY.write_text(
        markdown,
        encoding="utf-8"
    )

    MEMORY_INDEX.write_text(
        json.dumps(
            memory,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    print("✅ AI Memory 已建立")
    print(f"📄 {PUBLIC_MEMORY}")
    print(f"🧠 {MEMORY_INDEX}")


if __name__ == "__main__":

    create_memory(
        project="WindPower_BOT48_6AI_Capability",

        purpose=(
            "風力發電 AI 概念架構與多 Agent "
            "協作研究。"
        ),

        architecture=(
            "BOT48 作為概念性協調層，"
            "搭配多個專用 AI 模組進行環境、"
            "能源、安全、通訊、運算與記憶相關研究。"
        ),

        decisions=[
            "公開層以 Markdown 作為 AI 長期記憶。",
            "核心原始碼維持私有。",
            "敏感實作細節不寫入公開記憶。",
            "模擬資料必須標記 SIMULATION。",
            "Claim 不得自動升級為 Verified Fact。",
            "AI 忘記私有實作時，可透過公開記憶恢復專案脈絡。",
        ],
    )
