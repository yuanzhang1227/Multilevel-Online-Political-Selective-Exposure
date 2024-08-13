# importing the required module
import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd
from scipy import stats

survey_twitter_ID = pd.read_csv('./Data/Survey_Twitter_Handles_ID.csv', index_col = 0)
survey_data = pd.read_excel('./Data/Survey_Data.csv', index_col=0).reset_index()
merge_mapper_survey = pd.merge(survey_twitter_ID, survey_data, left_on = 'CodPanelista', right_on = 'panelist_id', how = 'left')


# Set up the figure and axes
fig, axes = plt.subplots(3, 2, figsize=(21, 20))

# Increase space between columns and rows
plt.subplots_adjust(wspace=0.5)
plt.subplots_adjust(hspace=0.5)

# List of columns to plot
columns = ['Age (C)', 'Gender', 'Ethnic', 'Religion', 'Income', 'Education']

# Iterate over the columns and axes to create histograms
for col, ax in zip(columns, axes.flatten()):
    # Preparing data
    data1 = merge_mapper_survey[col].tolist()
    data1 = [x for x in data1 if not math.isnan(x)]
    data2 = survey_data[col].tolist()  # Assuming survey_w1[col] is the same for this example
    data2 = [x for x in data2 if not math.isnan(x)]

    # Perform KS test
    ks_stat, p_value = stats.ks_2samp(data1, data2)

    # Combine unique values from both datasets to get the bin edges
    unique_values = np.unique(np.concatenate((data1, data2)))

    # Define the number of bins and the bin edges
    num_bins = len(unique_values)
    bin_edges = np.concatenate((unique_values, [unique_values[-1] + 1]))  # Add one more bin for values outside the unique set

    # Calculate bin widths
    bin_width = bin_edges[1] - bin_edges[0]

    # Create histogram bars for the first dataset (network data)
    hist1, _ = np.histogram(data1, bins=bin_edges)
    bar_centers1 = bin_edges[:-1] + bin_width
    bar_width = 0.3 * bin_width
    bars1 = ax.bar(bar_centers1, hist1, width=bar_width, color='skyblue', edgecolor='black', label='Network Data')

    # Calculate the bar centers for the second dataset (survey data)
    bar_centers2 = bar_centers1 + bar_width

    # Create a secondary axis for the second dataset (survey data)
    ax2 = ax.twinx()

    # Create histogram bars for the second dataset (survey data)
    hist2, _ = np.histogram(data2, bins=bin_edges)
    bars2 = ax2.bar(bar_centers2, hist2, width=bar_width, color='orange', edgecolor='black', label='Survey Data')

    # Manually set x-axis tick positions and labels
    x_ticks = unique_values
    x_tick_positions = [bar_centers1[i] + 0.15 for i in range(len(bar_centers1))]
    ax.set_xticks(x_tick_positions)
    ax.set_xticklabels([str(x) for x in x_ticks], fontsize=15)

    # Add a legend for the datasets
    ax.legend([bars1, bars2], ['271 Sub-sample', 'Survey participants'], loc='upper right', fontsize=15)

    # Add text annotation for KS test p-value
    ax.text(0.80, 0.76, f'K-S p-value: {p_value:.3f}', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=15)

    ax.tick_params(axis='both', labelsize=20)
    ax2.tick_params(axis='y', labelsize=20)
    ax.set_xlabel(col, fontsize=20)

    # Set specific settings for several subplots
    if col == 'Education':
        ax.set_ylim(0, max(hist1) + 50)
        ax2.set_ylim(0, max(hist2) + 125)
        edu_labels = ['Pre-K', 'Elem-5', 'Elem-9', 'HS-1', 'HS-2', 'HS-3', 'Inc.HE', 'Comp.HE', 'PG/MSc', 'Ph.D.']
        ax.set_xticklabels(edu_labels, fontsize=15, rotation=45)

    if col == 'Gender':
        gender_labels = ['Male', 'Female']
        ax.set_xticklabels(gender_labels, fontsize=15)
        ax.set_ylim(0, max(hist1) + 50)
        ax2.set_ylim(0, max(hist2) + 200)
    if col == 'Age (C)':
        age_labels = ['16-24', '25-34', '35-44', '45-54', '55+']
        ax.set_xticklabels(age_labels, fontsize=15)
        ax.set_xlabel('Age', fontsize=20)

    if col == 'Ethnic':
        ethnic_labels = ['White', 'Black', 'Mixed', 'Yellow', 'Indigenous', 'Other']
        ax.set_xticklabels(ethnic_labels, fontsize=15, rotation=45)

    if col == 'Religion':
        rel_labels = ['Catholic', 'Prot. Evang.', 'Prot. Non-Evang.','Non-Christian', 'Jeova’s Witness', 'Afro-Brazilian', 'Kardecist', 'Jewish', 'Others', 'Agnostic', 'Atheist']
        ax.set_xticklabels(rel_labels, fontsize=15, rotation=45)

    if col == 'Income':
        income_labels = ['≤$1.2K', '$1.2-2.4K', '$2.4-3.6K', '$3.6-6K', '$6K-12K', '$12-24K', '$24-36K', '>$36K']
        ax.set_xticklabels(income_labels, fontsize=15, rotation=45)
# Save the figure
plt.savefig('./Plots/SI_Fig.1_Sample_validation.png', dpi=500, bbox_inches='tight')

# Show the plot
plt.show()
