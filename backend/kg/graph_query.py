from .graph_loader import load_graph
import networkx as nx

def get_all_courses():

    G = load_graph()

    courses = []

    for node_id, attrs in G.nodes(data=True):

        if attrs.get("type") != "Course":
            continue

        courses.append({

            "id": node_id,

            "title": attrs.get("name"),

            "description": attrs.get("description"),

            "hours": attrs.get("credits", 3) * 15,

            "difficulty": (
                "beginner"
                if attrs.get("semester", 1) <= 2
                else (
                    "intermediate"
                    if attrs.get("semester", 1) <= 5
                    else "advanced"
                )
            ),

            "topics": [],

            "semester": attrs.get("semester"),

            "code": attrs.get("code"),

            "course_type": attrs.get("course_type")
        })

    courses.sort(
        key=lambda x: x["semester"]
    )

    return courses

def get_learning_path():

    G = load_graph()

    course_graph = nx.DiGraph()

    for source, target, attrs in G.edges(data=True):

        if attrs.get("relation") != "requires":
            continue

        source_type = G.nodes[source].get("type")
        target_type = G.nodes[target].get("type")

        if source_type == "Course" and target_type == "Course":

            # prerequisite → course
            course_graph.add_edge(
                target,
                source
            )

    return list(
        nx.topological_sort(course_graph)
    )

def get_course_by_id(course_id):

    G = load_graph()

    attrs = G.nodes[course_id]

    return {

        "id": course_id,

        "title": attrs.get("name"),

        "description": attrs.get("description"),

        "hours": attrs.get("credits", 3) * 15,

        "difficulty": (
            "beginner"
            if attrs.get("semester", 1) <= 2
            else (
                "intermediate"
                if attrs.get("semester", 1) <= 5
                else "advanced"
            )
        ),

        "topics": [],

        "semester": attrs.get("semester"),

        "code": attrs.get("code"),
    }
def get_course_context(course_id):

    G = load_graph()

    if course_id not in G:
        return None

    course = G.nodes[course_id]

    result = {
        "course": course,
        "prerequisites": [],
        "skills": [],
        "goals": [],
        "next_courses": []
    }

    for source, target, attrs in G.edges(data=True):

        relation = attrs.get("relation")

        # current course requires something
        if source == course_id and relation == "requires":

            result["prerequisites"].append(
                G.nodes[target]
            )

        # current course teaches skill
        if source == course_id and relation == "teaches":

            result["skills"].append(
                G.nodes[target]
            )

        # current course supports goal
        if source == course_id and relation == "supports_goal":

            result["goals"].append(
                G.nodes[target]
            )

        # future courses
        if target == course_id and relation == "requires":

            result["next_courses"].append(
                G.nodes[source]
            )

    return result

def get_node(node_id):

    G = load_graph()

    if node_id not in G:
        return None

    node = dict(G.nodes[node_id])

    node["id"] = node_id

    return node


def get_prerequisites(course_id):

    G = load_graph()

    results = []

    for source, target, data in G.edges(data=True):

        if (
            target == course_id
            and data.get("relation") == "requires"
        ):

            node = dict(G.nodes[source])

            node["id"] = source

            results.append(node)

    return results


def get_next_courses(course_id):

    G = load_graph()

    results = []

    for source, target, data in G.edges(data=True):

        if (
            source == course_id
            and data.get("relation") == "requires"
        ):

            node = dict(G.nodes[target])

            node["id"] = target

            results.append(node)

    return results


def get_skills(course_id):

    G = load_graph()

    results = []

    for source, target, data in G.edges(data=True):

        if (
            source == course_id
            and data.get("relation") == "teaches"
        ):

            node = dict(G.nodes[target])

            node["id"] = target

            results.append(node)

    return results


def get_goals(course_id):

    G = load_graph()

    results = []

    for source, target, data in G.edges(data=True):

        if (
            source == course_id
            and data.get("relation") == "supports_goal"
        ):

            node = dict(G.nodes[target])

            node["id"] = target

            results.append(node)

    return results

def get_skill_ids(course_id):

    G = load_graph()

    skills = set()

    for source, target, data in G.edges(data=True):

        if (
            source == course_id
            and data.get("relation") == "teaches"
        ):
            skills.add(target)

    return skills

def compute_similarity(course_a, course_b):

    skills_a = get_skill_ids(course_a)
    skills_b = get_skill_ids(course_b)

    if not skills_a and not skills_b:
        return 0

    intersection = len(
        skills_a.intersection(skills_b)
    )

    union = len(
        skills_a.union(skills_b)
    )

    return round(
        intersection / union,
        3
    )
def get_similar_courses(course_id, top_k=5):

    courses = get_all_courses()

    results = []

    for course in courses:

        if course["id"] == course_id:
            continue

        score = compute_similarity(
            course_id,
            course["id"]
        )

        results.append({
            "course_id": course["id"],
            "title": course["title"],
            "score": score
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]