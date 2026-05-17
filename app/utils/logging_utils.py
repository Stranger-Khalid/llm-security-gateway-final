import json
from datetime import datetime


LOG_FILE = "app/logs/audit_logs.jsonl"


def save_audit_log(data: dict):

    log_entry = {

        "timestamp": datetime.now().isoformat(),

        **data
    }

    with open(
            LOG_FILE,
            "a",
            encoding="utf-8"
    ) as file:

        file.write(
            json.dumps(log_entry) + "\n"
        )