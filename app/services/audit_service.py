import json
from pathlib import Path
from datetime import datetime


AUDIT_LOG_DIR = Path("data/audit_logs")
AUDIT_LOG_DIR.mkdir(parents=True, exist_ok=True)

AUDIT_LOG_FILE = AUDIT_LOG_DIR / "rag_audit_log.jsonl"


def write_audit_log(event: dict):
    audit_record = {
        "timestamp": datetime.utcnow().isoformat(),
        **event
    }

    with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(audit_record, ensure_ascii=False) + "\n")


def read_audit_logs(limit: int = 50):
    if not AUDIT_LOG_FILE.exists():
        return []

    lines = AUDIT_LOG_FILE.read_text(encoding="utf-8").splitlines()
    recent_lines = lines[-limit:]

    return [json.loads(line) for line in recent_lines]