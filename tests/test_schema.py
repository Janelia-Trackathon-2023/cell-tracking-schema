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
    return '{"node_id": 0, "coordinates": [1.0, 2.0], "score": 0.5}'


@pytest.fixture
def edge_json():
    return '{"edge_id": 0, "src_id": 0, "dst_id": 1, "score": 0.5}'


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
    node = NodeModel(node_id=0, coordinates=(1.0, 2.0), score=0.5)
    assert node.node_id == 0
    assert node.coordinates == (1.0, 2.0)
    assert node.score == 0.5


def test_node_model_no_node_id():
    with pytest.raises(ValidationError):
        NodeModel(coordinates=(1.0, 2.0))


def test_node_model_no_coordinates():
    with pytest.raises(ValidationError):
        NodeModel(node_id=0)


def test_node_model_no_score():
    node = NodeModel(node_id=0, coordinates=(1.0, 2.0))
    assert node.node_id == 0
    assert node.coordinates == (1.0, 2.0)
    assert node.score is None


def test_node_model_from_json(node_json):
    node = NodeModel.parse_raw(node_json)
    assert node.node_id == 0
    assert node.coordinates == (1.0, 2.0)
    assert node.score == 0.5


def test_node_model_extra():
    node = NodeModel(node_id=0, coordinates=(1.0, 2.0), extra="extra")
    assert node.node_id == 0
    assert node.coordinates == (1.0, 2.0)
    assert node.score is None
    assert node.extra == "extra"


# ----------------------------------------------
#              EdgeModel
# ----------------------------------------------


def test_edge_model():
    edge = EdgeModel(edge_id=0, src_id=0, dst_id=1, score=0.5)
    assert edge.edge_id == 0
    assert edge.src_id == 0
    assert edge.dst_id == 1
    assert edge.score == 0.5


def test_edge_model_no_edge_id():
    with pytest.raises(ValidationError):
        EdgeModel(src_id=0, dst_id=1)


def test_edge_model_no_src_id():
    with pytest.raises(ValidationError):
        EdgeModel(edge_id=0, dst_id=1)


def test_edge_model_no_dst_id():
    with pytest.raises(ValidationError):
        EdgeModel(edge_id=0, src_id=0)


def test_edge_model_no_score():
    edge = EdgeModel(edge_id=0, src_id=0, dst_id=1)
    assert edge.edge_id == 0
    assert edge.src_id == 0
    assert edge.dst_id == 1
    assert edge.score is None


def test_edge_model_from_json(edge_json):
    edge = EdgeModel.parse_raw(edge_json)
    assert edge.edge_id == 0
    assert edge.src_id == 0
    assert edge.dst_id == 1
    assert edge.score == 0.5


def test_edge_model_extra():
    edge = EdgeModel(edge_id=0, src_id=0, dst_id=1, extra="extra")
    assert edge.edge_id == 0
    assert edge.src_id == 0
    assert edge.dst_id == 1
    assert edge.score is None
    assert edge.extra == "extra"


# ----------------------------------------------
#              GraphModel
# ----------------------------------------------


def test_graph_model(node_json, edge_json):
    nodes = [
        NodeModel(node_id=0, coordinates=(1.0, 2.0), score=0.5),
        NodeModel(node_id=1, coordinates=(2.0, 3.0), score=0.5),
    ]
    edges = [EdgeModel(edge_id=0, src_id=0, dst_id=1, score=0.5)]
    graph = GraphModel(nodes=nodes, edges=edges, axis_order=("X", "Y"))
    assert graph.nodes[0].node_id == 0
    assert graph.nodes[0].coordinates == (1.0, 2.0)
    assert graph.nodes[0].score == 0.5
    assert graph.edges[0].edge_id == 0
    assert graph.edges[0].src_id == 0
    assert graph.edges[0].dst_id == 1
    assert graph.edges[0].score == 0.5
    assert graph.axis_order == ("X", "Y")


def test_graph_model_coordinates_axis_order_mismatch():
    nodes = [
        NodeModel(node_id=0, coordinates=(1.0, 2.0), score=0.5),
        NodeModel(node_id=1, coordinates=(2.0, 3.0), score=0.5),
    ]
    edges = [EdgeModel(edge_id=0, src_id=0, dst_id=1, score=0.5)]
    with pytest.raises(ValidationError):
        GraphModel(nodes=nodes, edges=edges, axis_order=("X",))


def test_graph_model_node_edge_mismatch():
    nodes = [NodeModel(node_id=0, coordinates=(1.0, 2.0), score=0.5)]
    edges = [EdgeModel(edge_id=0, src_id=0, dst_id=1, score=0.5)]
    with pytest.raises(ValidationError):
        GraphModel(nodes=nodes, edges=edges, axis_order=("X", "Y"))
