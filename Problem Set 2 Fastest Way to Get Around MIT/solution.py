import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer:
#


# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """

    # TODO
    graph = Digraph()
    edges = []
    nodes = set([])
    print("Loading map from file...")
    with open(map_filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue
            node_src, node_dest, total_dis, outdoor = line.split(" ")
            node_src_obj = Node(node_src)
            node_dest_obj = Node(node_dest)
            edge = WeightedEdge(
                node_src_obj, node_dest_obj, total_dis, outdoor)
            edges.append(edge)
            nodes.add(node_src_obj)
            nodes.add(node_dest_obj)
    for node in nodes:
        graph.add_node(node)
    for edge in edges:
        graph.add_edge(edge)

    # print(str(graph))
    return graph


g = load_map("./mit_map.txt")


def printPath(path):
    """Assumes path is a list of nodes"""
    result = ''
    for i in range(len(path)):
        result = result + str(path[i])
        if i != len(path) - 1:
            result = result + '->'
    return result


def get_best_path(digraph: Digraph, start: str, end: str, path: list, max_dist_outdoors: int, best_dist: int,
                  best_path: list) -> tuple:
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    # TODO
    start_node = Node(start)
    end_node = Node(end)
    if not (digraph.has_node(start_node) and digraph.has_node(end_node)):
        raise ValueError("Node is not in the graph")

    if path is None:
        path = [[], 0, 0]
    nodes, current_dist, current_outdoor = path
    nodes = nodes + [start]

    if start == end:
        return (nodes, current_dist)

    for edge in digraph.get_edges_for_node(start_node):
        next_node = edge.get_destination()
        next_name = next_node.get_name()
        #
        if next_name not in nodes:
            new_dist = current_dist + int(edge.get_total_distance())
            new_outdoor = current_outdoor + int(edge.get_outdoor_distance())
            #
            if new_outdoor <= max_dist_outdoors:
                if best_dist is None or new_dist < best_dist:
                    result = get_best_path(
                        digraph, next_name, end, [nodes, new_dist, new_outdoor], max_dist_outdoors, best_dist, best_path)

                    if result is not None:
                        best_dist = result[1]
                        best_path = result[0]
    if best_path is None:
        return None
    return (best_path, best_dist)

# for n in ['2', '6', '8', '4', '10', '3', '7', '9']:
#     print(f"Node: {n}")
#     for egde in g.get_edges_for_node(Node(n)):
#         print(egde)


def dfs(graph, start, end, path, max_dist_outdoors, best_dist, shortest):
    if path is None:
        path = ([], 0, 0)

    nodes, dist, out_door = path
    nodes = nodes + [start]

    if start == end:
        return (nodes, dist)

    for edge in graph.get_edges_for_node(Node(start)):
        next_node = edge.get_destination().get_name()

        if next_node not in nodes:

            new_dist = dist + int(edge.get_total_distance())
            new_out_door = out_door + int(edge.get_outdoor_distance())
            if new_out_door <= max_dist_outdoors:
                if best_dist is None or new_dist < best_dist:

                    result = dfs(
                        graph,
                        next_node,
                        end,
                        (nodes, new_dist, new_out_door),
                        max_dist_outdoors,
                        best_dist,
                        shortest
                    )

                    if result:
                        shortest = result
                        best_dist = result[1]

    if shortest[0] is None:
        return None
    return shortest


foundPath = get_best_path(g, '10', '32', None, 9999, 9999, None)
print(foundPath)

my_list = foundPath[0]
total_length = 0
for n in range(0, len(my_list)-1):

    # print(my_list[n])
    node = Node(my_list[n])
    print("Node: ", node)
    for edge in g.get_edges_for_node(node):
        if edge.get_destination().get_name() == my_list[n+1]:
            print("Edge: ", edge)
            total_length += int(edge.get_total_distance())
print("Total Length :", total_length)
