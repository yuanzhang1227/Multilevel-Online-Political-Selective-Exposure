# importing the required module
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# import datasets
df_2_merge = pd.read_csv('./Data/df_2_merge.csv', index_col=0)
df_3_merge = pd.read_csv('./Data/df_3_merge.csv', index_col=0)
df_8_merge = pd.read_csv('./Data/df_8_merge.csv', index_col=0)
df_14_merge = pd.read_csv('./Data/df_14_merge.csv', index_col=0)
df_46_merge = pd.read_csv('./Data/df_46_merge.csv', index_col=0)

L1 = 'L1'
L2 = 'L2'
L3 = 'L3'
L4 = 'L4'
L5 = 'L5'

def calculate_percentage(node_lists, df, label, community, L, threshold):
    try:
        community_size = len(df[df['Community'] == community])
        percentages = {category: len(node_list) / community_size * 100 for category, node_list in node_lists.items()}
        return percentages, "{}_{}".format(L, community), community_size
    except:
        return np.nan

def generate_node_lists(df, community, categories):
    node_lists = {}
    for category, conditions in categories.items():
        node_lists[category] = df[(df['Community'] == community) & df['Account type'].isin(conditions)]['Username'].tolist()
    return node_lists

def process_type(df, L, threshold, categories):
    results = []
    for i in range(1, df['Community'].nunique() + 1):
        node_lists = generate_node_lists(df, i, categories)
        result = calculate_percentage(node_lists, df, 'Account type', i, L, threshold)
        results.append(result)
    return results

# Define the categories for Type
categories = ['Individual', 'Media', 'Politician', 'Unlabeled']
category_colors = {'Individual': 'blue', 'Media': 'green', 'Politician': 'red', 'Unlabeled': 'grey'}

# Process communities for each level for Ideology
L_values = [L1, L2, L3, L4, L5]
dfs = [df_46_merge, df_14_merge, df_8_merge, df_3_merge, df_2_merge]
threshold = 60

# Process communities for each level for Type
type_46 = process_type(dfs[0], L_values[0], threshold, {'Individual': ['Individual'], 'Media': ['Media'], 'Politician': ['Politician'], 'Unlabeled': [np.nan]})
type_14 = process_type(dfs[1], L_values[1], threshold, {'Individual': ['Individual'], 'Media': ['Media'], 'Politician': ['Politician'], 'Unlabeled': [np.nan]})
type_8 = process_type(dfs[2], L_values[2], threshold, {'Individual': ['Individual'], 'Media': ['Media'], 'Politician': ['Politician'], 'Unlabeled': [np.nan]})
type_3 = process_type(dfs[3], L_values[3], threshold, {'Individual': ['Individual'], 'Media': ['Media'], 'Politician': ['Politician'], 'Unlabeled': [np.nan]})
type_2 = process_type(dfs[4], L_values[4], threshold, {'Individual': ['Individual'], 'Media': ['Media'], 'Politician': ['Politician'], 'Unlabeled': [np.nan]})

# Define the datasets for Type
type_datasets = [
    (type_46, 'Level 1', 24),
    (type_14, 'Level 2', 8),
    (type_8, 'Level 3', 4.57),
    (type_3, 'Level 4', 1.71),
    (type_2, 'Level 5', 1.14)
]

fig = plt.figure(figsize=(30, 60))
gs = gridspec.GridSpec(len(type_datasets), 1, height_ratios=[15, 5, 3, 1, 0.8])  # Allocate more space for lower levels

for i, (type_data, level_label, fig_height) in enumerate(type_datasets):
    ax = fig.add_subplot(gs[i])
    legend_handles = []
    bar_spacing = 6

    for j, (category_percentages, community, community_size) in enumerate(type_data):
        y_pos = j * (1 + bar_spacing)
        left = 0

        for category in categories:
            bar = ax.barh(y_pos, category_percentages[category], left=left, color=category_colors[category], height=6)
            if j == 0 and i == 0:
                legend_handles.append(bar)
            ax.text(-1, y_pos, f"{community} (N={community_size})", ha='right', va='center', color='black', fontsize=20)

            if category == 'Unlabeled' and category_percentages[category] > 0:
                ax.text(left + category_percentages[category] / 2, y_pos, f"{category_percentages[category]:.0f}%",
                        ha='center', va='center', color='white', fontsize=20, fontweight='bold')

            left += category_percentages[category]

    ax.text(-8, y_pos + 8, level_label, fontsize=30, fontweight='bold', ha='left', va='center')
    ax.set_xlim(0, 80)
    ax.set_xlabel('Percentage')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    if i == 0:
        ax.legend(handles=[handle[0] for handle in legend_handles], labels=categories, loc='upper right',
                  bbox_to_anchor=(1, 1.04), fontsize=20)

plt.subplots_adjust(left=0.2, right=0.8, top=0.95, bottom=0.05, hspace=0.1)
plt.savefig("./Plots/SI_Fig.3_Annotation_AT_C.png", dpi=500, bbox_inches='tight')
plt.show()