import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Directory containing the .txt files and output directory for plots
ovrl_directory = 'G:/Uni/Git/bachelors-thesis/results/LRS3_SIGMOS/'
output_directory = 'G:/Uni/Git/bachelors-thesis/plots/LRS3/SIGMOS'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Regex for the file names
pattern = r"(\d+)k_summary\.txt"

# Collect data for ovrl files
data_ovrl = {}

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

# Load data from the ovrl directory
load_data(ovrl_directory, data_ovrl)

# Sort steps to ensure consistent order
sorted_steps = sorted(data_ovrl.keys())

# Define metric groups to consider
metrics_to_plot = {
    "SI-SDR": "SI-SDR",
    "ESTOI": "ESTOI",
    "SSNR": "SSNR",
    "DNSMOS_OVRL": "DNSMOS_OVRL",
    "DNSMOS_SIG": "DNSMOS_SIG",
    "DNSMOS_BAK": "DNSMOS_BAK",
    "MOS_OVRL": "MOS_OVRL",
    "POLQA_WB": "POLQA_WB",
    "PESQ_WB": "PESQ_WB"
}

# Font sizes
axis_label_size = 16
title_size = 18
tick_label_size = 16

# Create plots for each metric
for metric, label in metrics_to_plot.items():
    means = []
    stds = []

    # Collect means and standard deviations for the metric over the steps
    for step in sorted_steps:
        df_ovrl = data_ovrl[step]
        means.append(df_ovrl.loc[metric, 'mean'])
        stds.append(df_ovrl.loc[metric, 'std'])

    # Create the plot
    plt.figure(figsize=(12, 8))
    plt.errorbar(sorted_steps, means, yerr=stds, capsize=5, label=label, color='skyblue', marker='o')

    # Plot details with adjusted font sizes
    # Display only every second step in first 10k for better readability
    plt.xticks(
    [step for step in sorted_steps if step % 2 == 0],  # Positions where labels should appear
    [f"{step}" for step in sorted_steps if step % 2 == 0],  # Labels for those positions
    ha='center',
    fontsize=tick_label_size
)
    plt.yticks(fontsize=tick_label_size)
    plt.ylabel('Score', fontsize=axis_label_size)
    plt.xlabel('Steps (k)', fontsize=axis_label_size)
    plt.title(f'{label} Scores over Steps', fontsize=title_size)
    plt.legend(fontsize=tick_label_size)
    plt.tight_layout()  # Adjust layout to fit axis labels well

    # Save the plot to the specified output directory
    output_path = os.path.join(output_directory, f'{label}_scores_over_steps.pdf')
    plt.savefig(output_path, format = 'pdf')
    plt.close()  # Close the figure to save memory

    print(f"Plot saved to {output_path}")
