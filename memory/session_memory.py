class SessionMemory:
    def __init__(self):
        self.history = []

    def add(self, user_query, response):
        self.history.append({
            "query": user_query,
            "response": response
        })

    def get_context(self, last_n=3):
        context = ""

        for item in self.history[-last_n:]:
            context += f"""
            User: {item['query']}
            Assistant: {item['response']}
            """

        return context.strip()