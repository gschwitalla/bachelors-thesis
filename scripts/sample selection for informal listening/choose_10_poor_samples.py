import pandas as pd
import numpy as np
import paramiko
from scp import SCPClient
import argparse
import subprocess

remote_address = 'sppc25.informatik.uni-hamburg.de'
username = '8schwita'
local_destination = 'G:\\Uni\\Git\\bachelors-thesis\\samples\\LRS3_lowest_1%_SIG\\'

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
    input_csv_file = 'G:\\Uni\\Git\\bachelors-thesis\\evaluation_results\\LRS3\\DNSMOS\\lrs3_pretrain.csv'
    df = pd.read_csv(input_csv_file)

    # Ensure the SIG column is numeric
    df['SIG'] = pd.to_numeric(df['SIG'], errors='coerce')

    # Get cutoff SIG value
    cutoff_value = np.percentile(df['SIG'].dropna(), 0.2)

    # Get samples with SIG below cutoff
    bottom_10_percent_df = df[df['SIG'] <= cutoff_value]

    # Choose 10 random filenames from previous samples
    random_samples = bottom_10_percent_df.sample(n=10, random_state=19)

    ssh_client = create_ssh_client(remote_address, username, password)

    scp_client = SCPClient(ssh_client.get_transport())

    # Download files via scp
    try:
        for index, row in random_samples.iterrows():
            filename = row['filename']
            ovr_score = row['SIG']
            local_file = f"{local_destination}/{ovr_score}_{filename.split('/')[-1]}"
            try:
                scp_client.get(filename, local_file)
                print(f"Successfully downloaded: {filename} (SIG: {ovr_score})")
            except subprocess.CalledProcessError as e:
                print(f"Failed to download: {filename}. Error: {e}")

    finally:
        scp_client.close()
        ssh_client.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download 10 random LRS3 samples with a poor SIG score (bottom 1%)')
    parser.add_argument('password', help='Remote server password')

    args = parser.parse_args()

    main(args.password)
