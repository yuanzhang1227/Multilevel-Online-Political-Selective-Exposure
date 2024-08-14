# importing the required module
import pandas as pd
import numpy as np

# import datasets
follow_merge_2 = pd.read_csv('./Data/follow_merge_2.csv')
follow_merge_3 = pd.read_csv('./Data/follow_merge_3.csv')
follow_merge_8 = pd.read_csv('./Data/follow_merge_8.csv')
follow_merge_14 = pd.read_csv('./Data/follow_merge_14.csv')
follow_merge_46 = pd.read_csv('./Data/follow_merge_46.csv')
survey_twitter_ID = pd.read_csv('./Data/Survey_Twitter_Handles_ID.csv', index_col = 0)
survey_data = pd.read_excel('./Data/Survey_Data.xlsx', index_col=0).reset_index()

from Calculate_Selective_Exposure import (
    identity_diversity_46, identity_diversity_14,
    identity_diversity_8, identity_diversity_3,
    identity_diversity_2, identity_diversity_add_46,
    identity_diversity_add_14, identity_diversity_add_8,
    identity_diversity_add_3, identity_diversity_add_2,
    information_diversity_46, information_diversity_14,
    information_diversity_8, information_diversity_3, information_diversity_2,
    structural_isolation_46, structural_isolation_14, structural_isolation_8,
    structural_isolation_3, structural_isolation_2, connectivity_inequality_46,
    connectivity_inequality_14, connectivity_inequality_8, connectivity_inequality_3,
    connectivity_inequality_2
)

# define function that assigns selective exposure measurements to each survey participant
def survey_index_calculate (survey_df, follow_df, identity1, identity2, information, isolation, connectivity):
    identity_diversity_with_nans = []
    identity_diversity_without_nans = []
    information_diversity = []
    structural_isolation = []
    connectivity_inequality = []
    community_overlap = []

    survey_list = survey_df['Name'].unique().tolist()

    for i in survey_list:
        comm = survey_df[survey_df['Name']==i]['Community'].tolist()
        identity_diversity_with_nans_tem = []
        identity_diversity_without_nans_tem = []
        information_diversity_tem = []
        structural_isolation_tem = []
        connectivity_inequality_tem = []
        community = len(list(survey_df[survey_df['Name']==i]['Community'].unique()))
        community_overlap.append(community)
        for c in comm:
            if c < 41:
                num_follow = len(follow_df[(follow_df['Source'] == i) & (follow_df['Community'] == c)]['Target'])
                identity_1 = identity1[c-1] * num_follow
                identity_2 = identity2[c-1] * num_follow
                info_diversity = information[c-1] * num_follow
                stru_isolation = isolation[c-1] * num_follow
                conn_inequality = connectivity[c-1] * num_follow

                identity_diversity_with_nans_tem.append(identity_1)
                identity_diversity_without_nans_tem.append(identity_2)
                information_diversity_tem.append(info_diversity)
                structural_isolation_tem.append(stru_isolation)
                connectivity_inequality_tem.append(conn_inequality)

        identity_diversity_with_nans_average = np.nansum(identity_diversity_with_nans_tem)/ len(follow_df[(follow_df['Source'] == i) & (follow_df['Community'].notna())]['Target'])
        identity_diversity_without_nans_average = np.nansum(identity_diversity_without_nans_tem)/ len(follow_df[(follow_df['Source'] == i) & (follow_df['Community'].notna())]['Target'])
        information_diversity_average = np.nansum(information_diversity_tem) / len(follow_df[(follow_df['Source'] == i) & (follow_df['Community'].notna())]['Target'])
        structural_isolation_average = np.nansum(structural_isolation_tem) / len(follow_df[(follow_df['Source'] == i) & (follow_df['Community'].notna())]['Target'])
        connectivity_inequality_average = np.nanmean(connectivity_inequality_tem) / len(follow_df[(follow_df['Source'] == i) & (follow_df['Community'].notna())]['Target'])

        identity_diversity_with_nans.append(identity_diversity_with_nans_average)
        identity_diversity_without_nans.append(identity_diversity_without_nans_average)
        information_diversity.append(information_diversity_average)
        structural_isolation.append(structural_isolation_average)
        connectivity_inequality.append(connectivity_inequality_average)

    return survey_list, identity_diversity_with_nans, identity_diversity_without_nans, information_diversity, structural_isolation, connectivity_inequality, community_overlap


# create survey variable lists
demographics = ['Age', 'Religion', 'Religious level', 'Gender', 'Ethnic', 'Education', 'Living ', 'Income']

