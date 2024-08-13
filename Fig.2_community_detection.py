# importing the required module
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

file_path1 = './Data/graph.pkl'
file_path2 = './Data/results_n_scales1000.pkl'

with open(file_path1, 'rb') as file:
    G_largest = pickle.load(file)

with open(file_path2, 'rb') as file:
    results = pickle.load(file)

## create lists that include node names and community labels -- the 177th cluster option
# node_name_list = list(G_largest.nodes())
# community_label_list = list(results['community_id'][177])
# name_comm_dic_1767 = {key: [] for key in range(1767)}
# for comm, names in zip(community_label_list, node_name_list):
#     name_comm_dic_1767[comm].append(names)

## create lists that include node names and community labels -- the 305th cluster option
# node_name_list = list(G_largest.nodes())
# community_label_list = list(results['community_id'][305])
# name_comm_dic_1170 = {key: [] for key in range(1170)}
# for comm, names in zip(community_label_list, node_name_list):
#     name_comm_dic_1170[comm].append(names)

## create lists that include node names and community labels -- the 433th cluster option
node_name_list = list(G_largest.nodes())
community_label_list = list(results['community_id'][433])
name_comm_dic_46 = {key: [] for key in range(46)}
for comm, names in zip(community_label_list, node_name_list):
    name_comm_dic_46[comm].append(names)

## create lists that include node names and community labels -- the 529th cluster option
node_name_list = list(G_largest.nodes())
community_label_list = list(results['community_id'][529])
name_comm_dic_14 = {key: [] for key in range(14)}
for comm, names in zip(community_label_list, node_name_list):
    name_comm_dic_14[comm].append(names)

## create lists that include node names and community labels -- the 645th cluster option
node_name_list = list(G_largest.nodes())
community_label_list = list(results['community_id'][645])
name_comm_dic_8 = {key: [] for key in range(8)}
for comm, names in zip(community_label_list, node_name_list):
    name_comm_dic_8[comm].append(names)

## create lists that include node names and community labels -- the 713th cluster option
node_name_list = list(G_largest.nodes())
community_label_list = list(results['community_id'][713])
name_comm_dic_3 = {key: [] for key in range(3)}
for comm, names in zip(community_label_list, node_name_list):
    name_comm_dic_3[comm].append(names)

## create lists that include node names and community labels -- the 856th cluster option
node_name_list = list(G_largest.nodes())
community_label_list = list(results['community_id'][856])
name_comm_dic_2 = {key: [] for key in range(2)}
for comm, names in zip(community_label_list, node_name_list):
    name_comm_dic_2[comm].append(names)

# create plot for distribution of number of communities at five levels
dic_list = [
    (name_comm_dic_46, "Level 1"),
    (name_comm_dic_14, "Level 2"),
    (name_comm_dic_8, "Level 3"),
    (name_comm_dic_3, "Level 4"),
    (name_comm_dic_2, "Level 5")
]

sns.set_theme(style="whitegrid")

# Create a 5x1 plot
fig, axes = plt.subplots(5, 1, figsize=(10, 25))

for i, (dic, title) in enumerate(dic_list):
    keys = list(dic.keys())
    values_lengths = [len(value) for value in dic.values()]

    sns.barplot(ax=axes[i], x=keys, y=values_lengths, color="b")

    ticks_to_show = list(range(0, len(keys), 2))
    labels_to_show = [str(x + 1) for x in ticks_to_show]

    axes[i].set_xticks(ticks_to_show)
    axes[i].set_xticklabels(labels_to_show, fontsize=20)
    axes[i].set_yticks(axes[i].get_yticks())
    axes[i].set_yticklabels(axes[i].get_yticks(), fontsize=20)

    axes[i].set_xlabel('Community Index', fontsize=30)
    axes[i].set_ylabel('Size', fontsize=30)
    axes[i].legend([plt.Line2D([0], [0], linestyle="")], [title], fontsize=22, handlelength=0, handletextpad=0)

plt.tight_layout()
plt.savefig("./Plots/Fig.2_community_detection_c.png", bbox_inches="tight", dpi=500)
plt.show()

## Please note that "Fig.2_community_detection_a" and "Fig.2_community_detection_b" are toy examples created by PowerPoint