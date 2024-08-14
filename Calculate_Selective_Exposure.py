# importing the required module
import pandas as pd
import numpy as np
import pickle

# import annotation datasets
df_2_merge = pd.read_csv('./Data/df_2_merge.csv', index_col = 0)
df_3_merge = pd.read_csv('./Data/df_3_merge.csv', index_col = 0)
df_8_merge = pd.read_csv('./Data/df_8_merge.csv', index_col = 0)
df_14_merge = pd.read_csv('./Data/df_14_merge.csv', index_col = 0)
df_46_merge = pd.read_csv('./Data/df_46_merge.csv', index_col = 0)
influencer_links = pd.read_csv('./Data/Links_Shared_by_Influencers.csv', index_col = 0)

file_path1 = './Data/graph.pkl'
file_path2 = './Data/results_n_scales1000.pkl'

with open(file_path1, 'rb') as file:
    G_largest = pickle.load(file)

with open(file_path2, 'rb') as file:
    results = pickle.load(file)

# Identity Diversity

def calculate_simpson_identity(num_of_community, df):
    simpson_with_actual_proportion_of_nans = {}
    simpson_without_nans = {}

    for i in range(1, num_of_community+1):

        filtered_df = df[df['Community']==i]
        ideology_list = filtered_df['Political ideology'].tolist()
        annot_pros = len(filtered_df[filtered_df['Political ideology'].notna()])/len(filtered_df)
        if annot_pros >= 0.25:
            try:
                simpson_ideo = 0
                for e in ['R', 'C', 'L']:
                    p_x1 = (ideology_list.count(e) + ideology_list.count(np.nan) * (ideology_list.count(e)/len(filtered_df[filtered_df['Political ideology'].notna()])))/len(ideology_list)
                    p_x2 = (ideology_list.count(e) + ideology_list.count(np.nan) * (ideology_list.count(e)/len(filtered_df[filtered_df['Political ideology'].notna()])) -1)/(len(ideology_list)-1)
                    simpson_ideo += p_x1 * p_x2
                    if simpson_ideo < 0:
                        simpson_ideo = 0

                simpson_with_actual_proportion_of_nan = 1-simpson_ideo
                simpson_with_actual_proportion_of_nans[i] = simpson_with_actual_proportion_of_nan
            except:
                simpson_with_actual_proportion_of_nans[i] = np.nan

            try:
                simpson_ideo = 0
                for e in ['R', 'C', 'L']:
                    p_x1 = (ideology_list.count(e)) / len(
                        filtered_df[filtered_df['Political ideology'].notna()])
                    p_x2 = (ideology_list.count(e) - 1) / (len(
                        filtered_df[filtered_df['Political ideology'].notna()]) - 1)
                    simpson_ideo += p_x1 * p_x2
                    if simpson_ideo < 0:
                        simpson_ideo = 0

                simpson_without_nan = 1 - simpson_ideo
                simpson_without_nans[i] = simpson_without_nan

            except:
                simpson_without_nans[i] = np.nan

    return simpson_with_actual_proportion_of_nans, simpson_without_nans

identity_diversity_46 = calculate_simpson_identity(40, df_46_merge)[0]
identity_diversity_14 = calculate_simpson_identity(14, df_14_merge)[0]
identity_diversity_8 = calculate_simpson_identity(8, df_8_merge)[0]
identity_diversity_3 = calculate_simpson_identity(3, df_3_merge)[0]
identity_diversity_2 = calculate_simpson_identity(2, df_2_merge)[0]

identity_diversity_add_46 = calculate_simpson_identity(40, df_46_merge)[1]
identity_diversity_add_14 = calculate_simpson_identity(14, df_14_merge)[1]
identity_diversity_add_8 = calculate_simpson_identity(8, df_8_merge)[1]
identity_diversity_add_3 = calculate_simpson_identity(3, df_3_merge)[1]
identity_diversity_add_2 = calculate_simpson_identity(2, df_2_merge)[1]

# Information Diversity

def read_dataset(address, influencer_links):
  df=pd.read_csv(address, index_col=0)[['Username', 'Community']]
  return pd.merge(influencer_links,df, how = 'left', left_on='Name', right_on = 'Username').reset_index(drop=True)[['Name', 'Community','Links_unshorten']]
