# import paramiko
# import requests
# import json
from flask import Flask, request

# def connect_to_server(hostname, username, password):
#     ssh_client = paramiko.SSHClient()
#     ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh_client.connect(hostname=hostname, username=username, password=password)
#     return ssh_client

# ssh_client = connect_to_server('ip', 'username', 'password')

# stdin, stdout, stderr = ssh_client.exec_command('echo hello there')
# print(stdout.read().decode())


# def send_json_data(url, json_data):
#     headers = {'Content-type': 'application/json'}
#     response = requests.post(url, data=json.dumps(json_data), headers=headers)
#     return response

import requests

server_ip = '4.246.191.213'
url = f'http://{server_ip}'

response = requests.get(url)
if response.status_code == 200:
    # process the response
    data = response
    print(data)
else:
    print(f'Request failed with status code {response.status_code}')

app = Flask(__name__)

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json
    # Do something with the data
    return 'Data received successfully'

if __name__ == '__main__':
    app.run(host=server_ip, port=5000)