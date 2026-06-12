from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()
driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
)

def get_course(course_id: str) -> dict:
    with driver.session() as s:
        result = s.run("""
            MATCH (c:Course {id:$id})
            OPTIONAL MATCH (c)-[:HAS_TOPIC]->(t:Topic)
            OPTIONAL MATCH (c)-[:BELONGS_TO]->(d:Domain)
            RETURN c, collect(t.name) AS topics, d.name AS domain
        """, id=course_id).single()
        if not result:
            return {}
        c = dict(result["c"])
        c["topics"] = result["topics"]
        c["domain"] = result["domain"]
        return c

def get_similar_courses(course_id: str) -> list:
    with driver.session() as s:
        results = s.run("""
            MATCH (c:Course {id:$id})-[r:SIMILAR_TO]->(other:Course)
            RETURN other, r.similarity AS score
            ORDER BY score DESC LIMIT 5
        """, id=course_id)
        return [{"course": dict(r["other"]), "similarity": r["score"]} for r in results]

def get_learning_path() -> list:
    with driver.session() as s:
        results = s.run("""
            MATCH path=(start:Course)-[:NEXT_IN_PATH*]->(end:Course)
            WHERE NOT (:Course)-[:NEXT_IN_PATH]->(start)
            RETURN [n IN nodes(path) | n.id] AS path_ids
            LIMIT 1
        """).single()
        if not results:
            return []
        return results["path_ids"]
    
def get_learning_path_position(course_id: str):
    path = get_learning_path()

    if course_id not in path:
        return None

    return {
        "position": path.index(course_id) + 1,
        "total": len(path)
    }

def get_domain_community(course_id: str) -> list:
    with driver.session() as s:
        results = s.run("""
            MATCH (c:Course {id:$id})-[:BELONGS_TO]->(d:Domain)<-[:BELONGS_TO]-(other:Course)
            WHERE other.id <> $id
            RETURN other
        """, id=course_id)
        return [dict(r["other"]) for r in results]

def get_full_context(course_id: str):
    return {
        "course": get_course(course_id),
        "similar_courses": get_similar_courses(course_id),
        "domain_community": get_domain_community(course_id),
        "learning_path": get_learning_path(),
        "path_position": get_learning_path_position(course_id)
    }