import json
import subprocess
from tools import Tools

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
        tools = Tools()
        router_mode = tools.get_router_mode()
        if router_mode == "kubernetes":
            local_default_route = self.get_local_default_route()
            route_to_neighbor = "ip route %s %s" % (peer_address+"/32", local_default_route)
        else:
            route_to_neighbor = ""
        if not self.bgp_neighbor_exists(peer_address):
            local_as = self.get_local_as()
            
            if local_as:
                if not self.bgp_peer_group_exists("v4"):
                    self.create_peer_group(local_as)
                vtysh_command = '''
                conf t
                router bgp %s
                neighbor %s remote-as %s
                neighbor %s peer-group v4
                neighbor %s ebgp-multihop 10
                neighbor %s disable-connected-check
                exit
                %s
                exit
                write
                ''' % (local_as, peer_address, remote_as, peer_address, peer_address, peer_address, route_to_neighbor)
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
        tools = Tools()
        router_mode = tools.get_router_mode()
        if router_mode == "kubernetes":
            local_default_route = self.get_local_default_route()
            route_to_neighbor = "ip route %s %s" % (peer_address+"/32", local_default_route)
        else:
            route_to_neighbor = ""
        if self.bgp_neighbor_exists(peer_address):
            local_as = self.get_local_as()
            local_default_route = self.get_local_default_route()
            if local_as:
                vtysh_command = '''
                conf t
                router bgp %s
                no neighbor %s
                exit
                no %s
                exit
                write
                ''' % (local_as, peer_address, route_to_neighbor)
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
    
    def get_local_default_route(self):
        default_route = ""
        vtysh_command = '''
        show ip route 0.0.0.0 json
        '''
        local_route_information = json.loads(self.exec_get_vty_command(vtysh_command))
        for key, value in local_route_information.items():
            if key == "0.0.0.0/0":
                route_value = value[0]
                rotute_next_hop_info = route_value["nexthops"][0]
                default_route = rotute_next_hop_info["ip"]
        return default_route
    
    def create_peer_group(self, local_as):
        vtysh_command = '''
        conf t
        router bgp %s
        neighbor v4 peer-group
        address-family ipv4 unicast
        neighbor v4 prefix-list EXPORT out
        neighbor v4 route-map IMPORT in
        neighbor v4 route-map EXPORT out
        neighbor v4 attribute-unchanged next-hop
        exit
        exit
        exit
        write
        ''' % (local_as)
        vtysh_command_result = self.exec_set_vty_command(vtysh_command)
        return vtysh_command_result

    def bgp_neighbor_exists(self, address):
        bgp_neighbor_list = self.get_bgp_neighbors()
        for key in bgp_neighbor_list:
            if key == address:
                return True
        return False
    
    def bgp_peer_group_exists(self, peer_group_name):
        vtysh_command = '''
        show bgp peer-group json
        '''
        peer_group_list = self.exec_get_vty_command(vtysh_command)
        for key in peer_group_list:
            if key == peer_group_name:
                return True
        return False
    
    def restart_bgp_export_rules(self):
        local_as = self.get_local_as()
        vtysh_command = '''
        conf t
        router bgp %s
        neighbor v4 peer-group
        address-family ipv4 unicast
        neighbor v4 prefix-list EXPORT out
        exit
        exit
        exit
        write
        ''' % (local_as)
        vtysh_command_result = self.exec_set_vty_command(vtysh_command)
        return vtysh_command_result
    
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