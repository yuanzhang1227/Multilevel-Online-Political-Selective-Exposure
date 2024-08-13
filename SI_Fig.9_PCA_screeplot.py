# importing the required module
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# import dataset
survey_data = pd.read_csv("./Data/Regression_Survey_Data_2.csv")
columns_to_remove = ['Overlap', 'Label_diversity_with_nans', 'Label_diversity_without_nans',
                     'Domain_diversity', 'Normalized_cut', 'Gini']
survey_data = survey_data.drop(columns=columns_to_remove)
# Find columns with more than 95 missing values
cols_to_remove = survey_data.isnull().sum() > 95

# Find rows with at least 75 missing values
rows_to_remove = survey_data.isnull().sum(axis=1) >= 75
columns_removed = cols_to_remove[cols_to_remove].index.tolist()

survey_data = survey_data.loc[:, ~cols_to_remove]
survey_data = survey_data.loc[~rows_to_remove]

ordinal_variables = ['Age', 'Religious level', 'Education', 'Income',

                     'News_Television news', 'News_National newspapers', 'News_Regional newspapers', 'News_Radio news', 'News_Online news sources', 'News_News via social media',
                     'Social Media_Twitter', 'Social Media_Facebook', 'Social Media_YouTube', 'Social Media_Whatsapp', 'Social Media_Telegram',
                     'Campaign News_Television news ','Campaign News_National newspapers', 'Campaign News_Regional newspapers', 'Campaign News_Radio news', 'Campaign News_Online news sources', 'Campaign News_News via social media',
                     ' Read/Watch_Twitter', ' Read/Watch_Youtube', ' Read/Watch_Facebook', ' Read/Watch_Whatsapp', ' Read/Watch_Telegram', 'Share/Liked_Twitter', 'Share/Liked_Youtube', 'Share/Liked_Facebook', 'Share/Liked_Whatsapp', 'Share/Liked_Telegram',
                     'Comment/Post_Twitter', 'Comment/Post_Youtube', 'Comment/Post_Facebook', 'Comment/Post_Whatsapp', 'Comment/Post_Telegram',

                     'Fatigue_1', 'Fatigue_2', 'Fatigue_3', 'Conflict Orientation_1',
                     'Conflict Orientation_2', 'Conflict Orientation_3', 'Conflict Orientation_4', 'Conflict Orientation_5', 'Discussion_1', 'Discussion_2', 'Discussion_3', 'Discussion_4', 'Conflicting Opinion_1','Conflicting Opinion_2', 'Conflicting Opinion_3',
                     'Conflicting Opinion_4', 'Incivility Perception_Exclusion_Twitter', 'Incivility Perception_Exclusion_Youtube', 'Incivility Perception_Exclusion_Facebook', 'Incivility Perception_Exclusion_Whatsapp', 'Incivility Perception_Exclusion_Telegram',
                     'Incivility Perception_Impoliteness_Twitter', 'Incivility Perception_Impoliteness_Youtube', 'Incivility Perception_Impoliteness_Facebook', 'Incivility Perception_Impoliteness_Whatsapp', 'Incivility Perception_Impoliteness_Telegram',
                     'Incivility Perception_Physical harm/violence_Twitter', 'Incivility Perception_Physical harm/violence_Youtube', 'Incivility Perception_Physical harm/violence_Facebook', 'Incivility Perception_Physical harm/violence_Whatsapp',
                     'Incivility Perception_Physical harm/violence_Telegram', 'Incivility Perception_Negativity_Twitter', 'Incivility Perception_Negativity_Youtube', 'Incivility Perception_Negativity_Facebook', 'Incivility Perception_Negativity_Whatsapp',
                     'Incivility Perception_Negativity_Telegram', 'Incivility Perception_Personal  attack_Twitter', 'Incivility Perception_Personal  attack_Youtube', 'Incivility Perception_Personal  attack_Facebook', 'Incivility Perception_Personal  attack_Whatsapp',
                     'Incivility Perception_Personal  attack_Telegram', 'Incivility Perception_Stereotype/Hate speech/Discrimination_Twitter', 'Incivility Perception_Stereotype/Hate speech/Discrimination_Youtube',
                     'Incivility Perception_Stereotype/Hate speech/Discrimination_Facebook', 'Incivility Perception_Stereotype/Hate speech/Discrimination_Whatsapp', 'Incivility Perception_Stereotype/Hate speech/Discrimination_Telegram',
                     'Incivility Perception_Threat to democratic freedoms_Twitter', 'Incivility Perception_Threat to democratic freedoms_Youtube', 'Incivility Perception_Threat to democratic freedoms_Facebook',
                     'Incivility Perception_Threat to democratic freedoms_Whatsapp', 'Incivility Perception_Threat to democratic freedoms_Telegram',

                     'Online-offline Incivility_1', 'Online-offline Incivility_2',
                     'Online-offline Incivility_3', 'Online-offline Incivility_4', 'Online-offline Incivility_5', 'Online-offline Incivility_6', 'Experience_1', 'Experience_2', 'Experience_3', 'Experience_4', 'Self-censorship_1', 'Self-censorship_2', 'Self-censorship_3',
                     'Self-censorship_4', 'Self-censorship_5', 'Self-censorship_6', 'Self-censorship_7',

                     'Participation_Institutional/Electoral campaign_1', 'Participation_Institutional/Electoral campaign_2', 'Participation_Institutional/Electoral campaign_3',
                     'Participation_Institutional/Electoral campaign_4', 'Participation_Institutional/Electoral campaign_5', 'Participation_Institutional/Electoral campaign_6', 'Participation_Institutional/Electoral campaign_7','Participation_Protest_1',
                     'Participation_Protest_2', 'Participation_Protest_3', 'Participation_Protest_4', 'Participation_Civic engagement_1', 'Participation_Civic engagement_2', 'Participation_Online participation_1', 'Participation_Online participation_2',
                     'Participation_Online participation_3', 'Participation_Online participation_4', 'Participation_Online participation_5',

                     'Political Interest', 'Ideological Position', 'Alignment Measurement',

                     'Politician Likeability_1', 'Politician Likeability_2', 'Politician Likeability_3', 'Politician Likeability_4', 'Politician Likeability_5', 'Politician Likeability_6', 'Politician Likeability_7', 'Politician Likeability_8', 'Politician Likeability_9',
                     'Politician Likeability_10', 'Politician Likeability_11', 'Politician Likeability_12', 'Party Likeability_1', 'Party Likeability_2', 'Party Likeability_3', 'Party Likeability_4', 'Party Likeability_5', 'Party Likeability_6', 'Party Likeability_7',
                     'Party Likeability_8', 'Party Likeability_9', 'Party Likeability_10', 'Party Likeability_11', 'Party Likeability_12',

                     'Media Trust_1', 'Media Trust_2', 'Media Trust_3', 'Media Trust_4', 'Media Trust_5', 'Media Trust_6', 'Media Trust_7', 'Media Trust_8',

                     'False Information_Facebook', 'False Information_Twitter', 'False Information_Youtube', 'False Information_Whatsapp', 'False Information_Telegram', 'False Information_News Media',

                     'Populism_1', 'Populism_2', 'Populism_3', 'Populism_4', 'Populism_5', 'Populism_6', 'Populism_7', 'Support for Democracy', 'Satisfactory with Democracy',

                     'Politician/Party Accounts Following_Twitter', 'Politician/Party Accounts Following_Facebook']

