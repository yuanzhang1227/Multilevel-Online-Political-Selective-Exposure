# importing the required module
import pandas as pd

# import followed data set
follow_network = pd.read_csv('./Survey_Influencer_Network.csv', index_col = 0, engine='python')

# Implement three filtering steps for identifying political influencer accounts
# Filter 1: remove accounts that are not located in Brazil
follow_network1 = follow_network[follow_network['Followers_count']>1000]

# Filter 2: remove accounts that are not located in Brazil

## create the location list
Locations= ['Brasil', 'Brazil', 'Brasilien', 'Acre', 'Alagoas', 'Amapa', 'Amazonas',
            'Bahia', 'Ceara', 'Distrito Federal', 'Espirito Santo', 'Goias', 'Maranhao', 'Mato Grosso',
            'Mato Grosso do Sul', 'Minas Gerais', 'Para', 'Paraiba', 'Parana', 'Pernambuco', 'Piaui',
            'Rio de Janeiro', 'Rio Grande do Norte', 'Rio Grande do Sul', 'Rondonia', 'Roraima',
            'Santa Catarina', 'São Paulo', 'Sao Paulo', 'Sergipe', 'Tocantins', 'Rio Branco', 'Maceio',
            'Macapa', 'Manaus', 'Salvador', 'Fortaleza', 'Brasilia', 'Vitoria', 'Serra', 'Goiania', 'Sao Luis',
            'Cuiaba', 'Campo Grande', 'Belo Horizonte', 'Belem', 'Joao Pessoa', 'Curitiba', 'Recife',
            'Teresina', 'Natal', 'Porto Alegre', 'Porto Velho', 'Boa Vista', 'Florianopolis', 'Joinville',
            'Aracaju', 'Palmas', 'São Bernardo do Campo']

## remove the accounts that do not show location
follow_network2 = follow_network1.dropna(subset=['Location'])

## remove the accounts that are not located in Brazil
follow_network2 = follow_network2[follow_network2['Location'].apply(lambda x: any(string in x for string in Locations))]

# Filter 3: remove accounts that are not politics relevant

## create the political keywords lits
List_pol = ['política', 'político', 'political', 'politics', 'democracia', 'democracy',
            'bolsonaro', 'bolsonarista', 'lula', 'lulista', 'candidato', 'partido', 'presidente',
            'federal', 'conselho nacional de', 'ministro', 'senador', 'deputado', 'governador', 'prefeito',
            'conservador', 'conservative', 'liberal', 'liberalismo', 'libertairia', 'esquerdopata', 'esquerda', 'direita', 'direitista', 'vereador', 'secretário',
            'comunista', 'comunismo', 'nacionalista', 'patriota', 'globalista', 'feminista', 'armamentista', 'fascista', 'racist', 'colonialista', 'socialista',
            'jornalista', 'journalist', 'correspondent', 'repírter', 'comandando', 'commentator', 'comentarista', 'influencer', 'ativista', 'progressista', 'notícias', 'news', 'semanal',
            'aborto', 'mulher', 'preta', 'lgbt', 'gay', 'bissexualismo', 'homophobic', 'catílico', 'jesus', 'deus', 'ambiente', 'clima', 'justiça', 'imigrante',  'foreigner',
            'economia', 'bem-estar', 'pobre', 'desigualdade'
            ]

## create the list that might be missed: media outlets, politicians, and political parties
News_list = ['GloboNews', 'UOL', 'recordnews', 'JornalOGlobo', 'BandTV', 'folha', 'Estadao', 'bbcbrasil',
                  'RedeTV', 'jornalextra', 'SBTonline', 'bandnewstv', 'CNNBrasil', 'TVBrasil']

Politician_list = ['aldorebelo', 'SorayaThronicke', 'jairbolsonaro','LulaOficial','cirogomes', 'simonetebetbr', 'AndreJanonesAdv',
                  'lfdavilaoficial', 'Eymaeloficial', 'LeoPericlesUP', 'SofiaManzanoPCB', 'bivaroficial', 'pablomarcal',
                  'wilsonwitzel', 'JanainaDoBrasil', 'Reguffe', 'ibaneisoficial', 'RenanFilho_', 'Casagrande_ES',
                  'MichelTemer', 'SenadorKajuru', 'padrekelmon1414']

Party_list = ['ptbrasil', 'PSDBoficial', 'PDT_Nacional', 'ptb14', 'uniaobrasil44', 'PartidoLiberal', 'PSBNacional40', 'republicanos10', 'PCdoB_Oficial', 'pscnacional',
            'PODEMOS', 'PSD_55', 'partidoverdemex', 'PMNPARAIBA33', 'somosavante70', 'PPtc36', 'psol50', 'prtboficial',
            'prosnacional', 'partidonovo30', 'REDE_18', 'pstu', 'PCBpartidao', 'PCO29', 'MDB_Nacional']

## filter the political influencers based on keywords
follow_network_tem = follow_network2.dropna(subset=['Description'])
follow_network_tem['Description'] = list(follow_network_tem.Description.str.lower())
follow_network_tem = follow_network_tem[follow_network_tem['Description'].apply(lambda x: any(string in x for string in List_pol))]

## we manually check the profile descriptions of political influencer accounts again, and delete the non-politics accounts such as sports, entertainment, business, etc.
manual_filter_politics = pd.read_csv('./Manual_Filter_Politics.csv', index_col = 0)
deleted_list = manual_filter_politics[manual_filter_politics['Manual_filter']=='Delete']['Target'].tolist()
follow_network_tem = follow_network_tem[follow_network_tem['Target'].apply(lambda x: x not in deleted_list)]

## filter the political influencers based on additional lists
political_account_list = list(follow_network_tem['Target'])
additional_lists = News_list + Politician_list + Party_list
supplemented_list = [i for i in additional_lists if i not in political_account_list]
overall_list = political_account_list + supplemented_list
follow_network3 = follow_network[follow_network['Target'].apply(lambda x: x in overall_list)]
print(len(follow_network3))
follow_network3.to_csv('Final_Network_Data.csv')
