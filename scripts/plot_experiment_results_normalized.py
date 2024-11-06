import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

# Directory containing the CSV files
directory = 'G:\\Uni\\Git\\bachelors-thesis\\results\\LRS3_enh_OVRL_50'

# Metrics to plot
metrics = ['POLQA_WB', 'PESQ_WB', 'SI-SDR', 'ESTOI', 'DNSMOS_OVRL', 'DNSMOS_SIG', 'DNSMOS_BAK']

# Extract step number from filename (e.g., "50k_metrics.csv" -> 50)
def extract_step(filename):
    match = re.search(r'(\d+)k', filename)
    if match:
        return int(match.group(1))
    return None

# Load all CSV files and organize data by steps
def load_data(directory):
    data = []

    for filename in os.listdir(directory):
        if filename.endswith('_metrics.csv'):
            filepath = os.path.join(directory, filename)
            step = extract_step(filename)
            if step is not None:
                df = pd.read_csv(filepath)

                # Calculate the mean scores for the entire dataset at this step
                mean_scores = df[metrics].mean().to_dict()
                mean_scores['step'] = step

                data.append(mean_scores)

    # Sort by step for consistent plotting
    data = sorted(data, key=lambda x: x['step'])

    return pd.DataFrame(data)

# Plot scores for all metrics
def plot_scores(df, metric, save_path, show_approx_curve=False):
    plt.figure(figsize=(10, 6))

    # Plot raw data points
    plt.plot(df['step'], df[metric], 'o-', label=metric, color='blue')

    if show_approx_curve:
        # Polynomial approximation (degree 2)
        fit = np.poly1d(np.polyfit(df['step'], df[metric], 2))

        # Generate smooth x values for curve plotting
        x_smooth = np.linspace(min(df['step']), max(df['step']), 500)

        # Plot the approximation curve
        plt.plot(x_smooth, fit(x_smooth), '--', color='blue', label='Approx curve')

    plt.xlabel('Steps (k)', fontsize=26)
    plt.ylabel(f'{metric} Score', fontsize=26)
    plt.title(f'{metric} Scores across Steps', fontsize=26)
    plt.tick_params(axis='both', labelsize=16)
    plt.legend()

    # Save and show the plot
    plt.savefig(os.path.join(save_path, f'{metric}_comparison.png'))
    plt.show()

# Main function to load data and generate plots
def main():
    save_path = 'G:\\Uni\\Git\\bachelors-thesis\\plots\\LRS3\\results\\LRS3_enh_OVRL_50'
    os.makedirs(save_path, exist_ok=True)

    # Load data from CSV files
    df = load_data(directory)

    # Generate plots for each metric
    for metric in metrics:
        plot_scores(df, metric, save_path)

    # Combined plot for all metrics
    plt.figure(figsize=(10, 6))
    colors = ['blue', 'green', 'purple', 'orange', 'cyan', 'magenta', 'yellow']

    for idx, metric in enumerate(metrics):
        plt.plot(df['step'], df[metric], 'o-', label=metric, color=colors[idx])

    plt.xlabel('Steps (k)', fontsize=20)
    plt.ylabel('Score', fontsize=20)
    plt.title('Scores across Steps', fontsize=20)
    plt.tick_params(axis='both', labelsize=16)
    plt.legend()

    # Save and show the combined plot
    combined_plot_path = os.path.join(save_path, 'combined_comparison.png')
    plt.savefig(combined_plot_path)
    plt.show()

if __name__ == '__main__':
    main()
