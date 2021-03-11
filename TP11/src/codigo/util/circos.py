import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from nxviz.plots import CircosPlot
import matplotlib.colors as color
import matplotlib.patches as mpatches
from matplotlib.colors import to_hex
from random import choice

def return_pack_k (class_name, packages):
    for k in packages:
        if (packages[k].__contains__(class_name)):
            return k

def initialize_circos_plot (obj):

    dict_rules = obj
    packages = dict_rules["packages"]
    ligacoes_de_classe = dict_rules["LigacoesDeClasses"]

    nodelist = []
    label_pack = []
    for k in packages:
        label_pack.append(k)
        for class_name in packages[k]:
            nodelist.append((class_name, {}))

    edgelist = []
    for k in ligacoes_de_classe:
        for class_name in ligacoes_de_classe[k]:
            edgelist.append((k, class_name, {}))

    graph_custom = nx.Graph()
    graph_custom.add_nodes_from(nodelist)
    graph_custom.add_edges_from(edgelist)

    color_pack = {}
    for k in packages:
        color_pack[k] = choice(["one", "two", "three", "four"])

    for n, d in graph_custom.nodes(data=True):
        key = return_pack_k(n, packages)
        d["class"] = color_pack[key]
        d["group"] = key

    for n in graph_custom.nodes(data=True):
        print("Node: ", n)

    for e in graph_custom.edges(data=True):
        u = e[0]
        v = e[1]
        if (graph_custom.node[u]["group"] == graph_custom.node[v]["group"] ):
            e[2]["weights"] = 5
        else:
            e[2]["weights"] = 2
        print("edge: ", e)


    c = CircosPlot(graph_custom,
        node_grouping="group",
        node_color="class",
        node_order="class",
        nodeprops={"radius": 20},
        node_labels=True,
        node_label_layout="rotation",

        group_label_position="middle",
        group_label_color=True,
        group_legend=True,
        group_label_offset=20, #Label de grupo distante do grafo

        rotate_labels=True,
        figsize = (25,25),
        dpi=600,
        edge_width="weights",
    )

    data = c

    seen = set()
    colors_group = [x for x in data.node_colors if not (x in seen or seen.add(x))]
    labels_group = sorted(list(set([data.graph.node[n][data.node_grouping] for n in data.nodes])))
    print("labels_group: ", labels_group)

    patchList = []
    for color, label in zip(colors_group, labels_group):
        color = to_hex(color, keep_alpha=True)
        data_key = mpatches.Patch(color=color, label=label)
        patchList.append(data_key)

    plt.legend(handles=patchList,
               loc="center left",
               title="Enterprise size",
               ncol=4,
               borderpad=1,
               bbox_to_anchor =(0.5, -0.05),
               shadow=True,
               fancybox=True)

    data.draw()
    plt.savefig('dummy1.png')
    plt.show()
