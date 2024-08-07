import pandas as pd

# Lade die CSV-Datei
df = pd.read_csv('C:\\Users\\student\\Documents\\dev-results.csv')

# Funktion zur Zählung der Samples mit Score unter einem bestimmten Wert
def count_under_threshold(df, column, thresholds):
    counts = {}
    for threshold in thresholds:
        count = df[df[column] < threshold].shape[0]
        counts[f'under_{threshold}'] = count
    return counts

# Zählung der Samples insgesamt
thresholds = [2, 3, 4]
ovrl_counts = count_under_threshold(df, 'OVRL', thresholds)
sig_counts = count_under_threshold(df, 'SIG', thresholds)
bak_counts = count_under_threshold(df, 'BAK', thresholds)

print("Anzahl der Samples insgesamt mit OVRL unter 2/3/4:", ovrl_counts)
print("Anzahl der Samples insgesamt mit SIG unter 2/3/4:", sig_counts)
print("Anzahl der Samples insgesamt mit BAK unter 2/3/4:", bak_counts)

# Zählung der Samples in den unteren 10% nach OVRL
df_sorted_by_OVRL = df.nsmallest(int(len(df) * 0.1), 'OVRL')

sig_counts_lowest_10_ovrl = count_under_threshold(df_sorted_by_OVRL, 'SIG', thresholds)
bak_counts_lowest_10_ovrl = count_under_threshold(df_sorted_by_OVRL, 'BAK', thresholds)

print("Anzahl der Samples in den unteren 10% nach OVRL mit SIG unter 2/3/4:", sig_counts_lowest_10_ovrl)
print("Anzahl der Samples in den unteren 10% nach OVRL mit BAK unter 2/3/4:", bak_counts_lowest_10_ovrl)
