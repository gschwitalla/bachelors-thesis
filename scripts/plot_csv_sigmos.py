import pandas as pd
import matplotlib.pyplot as plt

# CSV-Datei laden
df = pd.read_csv('G:\\Uni\\Git\\bachelors-thesis\\evaluation_results\\LRS3\\SIGMOS\\pretrain-results.csv')

# Erstellen von Subplots für die Score-Verteilungen
fig, axes = plt.subplots(3, 3, figsize=(18, 15))

# MOS_COL
axes[0, 0].hist(df['MOS_COL'], bins=50, color='purple', alpha=0.7)
axes[0, 0].set_title('Distribution of MOS_COL', fontsize=15)
axes[0, 0].set_xlabel('MOS_COL', fontsize=12)
axes[0, 0].set_ylabel('Count', fontsize=12)

# MOS_DISC
axes[0, 1].hist(df['MOS_DISC'], bins=50, color='red', alpha=0.7)
axes[0, 1].set_title('Distribution of MOS_DISC', fontsize=15)
axes[0, 1].set_xlabel('MOS_DISC', fontsize=12)
axes[0, 1].set_ylabel('Count', fontsize=12)

# MOS_LOUD
axes[0, 2].hist(df['MOS_LOUD'], bins=50, color='orange', alpha=0.7)
axes[0, 2].set_title('Distribution of MOS_LOUD', fontsize=15)
axes[0, 2].set_xlabel('MOS_LOUD', fontsize=12)
axes[0, 2].set_ylabel('Count', fontsize=12)

# MOS_NOISE
axes[1, 0].hist(df['MOS_NOISE'], bins=50, color='blue', alpha=0.7)
axes[1, 0].set_title('Distribution of MOS_NOISE', fontsize=15)
axes[1, 0].set_xlabel('MOS_NOISE', fontsize=12)
axes[1, 0].set_ylabel('Count', fontsize=12)

# MOS_REVERB
axes[1, 1].hist(df['MOS_REVERB'], bins=50, color='cyan', alpha=0.7)
axes[1, 1].set_title('Distribution of MOS_REVERB', fontsize=15)
axes[1, 1].set_xlabel('MOS_REVERB', fontsize=12)
axes[1, 1].set_ylabel('Count', fontsize=12)

# MOS_SIG
axes[1, 2].hist(df['MOS_SIG'], bins=50, color='magenta', alpha=0.7)
axes[1, 2].set_title('Distribution of MOS_SIG', fontsize=15)
axes[1, 2].set_xlabel('MOS_SIG', fontsize=12)
axes[1, 2].set_ylabel('Count', fontsize=12)

# MOS_OVRL
axes[2, 0].hist(df['MOS_OVRL'], bins=50, color='green', alpha=0.7)
axes[2, 0].set_title('Distribution of MOS_OVRL', fontsize=15)
axes[2, 0].set_xlabel('MOS_OVRL', fontsize=12)
axes[2, 0].set_ylabel('Count', fontsize=12)

# Leere Subplots entfernen
axes[2, 1].axis('off')
axes[2, 2].axis('off')

plt.tight_layout()
plt.show()

# Berechnung der unteren 10 % der MOS_OVRL-Werte
df_low_OVRL = df.nsmallest(int(len(df) * 0.1), 'MOS_OVRL')

# Verteilung von MOS_SIG für die 10 % niedrigsten MOS_OVRL
plt.figure(figsize=(7, 5))
plt.hist(df_low_OVRL['MOS_SIG'], bins=50, color='magenta', alpha=0.7)
plt.title('Distribution of MOS_SIG for the 10% lowest MOS_OVRL', fontsize=15)
plt.xlabel('MOS_SIG', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.show()

# Verteilung von MOS_NOISE für die 10 % niedrigsten MOS_OVRL
plt.figure(figsize=(7, 5))
plt.hist(df_low_OVRL['MOS_NOISE'], bins=50, color='blue', alpha=0.7)
plt.title('Distribution of MOS_NOISE for the 10% lowest MOS_OVRL', fontsize=15)
plt.xlabel('MOS_NOISE', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.show()
