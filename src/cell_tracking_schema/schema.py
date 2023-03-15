from typing import List, Optional
from pydantic import BaseModel, root_validator
import networkx as nx


class RequiredFieldsMixin:
    """Return only the required fields from a pydantic model."""

    @classmethod
    def required_fields(cls) -> List[str]:
        fields = [f for f, v in cls.__fields__.items() if v.required]
        return fields


class FloatTuple(List[float]):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, values: List[float]):
        return tuple(float(v) for v in values)


class StrTuple(List[str]):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, values: List[str]):
        return tuple(str(v) for v in values)


class NodeModel(BaseModel):
    node_id: int

    # coordinates: FloatTuple  # can be an empty tuple
    t: Optional[float] = None
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
    score: Optional[float] = None

    class Config:
        extra = "allow"


class EdgeModel(BaseModel):
    edge_id: int
    source_id: int
    target_id: int
    score: Optional[float] = None

    class Config:
        extra = "allow"


class GraphModel(BaseModel):
    nodes: List[NodeModel]
    edges: List[EdgeModel]

    @root_validator
    def validate(cls, values):
        nodes = values.get("nodes")
        edges = values.get("edges")
        node_ids = set(node.node_id for node in nodes)
        edge_node_set = set(edge.source_id for edge in edges).union(
            set(edge.target_id for edge in edges)
        )
        if not edge_node_set.issubset(node_ids):
            raise ValueError
        return values

    def as_networkx(self):
        g = nx.DiGraph()
        g.add_nodes_from([(node.node_id, node) for node in self.nodes])
        g.add_edges_from(
            [(edge.source_id, edge.target_id, edge) for edge in self.edges]
        )
        return g

    @classmethod
    def parse_networkx(cls, graph):
        nodes = [NodeModel.parse_obj(obj[1]) for obj in graph.nodes(data=True)]
        edges = [EdgeModel.parse_obj(obj[2]) for obj in graph.edges(data=True)]
        graph_model = cls(
            nodes=nodes,
            edges=edges,
        )
        return graph_model


class TrackModel(BaseModel):
    track_id: int
    start_id: int
    end_id: int

    class Config:
        extra = "allow"
