import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define a function to read the relevant columns from the file
def read_data(file_path):
    # Read the data into a pandas DataFrame
    df = pd.read_csv(file_path, delim_whitespace=True)  # Assuming tab-separated values
    print("Columns in the file:", df.columns)
    exclude_rows = ['DURATION', 'INPUT_SNR', 'SSNR', 'WER_QuartzNet15x5Base-En']
    df_filtered = df[~df['Metric'].isin(exclude_rows)]
    # Extract the relevant columns: Metric, Mean, Std
    df_relevant = df_filtered[['Metric', 'mean', 'std']]
    return df_relevant

# Path to the input .txt files
dnsmos_file = 'G:\\Uni\\Git\\bachelors-thesis\\results\\LRS3_OVRL_50\\ovrl_50k_summary.txt'
sigmos_file = 'G:\\Uni\\Git\\bachelors-thesis\\results\\LRS3_SIGMOS\\sigmos_50k_summary.txt'

# Read the data from the files
dnsmos_df = read_data(dnsmos_file)
sigmos_df = read_data(sigmos_file)

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 8))

# Set positions for the bars
x = np.arange(len(dnsmos_df))  # Number of metrics
width = 0.35  # Width of the bars

# Plot bars for DNSMOS and SIGMOS
bar1 = ax.bar(x - width / 2, dnsmos_df['mean'], width, yerr=dnsmos_df['std'], label='DNSMOS', capsize=5)
bar2 = ax.bar(x + width / 2, sigmos_df['mean'], width, yerr=sigmos_df['std'], label='SIGMOS', capsize=5)

# Add labels, title, and legend
ax.set_xlabel('Metrics')
ax.set_ylabel('Mean Scores')
ax.set_title('Comparison of Mean Scores and Standard Deviations for DNSMOS and SIGMOS')
ax.set_xticks(x)
ax.set_xticklabels(dnsmos_df['Metric'], rotation=90)
ax.legend()

# Show plot
plt.tight_layout()
plt.show()
