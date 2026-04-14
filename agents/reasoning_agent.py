def summarize(self, search_results, memory_context="", long_term_memory=""):
    print("[ReasoningAgent] Processing with memory...")

    content_blocks = []

    for idx, item in enumerate(search_results[:10]):
        block = f"""
        Title: {item['title']}
        Content: {item['content']}
        """
        content_blocks.append(block)

    combined_content = "\n\n".join(content_blocks)

    import os
import google.generativeai as genai


class ReasoningAgent:
    def __init__(self):
        genai.configure(api_key="")
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def summarize(self, search_results, memory_context="", long_term_memory=""):
        print("[ReasoningAgent] Processing with memory...")

        content_blocks = []

        for idx, item in enumerate(search_results[:10]):
            block = f"""
            Title: {item['title']}
            Content: {item['content']}
            """
            content_blocks.append(block)

        combined_content = "\n\n".join(content_blocks)

        prompt = f"""
        You are an advanced AI research assistant.

        PREVIOUS CONTEXT:
        {memory_context}

        RELEVANT PAST KNOWLEDGE:
        {long_term_memory}

        CURRENT DATA:
        {combined_content}

        TASK:
        - Provide key insights
        - Avoid repeating previous answers
        - Improve based on past context
        - Give final recommendation
        """

        response = self.model.generate_content(prompt)
        return response.text
