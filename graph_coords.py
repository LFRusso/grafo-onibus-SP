# 
#   Plot do grafo com as coordenadas das cidades
#
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from unicodedata import normalize

# Remove os acentos de uma string
def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

# Converte uma string de coordenada geográfica em float
def convert_coords(coordstr):
    coordstr = coordstr.replace("°", "")
    coordstr = coordstr.replace("'", "")
    
    deg, minutes, seconds = [float(i) for i in coordstr.split(' ')]
    if(deg < 0):
        return (float(deg) - float(minutes)/60 - float(seconds)/(60*60))
    else :
        return (float(deg) + float(minutes)/60 + float(seconds)/(60*60))

# Lendo dados das coordenadas das cidades
data = np.loadtxt("./data/latlon.dat", delimiter='\t', dtype=str)
df = pd.DataFrame(data, columns = ['nomes','lat', 'lon'])
points = []
for entry in data:
    points.append([convert_coords(entry[1]), convert_coords(entry[2])])
points = np.array(points)
df.lat = points[:,0]
df.lon = points[:,1]
df.nomes = ["{}-sp-br".format(remover_acentos(nome).lower()) for nome in df.nomes]

# Lendo e formatando vértices
paths = []
with open("data/caminhos.dat", 'r') as file:
    paths = file.readlines()
paths = [path[:-1].split('/') for path in paths]
paths = [path[-1].split('-x-') for path in paths]    

# Aplicando uma máscara aos vértices com as cidades que temos as coordenadas
mask = [np.isin(path, list(df.nomes)).all() for path in paths]
paths = np.array(paths)
paths = paths[mask]


## Construindo e plotando grafo
G = nx.Graph()
for i in range(len(list(df.nomes))):
    G.add_node(list(df.nomes)[i], pos=(list(df.lon)[i], list(df.lat)[i]))
G.add_edges_from(paths)

pos=nx.get_node_attributes(G,'pos')
options = {
    'node_color': 'red',
    'node_size': 20,
    'width': 0.1,
    'with_labels': False
}
nx.draw(G, pos, **options)
plt.show()