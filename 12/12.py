#!/usr/bin/env python3

import sys

with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = f.readlines()

data = [x.strip().split("-") for x in data]


class Node:
    def __init__(self, p):
        self.x = p
        self.neighbors = set()
        self.small = False if p in ["start", "end"] else self.x.islower()
        self.visited = 0

    def __eq__(self, obj):
        if self.x == obj.x:
            return True
        return False

    def __hash__(self):
        return hash(self.x)


def get_node(s, nodes):
    for n in nodes:
        if s == n.x:
            return n
    raise ValueError(f"Not found: {s}.")


def set_nodes(data):
    nodes = set()
    for d in data:
        for p in d:
            node = Node(p)
            exists = any(True for x in nodes if x == node)
            if not exists:
                nodes.add(node)

    for d in data:
        x, y = d
        node_x = get_node(x, nodes)
        node_y = get_node(y, nodes)
        node_x.neighbors.add(y)
        node_y.neighbors.add(x)

    return nodes


def copy_nodes(old_nodes):
    new_nodes = set()
    for n in old_nodes:
        new = Node(n.x)
        new.visited = n.visited
        new.neighbors = n.neighbors.copy()
        new_nodes.add(new)
    return new_nodes


def calc_paths(nodes, path, part2):
    x = path[-1]
    if x == "end":
        paths.append(path)
        return

    node = get_node(x, nodes)
    node.visited += 1
    neigh = []
    for x_n in node.neighbors:
        node_n = get_node(x_n, nodes)
        if x_n == "end":
            neigh.append(x_n)
            continue
        if x_n == "start" or node_n.visited > 100:
            continue
        if part2 and node_n.small:
            visited_twice = any(n.visited >= 2 for n in nodes if n.small)
            if node_n.visited > 0 and visited_twice:
                continue
        else:
            if node_n.small and node_n.visited > 0:
                continue
        neigh.append(x_n)

    if not neigh:
        return

    for n_x in neigh:
        new_nodes = copy_nodes(nodes)
        calc_paths(new_nodes, path + [n_x], part2)


def calc(nodes, part2=False):
    path = ["start"]
    calc_paths(nodes, path, part2)


nodes = set_nodes(data)
paths = []
calc(nodes)
print(f"Part 1: {len(paths)}")

nodes = set_nodes(data)
paths = []
calc(nodes, part2=True)
print(f"Part 2: {len(paths)}")
