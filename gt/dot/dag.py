from typing import Dict, List
from abc import ABC, abstractmethod


class Node(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def __repr__(self):
        pass


class ValueNode(Node):
    def __init__(self, name: str, value: float, grad: float):
        super().__init__(name)
        self.value = value
        self.grad = grad

    def __repr__(self):
        return f"Node(name={self.name}, value={self.value}, grad={self.grad})"


class OpNode(Node):
    def __init__(self, name: str):
        super().__init__(name)

    def __repr__(self):
        return f"OpNode(name={self.name})"


class Edge:
    def __init__(self, from_node: str, to_node: str):
        self.from_node = from_node
        self.to_node = to_node


class Graph:
    def __init__(self, nodes: Dict[str, Node], edges: List[Edge]):
        self.nodes = nodes
        self.edges = edges

    def add_node(self, node: Node):
        self.nodes[node.name] = node

    def add_edge(self, from_node: Node, to_node: Node):
        edge = Edge(from_node, to_node)
        self.edges.append(edge)

    def find_node(self, name: str):
        if name in self.nodes:
            return self.nodes[name]
        return None

    def __repr__(self):
        repr_str = "Graph:\n"
        repr_str += "Nodes:\n"
        for key, node in self.nodes.items():
            if isinstance(node, ValueNode):
                repr_str += f"  {node.name}: value={node.value}, grad={node.grad}\n"
            elif isinstance(node, OpNode):
                repr_str += f"  {node.name}\n"
        repr_str += "Edges:\n"
        for edge in self.edges:
            repr_str += f"  {edge.from_node.name} -> {edge.to_node.name}\n"
        return repr_str
