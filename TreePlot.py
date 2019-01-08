from igraph import *
from igraph.drawing import *
from igraph.drawing.graph import AbstractCairoGraphDrawer, AttributeCollectorBase
from igraph.drawing.vertex import *
from igraph.drawing.shapes import *
from igraph.drawing.edge import *
from igraph.drawing.text import *
from CSPSolver import CSPSolver
from CSPNode import CSPNode
from CSPVariable import CSPVariable

class SolverPlot:

    def __init__(self, solver: CSPSolver):
        self._solver = solver

    def create_node_label(self, node: CSPNode):
        return '\n'.join([str(v) for v in node.get_variables()])
        
    def draw_constraint_graph(self):
        graph = Graph()

        graph.add_vertices(len(self._solver._root.get_variables()))

        graph.vs["label"] = [variable.name for variable in self._solver._root.get_variables()]

        for index_1, variable_1 in enumerate(self._solver._root.get_variables()):
            if self._solver._constraints.get_unary_constraints(variable_1.name):
                graph.add_edges([(index_1, index_1)])

            for index_2, variable_2 in enumerate(self._solver._root.get_variables()):
                if index_2 > index_1:
                    cs1, cs2 = self._solver._constraints.get_binary_constraints(variable_1.name, variable_2.name)
                    if cs1 or cs2:
                        graph.add_edges([(index_1, index_2)])

        visual_style = {}
        visual_style["margin"] = 50
        visual_style["vertex_size"] = 24

        plot(graph, target="constraints.svg", **visual_style)



    def draw_decision_tree(self, print_domains=False):
        node = self._solver._root
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
            self.generate_graph(graph, child, 0, print_domains)

        layout = graph.layout_reingold_tilford(root=[0])

        visual_style = {}
        n_leaf = graph.vcount() - sum([1 for n in graph.vs["state"] if n == "normal"])

        margin = 70

        if print_domains:
            font_size = 7
            domains_length = [sum([len(str(val)) for val in v.domain]) + 2 + len(v.name) for v in node.get_variables()]
            visual_style["vertex_width"] = font_size * max(domains_length)
            visual_style["vertex_height"] = (font_size + 2) * len(node.get_variables())
            visual_style["vertex_label_size"] = font_size
            visual_style["bbox"] = (n_leaf * (visual_style["vertex_width"] + 20) + margin, (visual_style["vertex_height"] + 70) * len(node.get_variables()))
            
        else:
            variables_length = max([max([len(str(val)) for val in v.domain]) + 3 + len(v.name) for v in node.get_variables()])
            visual_style["vertex_width"] = 20
            visual_style["vertex_height"] = 20
            visual_style["vertex_label_size"] = 14
            visual_style["bbox"] = (n_leaf * (visual_style["vertex_width"] + variables_length * 14 + 5) + margin, (visual_style["vertex_height"] + 70) * len(node.get_variables()))

        visual_style["margin"] = margin
        visual_style["vertex_shape"] = "rectangle"
        visual_style["vertex_color"] = [colors_palette[state] for state in graph.vs["state"]]
        visual_style["vertex_label"] = graph.vs["name"]
        visual_style["layout"] = layout

        visual_style["drawer_factory"] = CustomGraphDrawer


        plot(graph, target="plot.svg", **visual_style)

    def generate_graph(self, graph, node: CSPNode, parent_vertex_id: int, print_domains):
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
            graph.es[node_vertex_id - 1]["label"] = " " + assigned_variable.name + " = " + str(assigned_variable.value)
        else:
            graph.es[node_vertex_id - 1]["label"] = ""

        for child in node.get_children():
            self.generate_graph(graph, child, node_vertex_id, print_domains)


class CustomVertexDrawer(DefaultVertexDrawer):
    def _construct_visual_vertex_builder(self):
        class VisualVertexBuilder(AttributeCollectorBase):
            """Collects some visual properties of a vertex for drawing"""
            _kwds_prefix = "vertex_"
            color = ("red", self.palette.get)
            frame_color = ("black", self.palette.get)
            frame_width = 1.0
            label = None
            label_angle = -pi/2
            label_dist  = 0.0
            label_color = ("black", self.palette.get)
            label_size  = 14.0
            position = dict(func=self.layout.__getitem__)
            shape = ("circle", ShapeDrawerDirectory.resolve_default)
            size  = 20.0
            width = 20.0
            height = 20.0
        return VisualVertexBuilder

    def draw(self, visual_vertex, vertex, coords):
        context = self.context

        visual_vertex.shape.draw_path(context, \
                coords[0], coords[1], visual_vertex.width, visual_vertex.height)
        context.set_source_rgba(*visual_vertex.color)
        context.fill_preserve()
        context.set_source_rgba(*visual_vertex.frame_color)
        context.set_line_width(visual_vertex.frame_width)
        context.stroke()


class CustomGraphDrawer(DefaultGraphDrawer):

    def __init__(self, context, bbox, \
                 vertex_drawer_factory = CustomVertexDrawer,
                 edge_drawer_factory = ArrowEdgeDrawer,
                 label_drawer_factory = TextDrawer):

        AbstractCairoGraphDrawer.__init__(self, context, bbox)
        self.vertex_drawer_factory = vertex_drawer_factory
        self.edge_drawer_factory = edge_drawer_factory
        self.label_drawer_factory = label_drawer_factory
