import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

# Directory containing the CSV files
directory = 'G:\\Uni\\Git\\bachelors-thesis\\results'

# Metrics to plot
metrics = ['POLQA_WB', 'PESQ_WB', 'SI-SDR', 'ESTOI', 'DNSMOS_OVRL', 'DNSMOS_SIG', 'DNSMOS_BAK']

# Extract step number from filename (e.g., "ovrl_50k_metrics.csv" -> 50)
def extract_step(filename):
    match = re.search(r'(\d+)k', filename)
    if match:
        return int(match.group(1))
    return None

# Load all CSV files and organize data by steps
def load_data(directory):
    ovrl_data = []
    rnd_data = []

    for filename in os.listdir(directory):
        if filename.endswith('_metrics.csv'):
            filepath = os.path.join(directory, filename)
            step = extract_step(filename)
            if step is not None:
                df = pd.read_csv(filepath)

                # Calculate the mean scores for the entire dataset at this step
                mean_scores = df[metrics].mean().to_dict()
                mean_scores['step'] = step

                if filename.startswith('ovrl'):
                    ovrl_data.append(mean_scores)
                elif filename.startswith('rnd'):
                    rnd_data.append(mean_scores)

    # Sort by step for consistent plotting
    ovrl_data = sorted(ovrl_data, key=lambda x: x['step'])
    rnd_data = sorted(rnd_data, key=lambda x: x['step'])

    return pd.DataFrame(ovrl_data), pd.DataFrame(rnd_data)

# Plot scores for OVRL and RND
def plot_scores(ovrl_df, rnd_df, metric, save_path, show_approx_curve=True):
    plt.figure(figsize=(10, 6))

    # Plot raw data points
    plt.plot(ovrl_df['step'], ovrl_df[metric], 'o-', label='OVRL ' + metric, color='blue')
    plt.plot(rnd_df['step'], rnd_df[metric], 'o-', label='RND ' + metric, color='red')

    if show_approx_curve:
        # Polynomial approximation (degree 2)
        ovrl_fit = np.poly1d(np.polyfit(ovrl_df['step'], ovrl_df[metric], 2))
        rnd_fit = np.poly1d(np.polyfit(rnd_df['step'], rnd_df[metric], 2))

        # Generate smooth x values for curve plotting
        x_smooth = np.linspace(min(ovrl_df['step']), max(ovrl_df['step']), 500)

        # Plot the approximation curves
        plt.plot(x_smooth, ovrl_fit(x_smooth), '--', color='blue', label='OVRL approx curve')
        plt.plot(x_smooth, rnd_fit(x_smooth), '--', color='red', label='RND approx curve')

    plt.xlabel('Steps (k)')
    plt.ylabel(f'{metric} Score')
    plt.title(f'{metric} Scores across Steps')
    plt.legend()

    # Save and show the plot
    plt.savefig(os.path.join(save_path, f'{metric}_comparison.png'))
    plt.show()

# Main function to load data and generate plots
def main():
    save_path = 'G:\\Uni\\Git\\bachelors-thesis\\plots\\LRS3\\results'
    os.makedirs(save_path, exist_ok=True)

    # Load data from CSV files
    ovrl_df, rnd_df = load_data(directory)

    # Generate separate and combined plots
    for metric in metrics:
        # Plot for each metric individually
        plot_scores(ovrl_df, rnd_df, metric, save_path)

    # Combined plot for all metrics
    plt.figure(figsize=(10, 6))
    colors = ['blue', 'green', 'purple', 'orange', 'cyan', 'magenta', 'yellow']

    for idx, metric in enumerate(metrics):
        plt.plot(ovrl_df['step'], ovrl_df[metric], 'o-', label=f'OVRL {metric}', color=colors[idx])
        plt.plot(rnd_df['step'], rnd_df[metric], 'o-', label=f'RND {metric}', linestyle='dashed', color=colors[idx])

    plt.xlabel('Steps (k)')
    plt.ylabel('Score')
    plt.title('DNSMOS Scores across Steps (OVRL vs RND)')
    plt.legend()

    # Save and show the combined plot
    combined_plot_path = os.path.join(save_path, 'combined_comparison.png')
    plt.savefig(combined_plot_path)
    plt.show()

if __name__ == '__main__':
    main()
