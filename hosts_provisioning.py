# -*- coding: utf-8 -*-
"""
* Author : Juniper Networks Advanced Services
* Version : v1.0
* Platform : MX series
* JUNOS Release : 17.1 and above
* Description : The script is based on PyEZ for JUNOS SQT automation
*
* Revision History:
* 1.0 04/05/2019 - initial Beta version, Author: LIU Tao
*
"""
#!/usr/bin/python3

import sys
from getpass import getpass
import configuring.conf_l2vpn_service_local as l2vpn_local
import configuring.conf_l2vpn_service_remote as l2vpn_remote
import configuring.conf_l2circuit_service_local as l2circuit_local
import configuring.conf_l2circuit_service_remote as l2circuit_remote
import configuring.service_groups_apply as group_apply
import checking.check_l2vpn as cl2
import checking.check_l2circuit as cc

local_hostname = input("Local PE's Hostname: ")
remote_hostname = input("Remote PE's Hostname: ")
junos_username = input("Junos device username: ")
junos_password = getpass("Junos device password: ")
# local_pe_interface = input("Local PE's Interface : ")
# remote_pe_interface = input("Remote PE's Interface : ")
local_pe_interface = 'ge-2/3/8'
remote_pe_interface = 'xe-2/0/2'

def l2vpn_service():
    Layer2_vpn='''
    * Provisioning Layer 2 VPN on local PE and remote PE under groups of L2vpn-services ;
    * And apply the Layer 2 VPN service group on the routers as well.
    '''
    print(Layer2_vpn)
    l2vpn_group = 'set apply-groups L2vpn-services'
    l2vpn_local.conf_l2vpn_service_local(local_hostname, junos_username, junos_password, local_pe_interface)
    l2vpn_remote.conf_l2vpn_service_remote(remote_hostname, junos_username, junos_password, remote_pe_interface)
    group_apply.groups_apply_by_cli(local_hostname,junos_username,junos_password,l2vpn_group)
    group_apply.groups_apply_by_cli(remote_hostname,junos_username,junos_password,l2vpn_group)
    Layer2_vpn_status = '''\n
    * Configuration provisioning completed on Layer 2 VPN services !
    * Starting to check the status of all Layer 2 VPN services ... ...\n'''
    cl2.check_l2vpn(local_hostname,junos_username,junos_password)
    cl2.check_l2vpn(remote_hostname,junos_username,junos_password)

def l2circuit_service():
    Layer2_circuit='''
    * Provisioning Layer 2 Circuit on local PE and remote PE under groups of L2circuit-services ;
    * And apply the Layer 2 Circuit service group on the routers as well.
    '''
    print(Layer2_circuit)
    l2circuit_group = 'set apply-groups L2circuit-services'
    l2circuit_local.conf_l2circuit_service_local(local_hostname,remote_hostname, junos_username, junos_password, local_pe_interface)
    l2circuit_remote.conf_l2circuit_service_remote(remote_hostname,local_hostname, junos_username, junos_password, remote_pe_interface)
    group_apply.groups_apply_by_cli(local_hostname,junos_username,junos_password,l2circuit_group)
    group_apply.groups_apply_by_cli(remote_hostname,junos_username,junos_password,l2circuit_group)
    Layer2_vpn_status = '''\n
    * Configuration provisioning completed on Layer 2 Circuit services !
    * Starting to check the status of all Layer 2 Circuit services ... ...\n'''
    cc.check_l2circuit(local_hostname,junos_username,junos_password)
    cc.check_l2circuit(remote_hostname,junos_username,junos_password)

l2circuit_service()
# ci.check_dev_inventory(local_hostname, junos_username, junos_password)