nominal_variables = ['Gender', 'Ethnic', 'Religion', 'Living ',
                     'Party Alignment',
                     'Mess Apps Information_1', 'Mess Apps Information_2', 'Mess Apps Information_3', 'Mess Apps Information_97',
                     'Mess Apps Discussion_1', 'Mess Apps Discussion_2', 'Mess Apps Discussion_3', 'Mess Apps Discussion_97', 'Mess App Groups',
                     'Distance of Following Accounts']

for var in ordinal_variables:
    if var in survey_data.columns:
        survey_data[var] = pd.to_numeric(survey_data[var])

for var in nominal_variables:
    if var in survey_data.columns:
        survey_data[var] = survey_data[var].astype('category')

numeric_columns = survey_data.select_dtypes(include=['number']).columns.tolist()
columns_to_impute = [col for col in numeric_columns]

for col in columns_to_impute:
    if survey_data[col].isnull().any():
        survey_data[col].fillna(survey_data[col].mean(), inplace=True)

def impute_with_mode(df):
    for column in df.select_dtypes(include=['category']).columns:
        mode = df[column].mode().iloc[0]
        df[column].fillna(mode, inplace=True)
    return df

survey_data = impute_with_mode(survey_data)

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

sublists = []
sublists.append(demographics)
sublists.append(news_consumption)
sublists.append(political_communication)
sublists.append(political_identification)
sublists.append(political_engagement)
sublists.append(incivility)
sublists.append(disinformation)
sublists.append(authority_trust)
sublists.append(populism)
sublists.append(democracy)

group_names = [
    "Demographics",
    "News Consumption",
    "Political Communication",
    "Political Identification",
    "Political Engagement",
    "Incivility",
    "Disinformation",
    "Authority Trust",
    "Populism",
    "Democracy"
]


def apply_pca(data, columns, n_components=None):
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data[columns])
    pca = PCA(n_components=n_components)
    pca_results = pca.fit_transform(data_scaled)
    explained_variance = pca.explained_variance_ratio_
    return explained_variance

plt.style.use('seaborn-v0_8')
fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(25, 10))
axes = axes.flatten()

# Plotting variance explained for each group
for i, sublist in enumerate(sublists[1:-1]):
    # Filter sublist to remove any columns in columns_removed
    filtered_sublist = [item for item in sublist if item not in columns_removed]
    if filtered_sublist:  # Check if there's anything left to process
        explained_variance = apply_pca(survey_data, filtered_sublist)
        cumulative_variance = np.cumsum(explained_variance) * 100
        ax = axes[i]
        ax.bar(range(1, len(explained_variance) + 1), explained_variance * 100, color='blue', label='Individual')
        ax.plot(range(1, len(cumulative_variance) + 1), cumulative_variance, color='red', marker='o', label='Cumulative')
        ax.set_xlabel('Principal Components', fontsize =20)
        ax.set_ylabel('Variance Explained (%)', fontsize =20)
        ax.set_title(f'Variance Explained for {group_names[1:-1][i]}', fontsize=20)
        ax.set_xticks(range(1, len(explained_variance) + 1))
        ax.set_xticklabels([f'PC{i}' for i in range(1, len(explained_variance) + 1)], rotation=90)
        ax.legend()
    else:
        print(f"Sublist {i+1} has no columns left after removing removed columns.")

plt.tight_layout()
plt.savefig('./Plots/SI_Fig.9_PCA_screeplot.png', format='png', dpi=600, bbox_inches='tight')
plt.show()