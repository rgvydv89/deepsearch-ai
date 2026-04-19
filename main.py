# from orchestrator.workflow import DeepSearchOrchestrator

# # orchestrator = DeepSearchOrchestrator()

# # response = orchestrator.run("Best cloud platform for AI startups")

# # print(response["final_answer"])

# from orchestrator.workflow import Orchestrator

# # Create orchestrator instance
# orchestrator = Orchestrator()

# # Run queries
# output1 = orchestrator.run("Best cloud platform for AI startups")
# print("\nFinal Output 1:", output1)

# output2 = orchestrator.run("Which one is cheapest?")
# print("\nFinal Output 2:", output2)


# # import google.generativeai as genai
# # import os
# # from dotenv import load_dotenv

# # load_dotenv()
# # genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # for m in genai.list_models():
# #     print(m.name)

# from orchestrator.workflow import Orchestrator

# if __name__ == "__main__":
#     # ✅ Create object
#     orchestrator = Orchestrator()

#     # ✅ Run query
#     response = orchestrator.run("Best cloud platform for AI startups")

#     print("\n========== FINAL OUTPUT ==========")

#     print("\nFINAL ANSWER:\n", response.get("final_answer"))

#     print("\nSCORE:", response.get("score"))

#     print("\nFEEDBACK:\n", response.get("feedback"))

from agents.search_agent import SearchAgent

agent = SearchAgent()
print(agent.run("AWS AI services"))
