import pandas as pd
import numpy as np
import sys
import os

def create_csv_splits(input_csv, cutoff):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_csv)

    # Calculate the number of samples based on the cutoff percentage
    cutoff_count = int(len(df) * (cutoff / 100))

    # Sort by OVRL, SIG, BAK
    df_sorted_ovrl = df.sort_values(by='MOS_OVRL', ascending=False).head(cutoff_count)
    df_sorted_sig = df.sort_values(by='MOS_SIG', ascending=False).head(cutoff_count)
    df_sorted_bak = df.sort_values(by='MOS_NOISE', ascending=False).head(cutoff_count)

    # Randomly select {cutoff} percentage of samples
    df_random = df.sample(n=cutoff_count, random_state=1)

    # Extract directory and filename from the input path
    input_dir, input_filename = os.path.split(input_csv)
    base_filename, _ = os.path.splitext(input_filename)

    # Generate output filenames
    output_filenames = {
        "ovrl": os.path.join(input_dir, f"{base_filename}_{cutoff}_OVRL.csv"),
        "sig": os.path.join(input_dir, f"{base_filename}_{cutoff}_SIG.csv"),
        "bak": os.path.join(input_dir, f"{base_filename}_{cutoff}_BAK.csv"),
        "random": os.path.join(input_dir, f"{base_filename}_{cutoff}_RND.csv")
    }

    # Save the sorted and random DataFrames to CSV
    df_sorted_ovrl.to_csv(output_filenames["ovrl"], index=False)
    df_sorted_sig.to_csv(output_filenames["sig"], index=False)
    df_sorted_bak.to_csv(output_filenames["bak"], index=False)
    df_random.to_csv(output_filenames["random"], index=False)

    print("CSV files created successfully:")
    for key, value in output_filenames.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <path_to_csv> <cutoff_percentage>")
        sys.exit(1)

    input_csv = sys.argv[1]
    cutoff = float(sys.argv[2])

    create_csv_splits(input_csv, cutoff)
