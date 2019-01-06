from igraph import *
from CSPNode import CSPNode
from CSPVariable import CSPVariable

class TreePlot:

    def __init__(self):
        pass


    def draw(self, node: CSPNode):
        graph = Graph()
        graph.vs['name'] = []

        graph.add_vertices(1)

        graph.vs['name'].append(0)

        for child in node.get_children():
            self.generate_graph(graph, child, 0)

        graph.write_svg(fname="plot.svg")
        

    def generate_graph(self, graph, node: CSPNode, parent_vertex_id: int):
        graph.add_vertices(1)
        node_vertex_id = graph.vcount() - 1
        graph.vs['name'].append(node_vertex_id)

        graph.add_edges([(parent_vertex_id, node_vertex_id)])

        for child in node.get_children():
            self.generate_graph(graph, child, node_vertex_id)