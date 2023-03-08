import paramiko
import requests
import json

def connect_to_server(hostname, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname, username=username, password=password)
    return ssh_client

ssh_client = connect_to_server('ip', 'username', 'password')

stdin, stdout, stderr = ssh_client.exec_command('echo hello there')
print(stdout.read().decode())


def send_json_data(url, json_data):
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(json_data), headers=headers)
    return response