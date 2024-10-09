import pandas as pd
import argparse

# Count samples with score below given threshold
def count_under_threshold(df, column, thresholds):
    counts = {}
    for threshold in thresholds:
        count = df[df[column] < threshold].shape[0]
        counts[f'under_{threshold}'] = count
    return counts

def main(file_path):
    # Load CSV file
    df = pd.read_csv(file_path)

    # Count total number of samples
    thresholds = [2, 3, 4]
    ovrl_counts = count_under_threshold(df, 'OVRL', thresholds)
    sig_counts = count_under_threshold(df, 'SIG', thresholds)
    bak_counts = count_under_threshold(df, 'BAK', thresholds)

    # Output total number of samples
    print("Total number of samples:", len(df))

    print("Number of samples with OVRL below 2/3/4:", ovrl_counts)
    print("Number of samples with SIG below 2/3/4:", sig_counts)
    print("Number of samples with BAK below 2/3/4:", bak_counts)

    # Count samples in the lowest 10% by OVRL
    df_sorted_by_OVRL = df.nsmallest(int(len(df) * 0.1), 'OVRL')

    sig_counts_lowest_10_ovrl = count_under_threshold(df_sorted_by_OVRL, 'SIG', thresholds)
    bak_counts_lowest_10_ovrl = count_under_threshold(df_sorted_by_OVRL, 'BAK', thresholds)

    print("Number of samples in the lowest 10% by OVRL with SIG below 2/3/4:", sig_counts_lowest_10_ovrl)
    print("Number of samples in the lowest 10% by OVRL with BAK below 2/3/4:", bak_counts_lowest_10_ovrl)

    # Calculate the average scores
    average_ovrl = df['OVRL'].mean()
    average_sig = df['SIG'].mean()
    average_bak = df['BAK'].mean()

    # Output the average scores
    print(f'Average OVRL score: {average_ovrl:.2f}')
    print(f'Average SIG score: {average_sig:.2f}')
    print(f'Average BAK score: {average_bak:.2f}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a CSV file and calculate various statistics.")
    parser.add_argument('file_path', type=str, help='Path to the CSV file')

    args = parser.parse_args()

    # Call the main function with the provided file path
    main(args.file_path)