news_consumption = ['News_Television news', 'News_National newspapers', 'News_Regional newspapers', 'News_Radio news', 'News_Online news sources', 'News_News via social media',

                    'Social Media_Twitter', 'Social Media_Facebook', 'Social Media_YouTube', 'Social Media_Whatsapp', 'Social Media_Telegram',

                    'Campaign News_Television news ','Campaign News_National newspapers', 'Campaign News_Regional newspapers', 'Campaign News_Radio news', 'Campaign News_Online news sources', 'Campaign News_News via social media',

                    ' Read/Watch_Twitter', ' Read/Watch_Youtube', ' Read/Watch_Facebook', ' Read/Watch_Whatsapp', ' Read/Watch_Telegram',

                    'Share/Liked_Twitter', 'Share/Liked_Youtube', 'Share/Liked_Facebook', 'Share/Liked_Whatsapp', 'Share/Liked_Telegram',

                    'Comment/Post_Twitter', 'Comment/Post_Youtube', 'Comment/Post_Facebook', 'Comment/Post_Whatsapp', 'Comment/Post_Telegram',

                    'Mess Apps Information_1', 'Mess Apps Information_2', 'Mess Apps Information_3', 'Mess Apps Information_97',

                    'Mess Apps Discussion_1', 'Mess Apps Discussion_2', 'Mess Apps Discussion_3', 'Mess Apps Discussion_97',

                    'Mess App Groups']

political_communication = ['Fatigue_1', 'Fatigue_2', 'Fatigue_3',

                           'Conflict Orientation_1', 'Conflict Orientation_2', 'Conflict Orientation_3', 'Conflict Orientation_4', 'Conflict Orientation_5',

                           'Discussion_1', 'Discussion_2', 'Discussion_3', 'Discussion_4',

                           'Conflicting Opinion_1','Conflicting Opinion_2', 'Conflicting Opinion_3', 'Conflicting Opinion_4']

political_identification = ['Ideological Position',

                            'Party Alignment',

                            'Alignment Measurement',

                            'Politician Likeability_1', 'Politician Likeability_2', 'Politician Likeability_3', 'Politician Likeability_4',
                            'Politician Likeability_5', 'Politician Likeability_6', 'Politician Likeability_7', 'Politician Likeability_8', 'Politician Likeability_9',
                            'Politician Likeability_10', 'Politician Likeability_11', 'Politician Likeability_12',

                            'Party Likeability_1', 'Party Likeability_2', 'Party Likeability_3', 'Party Likeability_4', 'Party Likeability_5', 'Party Likeability_6', 'Party Likeability_7',
                            'Party Likeability_8', 'Party Likeability_9', 'Party Likeability_10', 'Party Likeability_11', 'Party Likeability_12']

political_engagement = ['Participation_Institutional/Electoral campaign_1', 'Participation_Institutional/Electoral campaign_2', 'Participation_Institutional/Electoral campaign_3', 'Participation_Institutional/Electoral campaign_4', 'Participation_Institutional/Electoral campaign_5', 'Participation_Institutional/Electoral campaign_6', 'Participation_Institutional/Electoral campaign_7',

                        'Participation_Protest_1', 'Participation_Protest_2', 'Participation_Protest_3', 'Participation_Protest_4',

                        'Participation_Civic engagement_1', 'Participation_Civic engagement_2',

                        'Participation_Online participation_1', 'Participation_Online participation_2', 'Participation_Online participation_3', 'Participation_Online participation_4', 'Participation_Online participation_5',

                        'Political Interest', 'Politician/Party Accounts Following_Twitter', 'Politician/Party Accounts Following_Facebook', 'Distance of Following Accounts']

incivility = ['Incivility Perception_Exclusion_Twitter', 'Incivility Perception_Exclusion_Youtube', 'Incivility Perception_Exclusion_Facebook', 'Incivility Perception_Exclusion_Whatsapp', 'Incivility Perception_Exclusion_Telegram',

              'Incivility Perception_Impoliteness_Twitter', 'Incivility Perception_Impoliteness_Youtube', 'Incivility Perception_Impoliteness_Facebook', 'Incivility Perception_Impoliteness_Whatsapp', 'Incivility Perception_Impoliteness_Telegram',

              'Incivility Perception_Physical harm/violence_Twitter', 'Incivility Perception_Physical harm/violence_Youtube', 'Incivility Perception_Physical harm/violence_Facebook', 'Incivility Perception_Physical harm/violence_Whatsapp', 'Incivility Perception_Physical harm/violence_Telegram',

              'Incivility Perception_Negativity_Twitter', 'Incivility Perception_Negativity_Youtube', 'Incivility Perception_Negativity_Facebook', 'Incivility Perception_Negativity_Whatsapp', 'Incivility Perception_Negativity_Telegram',

              'Incivility Perception_Personal  attack_Twitter', 'Incivility Perception_Personal  attack_Youtube', 'Incivility Perception_Personal  attack_Facebook', 'Incivility Perception_Personal  attack_Whatsapp', 'Incivility Perception_Personal  attack_Telegram',

              'Incivility Perception_Stereotype/Hate speech/Discrimination_Twitter', 'Incivility Perception_Stereotype/Hate speech/Discrimination_Youtube', 'Incivility Perception_Stereotype/Hate speech/Discrimination_Facebook', 'Incivility Perception_Stereotype/Hate speech/Discrimination_Whatsapp', 'Incivility Perception_Stereotype/Hate speech/Discrimination_Telegram',

              'Incivility Perception_Threat to democratic freedoms_Twitter', 'Incivility Perception_Threat to democratic freedoms_Youtube', 'Incivility Perception_Threat to democratic freedoms_Facebook', 'Incivility Perception_Threat to democratic freedoms_Whatsapp', 'Incivility Perception_Threat to democratic freedoms_Telegram',

              'Online-offline Incivility_1', 'Online-offline Incivility_2', 'Online-offline Incivility_3', 'Online-offline Incivility_4', 'Online-offline Incivility_5', 'Online-offline Incivility_6',

              'Experience_1', 'Experience_2', 'Experience_3', 'Experience_4',

              'Self-censorship_1', 'Self-censorship_2', 'Self-censorship_3', 'Self-censorship_4', 'Self-censorship_5', 'Self-censorship_6', 'Self-censorship_7']

