from click import command
from netmiko import *

device = {
    'device_type': 'cisco_ios',
    'host': '192.168.11.100',
    'username': 'admin',
    'password': 'waf',
    'secret': 'waf'

}
ip = "192.168.11.1"
ssh = ConnectHandler(**device)
ssh.enable()
result = ssh.send_command_timing(
    command_string="""
    configure terminal
     access-list 100 deny ip host %s any 
     end
     show access-lists 100""" % ip)

print(result)
