from igraph import *
from CSPNode import CSPNode
from CSPVariable import CSPVariable

class TreePlot:

    def __init__(self):
        pass

    def create_node_label(self, node: CSPNode):
        return '\n'.join([str(v) for v in node.get_variables()])

    def draw(self, node: CSPNode, print_domains=False):
        graph = Graph()
        
        colors_palette = {"failure": "red", "solution": "green", "normal": "yellow"}

        graph.vs["name"] = []
        graph.vs["state"] = []

        graph.es["variable_assigned"] = []

        graph.add_vertices(1)

        if print_domains:
            graph.vs[0]["name"] = self.create_node_label(node)
        else:
            graph.vs[0]["name"] = 0
        
        graph.vs[0]["state"] = "normal"

        for child in node.get_children():
            self.generate_graph(graph, child, 0)

        layout = graph.layout_reingold_tilford(root=[0])

        #graph.write_svg(fname="plot.svg", , colors=graph.vs["color"], vertex_size=20)
        visual_style = {}

        if print_domains:
            visual_style["vertex_size"] = 10 * max(len(node.get_variables()), max([len(v.domain) for v in node.get_variables()]))
            visual_style["bbox"] = ((visual_style["vertex_size"] + 20) * graph.vcount(), (visual_style["vertex_size"] + 75) * len(node.get_variables()))
            visual_style["vertex_label_size"] = 7
            visual_style["margin"] = visual_style["vertex_size"] + 30
        else:
            visual_style["vertex_size"] = 20
            visual_style["vertex_label_size"] = 10
            visual_style["bbox"] = (20 * graph.vcount(), 100 * len(node.get_variables()))
            visual_style["margin"] = 50

        visual_style["vertex_shape"] = "rectangle"
        visual_style["vertex_color"] = [colors_palette[state] for state in graph.vs["state"]]
        visual_style["vertex_label"] = graph.vs["name"]
        visual_style["vertex_label_size"] = 7
        visual_style["layout"] = layout
        visual_style["bbox"] = ((visual_style["vertex_size"] + 20) * graph.vcount(), (visual_style["vertex_size"] + 75) * len(node.get_variables()))
        visual_style["margin"] = visual_style["vertex_size"] + 30
        plot(graph, target="plot.svg", **visual_style)

    def generate_graph(self, graph, node: CSPNode, parent_vertex_id: int):
        print_domains = False
        graph.add_vertices(1)
        node_vertex_id = graph.vcount() - 1

        if print_domains:
            graph.vs[node_vertex_id]["name"] = self.create_node_label(node)
        else:
            graph.vs[node_vertex_id]["name"] = node_vertex_id
        
        if node.solution:
            graph.vs[node_vertex_id]["state"] = "solution"
        elif node.failure:
            graph.vs[node_vertex_id]["state"] = "failure"
        else:
            graph.vs[node_vertex_id]["state"] = "normal"

        graph.add_edges([(parent_vertex_id, node_vertex_id)])
        assigned_variable = node.get_variable_by_name(node._last_assigned_variable_name)
        if assigned_variable:
            graph.es[node_vertex_id - 1]["label"] = assigned_variable.name + " = " + str(assigned_variable.value)
        else:
            graph.es[node_vertex_id - 1]["label"] = ""

        for child in node.get_children():
            self.generate_graph(graph, child, node_vertex_id)