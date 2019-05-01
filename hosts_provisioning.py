import sys
from getpass import getpass
import configuring.conf_l2vpn_service_local as l2vpn_local
import configuring.conf_l2vpn_service_remote as l2vpn_remote
import configuring.service_groups_apply as group_apply

local_hostname = input("Local PE's Hostname: ")
remote_hostname = input("Remote PE's Hostname: ")
junos_username = input("Junos OS username: ")
junos_password = getpass("Junos OS password: ")
#local_pe_interface = input("Local PE's Interface : ")
#remote_pe_interface = input("Remote PE's Interface : ")
local_if = 'ge-2/3/8'
remote_if = 'xe-2/0/2'

Layer2_vpn='''
Provisioning Layer 2 VPN on local PE and remote PE under groups of L2vpn-services ;
And apply the Layer 2 VPN service group on the routers as well.
'''
print(Layer2_vpn)
l2vpn_group = 'set apply-groups L2vpn-services'
l2vpn_local.conf_l2vpn_servic_local(local_hostname, junos_username, junos_password, local_if)
l2vpn_remote.conf_l2vpn_servic_remote(remote_hostname, junos_username, junos_password, remote_if)
group_apply.groups_apply_by_cli(local_hostname,junos_username,junos_password,l2vpn_group)
group_apply.groups_apply_by_cli(remote_hostname,junos_username,junos_password,l2vpn_group)

