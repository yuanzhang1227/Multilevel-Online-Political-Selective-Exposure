# importing the required module
import matplotlib.pyplot as plt
import networkx as nx
import random
from matplotlib.patches import Wedge
import pandas as pd
import math
plt.switch_backend('Qt5Agg')

# import datasets
df_2_merge = pd.read_csv('./Data/df_2_merge.csv')
df_3_merge = pd.read_csv('./Data/df_3_merge.csv')
df_8_merge = pd.read_csv('./Data/df_8_merge.csv')
df_14_merge = pd.read_csv('./Data/df_14_merge.csv')
df_46_merge = pd.read_csv('./Data/df_46_merge.csv')

follow_merge_2 = pd.read_csv('./Data/follow_merge_2.csv')
follow_merge_3 = pd.read_csv('./Data/follow_merge_3.csv')
follow_merge_8 = pd.read_csv('./Data/follow_merge_8.csv')
follow_merge_14 = pd.read_csv('./Data/follow_merge_14.csv')
follow_merge_46 = pd.read_csv('./Data/follow_merge_46.csv')

def plot_network(title, ax, num_nodes, df_merge, follow_merge, show_title, wedge_colors, trunk):
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

    proportion_dic = {}
    for i in range(1, num_nodes + 1):
        pro_list = []

        if trunk == 'Political ideology':
            p_L = df_merge[(df_merge['Community'] == i) & (df_merge['Political ideology'] == 'L')].shape[0]
            p_R = df_merge[(df_merge['Community'] == i) & (df_merge['Political ideology'] == 'R')].shape[0]
            p_C = df_merge[(df_merge['Community'] == i) & (df_merge['Political ideology'] == 'C')].shape[0]
            p_U = df_merge[(df_merge['Community'] == i) & pd.isna(df_merge['Political ideology'])].shape[0]
            pro_list.extend([p_L, p_R, p_C, p_U])

        elif trunk == 'Personal support':
            p_Lu = df_merge[(df_merge['Community'] == i) & (df_merge['Personal support'] == 'Lula camp')].shape[0]
            p_Bo = df_merge[(df_merge['Community'] == i) & (df_merge['Personal support'] == 'Bolsonaro camp')].shape[0]
            p_U = df_merge[(df_merge['Community'] == i) & pd.isna(df_merge['Personal support'])].shape[0]
            pro_list.extend([p_Lu, p_Bo, p_U])

        elif trunk == 'Social identity':
            p_Re = df_merge[(df_merge['Community'] == i) & (df_merge['Social identity'] == 'Religious')].shape[0]
            p_Wo = df_merge[(df_merge['Community'] == i) & (df_merge['Social identity'] == 'Woman')].shape[0]
            p_Bl = df_merge[(df_merge['Community'] == i) & (df_merge['Social identity'] == 'Black')].shape[0]
            p_Lg = df_merge[(df_merge['Community'] == i) & (df_merge['Social identity'] == 'LGBTQ')].shape[0]
            p_Wo_Re = df_merge[(df_merge['Community'] == i) & (df_merge['Social identity'] == 'Religious and Woman')].shape[0]
            p_Wo_Bl = df_merge[(df_merge['Community'] == i) & (df_merge['Social identity'] == 'Black and Woman')].shape[0]
            p_Wo_Lg = df_merge[(df_merge['Community'] == i) & (df_merge['Social identity'] == 'Woman and LGBTQ')].shape[0]
            p_U = df_merge[(df_merge['Community'] == i) & pd.isna(df_merge['Social identity'])].shape[0]
            pro_list.extend([p_Re, p_Wo, p_Bl, p_Lg, p_Wo_Re, p_Wo_Bl, p_Wo_Lg, p_U])

        elif trunk == 'Account type':
            p_In = df_merge[(df_merge['Community'] == i) & (df_merge['Account type'] == 'Individual')].shape[0]
            p_Me = df_merge[(df_merge['Community'] == i) & (df_merge['Account type'] == 'Media')].shape[0]
            p_Po = df_merge[(df_merge['Community'] == i) & (df_merge['Account type'] == 'Politician')].shape[0]
            p_U = df_merge[(df_merge['Community'] == i) & pd.isna(df_merge['Account type'])].shape[0]
            pro_list.extend([p_In, p_Me, p_Po, p_U])

        proportion_dic[i] = pro_list

    size_dic = {}
    for i in range(1, num_nodes + 1):
        size = df_merge[(df_merge['Community'] == i)].shape[0]
        size_dic[i] = size

    random.seed(42)
    pos = nx.spring_layout(G, k=6, iterations=50, seed=10)
    weights = [G[u][v]['weight'] / 12 for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, width=weights, edge_color='grey', ax=ax)

    for node, slices in proportion_dic.items():
        total_slices = sum(slices)
        wedge_sizes = [x / total_slices * 360 for x in slices]
        wedge_start = 0

        radius = size_dic[node] / 10000
        for i, size in enumerate(wedge_sizes):
            wedge = Wedge(center=pos[node], r=math.sqrt(radius), theta1=wedge_start, theta2=wedge_start + size, color=wedge_colors[i])
            ax.add_patch(wedge)
            wedge_start += size

        black_circle = plt.Circle(pos[node], radius=math.sqrt(radius), edgecolor='black', facecolor='none', linewidth=1)
        ax.add_patch(black_circle)

    if show_title:
        ax.set_title(title, fontsize=25)

    ax.set_aspect('equal')
    ax.axis('off')
    ax.margins(0.05)
    plt.subplots_adjust(left=0.1, right=0.2, top=0.2, bottom=0.1)  # Add margins to the plot

def main():
    levels = [41, 14, 8, 3, 2]
    level_titles = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5"]
    dataframes = [df_46_merge, df_14_merge, df_8_merge, df_3_merge, df_2_merge]
    follow_dataframes = [follow_merge_46, follow_merge_14, follow_merge_8, follow_merge_3, follow_merge_2]

    wedge_colors_list = [
        ['red', 'blue', 'orange', 'grey'],  # Ideology
        ['green', 'yellow', 'grey'],  # Personal Support
        ['pink', 'green', 'lightblue', 'purple', '#E2725B', '#40E0D0', '#6B8E23', 'grey'],  # Identity
        ['cyan', 'magenta', 'yellow', 'grey']  # Type
    ]

    trunks = ['Ideology', 'Personal Support', 'Identity', 'Type']
    labels_list = [
        ['Left', 'Right', 'Center', 'Unknown'],  # Ideology
        ['Lula camp', 'Bolsonaro camp', 'Unknown'],  # Personal Support
        ['Religious', 'Woman', 'Black', 'LGBTQ', 'Religious and Woman', 'Black and Woman', 'Woman and LGBTQ', 'Unknown'],  # Identity
        ['Individual', 'Media', 'Politician', 'Unknown']  # Type
    ]

    fig, axes = plt.subplots(len(trunks), len(levels), figsize=(30, 18))

    for i, (wedge_colors, trunk, labels) in enumerate(zip(wedge_colors_list, trunks, labels_list)):
        for j, (num_nodes, level_title, df_merge, follow_merge) in enumerate(zip(levels, level_titles, dataframes, follow_dataframes)):
            show_title = i == None
            plot_network(level_title, axes[i, j], num_nodes, df_merge, follow_merge, show_title, wedge_colors, trunk)
        axes[i, 0].set_ylabel(trunk, fontsize=35)

    plt.tight_layout(rect=[0, 0, 0.9, 1], h_pad=3, w_pad=1)
    plt.savefig('./Plots/Fig.4_community_visualization_b.png', format='png', bbox_inches='tight', dpi=500)
    plt.show()

main()
