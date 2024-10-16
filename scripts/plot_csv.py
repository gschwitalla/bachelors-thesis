import pandas as pd
import matplotlib.pyplot as plt

# load csv file
df = pd.read_csv('C:\\Dev\\evaluation_results\\LRS3\\lrs3_pretrain.csv')

# OVRL, SIG, BAK, P808_MOS distribution
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# total OVRL
axes[0, 0].hist(df['OVRL'], bins=50, color='purple', alpha=0.7)
axes[0, 0].set_title('Total OVRL distribution', fontsize=16)
axes[0, 0].set_xlabel('OVRL', fontsize=16)
axes[0, 0].set_ylabel('Count', fontsize=16)

# total SIG
axes[0, 1].hist(df['SIG'], bins=50, color='red', alpha=0.7)
axes[0, 1].set_title('Total SIG distribution', fontsize=16)
axes[0, 1].set_xlabel('SIG', fontsize=16)
axes[0, 1].set_ylabel('Count', fontsize=16)

# total BAK
axes[1, 0].hist(df['BAK'], bins=50, color='blue', alpha=0.7)
axes[1, 0].set_title('Total BAK distribution', fontsize=16)
axes[1, 0].set_xlabel('BAK', fontsize=16)
axes[1, 0].set_ylabel('Count', fontsize=16)

# total P808_MOS
axes[1, 1].hist(df['P808_MOS'], bins=50, color='green', alpha=0.7)
axes[1, 1].set_title('Total P808_MOS distribution', fontsize=16)
axes[1, 1].set_xlabel('P808_MOS', fontsize=16)
axes[1, 1].set_ylabel('Count', fontsize=16)

plt.tight_layout()
plt.show()

# SIG for the 10% of samples with the lowest OVRL
df_sorted_by_OVRL = df.nsmallest(int(len(df) * 0.1), 'OVRL')
plt.figure(figsize=(7, 5))
plt.hist(df_sorted_by_OVRL['SIG'], bins=50, color='red', alpha=0.7)
plt.title('Distribution of SIG for the 10% lowest OVRL', fontsize=16)
plt.xlabel('SIG', fontsize=16)
plt.ylabel('Count', fontsize=16)
plt.show()

# BAK for the 10% of samples with the lowest OVRL
plt.figure(figsize=(7, 5))
plt.hist(df_sorted_by_OVRL['BAK'], bins=50, color='blue', alpha=0.7)
plt.title('Distribution of BAK for the 10% lowest OVRL', fontsize=16)
plt.xlabel('BAK', fontsize=16)
plt.ylabel('Count', fontsize=16)
plt.show()
