library(ggplot2)
library(tidyverse)
library(dplyr)
library(FactoMineR)
library(factoextra)
library(gridExtra) 
library(patchwork)
library(scales)
library(ggrepel)
library(DHARMa)
library(broom)
library(kableExtra)

#### Define categories of variables

demographics <- c('Age', 'Religion', 'Religious.level', 'Gender', 'Ethnic', 'Education', 'Living ', 'Income')

news_consumption <- c('News_Television.news', 'News_National.newspapers', 'News_Regional.newspapers', 'News_Radio.news', 'News_Online.news.sources', 'News_News.via.social.media',
                      
                      'Social.Media_Twitter', 'Social.Media_Facebook', 'Social.Media_YouTube', 'Social.Media_Whatsapp', 'Social.Media_Telegram',
                      
                      'Campaign.News_Television.news ','Campaign.News_National.newspapers', 'Campaign.News_Regional.newspapers', 'Campaign.News_Radio.news', 'Campaign.News_Online.news.sources', 'Campaign.News_News.via.social.media',
                      
                      'Read.Watch_Twitter', 'Read.Watch_Youtube', 'Read.Watch_Facebook', ' Read.Watch_Whatsapp', ' Read.Watch_Telegram',
                      
                      'Share.Liked_Twitter', 'Share.Liked_Youtube', 'Share.Liked_Facebook', 'Share.Liked_Whatsapp', 'Share.Liked_Telegram',
                      
                      'Comment.Post_Twitter', 'Comment.Post_Youtube', 'Comment.Post_Facebook', 'Comment.Post_Whatsapp', 'Comment.Post_Telegram',
                      
                      'Mess.Apps.Information_1', 'Mess.Apps.Information_2', 'Mess.Apps.Information_3', 'Mess.Apps.Information_97',
                      
                      'Mess.Apps.Discussion_1', 'Mess.Apps.Discussion_2', 'Mess.Apps.Discussion_3', 'Mess.Apps.Discussion_97',
                      
                      'Mess.App.Groups')

political_communication <- c('Fatigue_1', 'Fatigue_2', 'Fatigue_3',
                             
                             'Conflict.Orientation_1', 'Conflict.Orientation_2', 'Conflict.Orientation_3', 'Conflict.Orientation_4', 'Conflict.Orientation_5',
                             
                             'Discussion_1', 'Discussion_2', 'Discussion_3', 'Discussion_4',
                             
                             'Conflicting.Opinion_1','Conflicting.Opinion_2', 'Conflicting.Opinion_3', 'Conflicting.Opinion_4')

political_identification <- c('Ideological.Position',
                              
                              'Party.Alignment',
                              
                              'Alignment.Measurement',
                              
                              'Politician.Likeability_1', 'Politician.Likeability_2', 'Politician.Likeability_3', 'Politician.Likeability_4',
                              'Politician.Likeability_5', 'Politician.Likeability_6', 'Politician.Likeability_7', 'Politician.Likeability_8', 'Politician.Likeability_9',
                              'Politician.Likeability_10', 'Politician.Likeability_11', 'Politician.Likeability_12',
                              
                              'Party.Likeability_1', 'Party.Likeability_2', 'Party.Likeability_3', 'Party.Likeability_4', 'Party.Likeability_5', 'Party.Likeability_6', 'Party.Likeability_7',
                              'Party.Likeability_8', 'Party.Likeability_9', 'Party.Likeability_10', 'Party.Likeability_11', 'Party.Likeability_12')

political_engagement <- c('Participation_Institutional.Electoral campaign_1', 'Participation_Institutional.Electoral campaign_2', 'Participation_Institutional.Electoral campaign_3', 'Participation_Institutional.Electoral campaign_4', 'Participation_Institutional.Electoral campaign_5', 'Participation_Institutional.Electoral campaign_6', 'Participation_Institutional.Electoral campaign_7',
                          
                          'Participation_Protest_1', 'Participation_Protest_2', 'Participation_Protest_3', 'Participation_Protest_4',
                          
                          'Participation_Civic.engagement_1', 'Participation_Civic.engagement_2',
                          
                          'Participation_Online.participation_1', 'Participation_Online.participation_2', 'Participation_Online.participation_3', 'Participation_Online.participation_4', 'Participation_Online.participation_5',
                          
                          'Political.Interest', 'Politician.Party.Accounts.Following_Twitter', 'Politician.Party.Accounts.Following_Facebook', 'Distance.of.Following.Accounts')

