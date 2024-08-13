# importing the required module
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# import followed data set
following_following = pd.read_csv('./Data/Following_Following.csv', index_col = 0)
def compute_CCDF(data, normalize=True):
    # Sort the data in ascending order
    x = np.sort(data)

    # Compute the CCDF counts
    # For each value in x, count how many values are greater or equal to it.
    counts = len(data) - np.searchsorted(x, x, side='right')

    # Normalize if required
    if normalize:
        counts = counts / len(data)

    return x, counts

# Compute CCDF
num_follower = list(following_following['Followers_count'])
x_ccdf, ccdf = compute_CCDF(num_follower)

# Find the closest x-value to 1000 and its corresponding y-value in CCDF
closest_x_index = np.argmin(np.abs(x_ccdf - 1000))
x_at_1000 = x_ccdf[closest_x_index]
y_at_1000 = ccdf[closest_x_index]
print(x_ccdf)
# Plotting
plt.figure(figsize=(6,5))
plt.loglog(x_ccdf, ccdf, marker='o', linestyle='-', color='blue')
plt.axvline(x=x_at_1000, color='red', linestyle='--', label=f"x=1,000 (y={y_at_1000:.2f})")

plt.xlabel('Counts (log scale)', fontsize=15)
plt.ylabel('CCDF (log scale)', fontsize=15)
plt.title('CCDF of Followers (cutoff = 1,000)', fontsize=15)
plt.legend(loc='upper right')

plt.savefig("./Plots/SI_Fig.2_Community_detection_A", dpi=500)
plt.tight_layout()
plt.show()