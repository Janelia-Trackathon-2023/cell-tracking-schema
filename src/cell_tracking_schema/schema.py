from typing import Any, List, Tuple, Optional
from pydantic import BaseModel, root_validator


class RequiredFieldsMixin:
    """Return only the required fields from a pydantic model."""
    @classmethod
    def required_fields(cls) -> list[str]:
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


class NodeModel(RequiredFieldsMixin, BaseModel):
    node_id: int
    coordinates: FloatTuple  # can be an empty tuple
    score: Optional[float] = None

    class Config:
        extra = "allow"


class EdgeModel(RequiredFieldsMixin, BaseModel):
    edge_id: int
    src_id: int
    dst_id: int
    score: Optional[float] = None

    class Config:
        extra = "allow"


class GraphModel(BaseModel):
    nodes: List[NodeModel]
    edges: List[EdgeModel]
    axis_order: StrTuple  # can be an empty tuple

    @root_validator
    def validate(cls, values):
        nodes = values.get("nodes")
        edges = values.get("edges")
        axis_order = values.get("axis_order")
        for node in nodes:
            if len(node.pos) != len(axis_order):
                raise ValueError
        node_ids = set(node.id for node in nodes)
        edge_node_set = set(edge.src_id for edge in edges).union(
            set(edge.dst_id for edge in edges)
        )
        if not edge_node_set.issubset(node_ids):
            raise ValueError


class TrackModel(GraphModel):
    track_id: int
    start_id: int
    end_id: int

    class Config:
        extra = "allow"
