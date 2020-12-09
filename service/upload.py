from flask import Flask, render_template, request, redirect, url_for
import os
import paramiko
from scp import SCPClient

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/', methods=['POST', 'GET'])
def upload_file():
    if request.form.get('button_1'):
        uploaded_file = request.files['file']
        role = request.form.get('role')

        if role == "owner":
            if uploaded_file.filename in os.listdir(role):
                os.remove(role + "/" + uploaded_file.filename)
                print("Existing same filename in current dictionary, but deleted")
 
            if uploaded_file.filename != '':
                uploaded_file.save(role + "/" + uploaded_file.filename)
                ssh = createSSHClient("csa1.bu.edu", 22, "USERNAME-HERE", "PASSWORD-HERE")
                scp = SCPClient(ssh.get_transport())
                scp.put(role + "/" + uploaded_file.filename, "SIMS/" + role + "/")
                os.remove(role + "/" + uploaded_file.filename)

        elif role == "developer":
            if uploaded_file.filename in os.listdir(role):
                os.remove(role + "/" + uploaded_file.filename)
                print("Existing same filename in current dictionary, but deleted")
                
            if uploaded_file.filename != '':
                uploaded_file.save(role + "/" + uploaded_file.filename)
                ssh = createSSHClient("csa1.bu.edu", 22, "USERNAME-HERE", "PASSWORD-HERE")
                scp = SCPClient(ssh.get_transport())
                scp.put(role + "/" + uploaded_file.filename, "SIMS/" + role + "/")
                os.remove(role + "/" + uploaded_file.filename)

        return redirect(url_for('index'))

    if request.form.get('button_2'):
        role = request.form.get('role2')

        if request.form.get('button_2') and role == "owner":
            name = os.listdir(role)

        elif request.form.get('button_2') and role == "developer":
            name = os.listdir(role)

        # print(name)

        return("<p>" + "</p><p>".join(name) + "</p>")


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host = '0.0.0.0', port = 80)

