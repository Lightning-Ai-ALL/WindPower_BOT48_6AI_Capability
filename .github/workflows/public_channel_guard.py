# public_channel_guard.py

from pathlib import Path

BLOCKED_EXTENSIONS = {
    ".zip", ".7z", ".rar", ".tar", ".gz",
    ".py", ".js", ".ts", ".sh", ".ps1",
    ".yml", ".yaml", ".json",
    ".exe", ".dll", ".so",
}

BLOCKED_PATHS = {
    ".git",
    ".github",
    ".gitlab",
    ".ci",
    "ci",
    "workflow",
    "workflows",
    "private",
    "secrets",
    "credentials",
    "backup",
}


def inspect_public_tree(root: str = "."):
    root = Path(root)
    blocked = []

    for path in root.rglob("*"):
        relative = path.relative_to(root)

        if any(part.lower() in BLOCKED_PATHS
               for part in relative.parts):
            blocked.append(
                ("PATH_BLOCKED", str(relative))
            )
            continue

        if path.is_file() and path.suffix.lower() in BLOCKED_EXTENSIONS:
            blocked.append(
                ("FILE_BLOCKED", str(relative))
            )

    return blocked


def main():
    findings = inspect_public_tree()

    if findings:
        print("🚫 PUBLIC CHANNEL BLOCKED")
        print()

        for reason, path in findings:
            print(f"[{reason}] {path}")

        raise SystemExit(1)

    print("✅ PUBLIC CHANNEL CLEAN")
    print("只允許公開文件與 AI Memory。")


if __name__ == "__main__":
    main()
