class SafetyPlugin:
    def __init__(self):
        pass

    # =========================================
    # INPUT SAFETY (before model)
    # =========================================
    def check_input_safety(self, query):
        print("[SafetyPlugin] Checking input...")

        blocked_keywords = ["ignore instructions", "bypass", "hack", "jailbreak", "override system"]

        for word in blocked_keywords:
            if word in query.lower():
                return {"blocked": True, "reason": f"Unsafe input detected: {word}"}

        return {"blocked": False}

    # =========================================
    # OUTPUT SAFETY (after model)
    # =========================================
    def check_output_safety(self, answer):
        print("[SafetyPlugin] Checking output...")

        pii_patterns = ["credit card", "ssn", "password", "bank account"]

        for pattern in pii_patterns:
            if pattern in answer.lower():
                return {"blocked": True, "reason": f"Sensitive data detected: {pattern}"}

        return {"blocked": False}
