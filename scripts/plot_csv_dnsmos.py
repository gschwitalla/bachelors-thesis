import pandas as pd
import matplotlib.pyplot as plt

# Load CSV file
# df = pd.read_csv('G:\\Uni\\Git\\bachelors-thesis\\evaluation_results\\LRS3\\DNSMOS\\lrs3_pretrain.csv')
df = pd.read_csv('G:\\Uni\\Git\\bachelors-thesis\\evaluation_results\\VoxCeleb2\\DNSMOS\\results_vc2.csv')

# Plot each distribution separately with individual figures

# Total OVRL
plt.figure(figsize=(7, 5))
plt.hist(df['OVRL'], bins=50, color='purple', alpha=0.7)
plt.title('Total OVRL distribution', fontsize=20)
plt.xlabel('OVRL', fontsize=20)
plt.ylabel('Count', fontsize=20)
plt.tick_params(axis='both', labelsize=20)
plt.tight_layout()
plt.show()

# Total SIG
plt.figure(figsize=(7, 5))
plt.hist(df['SIG'], bins=50, color='red', alpha=0.7)
plt.title('Total SIG distribution', fontsize=20)
plt.xlabel('SIG', fontsize=20)
plt.ylabel('Count', fontsize=20)
plt.tick_params(axis='both', labelsize=20)
plt.tight_layout()
plt.show()

# Total BAK
plt.figure(figsize=(7, 5))
plt.hist(df['BAK'], bins=50, color='blue', alpha=0.7)
plt.title('Total BAK distribution', fontsize=20)
plt.xlabel('BAK', fontsize=20)
plt.ylabel('Count', fontsize=20)
plt.tick_params(axis='both', labelsize=20)
plt.tight_layout()
plt.show()

# Total P808_MOS
plt.figure(figsize=(7, 5))
plt.hist(df['P808_MOS'], bins=50, color='green', alpha=0.7)
plt.title('Total P808_MOS distribution', fontsize=20)
plt.xlabel('P808_MOS', fontsize=20)
plt.ylabel('Count', fontsize=20)
plt.tick_params(axis='both', labelsize=20)
plt.tight_layout()
plt.show()

# SIG for the 10% of samples with the lowest OVRL
df_sorted_by_OVRL = df.nsmallest(int(len(df) * 0.1), 'OVRL')
plt.figure(figsize=(7, 5))
plt.hist(df_sorted_by_OVRL['SIG'], bins=50, color='red', alpha=0.7)
plt.title('Distribution of SIG for the 10% lowest OVRL', fontsize=20)
plt.xlabel('SIG', fontsize=20)
plt.ylabel('Count', fontsize=20)
plt.tight_layout()
plt.show()

# BAK for the 10% of samples with the lowest OVRL
plt.figure(figsize=(7, 5))
plt.hist(df_sorted_by_OVRL['BAK'], bins=50, color='blue', alpha=0.7)
plt.title('Distribution of BAK for the 10% lowest OVRL', fontsize=20)
plt.xlabel('BAK', fontsize=20)
plt.ylabel('Count', fontsize=20)
plt.tight_layout()
plt.show()
