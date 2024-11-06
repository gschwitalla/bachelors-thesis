import pandas as pd
import os
import re

# Directory containing the .txt files
directory = 'G:\\Uni\\Git\\bachelors-thesis\\results\\LRS3_enh_OVRL_50'  # Replace with your file path

# List of training step counts as specified
steps = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

# Dictionary to hold the data
summary_data = {}

# Loop through each step, read the respective file, and extract mean/std values
for step in steps:
    filename = f"{step}k_summary.txt"
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

# Create a LaTeX table
latex_table = "\\begin{table}[h]\n\\centering\n\\begin{tabular}{l" + "c" * len(steps) + "}\n"
latex_table += "\\hline\n"
latex_table += "Metric "

# Column headers for each step
for step in steps:
    latex_table += f" & {step}k"
latex_table += " \\\\\n\\hline\n"

# Populate rows with metrics and their mean ± std values at each step
metrics = df.index  # Assuming all files have the same metrics
for metric in metrics:
    latex_table += metric
    for step in steps:
        if step in summary_data and metric in summary_data[step]:
            mean, std = summary_data[step][metric]
            latex_table += f" & {mean:.3f} ± {std:.3f}"
        else:
            latex_table += " & -"
    latex_table += " \\\\\n"

# Closing the LaTeX table
latex_table += "\\hline\n\\end{tabular}\n\\caption{Mean ± Standard Deviation across Training Steps}\n\\end{table}"

# Print LaTeX table
print(latex_table)
