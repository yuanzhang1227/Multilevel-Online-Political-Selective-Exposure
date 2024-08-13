# importing the required module
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Read the dataset
influencer_links = pd.read_csv('./Data/Links_Shared_by_Influencers.csv')

def read_dataset(address, influencer_links):
    df = pd.read_csv(address, index_col=0)[['Username', 'Community']]
    return pd.merge(influencer_links, df, how='left', left_on='Name', right_on='Username').reset_index(drop=True)[
        ['Name', 'Community', 'Links_unshorten']]

community_nums = [46, 14, 8, 3, 2]

# Create the figure and axes
fig, axes = plt.subplots(len(community_nums), 2, figsize=(15, 5 * len(community_nums)), dpi=100)

for idx, num_communities in enumerate(community_nums):
    proportion = []
    num_of_links = []

    for community in np.arange(1, num_communities + 1):
        data = read_dataset(f'./Data/df_{num_communities}_merge.csv', influencer_links)
        df_merge = pd.read_csv(f'./Data/df_{num_communities}_merge.csv')
        name_list = np.array(data[data['Community'] == community]['Name'].unique())
        overall = len(df_merge[df_merge['Community'] == community]['Username'].unique())
        overall_links = len(data[data['Community'] == community])
        proportion.append(len(name_list) / overall if overall else 0)
        num_of_links.append(overall_links)

    sorted_pairs = sorted(zip(num_of_links, range(1, num_communities + 1)), reverse=True, key=lambda x: x[0])
    sorted_num_of_links, sorted_Community_list = zip(*sorted_pairs)

    sorted_pairs_proportion = sorted(zip(proportion, range(1, num_communities + 1)), reverse=True, key=lambda x: x[0])
    sorted_proportion, sorted_Community_list_prop = zip(*sorted_pairs_proportion)
    # Bar plot for the number of shared domains
    ax1 = axes[idx, 0]
    bars = ax1.bar(sorted_Community_list, sorted_num_of_links, align='center')
    ax1.set_xlabel('Communities', fontsize=12)
    ax1.set_ylabel('Total shared domains', fontsize=12)
    ax1.set_xticks(sorted_Community_list)

    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_visible(False)

    for bar, height in zip(bars, sorted_num_of_links):
        ax1.text(bar.get_x() + bar.get_width() / 2, height, f'{height}', ha='center', va='bottom', rotation=60,
                fontsize=10)

    # Line plot for the proportion of shares
    ax2 = axes[idx, 1]
    ax2.plot(sorted_Community_list_prop, sorted_proportion, color='red', marker='o', linestyle='-', linewidth=2,
             markersize=5)
    for i, txt in enumerate(sorted_proportion):
        ax2.annotate(f'{txt:.2f}', (sorted_Community_list_prop[i], sorted_proportion[i]), textcoords="offset points",
                     xytext=(0, 10), ha='center', fontsize=10)

    ax2.set_xlabel('Communities', fontsize=12)
    ax2.set_ylabel('Proportion of shares', fontsize=12)
    ax2.set_xticks(sorted_Community_list_prop)
    ax2.set_xticklabels(sorted_Community_list_prop, fontsize=10)

    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)

plt.subplots_adjust(hspace=1)  # Adjust vertical space between plots
plt.savefig('./Plots/SI_Fig.7_Share_of_domains.png', bbox_inches='tight', dpi=300)
plt.show()