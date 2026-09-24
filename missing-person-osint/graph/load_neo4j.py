"""
Idempotent Neo4j Graph Database Loader.
Loads NetworkX nodes and relationships into Neo4j using Cypher MERGE statements.
Creates unique constraints and handles connection testing gracefully.
"""
from __future__ import annotations
import argparse
import logging
from typing import Dict, Any, Optional
import networkx as nx

from graph.build_networkx import build_investigation_graph

logger = logging.getLogger(__name__)

def load_graph_to_neo4j(
    G: nx.MultiDiGraph,
    uri: str = "bolt://localhost:7687",
    user: str = "neo4j",
    password: str = "investigation2026",
    clear_existing: bool = True
) -> Dict[str, Any]:
    """
    Connects to Neo4j, enforces unique constraints, and writes all graph nodes & edges idempotently.
    """
    try:
        from neo4j import GraphDatabase
    except ImportError:
        return {"status": "error", "message": "neo4j python package not installed."}

    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session() as session:
            # Verify connectivity
            session.run("RETURN 1").single()

            if clear_existing:
                logger.info("Clearing existing Neo4j graph data...")
                session.run("MATCH (n) DETACH DELETE n")

            # 1. Setup Constraints
            constraints = [
                "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (a:Account) REQUIRE a.id IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (ph:Phone) REQUIRE ph.id IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (l:Location) REQUIRE l.id IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Post) REQUIRE p.id IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (ph:Photo) REQUIRE ph.id IS UNIQUE"
            ]
            for c in constraints:
                try:
                    session.run(c)
                except Exception as ce:
                    logger.debug(f"Constraint notice: {ce}")

            # 2. Insert Nodes via MERGE
            logger.info("Ingesting nodes into Neo4j...")
            for node_id, data in G.nodes(data=True):
                ntype = data.get("node_type", "Entity")
                label = data.get("label", node_id)
                query = f"""
                MERGE (n:{ntype} {{id: $node_id}})
                SET n.label = $label, n += $props
                """
                props = {k: str(v) if isinstance(v, (list, dict)) else v for k, v in data.items() if k not in ["node_type", "label"]}
                session.run(query, node_id=node_id, label=label, props=props)

            # 3. Insert Relationships via MERGE
            logger.info("Ingesting relationships into Neo4j...")
            for u, v, k, data in G.edges(keys=True, data=True):
                rel_type = data.get("edge_type", "RELATED_TO").replace(" ", "_").upper()
                u_type = G.nodes[u].get("node_type", "Entity")
                v_type = G.nodes[v].get("node_type", "Entity")
                rel_query = f"""
                MATCH (source:{u_type} {{id: $source_id}}), (target:{v_type} {{id: $target_id}})
                MERGE (source)-[r:{rel_type}]->(target)
                SET r += $props
                """
                rel_props = {k: str(v) if isinstance(v, (list, dict)) else v for k, v in data.items() if k != "edge_type"}
                session.run(rel_query, source_id=u, target_id=v, props=rel_props)

        driver.close()
        logger.info("Neo4j database population completed successfully.")
        return {
            "status": "success",
            "nodes_inserted": G.number_of_nodes(),
            "edges_inserted": G.number_of_edges()
        }

    except Exception as e:
        logger.warning(f"Neo4j live load skipped or unreachable ({uri}): {str(e)}.")
        return {
            "status": "unreachable",
            "message": f"Could not connect to Neo4j at {uri}. Ensure docker-compose is running.",
            "error": str(e)
        }

def main():
    parser = argparse.ArgumentParser(description="Load Investigation Graph into Neo4j")
    parser.add_argument("--uri", type=str, default="bolt://localhost:7687")
    parser.add_argument("--user", type=str, default="neo4j")
    parser.add_argument("--password", type=str, default="investigation2026")
    parser.add_argument("--no-clear", action="store_true")
    args = parser.parse_args()

    g = build_investigation_graph()
    res = load_graph_to_neo4j(
        g,
        uri=args.uri,
        user=args.user,
        password=args.password,
        clear_existing=not args.no_clear
    )
    print(res)

if __name__ == "__main__":
    main()
