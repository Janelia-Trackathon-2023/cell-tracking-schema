import networkx as nx
from networkx.utils import graphs_equal
from cell_tracking_schema.schema import NodeModel, EdgeModel, GraphModel


def create_linear_graph(num_nodes=10):
    nodes = [(i, NodeModel(node_id=i, t=float(i))) for i in range(num_nodes)]

    edges = [
        (i, i + 1, EdgeModel(edge_id=i, source_id=i, target_id=i + 1))
        for i in range(num_nodes - 1)
    ]
    g = nx.DiGraph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    return g


def test_networkx_io():
    g = create_linear_graph()
    # Convert to schema
    graph_model = GraphModel.parse_networkx(g)
    # Convert from schema
    nx_graph = graph_model.as_networkx()
    assert graphs_equal(
        g, nx_graph
    ), "Graph was changed during conversion to/from schema."
