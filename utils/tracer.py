import json
import time


class TraceLogger:
    def __init__(self):
        self.traces = []

    # -----------------------------------------
    # START SPAN
    # -----------------------------------------
    def start_span(self, name, input_data=None):
        return {
            "name": name,
            "start_time": time.time(),
            "end_time": None,
            "duration_ms": None,
            "input": input_data,
            "output": None,
            "error": None,
        }

    # -----------------------------------------
    # END SPAN
    # -----------------------------------------
    def end_span(self, span, output=None, error=None):
        span["end_time"] = time.time()
        span["duration_ms"] = round((span["end_time"] - span["start_time"]) * 1000, 2)
        span["output"] = output
        span["error"] = str(error) if error else None

        self.traces.append(span)

    # -----------------------------------------
    # GET TRACE
    # -----------------------------------------
    def get_trace(self):
        return json.dumps(self.traces, indent=2)

    # -----------------------------------------
    # PRINT TRACE
    # -----------------------------------------
    def print_trace(self):
        print("\n🔍 TRACE OUTPUT")
        print(self.get_trace())
