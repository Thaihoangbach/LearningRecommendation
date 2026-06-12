from kg.retriever import (
    get_graph_evidence,
    get_reasoning_path
)


def build_context(intent, course_id):

    evidence = get_graph_evidence(course_id)

    reasoning_path = get_reasoning_path(
        course_id
    )

    return {
        "intent": intent,
        "course_id": course_id,
        "evidence": evidence,
        "reasoning_path": reasoning_path
    }


def context_to_prompt_string(ctx):

    return f"""
You are an explainable learning recommendation assistant.

Use ONLY information from the provided Knowledge Graph context.

Knowledge Graph Context:

{ctx}

Rules:
1. Do not invent facts.
2. If information is missing, say so.
3. Answer clearly and concisely.
4. Explain recommendations using graph evidence.
"""