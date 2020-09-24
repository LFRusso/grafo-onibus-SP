import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from networkx import centrality

# Lendo e formatando vértices
paths = []
with open("data/caminhos.dat", 'r') as file:
    paths = file.readlines()
paths = [path[:-1].split('/') for path in paths]
paths = np.array([path[-1].split('-x-') for path in paths])

G = nx.Graph()
G.add_edges_from(paths)

# Imprimindo cidades em ordem de centralidade
cntr = centrality.degree_centrality(G)
sorted_cntr = {k: v for k, v in sorted(cntr.items(), key=lambda item: -item[1])}
for i in sorted_cntr:
    print(i)


options = {
    'node_color': 'red',
    'node_size': 20,
    'width': 0.1,
    'with_labels': False
}
nx.draw_spring(G, **options)
plt.show()