incivility <- c('Incivility.Perception_Exclusion_Twitter', 'Incivility.Perception_Exclusion_Youtube', 'Incivility.Perception_Exclusion_Facebook', 'Incivility.Perception_Exclusion_Whatsapp', 'Incivility.Perception_Exclusion_Telegram',
                
                'Incivility.Perception_Impoliteness_Twitter', 'Incivility.Perception_Impoliteness_Youtube', 'Incivility.Perception_Impoliteness_Facebook', 'Incivility.Perception_Impoliteness_Whatsapp', 'Incivility.Perception_Impoliteness_Telegram',
                
                'Incivility.Perception_Physical.harm.violence_Twitter', 'Incivility.Perception_Physical.harm.violence_Youtube', 'Incivility.Perception_Physical.harm.violence_Facebook', 'Incivility.Perception_Physical.harm.violence_Whatsapp', 'Incivility.Perception_Physical.harm.violence_Telegram',
                
                'Incivility.Perception_Negativity_Twitter', 'Incivility.Perception_Negativity_Youtube', 'Incivility.Perception_Negativity_Facebook', 'Incivility.Perception_Negativity_Whatsapp', 'Incivility.Perception_Negativity_Telegram',
                
                'Incivility.Perception_Personal.attack_Twitter', 'Incivility.Perception_Personal.attack_Youtube', 'Incivility.Perception_Personal.attack_Facebook', 'Incivility.Perception_Personal.attack_Whatsapp', 'Incivility.Perception_Personal.attack_Telegram',
                
                'Incivility.Perception_Stereotype.Hate speech.Discrimination_Twitter', 'Incivility.Perception_Stereotype.Hate speech.Discrimination_Youtube', 'Incivility.Perception_Stereotype.Hate speech.Discrimination_Facebook', 'Incivility.Perception_Stereotype.Hate speech.Discrimination_Whatsapp', 'Incivility.Perception_Stereotype.Hate speech.Discrimination_Telegram',
                
                'Incivility.Perception_Threat.to.democratic.freedoms_Twitter', 'Incivility.Perception_Threat.to.democratic.freedoms_Youtube', 'Incivility.Perception_Threat.to.democratic.freedoms_Facebook', 'Incivility.Perception_Threat.to.democratic.freedoms_Whatsapp', 'Incivility.Perception_Threat.to.democratic.freedoms_Telegram',
                
                'Online.offline.Incivility_1', 'Online.offline.Incivility_2', 'Online.offline.Incivility_3', 'Online.offline.Incivility_4', 'Online.offline.Incivility_5', 'Online.offline.Incivility_6',
                
                'Experience_1', 'Experience_2', 'Experience_3', 'Experience_4',
                
                'Self.censorship_1', 'Self.censorship_2', 'Self.censorship_3', 'Self.censorship_4', 'Self.censorship_5', 'Self.censorship_6', 'Self.censorship_7')

disinformation <- c('False.Information_Facebook', 'False.Information_Twitter', 'False.Information_Youtube', 'False.Information_Whatsapp', 'False.Information_Telegram', 'False.Information_News.Media')

authority_trust <- c('Media.Trust_1', 'Media.Trust_2', 'Media.Trust_3', 'Media.Trust_4', 'Media.Trust_5', 'Media.Trust_6', 'Media.Trust_7', 'Media.Trust_8')

populism <- c('Populism_1', 'Populism_2', 'Populism_3', 'Populism_4', 'Populism_5', 'Populism_6', 'Populism_7')

democracy <- c('Support.for.Democracy', 'Satisfactory.with.Democracy')

variable_list <- c(demographics, news_consumption, political_communication, political_identification, political_engagement, incivility, disinformation, authority_trust, populism, democracy)

