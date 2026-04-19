import json


class MetricsCollector:
    def __init__(self):
        self.runs = []

    # -----------------------------------------
    # ADD RUN DATA
    # -----------------------------------------
    def add_run(self, trace, evaluation=None, judge=None):
        run_data = {"trace": trace, "evaluation": evaluation or {}, "judge": judge or {}}

        self.runs.append(run_data)

    # -----------------------------------------
    # CALCULATE METRICS
    # -----------------------------------------
    def compute(self):
        total_runs = len(self.runs)

        if total_runs == 0:
            return {}

        total_latency = 0
        error_count = 0
        tool_usage = {}

        eval_scores = []
        judge_scores = []

        for run in self.runs:
            trace = run["trace"]

            # ---------------------------
            # LATENCY
            # ---------------------------
            run_latency = sum(span.get("duration_ms", 0) for span in trace)
            total_latency += run_latency

            # ---------------------------
            # ERROR RATE
            # ---------------------------
            for span in trace:
                if span.get("error"):
                    error_count += 1

            # ---------------------------
            # TOOL USAGE
            # ---------------------------
            for span in trace:
                name = span.get("name")

                if name not in tool_usage:
                    tool_usage[name] = 0

                tool_usage[name] += 1

            # ---------------------------
            # EVALUATION SCORE
            # ---------------------------
            if run["evaluation"]:
                eval_scores.append(run["evaluation"].get("score", 0))

            # ---------------------------
            # JUDGE SCORE
            # ---------------------------
            if run["judge"]:
                judge_scores.append(run["judge"].get("overall_score", 0))

        return {
            "total_runs": total_runs,
            "avg_latency_ms": round(total_latency / total_runs, 2),
            "error_rate": round(error_count / total_runs, 2),
            "tool_usage": tool_usage,
            "avg_eval_score": round(sum(eval_scores) / len(eval_scores), 2) if eval_scores else 0,
            "avg_judge_score": (
                round(sum(judge_scores) / len(judge_scores), 2) if judge_scores else 0
            ),
        }
