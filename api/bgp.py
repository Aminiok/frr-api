import json
import subprocess

class BGP:
    return_value = {"code": 0, "result": ""}
    def __init__(self):
        return

    def get_bgp_summary(self):
        vtysh_command = '''
        show ip bgp json
        '''
        return(json.loads(self.exec_get_vty_command(vtysh_command)))
    
    def get_bgp_neighbors(self):
        vtysh_command = '''
        show bgp neighbors json
        '''
        return(json.loads(self.exec_get_vty_command(vtysh_command)))
    
    def set_bgp_neighbor(self, peer_address, remote_as):
        if not self.bgp_neighbor_exists(peer_address):
            local_as = self.get_local_as()
            if local_as:
                vtysh_command = '''
                conf t
                router bgp %s
                neighbor %s remote-as %s
                neighbor %s peer-group v4
                exit
                exit
                write
                ''' % (local_as, peer_address, remote_as, peer_address)
                vtysh_command_result = self.exec_set_vty_command(vtysh_command)
                if vtysh_command_result == "OK":
                    self.return_value["code"] = 201
                    self.return_value["result"] = "BGP neighbor %s created." % peer_address
                else:
                    self.return_value["code"] = 500
                    self.return_value["result"] = vtysh_command_result
            else:
                self.return_value["code"] = 500
                self.return_value["result"] = "Local AS number not found"
        else:
            self.return_value["code"] = 409
            self.return_value["result"] = "BGP neighbor %s exists." % peer_address
        return(self.return_value)
    
    def delete_bgp_neighbor(self, peer_address):
        if self.bgp_neighbor_exists(peer_address):
            local_as = self.get_local_as()
            if local_as:
                vtysh_command = '''
                conf t
                router bgp %s
                no neighbor %s
                exit
                exit
                write
                ''' % (local_as, peer_address)
                vtysh_command_result = self.exec_set_vty_command(vtysh_command)
                if vtysh_command_result == "OK":
                    self.return_value["code"] = 410
                    self.return_value["result"] = "BGP neighbor %s deleted." % peer_address
                else:
                    self.return_value["code"] = 500
                    self.return_value["result"] = vtysh_command_result
            else:
                self.return_value["code"] = 500
                self.return_value["result"] = "Local AS number not found"
        else:
            self.return_value["code"] = 404
            self.return_value["result"] = "BGP neighbor %s does not exist" % peer_address
        return(self.return_value)
    
    def get_ip_bgp(self):
        vtysh_command = '''
        show ip bgp json
        '''
        return(self.exec_get_vty_command(vtysh_command))

    def get_local_as(self):
        as_number = ""
        bgp_configuration = json.loads(self.get_ip_bgp())
        if "localAS" in bgp_configuration:
            as_number = bgp_configuration["localAS"]
        return as_number

    def bgp_neighbor_exists(self, address):
        bgp_neighbor_list = self.get_bgp_neighbors()
        for key in bgp_neighbor_list:
            if key == address:
                return True
        return False
    
    def exec_sys_command(self, cmd):
        return_value = "OK"
        try:
            subprocess.check_output(cmd)
        except subprocess.CalledProcessError as e:
            return_value = str(e)
        return(return_value)

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