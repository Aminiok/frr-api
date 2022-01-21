import subprocess
import json
from flask import Flask
from flask import request
from interface import Interface

app = Flask(__name__)

@app.route('/')
def get_all_functions():
    return get_all_functions()

@app.route('/interfaces', methods=["GET", "POST"])
def edit_interface():
    if request.method == "GET":
        interface = Interface()
        return(interface.get_interface_list())
    elif request.method == "POST":
        interface = Interface()
        data = request.json
        return interface.create_interface(data)

@app.route('/interfaces/<name>', methods=["DELETE"])
def delete_interface(name):
    if request.method == "DELETE":
        interface = Interface()
        return interface.delete_interface(name)

@app.route('/bgp-summary')
def get_bgp_summary():
    vtysh_command = '''
    show bgp summary json
    '''
    return exec_command(vtysh_command)

@app.route('/bgp-neighbors')
def get_bgp_neighbors():
    vtysh_command = '''
    show bgp neighbors json
    '''
    return exec_command(vtysh_command)

@app.route('/ip-route')
def get_ip_route():
    vtysh_command = '''
    show ip route json
    '''
    return exec_command(vtysh_command) 

@app.route('/ip-bgp')
def get_ip_bgp():
    vtysh_command = '''
    show ip bgp json
    '''
    return exec_command(vtysh_command)   

    


def exec_command(cmd):
    try:
        process = subprocess.Popen(['vtysh', '-c', cmd], stdout=subprocess.PIPE)
        return_value = process.communicate()[0]
    except subprocess.CalledProcessError as e:
        print(e)
        return_value = "{}"
    return json.loads(return_value)

def get_all_functions():
    functions = {
        "get": [
            "interfaces",
            "bgp-summary",
            "bgp-neighbors",
            "ip-route",
            "ip-bgp"
        ]
    }
    return functions