#### differentiate continous variables and categorical variables
continuous_vars <- c('Overlap', 'Label_diversity_with_nans', 'Label_diversity_without_nans', 'Domain_diversity', 'Normalized_cut', 'Gini', 'Age', 'Religious.level', 'Education', 'Income',
                     
                     'News_Television.news', 'News_National.newspapers', 'News_Regional.newspapers', 'News_Radio.news', 'News_Online.news.sources', 'News_News.via.social.media',
                     'Social.Media_Twitter', 'Social.Media_Facebook', 'Social.Media_YouTube', 'Social.Media_Whatsapp', 'Social.Media_Telegram',
                     'Campaign.News_Television.news','Campaign.News_National.newspapers', 'Campaign.News_Regional.newspapers', 'Campaign.News_Radio.news', 'Campaign.News_Online.news.sources', 'Campaign.News_News.via.social.media',
                     'Read.Watch_Twitter', 'Read.Watch_Youtube', 'Read.Watch_Facebook', 'Read.Watch_Whatsapp', 'Read.Watch_Telegram', 'Share.Liked_Twitter', 'Share.Liked_Youtube', 'Share.Liked_Facebook', 'Share.Liked_Whatsapp', 'Share.Liked_Telegram',
                     'Comment.Post_Twitter', 'Comment.Post_Youtube', 'Comment.Post_Facebook', 'Comment.Post_Whatsapp', 'Comment.Post_Telegram',
                     
                     'Fatigue_1', 'Fatigue_2', 'Fatigue_3', 'Conflict.Orientation_1',
                     'Conflict.Orientation_2', 'Conflict.Orientation_3', 'Conflict.Orientation_4', 'Conflict.Orientation_5', 'Discussion_1', 'Discussion_2', 'Discussion_3', 'Discussion_4', 'Conflicting.Opinion_1','Conflicting.Opinion_2', 'Conflicting.Opinion_3',
                     'Conflicting.Opinion_4', 'Incivility.Perception_Exclusion_Twitter', 'Incivility.Perception_Exclusion_Youtube', 'Incivility.Perception_Exclusion_Facebook', 'Incivility.Perception_Exclusion_Whatsapp', 'Incivility.Perception_Exclusion_Telegram',
                     'Incivility.Perception_Impoliteness_Twitter', 'Incivility.Perception_Impoliteness_Youtube', 'Incivility.Perception_Impoliteness_Facebook', 'Incivility.Perception_Impoliteness_Whatsapp', 'Incivility.Perception_Impoliteness_Telegram',
                     'Incivility.Perception_Physical.harm.violence_Twitter', 'Incivility.Perception_Physical.harm.violence_Youtube', 'Incivility.Perception_Physical.harm.violence_Facebook', 'Incivility.Perception_Physical.harm.violence_Whatsapp',
                     'Incivility.Perception_Physical.harm.violence_Telegram', 'Incivility.Perception_Negativity_Twitter', 'Incivility.Perception_Negativity_Youtube', 'Incivility.Perception_Negativity_Facebook', 'Incivility.Perception_Negativity_Whatsapp',
                     'Incivility.Perception_Negativity_Telegram', 'Incivility.Perception_Personal..attack_Twitter', 'Incivility.Perception_Personal..attack_Youtube', 'Incivility.Perception_Personal..attack_Facebook', 'Incivility.Perception_Personal..attack_Whatsapp',
                     'Incivility.Perception_Personal..attack_Telegram', 'Incivility.Perception_Stereotype.Hate.speech.Discrimination_Twitter', 'Incivility.Perception_Stereotype.Hate.speech.Discrimination_Youtube',
                     'Incivility.Perception_Stereotype.Hate.speech.Discrimination_Facebook', 'Incivility.Perception_Stereotype.Hate.speech.Discrimination_Whatsapp', 'Incivility.Perception_Stereotype.Hate.speech.Discrimination_Telegram',
                     'Incivility.Perception_Threat.to.democratic.freedoms_Twitter', 'Incivility.Perception_Threat.to.democratic.freedoms_Youtube', 'Incivility.Perception_Threat.to.democratic.freedoms_Facebook',
                     'Incivility.Perception_Threat.to.democratic.freedoms_Whatsapp', 'Incivility.Perception_Threat.to.democratic.freedoms_Telegram',
                     
                     'Online.offline.Incivility_1', 'Online.offline.Incivility_2',
                     'Online.offline.Incivility_3', 'Online.offline.Incivility_4', 'Online.offline.Incivility_5', 'Online.offline.Incivility_6', 'Experience_1', 'Experience_2', 'Experience_3', 'Experience_4', 
                     #'Self.censorship_1', 'Self.censorship_2', 'Self.censorship_3', 'Self.censorship_4', 'Self.censorship_5', 'Self.censorship_6', 'Self.censorship_7',
                     
                     'Participation_Institutional.Electoral.campaign_1', 'Participation_Institutional.Electoral.campaign_2', 'Participation_Institutional.Electoral.campaign_3',
                     'Participation_Institutional.Electoral.campaign_4', 'Participation_Institutional.Electoral.campaign_5', 'Participation_Institutional.Electoral.campaign_6', 'Participation_Institutional.Electoral.campaign_7','Participation_Protest_1',
                     'Participation_Protest_2', 'Participation_Protest_3', 'Participation_Protest_4', 'Participation_Civic.engagement_1', 'Participation_Civic.engagement_2', 'Participation_Online.participation_1', 'Participation_Online.participation_2',
                     'Participation_Online.participation_3', 'Participation_Online.participation_4', 'Participation_Online.participation_5',
                     
                     'Political.Interest', 'Ideological.Position', 'Alignment.Measurement',
                     
                     'Politician.Likeability_1', 'Politician.Likeability_2', 'Politician.Likeability_3', 'Politician.Likeability_4', 'Politician.Likeability_5', 'Politician.Likeability_6', 'Politician.Likeability_7', 'Politician.Likeability_8', 'Politician.Likeability_9',
                     'Politician.Likeability_10', 'Politician.Likeability_11', 'Politician.Likeability_12', 'Party.Likeability_1', 'Party.Likeability_2', 'Party.Likeability_3', 'Party.Likeability_4', 'Party.Likeability_5', 'Party.Likeability_6', 'Party.Likeability_7',
                     'Party.Likeability_8', 'Party.Likeability_9', 'Party.Likeability_10', 'Party.Likeability_11', 'Party.Likeability_12',
                     
                     'Media.Trust_1', 'Media.Trust_2', 'Media.Trust_3', 'Media.Trust_4', 'Media.Trust_5', 'Media.Trust_6', 'Media.Trust_7', 'Media.Trust_8',
                     
                     'False.Information_Facebook', 'False.Information_Twitter', 'False.Information_Youtube', 'False.Information_Whatsapp', 'False.Information_Telegram', 'False.Information_News.Media',
                     
                     'Populism_1', 'Populism_2', 'Populism_3', 'Populism_4', 'Populism_5', 'Populism_6', 'Populism_7', 'Support.for.Democracy', 'Satisfactory.with.Democracy',
                     'Politician.Party.Accounts.Following_Twitter', 'Politician.Party.Accounts.Following_Facebook')

