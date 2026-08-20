# public_docs_only.py
# WindPower_BOT48_6AI_Capability
# Public Repository → Markdown-only 展示層
#
# 目的：
# 1. 公開層只保留 Markdown 文件
# 2. 移除/隔離程式碼與自動化流程
# 3. 避免測試資料、API、模型與私有實作誤公開
#
# 執行前請先備份 Git repository。

from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent

# 公開層允許的檔案
ALLOWED_FILES = {
    ".md",
    ".markdown",
    "LICENSE",
    "LICENSE.md",
}

# 明確禁止公開的副檔名
BLOCKED_EXTENSIONS = {
    ".py",
    ".pyc",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".java",
    ".go",
    ".rs",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".cs",
    ".php",
    ".rb",
    ".sh",
    ".bat",
    ".cmd",
    ".ps1",
    ".yml",
    ".yaml",
    ".json",
    ".toml",
    ".ini",
    ".env",
    ".sql",
    ".ipynb",
}

# 不應出現在公開展示層的目錄
BLOCKED_DIRECTORIES = {
    ".github",
    ".git",
    "__pycache__",
    "backend",
    "frontend",
    "api",
    "server",
    "client",
    "src",
    "scripts",
    "workflow",
    "workflows",
    "models",
    "model",
    "simulator",
    "simulation",
    "private",
    "core",
    "secrets",
    "configs",
    "config",
    "tests",
    "test",
}


def is_allowed_file(path: Path) -> bool:
    name = path.name

    if name in ALLOWED_FILES:
        return True

    return path.suffix.lower() in {".md", ".markdown"}


def scan_repository():
    findings = []

    for path in ROOT.rglob("*"):

        if not path.is_file():
            continue

        relative = path.relative_to(ROOT)

        # 跳過 Git 本身
        if ".git" in relative.parts:
            continue

        # 目錄封鎖
        if any(part in BLOCKED_DIRECTORIES for part in relative.parts):
            findings.append(("BLOCKED_DIRECTORY", relative))
            continue

        # 副檔名封鎖
        if path.suffix.lower() in BLOCKED_EXTENSIONS:
            findings.append(("BLOCKED_EXTENSION", relative))
            continue

        # 非 Markdown / LICENSE
        if not is_allowed_file(path):
            findings.append(("NON_DOCUMENT_FILE", relative))

    return findings


def quarantine(findings):
    """
    不直接刪除，先移到 ../PRIVATE_QUARANTINE。
    """

    quarantine_root = ROOT.parent / "PRIVATE_QUARANTINE"

    for category, relative in findings:

        source = ROOT / relative
        destination = quarantine_root / relative

        destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if source.exists():
            shutil.move(str(source), str(destination))

    return quarantine_root


def generate_gitignore():
    content = """# ==========================================
# PUBLIC DOCS ONLY
# ==========================================

# Python
*.py
*.pyc
__pycache__/

# JavaScript / TypeScript
*.js
*.jsx
*.ts
*.tsx

# Other source code
*.java
*.go
*.rs
*.cpp
*.c
*.h
*.hpp
*.cs
*.php
*.rb

# Automation
*.sh
*.bat
*.cmd
*.ps1

# Configuration / data
*.yml
*.yaml
*.json
*.toml
*.ini
*.env
*.sql
*.ipynb

# Private directories
.github/
backend/
frontend/
api/
server/
client/
src/
scripts/
workflow/
workflows/
models/
model/
simulator/
simulation/
private/
core/
secrets/
configs/
config/
tests/
test/

# Local/private quarantine
PRIVATE_QUARANTINE/
"""

    (ROOT / ".gitignore").write_text(
        content,
        encoding="utf-8"
    )


def main():

    print("=" * 60)
    print(" WindPower BOT48 - Public Docs Only")
    print("=" * 60)

    findings = scan_repository()

    if not findings:
        print("\n✅ 未發現需要隔離的非公開檔案。")
        generate_gitignore()
        return

    print(f"\n⚠️ 發現 {len(findings)} 個非公開項目：\n")

    for category, path in findings:
        print(f"[{category}] {path}")

    answer = input(
        "\n是否移至 PRIVATE_QUARANTINE？"
        " [y/N]: "
    ).strip().lower()

    if answer != "y":
        print("\n取消操作，沒有移動檔案。")
        return

    quarantine_root = quarantine(findings)
    generate_gitignore()

    print("\n✅ 整理完成")
    print(f"📁 私有檔案暫存位置：{quarantine_root}")
    print("📄 公開層：Markdown / LICENSE")
    print("\n⚠️ 請接著檢查 Git history。")


if __name__ == "__main__":
    main()
