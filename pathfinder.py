import numpy as np
import copy
from itertools import chain, combinations

"""
Least Admissible Set of Covariates for Conditioning
As Per Judea Pearl's 2009 Paper

Program Created By:
Joshua LeVar
Charlie Skinner
Dennis Konan
"""

def main():
    graph = ex6    # Examples at bottom of file
    descendants_of_x = find_descendants(graph, 0)
    backdoor_paths = all_backdoor_paths_x_to_y(graph)

    # Generate all possible sets of nodes (excluding X and Y) 
    power_set = powerset(range(2, graph.shape[0]))
    # Remove all sets with descendants of X 
    adjusted_set = [set for set in power_set if not list_in_set(descendants_of_x, set)]

    # Check all sets from smallest to largest until solution(s) are found
    admissible_sets = []
    size_of_smallest_admissible_set = np.inf
    for set in adjusted_set:
        if len(set) > size_of_smallest_admissible_set:
            break
    
        if blocks_all_paths(set, backdoor_paths, graph):
            size_of_smallest_admissible_set = len(set)
            admissible_sets.append(set)

    print("GRAPH\n", graph, "\n========") 
    print("DESCENDANTS OF X\n", descendants_of_x, "\n========")
    print("BACKDOOR PATHS\n", [path for path in backdoor_paths], "\n========")
    print("POWERSET\n", power_set, "\n========")
    print("ADJUSTED SET\n", adjusted_set, "\n========")
    print("LEAST ADMISSIBLE SETS\n", [set for set in admissible_sets])


def find_descendants(graph, node):
    descendants = []
    
    def find_descendants_recursive(current_node):
        successors = []
        for i in range(graph.shape[0]):
            node = graph.item((current_node, i))
            if node and i not in descendants:
                successors.append(i)
                descendants.append(i)

        for successor in successors:
            find_descendants_recursive(successor)

    find_descendants_recursive(node)
        
    return descendants
 

def all_backdoor_paths_x_to_y(graph):
    # Generate all starting points for a path        
    starting_points = []
    for i, node in enumerate(graph[:, 0]):
        if node == 1:
            starting_points.append(i)    

    def find_paths_recursion(graph, current, goal, current_path):
        current_path.append(current)

        if current == goal:
            paths_found.append(copy.copy(current_path))

            current_path.pop()
            return

        else:
            connections = []

            for i in range(graph.shape[0]):
                if (graph.item(current, i) or graph.item(i, current)) and (i not in current_path):
                    connections.append(i)

            for connection in connections:
                find_paths_recursion(graph, connection, goal, current_path)

        current_path.pop()

    all_paths = []   

    for point in starting_points:
        paths_found = []
        find_paths_recursion(graph, point, 1, [0])
        for path in paths_found:
            all_paths.append(path)

    return all_paths


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))


def list_in_set(list, set):
    for elem in list:
        if elem in set:
            return True
    return False


def list_not_in_set(list, set):
    for elem in list:
        if elem in set:
            return False
    return True


def is_collider(node_index, path, graph) -> bool:
    if node_index <= 0 or node_index >= (len(path)-1):
        return False

    incoming_arrow_left = graph.item(path[node_index-1], path[node_index])
    incoming_arrow_right = graph.item(path[node_index+1], path[node_index])

    return incoming_arrow_left and incoming_arrow_right


def blocks_all_paths(set, paths, graph) -> bool:
    for path in paths:
        if not blocks_path(set, path, graph):
            return False
    return True


def blocks_path(set, path, graph) -> bool:
    for i in range(1, len(path)-1):
        node = path[i]        
        if node in set: 
            ## Condition 1 -- Is arrow emitting node
            arrow_backwards = bool(graph.item(node, path[i-1]))
            arrow_forwards = bool(graph.item(node, path[i+1]))

            if arrow_backwards or arrow_forwards:
                return True 
        else:
            ## Condition 2 -- Collider (or descendant) outside of set
            if is_collider(i, path, graph):
                collider_and_descendants = [i] + find_descendants(graph, i)
                if list_not_in_set(collider_and_descendants, set):
                    return True
    return False


### Examples
ex2 = np.matrix([[0, 1, 1, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [0, 1, 0, 0, 0]])

ex3 = np.matrix([[0, 1, 1, 0],
                [0, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 1, 0]])

ex4 = np.matrix([[0, 1, 1, 1],
                [0, 0, 0, 0],
                [0, 0, 0, 1],
                [0, 1, 0, 0]])

ex5 = np.matrix([[0, 1, 1, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1],
                [1, 1, 0, 0, 1],
                [0, 1, 0, 0, 0]])

# example 6: Confouding M Triangles
ex6 = np.matrix([[0, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [1, 0, 0, 1, 0],
                 [1, 1, 0, 0, 0],
                 [0, 1, 0, 1, 0]])

ex7 = np.matrix([[0, 1, 0, 1],
                 [0, 0, 0, 0],
                 [1, 0, 0, 1],
                 [0, 1, 0, 0]])

ex8 = np.matrix([
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]])

ex9 = np.matrix([[0, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [1, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0],
                 [0, 1, 0, 1, 0]])

if __name__=="__main__":
    main()


