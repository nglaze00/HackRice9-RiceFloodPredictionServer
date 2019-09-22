"""
Functions for calculating shortest dry paths between nodes

1. 29.719204, -95.407239 : {2:.6, 7:1, 21:2} Entrance 16


"""
import networkx as nx
import ast


GRAPH_FILENAME = "NewNodes.txt"

class Graph:
    """
    Graph representations + operations on Rice campus graph
    """
    def __init__(self, filename):
        self.graph = self.text_to_graph(filename)

    def nodes(self):
        return self.graph.nodes.data()
    def edges(self):
        return self.graph.edges.data()

    def text_to_graph(self, filename):
        """
        Converts a correctly-formatted text file to an adjacency list
        :param filename: *.txt
        :return: nx.Graph object
        """
        graph = nx.Graph()
        for idx, line in enumerate(open(filename).readlines()):
            print([line])
            if line == "\n":
                continue
            splits = line.split(" ", 4)
            coords = (float(splits[1][:-1]), float(splits[2]))
            edges = ast.literal_eval(splits[-1].split("}")[0] + "}")
            potential_entrance = splits[-1].split("}")[-1].split(" ")[-1]
            print([potential_entrance])
            if potential_entrance != "\n":

                graph.add_node(idx, coords=coords, entrance=int(potential_entrance[:-1]))
            else:
                graph.add_node(idx, coords=coords, entrance=-1)
            for nbr, dist in edges.items():
                graph.add_edge(int(idx), int(nbr) - 1, dist = dist)

        return graph

    def shortest_path_without(self, start, end, wet_nodes):
        """
        Uses Dijsktra's algorithm to compute the shortest path from start to end, excluding all flooded nodes.
        :return: tuple: (path_type, list of successive nodes)

            path types:
                0: dry path
                1: wet path (ur fucked)
        """
        path_type = 0
        dry_graph = self.graph.copy()
        for node in wet_nodes:
            dry_graph.remove_node(node)
        try:
            path = nx.shortest_path(dry_graph, start, end, weight="dist")
            if len(path) == 1 and start != end:
                raise Exception

            else:
                return path
        except: # ValueError or NetworkXNoPath
            path_type = 1


g = Graph("nodes.txt")
print(g.nodes())

