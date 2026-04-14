class AgentState:
    def __init__(self, query):
        self.query = query
        self.plan = []
        self.results = []
        self.final_answer = ""
        self.score = 0
        self.feedback = ""