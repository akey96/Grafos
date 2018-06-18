#!/usr/bin/python3
# coding: utf-8

import networkx as nx
import matplotlib.pyplot as plt


def firstTest():
    G = nx.Graph()
    routes = []
    routes.append(('LPZ', 'ORU', 3))
    routes.append(('ORU', 'PT', 10))
    routes.append(('ORU', 'CBA', 50))
    routes.append(('PT', 'CHQ', 3))
    routes.append(('PT', 'TJA', 7))
    routes.append(('TJA', 'CHQ', 6))
    routes.append(('TJA', 'SCZ', 8))
    routes.append(('SCZ', 'CBA', 4))
    G.add_weighted_edges_from(routes)
    nx.draw(G, with_labels=True)

    for vertice in G.edges.data():
        print(vertice)

    path = nx.single_source_dijkstra_path(G, 'LPZ', cutoff=90)
    for k, v in path.items():
        print(k, v)
    print("===================")
    G['ORU']['CBA']['weight'] = 1
    print("===================")
    for vertice in G.edges.data():
        print(vertice)
    path = nx.single_source_dijkstra_path(G, 'LPZ', cutoff=90)
    for k, v in path.items():
        print(k, v)




    plt.show()


firstTest()

