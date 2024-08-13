# importing the required module

import matplotlib.pyplot as plt
import networkx as nx
import random
from matplotlib.patches import Wedge
import math
import matplotlib.colors as mcolors
import pandas as pd

from Calculate_Selective_Exposure import (
    identity_diversity_46, identity_diversity_14,
    identity_diversity_8, identity_diversity_3,
    identity_diversity_2, information_diversity_46, information_diversity_14,
    information_diversity_8, information_diversity_3, information_diversity_2,
    structural_isolation_46, structural_isolation_14, structural_isolation_8,
    structural_isolation_3, structural_isolation_2, connectivity_inequality_46,
    connectivity_inequality_14, connectivity_inequality_8, connectivity_inequality_3,
    connectivity_inequality_2
)

df_2_merge = pd.read_csv('./Data/df_2_merge.csv', index_col = 0)
df_3_merge = pd.read_csv('./Data/df_3_merge.csv', index_col = 0)
df_8_merge = pd.read_csv('./Data/df_8_merge.csv', index_col = 0)
df_14_merge = pd.read_csv('./Data/df_14_merge.csv', index_col = 0)
df_46_merge = pd.read_csv('./Data/df_46_merge.csv', index_col = 0)

follow_merge_2 = pd.read_csv('./Data/follow_merge_2.csv')
follow_merge_3 = pd.read_csv('./Data/follow_merge_3.csv')
follow_merge_8 = pd.read_csv('./Data/follow_merge_8.csv')
follow_merge_14 = pd.read_csv('./Data/follow_merge_14.csv')
follow_merge_46 = pd.read_csv('./Data/follow_merge_46.csv')

# Define the custom colormap with enhanced range of blue shades
colors = [
    (0, 0, 0.1),  # Very dark blue
    (0, 0, 0.3),  # Dark blue
    (0, 0, 0.5),  # Medium dark blue
    (0, 0, 0.7),  # Medium blue
    (0, 0.2, 0.9),  # Lighter blue
    (0.2, 0.4, 1),  # Light blue
    (0.5, 0.7, 1),  # Very light blue
    (0.8, 0.9, 1)  # Almost white blue
]
n_bins = 100  # Discretize the colormap into 100 steps
cmap_name = 'custom_blue'
custom_cmap = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)

def plot_network(values, title, ax, num_nodes, df_merge, follow_merge, show_title):
    # Create the graph
    G = nx.Graph()
    G.add_nodes_from(range(1, num_nodes + 1))
    for i in range(1, num_nodes + 1):
        for j in range(i + 1, num_nodes + 1):
            list_i = list(follow_merge[follow_merge['Community'] == i]['Source'])
            list_j = list(follow_merge[follow_merge['Community'] == j]['Source'])
            overlap = len(set(list_i) & set(list_j))
            if overlap > 0:
                G.add_edge(i, j, weight=overlap)

    # Calculate the size of each community
    size_dic = {i: df_merge[df_merge['Community'] == i].shape[0] for i in range(1, num_nodes + 1)}

    random.seed(42)
    pos = nx.spring_layout(G, k=6, iterations=50, seed=10)  # Adjusted k value to spread nodes more
    weights = [G[u][v]['weight'] / 15 for u, v in G.edges()]  # Adjusted weights for clearer edges
    nx.draw_networkx_edges(G, pos, width=weights, edge_color='grey', ax=ax)

    # Draw the nodes with color based on the provided values
    for node in G.nodes:
        radius = size_dic[node] / 10000
        color_value = values[node - 1] if node - 1 < len(values) else 0
        node_color = custom_cmap(color_value)

        # Draw the node as a single colored circle
        node_circle = plt.Circle(pos[node], radius=math.sqrt(radius), color=node_color, ec='black', lw=1)
        ax.add_patch(node_circle)

    if show_title:
        ax.set_title(title, fontsize=25)

    ax.set_aspect('equal')
    ax.axis('off')
    ax.margins(0.05)
    plt.subplots_adjust(left=0.1, right=0.2, top=0.2, bottom=0.1)

def main():
    datasets = {
        'Identity Diversity': [identity_diversity_46, identity_diversity_14, identity_diversity_8, identity_diversity_3, identity_diversity_2],
        'Information Diversity': [information_diversity_46, information_diversity_14, information_diversity_8, information_diversity_3, information_diversity_2],
        'Structural Isolation': [structural_isolation_46, structural_isolation_14, structural_isolation_8, structural_isolation_3, structural_isolation_2],
        'Connectivity Inequality': [connectivity_inequality_46, connectivity_inequality_14, connectivity_inequality_8, connectivity_inequality_3, connectivity_inequality_2],
    }

    levels = [40, 14, 8, 3, 2]
    level_titles = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5"]
    dataframes = [df_46_merge, df_14_merge, df_8_merge, df_3_merge, df_2_merge]
    follow_dataframes = [follow_merge_46, follow_merge_14, follow_merge_8, follow_merge_3, follow_merge_2]

    fig, axes = plt.subplots(len(datasets), len(levels), figsize=(30, 19))

    for i, (name, data_list) in enumerate(datasets.items()):
        for j, (num_nodes, level_title, df_merge, follow_merge, data) in enumerate(zip(levels, level_titles, dataframes, follow_dataframes, data_list)):
            show_title = i == 0  # Only show title on the first row
            plot_network(data, level_title, axes[i, j], num_nodes, df_merge, follow_merge, show_title)
            if show_title:
                axes[0, j].set_title(level_title, fontsize=35, fontweight='bold')
            if j == len(levels) - 1:
                # Create colorbar only at the end of each row
                norm = plt.Normalize(0, 1)
                sm = plt.cm.ScalarMappable(cmap=custom_cmap, norm=norm)
                sm.set_array([])
                cbar = plt.colorbar(sm, ax=axes[i, j], orientation='vertical')
                cbar.set_label(name, fontsize=26)  # Increase fontsize of the colorbar labels
                cbar.ax.tick_params(labelsize=30)  # Increase fontsize of the colorbar scales
        axes[i, 0].set_ylabel(name, fontsize=35)  # Increase fontsize of the y-axis labels

    plt.tight_layout(rect=[0, 0, 1, 0.95], h_pad=3, w_pad=1)  # Adjust the rect parameter for the whole figure layout

    plt.savefig('./Plots/Fig.5_local_measurements.png', format='png', bbox_inches='tight', dpi=500)
    plt.show()

main()