def calculate_simpson_information(dataset, Number_of_communities, df):
  community_assignments = np.arange(1, Number_of_communities + 1)
  final_simpson_dict={}
  for community in community_assignments:
      name_list = np.array(dataset[dataset['Community'] == community]['Name'].unique())
      overall = len(df[df['Community']==community]['Username'].unique())
      filtered_dataset = dataset[dataset['Community'] == community]
      if len(name_list)!=1 and len(filtered_dataset)>100 and len(name_list)/overall > 0.5:
          links_list = filtered_dataset['Links_unshorten'].unique().tolist()
          sum_N = 0
          sum_n = 0
          for i in links_list:
              num_i = len(filtered_dataset[filtered_dataset['Links_unshorten']==i])
              deno_i = num_i * (num_i-1)
              sum_N += num_i
              sum_n += deno_i
          sum_N = sum_N * (sum_N-1)
          simpson_index = 1-(sum_n/sum_N)
          final_simpson_dict[community]=simpson_index
      else:
          final_simpson_dict[community]=np.nan
  return final_simpson_dict

information_diversity = [
    calculate_simpson_information(
        dataset=read_dataset(f'./Data/df_{i}_merge.csv', influencer_links),
        Number_of_communities=j,
        df=pd.read_csv(f'./Data/df_{i}_merge.csv', index_col=0)
    )
    for i in [2, 3, 8, 14, 46]
    for j in [2, 3, 8, 14, 40]
]

information_diversity_46 = information_diversity[4]
information_diversity_14 = information_diversity[3]
information_diversity_8 = information_diversity[2]
information_diversity_3 = information_diversity[1]
information_diversity_2 = information_diversity[0]

# Normalized Cut

def calculate_normalized_cut(G, df, Number_of_communities):
    normalized_cut = {}

    # Calculate the total weight of all edges in the graph
    num_weights = sum(data['weight'] for u, v, data in G.edges(data=True))

    for i in range(1,Number_of_communities + 1):
        out_edges = []
        within_edges = []

        # Get the list of nodes in the current community
        nodes_list = df[df['Community'] == i]['Username'].to_list()
        N_current_community = len(nodes_list)
        N_other_community = len(df[df['Community'] != i])

        for j in nodes_list:
            neighbors = list(G.neighbors(j))

            neighbors_inside = [n for n in neighbors if df.loc[df['Username'] == n, 'Community'].values[0] == i]
            neighbors_outside = [n for n in neighbors if df.loc[df['Username'] == n, 'Community'].values[0] != i]

            # Calculate the sum of weights with the nodes outside of the current subgraph
            out_weight = sum(G.get_edge_data(j, m)['weight'] for m in neighbors_outside if G.has_edge(j, m))
            out_edges.append(out_weight)

            # Calculate the sum of weights with the nodes inside the current subgraph
            within_weight = sum(G.get_edge_data(j, m)['weight'] for m in neighbors_inside if G.has_edge(j, m))
            within_edges.append(within_weight)

        # Calculate the normalized cut
        sum_out_edges = sum(out_edges)
        sum_within_edges = sum(within_edges)
        frac = sum_out_edges / (sum_within_edges + sum_out_edges) + sum_out_edges / (2 * (num_weights - sum_within_edges / 2) + sum_out_edges)
        normalized_cut[i] = frac

    return normalized_cut

structural_isolation_46 = calculate_normalized_cut(G_largest, df_46_merge, 40)
structural_isolation_14 = calculate_normalized_cut(G_largest, df_14_merge, 14)
structural_isolation_8 = calculate_normalized_cut(G_largest, df_8_merge, 8)
structural_isolation_3 = calculate_normalized_cut(G_largest, df_3_merge, 3)
structural_isolation_2 = calculate_normalized_cut(G_largest, df_2_merge, 2)

# Connectivity Inequality

def calculate_gini_index (G, name_comm_dic, Number_of_communities):
    gini_index = {}
    for i in range(1,Number_of_communities + 1):
        subgraph = G.subgraph(name_comm_dic[i-1])
        weight_sequence = [sum(data['weight'] for _, _, data in subgraph.edges(n, data=True)) for n in subgraph.nodes()]

        total = 0
        for i, xi in enumerate(np.array(weight_sequence)[:-1], 1):
            total += np.sum(np.abs(xi - np.array(weight_sequence)[i:]))
            gini =  total / (len(np.array(weight_sequence))**2 * np.mean(np.array(weight_sequence)))
            gini_index[i] = gini
    return gini_index

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

connectivity_inequality_46 = calculate_gini_index(G_largest, name_comm_dic_46, 40)
connectivity_inequality_14 = calculate_gini_index(G_largest, name_comm_dic_14, 14)
connectivity_inequality_8 = calculate_gini_index(G_largest, name_comm_dic_8, 8)
connectivity_inequality_3 = calculate_gini_index(G_largest, name_comm_dic_3, 3)
connectivity_inequality_2 = calculate_gini_index(G_largest, name_comm_dic_2, 2)


