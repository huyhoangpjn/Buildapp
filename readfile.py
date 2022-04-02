from dataclasses import dataclass
from enum import Enum
from optparse import OptionParser
import sys

@dataclass
class Node:
    lat: float
    lon: float

@dataclass
class Edge:
    source_id: int
    target_id: int
    length: float
    max_speed: int
    time: float

class InputState(Enum):
    NMB_NODES = 2
    NMB_EDGES = 3
    NODES = 4
    EDGES = 5

def read_file(filename):
    state = InputState.NMB_NODES

    nodes = {}
    edges = []
    nmb_nodes = None
    nmb_edges = None
    with open(filename, "r", encoding="utf-8") as input_file:
        for line in input_file:
            if line.startswith("#"):
                continue

            if state == InputState.NMB_NODES:
                nmb_nodes = int(line)
                state = InputState.NMB_EDGES
            elif state == InputState.NMB_EDGES:
                nmb_edges = int(line)
                state = InputState.NODES
            elif state == InputState.NODES:
                node_id, lat, lon = line.split(" ")
                nodes[int(node_id)] = Node(float(lat), float(lon))
                if len(nodes) == nmb_nodes:
                    state = InputState.EDGES
            elif state == InputState.EDGES:
                (
                    source_id,
                    target_id,
                    length,
                    street_type,
                    max_speed,
                    bidirectional,
                ) = line.split(" ")
                time = float(length)/float(max_speed)
                edges.append(Edge(int(source_id), int(target_id), float(length),int(max_speed),float(time)))
                if int(bidirectional)==1:
                    edges.append(Edge(int(target_id), int(source_id), float(length),int(max_speed),float(time)))

    return nodes, edges