import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Directories containing the .txt files and output directory for plots
ovrl_directory = 'G:/Uni/Git/bachelors-thesis/results/LRS3_OVRL_50/'
rnd_directory = 'G:/Uni/Git/bachelors-thesis/results/LRS3_RND_50/'
enh_directory = 'G:/Uni/Git/bachelors-thesis/results/LRS3_enh_OVRL_50/'
output_directory = 'G:/Uni/Git/bachelors-thesis/plots/LRS3/selection-exp'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Regex for the file names
pattern = r"(\d+)k_summary\.txt"

# Collect data for ovrl, rnd, and enh files
data_ovrl = {}
data_rnd = {}
data_enh = {}

def load_data(directory, data_dict):
    """Loads data from .txt files in the given directory into the provided dictionary."""
    for filename in os.listdir(directory):
        match = re.search(pattern, filename)
        if match:
            step = int(match.group(1))  # Extract step from filename
            filepath = os.path.join(directory, filename)

            # Read file and convert to DataFrame
            df = pd.read_csv(filepath, delim_whitespace=True, index_col=0)

            # Store data for this step
            data_dict[step] = df

# Load data from all directories
load_data(ovrl_directory, data_ovrl)
load_data(rnd_directory, data_rnd)
load_data(enh_directory, data_enh)

# Sort steps to ensure consistent order
sorted_steps = sorted(set(data_ovrl.keys()) & set(data_rnd.keys()) & set(data_enh.keys()))

# Define metric groups for each plot
metrics_groups = {
    "DNSMOS": ["DNSMOS_P808", "DNSMOS_OVRL", "DNSMOS_SIG", "DNSMOS_BAK"],
    "MOS": ["MOS_COL", "MOS_DISC", "MOS_LOUD", "MOS_REVERB", "MOS_SIG", "MOS_OVRL"],
    "SI-SDR": ["SI-SDR"],
    "ESTOI": ["ESTOI"],
    "SSNR": ["SSNR"]
}

# Font sizes
axis_label_size = 16
title_size = 18
tick_label_size = 16

# Plot each metric group for each step
for step in sorted_steps:
    df_ovrl = data_ovrl[step]
    df_rnd = data_rnd[step]
    df_enh = data_enh[step]

    for group_name, metrics in metrics_groups.items():
        # Prepare plot data
        labels = metrics
        means_ovrl = df_ovrl.loc[metrics, 'mean']
        stds_ovrl = df_ovrl.loc[metrics, 'std']
        means_rnd = df_rnd.loc[metrics, 'mean']
        stds_rnd = df_rnd.loc[metrics, 'std']
        means_enh = df_enh.loc[metrics, 'mean']
        stds_enh = df_enh.loc[metrics, 'std']

        x = np.arange(len(metrics))  # Label locations
        width = 0.25  # Adjusted width to fit three bars

        # Create the plot
        plt.figure(figsize=(12, 8))
        plt.bar(x - width, means_rnd, width, yerr=stds_rnd, capsize=5, label='rnd', color='salmon', edgecolor='black', alpha=0.7)
        plt.bar(x, means_ovrl, width, yerr=stds_ovrl, capsize=5, label='ovrl', color='skyblue', edgecolor='black', alpha=0.7)
        plt.bar(x + width, means_enh, width, yerr=stds_enh, capsize=5, label='enh', color='lightgreen', edgecolor='black', alpha=0.7)

        # Plot details with adjusted font sizes
        plt.xticks(x, labels, rotation=45, ha='right', fontsize=tick_label_size)
        plt.yticks(fontsize=tick_label_size)
        plt.ylabel('Score', fontsize=axis_label_size)
        plt.xlabel('Metrics', fontsize=axis_label_size)
        plt.title(f'{group_name} Scores for Step {step}k', fontsize=title_size)
        plt.legend(fontsize=tick_label_size)
        plt.tight_layout()  # Adjust layout to fit axis labels well

        # Save the plot to the specified output directory
        output_path = os.path.join(output_directory, f"{step}k_{group_name}.pdf")
        plt.savefig(output_path, format='pdf')
        plt.close()  # Close the figure to save memory

        print(f"Plot saved to {output_path}")
