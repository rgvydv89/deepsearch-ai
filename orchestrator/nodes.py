def planner_node(state, planner):
    print("[Node] Planner")
    state.plan = planner.create_plan(state.query)
    return state


def executor_node(state, executor, decision_agent):
    print("[Node] Executor (FORCED SEARCH MODE)")

    for step in state.plan:
        if not isinstance(step, str):
            continue

        print("[DEBUG] Executing step:", step)

        # 🔥 FORCE SEARCH (no decision agent for now)
        result = executor.execute_step(step)

        if result and "results" in result:
            # print("[DEBUG] Results received:", len(result["results"]))
            state.results.extend(result["results"])
        else:
            print("[DEBUG] No results returned")
        
        print("[FINAL DEBUG] Results count:", len(state.results))

    return state


def reasoning_node(state, reasoning_agent, session_context, long_term_context):
    print("[Node] Reasoning")

    state.final_answer = reasoning_agent.summarize(
        state.results,
        memory_context=session_context,
        long_term_memory=long_term_context
    )

    return state


def evaluation_node(state, evaluator, query):
    print("[Node] Evaluation")

    evaluation = evaluator.evaluate(query, state.final_answer)

    state.score = evaluation["score"]
    state.feedback = evaluation["feedback"]

    return state