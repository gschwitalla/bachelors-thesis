import pandas as pd
import numpy as np
import paramiko
from scp import SCPClient
import argparse

remote_address = 'sppc25.informatik.uni-hamburg.de'
username = '8schwita'
local_destination = 'C:\\Dev\\samples\\LRS3_highest_10%_OVRL\\'

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
    input_csv_file = 'C:\\Users\\student\\Documents\\LRS3\\results_trainval.csv'
    df = pd.read_csv(input_csv_file)

    # Ensure the OVRL column is numeric
    df['OVRL'] = pd.to_numeric(df['OVRL'], errors='coerce')

    # Get cutoff OVRL value (bottom 10%)
    cutoff_value = np.percentile(df['OVRL'].dropna(), 10)

    # Get samples with OVRL below cutoff
    bottom_10_percent_df = df[df['OVRL'] <= cutoff_value]

    # Choose 10 random filenames from previous samples
    random_filenames = bottom_10_percent_df['filename'].sample(n=10, random_state=42)

    print(random_filenames.tolist())

    ssh_client = create_ssh_client(remote_address, username, password)

    scp_client = SCPClient(ssh_client.get_transport())

    # Download files via scp
    try:
        for filename in random_filenames:
            local_file = f"{local_destination}/{filename.split('/')[-1]}"
            try:
                scp_client.get(filename, local_file)
                print(f"Successfully downloaded: {filename}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to download: {filename}. Error: {e}")

    finally:
        scp_client.close()
        ssh_client.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description= 'Download 10 random LRS3 samples with a poor OVRL score (bottom 10%)')
    parser.add_argument('password', help='Remote server password')

    args = parser.parse_args()

    main(args.password)
