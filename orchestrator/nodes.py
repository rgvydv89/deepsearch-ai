def planner_node(state, planner):
    print("[Node] Planner")
    state.plan = planner.create_plan(state.query)
    return state


def executor_node(state, executor, memory_context):
    print("[Node] Executor (SMART MODE)")

    # 🔥 Use ORIGINAL query (correct design for now)
    query = state.query

    result = executor.execute_step(query, memory_context)

    if result and "results" in result:
        state.results.extend(result["results"])
    else:
        print("[DEBUG] No results returned")

    print("[FINAL DEBUG] Results count:", len(state.results))

    return state


def reasoning_node(state, reasoning_agent, memory_context, long_term_context=""):
    print("[Node] Reasoning")

    state.final_answer = reasoning_agent.summarize(
        state.query,
        state.results,
        memory_context,
        long_term_context
    )

    return state


def evaluation_node(state, evaluator, query):
    print("[Node] Evaluation")

    evaluation = evaluator.evaluate(query, state.final_answer)

    state.score = evaluation["score"]
    state.feedback = evaluation["feedback"]

    return state