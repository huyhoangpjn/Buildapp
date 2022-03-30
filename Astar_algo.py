import networkx as nx
from readfile import read_file
import utm
import numpy as np
from scipy import spatial
from heapq import heappush, heappop
from itertools import count
from networkx.algorithms.shortest_paths.weighted import _weight_function
import utm

def ConvertToGraph(filename,output_graph):
    _, edge = read_file(filename)
    edge = [(edge[i].source_id,edge[i].target_id,edge[i].length) for i in range(0,len(edge))]
    G = nx.MultiDiGraph()
    G.add_weighted_edges_from(edge)
    nx.write_gml(G,output_graph + ".gml")
    nx.write_gpickle(G,output_graph + ".gpickle")

def load_graph_gpickle(filename):
    G = nx.read_gpickle(filename)
    return G

def get_coordinate(filename):
    node, _ = read_file(filename)
    x_coor = []
    y_coor = []
    for i in range(0,len(node)): 
        x,y,_,_ = utm.from_latlon(node[i].lat,node[i].lon)
        x_coor.append(x)
        y_coor.append(y)
    return x_coor, y_coor

def CalHeuristic(src_x,src_y,des_x,des_y):
    #EUCLIDEAN DISTANCE
    return ((src_x-des_x)**2+(src_y-des_y)**2)**0.5

def astar(G,src,des,x_coor,y_coor):
    push = heappush
    pop = heappop
    c = count()
    open_tup = [(0, next(c), src, 0, None)]
    parents = {}
    cost = {}

    #GET MIN WEIGHT BETWEEN 2 NODE
    weight = _weight_function(G,"weight")

    while open_tup:
        _, __, curr, g, parent = pop(open_tup)
        
        if curr == des:
            path = [curr]
            curr = parent
            while curr is not None:
                path.append(curr)
                curr = parents[curr]
            path.reverse()
            return path
        
        #Throw neighbors that were traversed
        if curr in parents:
            if parents[curr] is None:
                continue

            qg, h = cost[curr]
            if qg < g:
                continue
        
        parents[curr] = parent

        for neighbor, w in G[curr].items():
            g_new = g + weight(curr,neighbor,w)
            if neighbor in cost:
                g_old, h = cost[neighbor]
                if g_old < g_new:
                    continue
            else:
                h = CalHeuristic(x_coor[neighbor],y_coor[neighbor],x_coor[des],y_coor[des])
            cost[neighbor] = g_new, h
            push(open_tup,(g_new+h,next(c),neighbor,g_new,curr))
    
    raise nx.NetworkXNoPath(f"Node {des} not reachable from {src}")

def get_nearest_node(x,y,point):
    xy_matrix = np.dstack([x,y])[0]
    mytree = spatial.cKDTree(xy_matrix)
    _, index = mytree.query(point)
    return index

#ConvertToGraph("HCM_data_pedestrian.pypgr","Graph_pedestrian")
# x_coor,y_coor = get_coordinate('data\HCM_data_car.pycgr')
# G = load_graph_gpickle('graph/Graph_car.gpickle')
# # print(astar(G,27958,7804,x_coor,y_coor))
# max_weight = max(dict(G.edges).items(), key=lambda x: x[1]["weight"])
# print(max_weight)