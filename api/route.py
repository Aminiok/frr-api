import json
import subprocess

class Route:
    return_value = {"code": 0, "result": ""}
    def __init__(self):
        return

    def get_ip_routes(self):
        vtysh_command = '''
        show ip route json
        '''
        return(json.loads(self.exec_get_vty_command(vtysh_command)))
    
    def set_ip_route(self, network, next_hop):
        if not self.ip_route_exists(network):
            vtysh_command = '''
            conf t
            ip route %s %s
            exit
            write
            ''' % (network, next_hop)
            vtysh_command_result = self.exec_set_vty_command(vtysh_command)
            if vtysh_command_result == "OK":
                self.return_value["code"] = 201
                self.return_value["result"] = "IP route %s %s created." % (network, next_hop)
            else:
                self.return_value["code"] = 500
                self.return_value["result"] = vtysh_command_result
        else:
            self.return_value["code"] = 409
            self.return_value["result"] = "IP route %s %s exists." % (network, next_hop)
        return(self.return_value)
    
    def delete_ip_route(self, network, next_hop):
        if self.ip_route_exists(network):
            vtysh_command = '''
            conf t
            no ip route %s %s
            exit
            write
            ''' % (network, next_hop)
            vtysh_command_result = self.exec_set_vty_command(vtysh_command)
            if vtysh_command_result == "OK":
                self.return_value["code"] = 410
                self.return_value["result"] = "IP route %s %s deleted." % (network, next_hop)
            else:
                self.return_value["code"] = 500
                self.return_value["result"] = vtysh_command_result
        else:
            self.return_value["code"] = 404
            self.return_value["result"] = "IP route %s %s does not exist" % (network, next_hop)
        return(self.return_value)

    def ip_route_exists(self, network):
        ip_route_list = self.get_ip_routes()
        for key in ip_route_list:
            if key == network:
                return True
        return False
    
    def exec_get_vty_command(self, cmd):
        try:
            process = subprocess.Popen(['vtysh', '-c', cmd], stdout=subprocess.PIPE)
            return_value = process.communicate()[0]
        except subprocess.CalledProcessError as e:
            print(e)
            return_value = str(e)
        return(return_value) 

    def exec_set_vty_command(self, cmd):
        try:
            process = subprocess.Popen(['vtysh', '-c', cmd], stdout=subprocess.PIPE)
            return_value = process.communicate()[0]
            return_value = "OK"
        except subprocess.CalledProcessError as e:
            print(e)
            return_value = str(e)
        return(return_value)