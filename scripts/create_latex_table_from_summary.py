import pandas as pd
import os

# Directory containing the .txt files
directory = 'G:\\Uni\\Git\\bachelors-thesis\\results\\LRS3_SIGMOS'

# List of training step counts as specified
steps = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

# Dictionary to hold the data
summary_data = {}

# Loop through each step, read the respective file, and extract mean/std values
for step in steps:
    filename = f"sigmos_{step}k_summary.txt"
    filepath = os.path.join(directory, filename)

    if os.path.exists(filepath):
        # Read the file and extract the table as a DataFrame
        df = pd.read_csv(filepath, delim_whitespace=True, index_col=0)

        # Extract mean and std columns
        mean_values = df['mean']
        std_values = df['std']

        # Store in the dictionary under the current step
        summary_data[step] = {
            metric: (mean_values[metric], std_values[metric])
            for metric in df.index
        }

# Get list of metrics from the last processed DataFrame
metrics = df.index[[2, 4, 5, 7]]]

# Create a LaTeX table
latex_table = "\\begin{table}[h]\n\\centering\n\\begin{tabular}{l" + "c" * len(metrics) + "}\n"
latex_table += "\\hline\n"
latex_table += "Step (k)"

# Column headers for each metric
for metric in metrics:
    latex_table += f" & {metric}"
latex_table += " \\\\\n\\hline\n"

# Populate rows with steps and their mean ± std values for each metric
for step in steps:
    latex_table += f"{step}k"
    for metric in metrics:
        if step in summary_data and metric in summary_data[step]:
            mean, std = summary_data[step][metric]
            latex_table += f" & ${mean:.2f} \pm {std:.2f}$"
        else:
            latex_table += " & -"
    latex_table += " \\\\\n"

# Closing the LaTeX table
latex_table += "\\hline\n\\end{tabular}\n\\caption{Mean ± Standard Deviation for Each Metric Across Training Steps}\n\\end{table}"

# Print LaTeX table
print(latex_table)
