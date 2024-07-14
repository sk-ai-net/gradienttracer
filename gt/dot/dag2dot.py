from graphviz import Digraph

from gt.dot.dag import Graph, ValueNode, OpNode


def dag_2_dot(dag: Graph, format='svg', rankdir='LR'):
    """
    format: png | svg | ...
    rankdir: TB (top to bottom graph) | LR (left to right)
    """
    assert rankdir in ['LR', 'TB']
    dot = Digraph(format=format, graph_attr={'rankdir': rankdir})

    for key, node in dag.nodes.items():
        if isinstance(node, ValueNode):
            if node.value is not None and node.grad is None:
                dot.node(name=key, label="{ data %.4f | grad %.4f }" % (node.value, 0.0), shape='record')
            elif node.grad is not None:
                dot.node(name=key, label="{ data %.4f | grad %.4f }" % (node.value, node.grad), shape='record')

        if isinstance(node, OpNode):
            dot.node(name=key, label=node.name)

    for e in dag.edges:
        dot.edge(e.from_node, e.to_node)

    return dot
