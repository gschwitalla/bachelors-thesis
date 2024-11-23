import pandas as pd
import numpy as np
import paramiko
from scp import SCPClient
import argparse
import subprocess

remote_address = 'sppc25.informatik.uni-hamburg.de'
username = '8schwita'
local_destination = 'G:\\Uni\\Git\\bachelors-thesis\\samples\\VoxCeleb2_highest_1%_OVRL\\'

def create_ssh_client(server, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(server, username=user, password=password)
        print(f"Successfully connected to {server}")
    except paramiko.AuthenticationException:
        print("Authentication failed, please verify your credentials")
        return None
    except paramiko.SSHException as sshException:
        print(f"Unable to establish SSH connection: {sshException}")
        return None
    except Exception as e:
        print(f"Operation error: {e}")
        return None
    return client

def main(password):
    # Get CSV file
    input_csv_file = 'G:\\Uni\\Git\\bachelors-thesis\\evaluation_results\\VoxCeleb2\\DNSMOS\\results_vc2.csv'
    df = pd.read_csv(input_csv_file)

    # Ensure the OVRL column is numeric
    df['OVRL'] = pd.to_numeric(df['OVRL'], errors='coerce')

    # Get cutoff OVRL value
    cutoff_value = np.percentile(df['OVRL'].dropna(), 99.9)

    # Get samples with OVRL below cutoff
    top_10_percent_df = df[df['OVRL'] >= cutoff_value]

    # Choose 10 random filenames from previous samples
    random_samples = top_10_percent_df.sample(n=10, random_state=6)

    ssh_client = create_ssh_client(remote_address, username, password)

    scp_client = SCPClient(ssh_client.get_transport())

    # Download files via scp
    try:
        for index, row in random_samples.iterrows():
            filename = row['filename']
            ovr_score = row['OVRL']
            local_file = f"{local_destination}/{ovr_score}_{filename.split('/')[-1]}"
            try:
                scp_client.get(filename, local_file)
                print(f"Successfully downloaded: {filename} (OVRL: {ovr_score})")
            except subprocess.CalledProcessError as e:
                print(f"Failed to download: {filename}. Error: {e}")

    finally:
        scp_client.close()
        ssh_client.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download 10 random LRS3 samples with a poor OVRL score (top 10%)')
    parser.add_argument('password', help='Remote server password')

    args = parser.parse_args()

    main(args.password)
