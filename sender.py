from paramiko import SSHClient
def send(host: str, files: list, dest: str):
    
    client = SSHClient()
    client.load_system_host_keys()
    client.connect(host)
    sftp = client.open_sftp()

    for file_path in files:
        filename = file_path.split('/')[-1]
        remote_path = f"{dest}/{filename}"
        sftp.put(file_path, remote_path)  
    sftp.close()

    client.close()
    
