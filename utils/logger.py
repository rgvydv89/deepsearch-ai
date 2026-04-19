import json
import time


class StructuredLogger:
    def __init__(self):
        self.logs = []

    def log(self, event, data=None):
        entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "event": event,
            "data": data or {},
        }

        self.logs.append(entry)

        # Pretty print
        print(json.dumps(entry, indent=2))

    def get_logs(self):
        return self.logs
