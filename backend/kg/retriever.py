from kg.graph_loader import load_graph
from kg.graph_query import get_node


def get_graph_evidence(course_id):

    """
    Retrieve all graph evidence associated with a course.
    """

    G = load_graph()

    evidence = {
        "course": get_node(course_id),
        "prerequisites": [],
        "skills": [],
        "goals": [],
        "topics": [],
        "similar_courses": []
    }

    for source, target, data in G.edges(data=True):

        if source != course_id:
            continue

        relation = data.get("relation")

        target_node = get_node(target)

        if relation == "requires":

            evidence["prerequisites"].append(
                target_node
            )

        elif relation == "teaches":

            evidence["skills"].append(
                target_node
            )

        elif relation == "supports_goal":

            evidence["goals"].append(
                target_node
            )

        elif relation == "belongs_to_topic":

            evidence["topics"].append(
                target_node
            )

        elif relation == "similar_to":

            evidence["similar_courses"].append(
                target_node
            )

    return evidence


def get_reasoning_path(course_id):

    """
    Build graph reasoning chains that can be shown
    to the LLM as explanation evidence.
    """

    G = load_graph()

    path = []

    for source, target, data in G.edges(data=True):

        if source != course_id:
            continue

        relation = data.get("relation")

        target_node = get_node(target)

        path.append({
            "source": course_id,
            "relation": relation,
            "target": target,
            "target_name": (
                target_node.get("name")
                or target_node.get("title")
                or target
            )
        })

    return path

