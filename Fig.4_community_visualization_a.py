# importing the required module
import pandas as pd
import matplotlib.pyplot as plt
import hypernetx as hnx

# import datasets
follow_merge_2 = pd.read_csv('./Data/follow_merge_2.csv')
follow_merge_3 = pd.read_csv('./Data/follow_merge_3.csv')
follow_merge_8 = pd.read_csv('./Data/follow_merge_8.csv')
follow_merge_14 = pd.read_csv('./Data/follow_merge_14.csv')
follow_merge_46 = pd.read_csv('./Data/follow_merge_46.csv')

# create hypergraph data
hyper_survey_2 = {}
for i in range(1,3):
    hyper_survey_2[i] = list(follow_merge_2[follow_merge_2['Community']==i]['Source'].unique())

hyper_survey_3 = {}
for i in range(1,4):
    hyper_survey_3[i] = list(follow_merge_3[follow_merge_3['Community']==i]['Source'].unique())

hyper_survey_8 = {}
for i in range(1,9):
    hyper_survey_8[i] = list(follow_merge_8[follow_merge_8['Community']==i]['Source'].unique())

hyper_survey_14 = {}
for i in range(1,15):
    hyper_survey_14[i] = list(follow_merge_14[follow_merge_14['Community']==i]['Source'].unique())

hyper_survey_46 = {}
for i in range(1,47):
    hyper_survey_46[i] = list(follow_merge_46[follow_merge_46['Community']==i]['Source'].unique())

datasets = {
    "Level 1": hyper_survey_46,
    "Level 2": hyper_survey_14,
    "Level 3": hyper_survey_8,
    "Level 4": hyper_survey_3,
    "Level 5": hyper_survey_2
}
annotations = ["N_Community = 46", "N_Community = 14", "N_Community = 8", "N_Community = 3", "N_Community = 2"]

fig, axes = plt.subplots(1, 5, figsize=(30, 10))

for ax, (name, data), annotation in zip(axes, datasets.items(), annotations):
    H = hnx.Hypergraph(data)
    node_community_count = {}
    for community, nodes in H.incidence_dict.items():
        for node in nodes:
            if node not in node_community_count:
                node_community_count[node] = 0
            node_community_count[node] += 1

    node_colors = []
    for node in H.nodes:
        if node in node_community_count and node_community_count[node] == 1:
            node_colors.append('green')
        else:
            node_colors.append('purple')



    hnx.drawing.rubber_band.draw(
        H,
        ax=ax,
        with_node_counts=True,
        node_labels_kwargs={'fontsize':60},
        with_edge_labels=False,
        nodes_kwargs={'facecolors': node_colors}
    )

    ax.set_title(name, fontsize=40, fontweight='bold')
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(10)

    ax.text(0.5, -0.1, annotation, transform=ax.transAxes, fontsize=35, va='top', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig("./Plots/Fig.4_community_visualization_a.png", bbox_inches="tight", dpi=500)
plt.show()
