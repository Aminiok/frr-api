import json
import subprocess

class Interface:
    def __init__(self):
        return

    def get_interface_list(self):
        vtysh_command = '''
        show interface brief json
        '''
        return(self.exec_get_vty_command(vtysh_command))
    
    def create_interface(self, data):
        print(data)
        name = data["name"]
        ip = data["ip"]
        description = data["description"]

        if not self.interface_exists(name):
            sys_command = ["ip", "link", "add", name, "type", "dummy"]
            self.exec_sys_command(sys_command)

            vtysh_command = '''
            conf t
            interface %s
            ip address %s
            description %s
            exit
            exit
            write
            ''' % (name, ip, description)
            return(self.exec_set_vty_command(vtysh_command))
        else:
            return('{"result": "Interface exists"}')
    
    def delete_interface(self, name):
        if self.interface_exists(name):
            sys_command = ["ip", "link", "delete", name]
            self.exec_sys_command(sys_command)

            vtysh_command = '''
            conf t
            no interface %s
            exit
            write
            ''' % (name)
            return(self.exec_set_vty_command(vtysh_command))
        else:
            return('{"result": "Interface doesnt exist"}')

    def interface_exists(self, name):
        interface_list = self.get_interface_list()
        for key in interface_list:
            if key == name:
                return True
        return False

    def exec_sys_command(self, cmd):
        try:
            process = subprocess.run(cmd)
            return_value = '{"result": "OK"}'
        except subprocess.CalledProcessError as e:
            print(e)
            return_value = '{"result": "ERROR"}'
        return json.loads(return_value)

    def exec_get_vty_command(self, cmd):
        try:
            process = subprocess.Popen(['vtysh', '-c', cmd], stdout=subprocess.PIPE)
            return_value = process.communicate()[0]
        except subprocess.CalledProcessError as e:
            print(e)
            return_value = '{"result": "ERROR"}'
        return json.loads(return_value) 

    def exec_set_vty_command(self, cmd):
        try:
            process = subprocess.Popen(['vtysh', '-c', cmd], stdout=subprocess.PIPE)
            return_value = process.communicate()[0]
            return_value = '{"result": "OK"}'
        except subprocess.CalledProcessError as e:
            print(e)
            return_value = '{"result": "ERROR"}'
        return json.loads(return_value)