from orchestrator.workflow import Orchestrator

class MockSearchTool:
    def run(self, query):
        return {"results": ["mock result about AI"]}


def test_ai_basic_response(monkeypatch):
    # 🔥 Replace Tavily with mock
    monkeypatch.setattr(
        "tools.tavily_search.TavilySearchTool",
        lambda: MockSearchTool()
    )

    orchestrator = Orchestrator()
    response = orchestrator.run("What is AI?")
    
    assert response is not None
    assert len(response) > 20
