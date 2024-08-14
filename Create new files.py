import pandas as pd
import pickle

# following_following = pd.read_csv('./Data/Following_Following.csv', index_col=0)
# following_following['User_ID'] = pd.factorize(following_following['Username'])[0] + 1
# following_following = following_following.drop(columns=['Username'])
# username_to_id = following_following.set_index('Username')['User_ID'].to_dict()
# with open('./Data/username_to_id.pkl', 'wb') as file:
#     pickle.dump(username_to_id, file)
# print(following_following)
# following_following.to_csv('./Data/Following_Following_anonymised.csv')
#
#
# replace = ['douglas955534', 'LucasBR732618', 'Alexandre saladrigas', 'Adriana Chinelatto', 'Eduardo_Tadeu _P', 'Elizabeth Alves de Souza', 'Gabrielshindi',
#            'HRG tutoriais', 'jhonathanbh', 'jhuaquino', 'Lealdo Almeida', 'Narrador Bicolor', 'Aldenira Monteiro', 'Rafael Hongaro', 'Rosana Roro', 'yedda campos']
# mismatch_dic = dict(zip(diff, replace))


with open('./Data/username_to_id.pkl', 'rb') as file:
    username_to_id = pickle.load(file)
with open('./Data/mismatch.pkl', 'rb') as file:
    mismatch = pickle.load(file)
with open('./Data/survey_to_id.pkl', 'rb') as file:
    survey_to_id = pickle.load(file)


# df_46_merge = pd.read_csv('./Data/df_46_merge.csv', index_col=0)
# df_46_merge['User_ID'] = df_46_merge['Username'].map(username_to_id)
# df_46_merge = df_46_merge.drop(columns=['Username', 'Description'])
# df_46_merge.to_csv('./Data/df_46_merge_anonymised.csv')

follow_merge_46 = pd.read_csv('./Data/follow_merge_46.csv', index_col=0)
follow_merge_46['Source'] = follow_merge_46['Source'].apply(lambda x: mismatch.get(x, x))
# survey_twitter_id = pd.read_csv('./Data/Survey_Twitter_Handles_ID.csv', index_col=0)
# survey_to_id = dict(zip(survey_twitter_id['K43B_BIS'], survey_twitter_id['CodPanelista']))
follow_merge_46['Source'] = follow_merge_46['Source'].map(survey_to_id)
follow_merge_46['Target'] = follow_merge_46['Target'].map(username_to_id)
follow_merge_46.to_csv('./Data/follow_merge_46_anonymised.csv')
# final_network_data = final_network_data.drop(columns=['Description'])
# final_network_data.to_csv('./Data/Final_Network_Data_anonymised.csv')
# list1 = list(final_network_data['Source'].unique())
# list2 = list(survey_twitter_id['K43B_BIS'].unique())
# diff = [i for i in list1 if i not in list2]


# final_network_data['Survey_ID'] = pd.factorize(following_following['Username'])[0] + 1
# survey_to_id = following_following.set_index('Username')['User_ID'].to_dict()