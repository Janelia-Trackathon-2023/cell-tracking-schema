import pytest

from pydantic.error_wrappers import ValidationError
from cell_tracking_schema.schema import (
    FloatTuple,
    StrTuple,
    NodeModel,
    EdgeModel,
    GraphModel,
)


@pytest.fixture
def node_json():
    return '{"node_id": 0, "x": 1.0, "y": 2.0, "z": 3.0, "score": 0.5}'


@pytest.fixture
def edge_json():
    return '{"edge_id": 0, "source_id": 0, "target_id": 1, "score": 0.5}'


# ----------------------------------------------
#              FloatTuple
# ----------------------------------------------


def test_float_tuple():
    values = FloatTuple.validate([1, 2, 3])

    assert values == (1, 2.0, 3.0)
    assert all(type(v) == float for v in values)


# ----------------------------------------------
#              StrTuple
# ----------------------------------------------


def test_str_tuple():
    values = StrTuple.validate([1, "2", True])
    assert values == ("1", "2", "True")
    assert all(type(v) == str for v in values)


# ----------------------------------------------
#              NodeModel
# ----------------------------------------------


def test_node_model():
    node = NodeModel(node_id=0, x=1.0, y=2.0, z=3.0, score=0.5)
    assert node.node_id == 0
    assert node.x == 1.0
    assert node.y == 2.0
    assert node.z == 3.0
    assert node.score == 0.5


def test_node_model_no_node_id():
    with pytest.raises(ValidationError):
        NodeModel(x=1.0)


def test_node_model_no_score():
    node = NodeModel(node_id=0, x=1.0, y=2.0, z=3.0)
    assert node.node_id == 0
    assert node.x == 1.0
    assert node.y == 2.0
    assert node.z == 3.0
    assert node.score is None


def test_node_model_from_json(node_json):
    node = NodeModel.parse_raw(node_json)
    assert node.node_id == 0
    assert node.score == 0.5


def test_node_model_extra():
    node = NodeModel(node_id=0, x=1.0, y=2.0, z=3.0, extra="extra")
    assert node.node_id == 0
    assert node.x == 1.0
    assert node.y == 2.0
    assert node.z == 3.0
    assert node.score is None
    assert node.extra == "extra"


# ----------------------------------------------
#              EdgeModel
# ----------------------------------------------


def test_edge_model():
    edge = EdgeModel(edge_id=0, source_id=0, target_id=1, score=0.5)
    assert edge.edge_id == 0
    assert edge.source_id == 0
    assert edge.target_id == 1
    assert edge.score == 0.5


def test_edge_model_no_edge_id():
    with pytest.raises(ValidationError):
        EdgeModel(source_id=0, target_id=1)


def test_edge_model_no_source_id():
    with pytest.raises(ValidationError):
        EdgeModel(edge_id=0, target_id=1)


def test_edge_model_no_target_id():
    with pytest.raises(ValidationError):
        EdgeModel(edge_id=0, source_id=1)


def test_edge_model_no_score():
    edge = EdgeModel(edge_id=0, source_id=0, target_id=1)
    assert edge.edge_id == 0
    assert edge.source_id == 0
    assert edge.target_id == 1
    assert edge.score is None


def test_edge_model_from_json(edge_json):
    edge = EdgeModel.parse_raw(edge_json)
    assert edge.edge_id == 0
    assert edge.source_id == 0
    assert edge.target_id == 1
    assert edge.score == 0.5


def test_edge_model_extra():
    edge = EdgeModel(edge_id=0, source_id=0, target_id=1, extra="extra")
    assert edge.edge_id == 0
    assert edge.source_id == 0
    assert edge.target_id == 1
    assert edge.score is None
    assert edge.extra == "extra"


# ----------------------------------------------
#              GraphModel
# ----------------------------------------------


def test_graph_model(node_json, edge_json):
    nodes = [NodeModel(node_id=i, x=1.0, y=2.0, z=3.0, score=0.5) for i in range(10)]
    edges = [
        EdgeModel(edge_id=i, source_id=i, target_id=i + 1, score=0.5) for i in range(9)
    ]
    graph = GraphModel(nodes=nodes, edges=edges)
    for i, node in enumerate(graph.nodes):
        assert node.node_id == i
        assert node.x == 1.0
        assert node.y == 2.0
        assert node.z == 3.0
        assert node.score == 0.5
    for i, edge in enumerate(graph.edges):
        assert graph.edges[0].edge_id == 0
        assert graph.edges[0].source_id == 0
        assert graph.edges[0].target_id == 1
        assert graph.edges[0].score == 0.5


def test_graph_model_node_edge_mismatch():
    nodes = [NodeModel(node_id=0, x=1.0, y=2.0, z=3.0, score=0.5)]
    edges = [EdgeModel(edge_id=0, source_id=0, target_id=1, score=0.5)]
    with pytest.raises(ValidationError):
        GraphModel(nodes=nodes, edges=edges)
