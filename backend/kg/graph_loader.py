import json
import networkx as nx
from pathlib import Path

DATA_FILE = (
    Path(__file__).parent.parent
    / "data"
    / "kg_ai_uet_demo.json"
)

def load_graph():

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    G = nx.DiGraph()

    for node in data["nodes"]:
        G.add_node(
            node["id"],
            **node
        )

    for edge in data["edges"]:
        G.add_edge(
            edge["source"],
            edge["target"],
            relation=edge["relation"]
        )

    return G