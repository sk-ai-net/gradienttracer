from typing import List, Dict

import torch
from torch import Tensor

from gt.dot.dag import Graph, Node, OpNode, Edge, ValueNode


def trace(root: Tensor) -> Graph:
    """
    Converts pytorch's DAG with tensors and operations into generic graph
    :param root: output tensor
    :return: generic graph
    """
    nodes: Dict[str, Node] = dict()
    edges: List[Edge] = list()

    def get_unique_name(obj, suffix=""):
        return f"{id(obj)}{suffix}"

    def build(v):
        if get_unique_name(v) not in nodes:
            if hasattr(v, 'data'):
                id = get_unique_name(v)
                node = ValueNode(
                    name=id,
                    value=v.item() if hasattr(v, 'data') else None,
                    grad=v.grad.item() if v.grad is not None else None
                )
                nodes[id] = node
            elif hasattr(v, 'variable'):
                # Handles the case for leaf tensors
                id = get_unique_name(v)
                node = ValueNode(
                    name=id,
                    value=v.variable.item() if hasattr(v.variable, 'data') else None,
                    grad=v.variable.grad.item() if v.variable.grad is not None else None
                )
                nodes[id] = node
            if hasattr(v, 'grad_fn') and v.grad_fn:
                op_name = type(v.grad_fn).__name__.replace('Backward', '')
                op_node_name = get_unique_name(v, op_name)
                op_node = OpNode(op_node_name)
                nodes[op_node_name] = op_node
                edges.append(Edge(op_node_name, get_unique_name(v)))
                for child, _ in v.grad_fn.next_functions:
                    if child is not None:
                        edges.append(Edge(get_unique_name(child), op_node_name))
                        build(child)
            elif isinstance(v, torch.Tensor) and v.grad_fn is None:
                node = ValueNode(
                    name=get_unique_name(v),
                    value=v.item() if hasattr(v, 'data') else None,
                    grad=v.grad.item() if v.grad is not None else None
                )
                nodes[get_unique_name(v)] = node

    build(root)
    return Graph(nodes, edges)


if __name__ == '__main__':
    # Simple example to test the trace function
    a = torch.tensor(3.0, requires_grad=True)
    b = torch.tensor(2.0, requires_grad=True)
    c = a * b

    graph = trace(c)

    # Print the traced nodes and edges
    for k, n in graph.nodes.items():
        if isinstance(n, ValueNode):
            print(f"Node {n.name}: value={n.value}, grad={n.grad}")
        elif isinstance(n, OpNode):
            print(f"OpNode {n.name}")
    for n1 in graph.edges:
        print(f"Edge from {n1.from_node} to {n1.to_node}")
