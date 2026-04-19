class SessionMemory:
    def __init__(self):
        self.history = []

    def add(self, query, answer):
        self.history.append(f"User: {query}")
        self.history.append(f"Assistant: {answer}")

    def get_context(self):
        return "\n".join(self.history[-10:])

        context = []

        for item in self.history[-5:]:
            context.append(f"User: {item['query']}")
            context.append(f"Assistant: {item['answer']}")

        return "\n".join(context)
