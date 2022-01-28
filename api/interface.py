import json
import subprocess
from typing import Optional
from pydantic import BaseModel


class Interface():
    return_value = {"code": 0, "result": ""}
    def __init__(self):
        return

    def get_interface_list(self):
        vtysh_command = '''
        show interface brief json
        '''
        vtysh_command_result = self.exec_get_vty_command(vtysh_command)
        return(json.loads(vtysh_command_result))
    
    def create_interface(self, name, description, ip):
        if not self.interface_exists(name):
            sys_command = ["ip", "link", "add", name, "type", "dummy"]
            sys_command_result = self.exec_sys_command(sys_command)
            if sys_command_result == "OK":
                vtysh_command = '''
                conf t
                interface %s
                ip address %s
                description %s
                exit
                exit
                write
                ''' % (name, ip, description)
                vtysh_command_result = self.exec_set_vty_command(vtysh_command)
                if vtysh_command_result == "OK":
                    self.return_value["code"] = 201
                    self.return_value["result"] = "Interface %s created." % name
            else:
                self.return_value["code"] = 500
                self.return_value["result"] = sys_command_result
        else:
            self.return_value["code"] = 409
            self.return_value["result"] = "Interface %s exists." % name
        return(self.return_value)
    
    def delete_interface(self, name):
        if self.interface_exists(name):
            sys_command = ["ip", "link", "delete", name]
            sys_command_result = self.exec_sys_command(sys_command)
            print(sys_command_result)
            if sys_command_result == "OK":
                vtysh_command = '''
                conf t
                no interface %s
                exit
                write
                ''' % (name)
                vtysh_command_result = self.exec_set_vty_command(vtysh_command)
                if vtysh_command_result == "OK":
                    self.return_value["code"] = 410
                    self.return_value["result"] = "Interface %s deleted." % name
            else:
                self.return_value["code"] = 500
                self.return_value["result"] = sys_command_result
        else:
            self.return_value["code"] = 404
            self.return_value["result"] = "Interface %s does not exist" % name
        return(self.return_value)

    def interface_exists(self, name):
        interface_list = self.get_interface_list()
        for key in interface_list:
            if key == name:
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