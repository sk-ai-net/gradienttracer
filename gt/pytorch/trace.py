import torch
from torch import Tensor


class Node:
    def __init__(self, name: str, value: float, grad: float):
        self.name = name
        self.value = value
        self.grad = grad


class OpNode:
    def __init__(self, name: str):
        self.name = name


def trace(root: Tensor):
    nodes, edges = {}, set()

    def get_unique_name(obj, suffix=""):
        return f"{id(obj)}{suffix}"

    def build(v):
        if get_unique_name(v) not in nodes:
            if hasattr(v, 'data'):
                id = get_unique_name(v)
                node = Node(
                    name=id,
                    value=v.item() if hasattr(v, 'data') else None,
                    grad=v.grad.item() if v.grad is not None else None
                )
                nodes[id] = node
            elif hasattr(v, 'variable'):
                # Handles the case for leaf tensors
                id = get_unique_name(v)
                node = Node(
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
                edges.add((op_node_name, get_unique_name(v)))
                for child, _ in v.grad_fn.next_functions:
                    if child is not None:
                        edges.add((get_unique_name(child), op_node_name))
                        build(child)
            elif isinstance(v, torch.Tensor) and v.grad_fn is None:
                node = Node(
                    name=get_unique_name(v),
                    value=v.item() if hasattr(v, 'data') else None,
                    grad=v.grad.item() if v.grad is not None else None
                )
                nodes[get_unique_name(v)] = node

    build(root)
    return nodes, edges


if __name__ == '__main__':
    # Simple example to test the trace function
    a = torch.tensor(3.0, requires_grad=True)
    b = torch.tensor(2.0, requires_grad=True)
    c = a * b

    nodes, edges = trace(c)

    # Print the traced nodes and edges
    for n in nodes.values():
        if isinstance(n, Node):
            print(f"Node {n.name}: value={n.value}, grad={n.grad}")
        elif isinstance(n, OpNode):
            print(f"OpNode {n.name}")
    for n1, n2 in edges:
        print(f"Edge from {n1} to {n2}")
