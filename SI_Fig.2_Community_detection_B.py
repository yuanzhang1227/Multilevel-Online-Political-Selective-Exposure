# importing the required module
import matplotlib.pyplot as plt
import pickle
from pygenstability import plotting

# import the results of PyGenstability
file_path = './Data/results_n_scales1000.pkl'
with open(file_path, 'rb') as file:
    results = pickle.load(file)

# plot the results of Pygenstability
plt.figure(figsize=(7, 5))
axes = plotting.plot_scan(results, figure_name=None)

## alignment positions for left side and right side
left_alignment = -0.1
right_alignment = 1.1

## apply alignment settings to all axes
for ax in axes:
    if ax.yaxis.get_label_position() == 'left':
        ax.yaxis.set_label_coords(left_alignment, 0.5)
    else:
        ax.yaxis.set_label_coords(right_alignment, 0.5)

## specific plot adjustments
axes[3].set_ylim(0, 50)
axes[3].axhline(3, ls="--", color="k", zorder=-1, lw=0.5)
axes[3].axhline(9, ls="--", color="k", zorder=-1, lw=0.5)
axes[3].axhline(27, ls="--", color="k", zorder=-1, lw=0.5)

# save the plot
plt.savefig("./Plots/SI_Fig.2_Community_detection_B.png", dpi=500, bbox_inches='tight')
plt.show()
plt.close()