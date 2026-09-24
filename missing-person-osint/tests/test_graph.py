"""
Unit tests for NetworkX multi-modal graph construction and analytics.
"""
import pytest
from graph.build_networkx import build_investigation_graph
from graph.analytics import run_graph_analytics
from graph.export_maltego import export_all_formats
from graph.cypher_queries import CYPHER_QUERIES

def test_graph_node_and_edge_types():
    G = build_investigation_graph()
    assert G.number_of_nodes() >= 50
    assert G.number_of_edges() >= 50

    node_types = set(d.get("node_type") for n, d in G.nodes(data=True))
    assert "Person" in node_types
    assert "Account" in node_types
    assert "Phone" in node_types
    assert "Location" in node_types
    assert "Post" in node_types

    edge_types = set(d.get("edge_type") for u, v, k, d in G.edges(keys=True, data=True))
    assert "OWNS" in edge_types
    assert "FOLLOWS" in edge_types
    assert "POSTED" in edge_types
    assert "SAME_AS" in edge_types

def test_graph_analytics():
    G = build_investigation_graph()
    analytics = run_graph_analytics(G)
    assert analytics["total_nodes"] == G.number_of_nodes()
    assert len(analytics["top_degree_centrality"]) > 0
    assert len(analytics["communities"]) > 0
    assert analytics["last_72h_subgraph"]["node_count"] > 0

def test_cypher_queries_catalogue():
    assert len(CYPHER_QUERIES) >= 10
    for q in CYPHER_QUERIES:
        assert "query_id" in q
        assert "title" in q
        assert "cypher" in q
        assert len(q["cypher"]) > 10
