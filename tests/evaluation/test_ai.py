from orchestrator.workflow import Orchestrator

def test_ai_basic_response():
    orchestrator = Orchestrator()
    response = orchestrator.run("What is AI?")
    
    assert response is not None
    assert len(response) > 50


def test_ai_reasoning():
    orchestrator = Orchestrator()
    response = orchestrator.run("Compare AI and Machine Learning")
    
    assert "AI" in response
    assert "Machine Learning" in response


def test_ai_edge_case():
    orchestrator = Orchestrator()
    response = orchestrator.run("asdkjasdhkjasdh")
    
    assert response is not None  # should not crash