disinformation = ['False Information_Facebook', 'False Information_Twitter', 'False Information_Youtube', 'False Information_Whatsapp', 'False Information_Telegram', 'False Information_News Media']

authority_trust = ['Media Trust_1', 'Media Trust_2', 'Media Trust_3', 'Media Trust_4', 'Media Trust_5', 'Media Trust_6', 'Media Trust_7', 'Media Trust_8']

populism = ['Populism_1', 'Populism_2', 'Populism_3', 'Populism_4', 'Populism_5', 'Populism_6', 'Populism_7']

democracy = ['Support for Democracy', 'Satisfactory with Democracy']

variable_list = demographics + news_consumption + political_communication + political_identification + political_engagement + incivility + disinformation + authority_trust + populism + democracy

lists_dict = {variable: [] for variable in variable_list}

# define function that creates regression data file
def create_regression_df (follow_merge, Num_of_communities, survey_twitter_ID, survey_data, identity1, identity2, information, isolation, connectivity):
    community_detection_results = follow_merge[["Source", "Target", "Community"]]
    survey_list = []
    community_list = []
    for i in range(1, Num_of_communities+1):
        survey_i = list(community_detection_results[community_detection_results["Community"] == i]['Source'].unique())
        community_i = [i] * len(survey_i)
        survey_list.extend(survey_i)
        community_list.extend(community_i)

    survey_partition = pd.DataFrame({'Name': survey_list, 'Community': community_list})
    survey_partition_merge1 = pd.merge(survey_partition, survey_twitter_ID, left_on='Name', right_on='K43B_BIS',
                                         how='left')
    survey_partition_merge2 = pd.merge(survey_partition_merge1, survey_data, left_on='CodPanelista',
                                         right_on='panelist_id', how='left')

    survey_list = survey_index_calculate(survey_partition_merge2, follow_merge, identity1, identity2, information, isolation, connectivity)[0]

    identity_diversity_with_nans = survey_index_calculate(survey_partition_merge2, follow_merge, identity1, identity2, information, isolation, connectivity)[1]

    identity_diversity_without_nans = survey_index_calculate(survey_partition_merge2, follow_merge, identity1, identity2, information, isolation, connectivity)[2]

    information_diversity = survey_index_calculate(survey_partition_merge2, follow_merge, identity1, identity2, information, isolation, connectivity)[3]

    structural_isolation = survey_index_calculate(survey_partition_merge2, follow_merge, identity1, identity2, information, isolation, connectivity)[4]

    connectivity_inequality = survey_index_calculate(survey_partition_merge2, follow_merge, identity1, identity2, information, isolation, connectivity)[5]

    community_overlap = survey_index_calculate(survey_partition_merge2, follow_merge, identity1, identity2, information, isolation, connectivity)[6]

    for i in survey_list:
        for j in variable_list:
            lists_dict[j].append(list(survey_partition_merge2[survey_partition_merge2['Name'] == i][j].unique())[0])
    lists_dict['identity_diversity_with_nans'] = identity_diversity_with_nans
    lists_dict['identity_diversity_without_nans'] = identity_diversity_without_nans
    lists_dict['information_diversity'] = information_diversity
    lists_dict['structural_isolation'] = structural_isolation
    lists_dict['connectivity_inequality'] = connectivity_inequality
    lists_dict['community_overlap'] = community_overlap

    df = pd.DataFrame(lists_dict)

    return df.to_csv("./Data/Regression_Survey_Data_{}.csv".format(Num_of_communities))


def main():
    for i in [2, 3, 8, 14, 46]:
        follow_merge_file = f"follow_merge_{i}"
        identity1 = f"identity_diversity_{i}"
        identity2 = f"identity_diversity_add_{i}"
        information = f"information_diversity_{i}"
        isolation = f"structural_isolation_{i}"
        connectivity = f"connectivity_inequality_{i}"
        create_regression_df(follow_merge_file, i, survey_twitter_ID, survey_data, identity1, identity2, information, isolation, connectivity)
main()
