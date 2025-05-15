import json
import os
from datetime import datetime

# File location
STATE_FILE = "monitor_state.json"

# Load state from file (if exists)
def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Failed to parse state file. Starting fresh.")
            return {}
    return {}

# Save state to file
def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

# Add a failure log
def log_failure(state, failure_type, message=None):
    state.setdefault("failures", []).append({
        "type": failure_type,
        "message": message or "",
        "time": datetime.now().isoformat()
    })