categorical_vars <- c('Gender', 'Ethnic', 'Religion', 'Living',
                      'Party.Alignment',
                      'Mess.Apps.Information_1', 'Mess.Apps.Information_2', 'Mess.Apps.Information_3', 'Mess.Apps.Information_97',
                      'Mess.Apps.Discussion_1', 'Mess.Apps.Discussion_2', 'Mess.Apps.Discussion_3', 'Mess.Apps.Discussion_97', 'Mess.App.Groups',
                      'Distance.of.Following.Accounts')

### After PCA
pca_continuous_vars <- c(
  
  'Age', 'Religious.level', 'Education', 'Income',
  
  'Read.Watch_Twitter',  'Read.Watch_Whatsapp',  
  
  'Fatigue_1', 'Conflicting.Opinion_1',
  
  'Incivility.Perception_Impoliteness_Twitter', 'Online.offline.Incivility_1',  
  
  'Participation_Protest_1', 
  
  'Ideological.Position', 'Alignment.Measurement',
  
  'Media.Trust_3', 'Media.Trust_7', 
  
  'False.Information_Youtube',
  
  'Populism_1', 'Populism_7', 'Support.for.Democracy', 'Satisfactory.with.Democracy')

pca_categorical_vars <- c('Gender', 'Ethnic', 'Religion', 'Living',
                          'Mess.Apps.Information_1')


length(pca_continuous_vars) + length(pca_categorical_vars)


# Load a CSV file into a dataframe
my_data <- read.csv("./Data/Regression_Survey_Data_3.csv") ## replaced by "Regression_Survey_Data_8", "Regression_Survey_Data_14", "Regression_Survey_Data_46"

# Find columns with more than 50 missing values
cols_to_remove <- colSums(is.na(my_data)) > 95
rows_to_remove <- rowSums(is.na(my_data)) >= 75

# Calculate the number of rows to be removed
number_of_rows_removed <- sum(rows_to_remove)
number_of_cols_removed <- sum(cols_to_remove)

# Print the number of rows removed
cat("Number of rows removed:", number_of_rows_removed, "\n")
cat("Number of columns removed:", number_of_cols_removed, "\n")

# Remove them
my_data <- my_data[, !cols_to_remove]
my_data <- my_data[!rows_to_remove, ]
data_shape <- dim(my_data)
data_shape[1]
data_shape[2]

# Convert categorical variables to factors

for (var in categorical_vars) {
  my_data[[var]] <- as.factor(my_data[[var]])
}

# Convert continuous variables to numeric
for (var in continuous_vars) {
  my_data[[var]] <- as.numeric(my_data[[var]])
}

# Impute numeric columns with the mean
columns_not_to_impute <- c('Overlap', 'Label_diversity_with_nans', 'Label_diversity_without_nans', 
                           'Domain_diversity', 'Normalized_cut', 'Gini')
numeric_columns <- sapply(my_data, is.numeric)
columns_to_impute <- setdiff(names(my_data)[numeric_columns], columns_not_to_impute)
my_data[columns_to_impute] <- lapply(my_data[columns_to_impute], function(x) {
  x[is.na(x)] <- mean(x, na.rm = TRUE)
  return(x)
})

# Impute factor columns with the mode (most frequent value)
getmode <- function(v) {
  uniqv <- unique(v)
  uniqv[which.max(tabulate(match(v, uniqv)))]
}

my_data[sapply(my_data, is.factor)] <- lapply(my_data[sapply(my_data, is.factor)], function(x) {
  # Replace NA values with the mode of the column
  x[is.na(x)] <- getmode(x[!is.na(x)])
  return(x)
})