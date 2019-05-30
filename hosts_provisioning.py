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
import configuring.conf_l3vpn_service_pe1 as l3vpn_pe1
import configuring.conf_l3vpn_service_pe2 as l3vpn_pe2
import configuring.conf_l3vpn_service_pe3 as l3vpn_pe3
import configuring.conf_vpls_service_pe1 as vpls_pe1
import configuring.conf_vpls_service_pe2 as vpls_pe2
import configuring.conf_vpls_service_pe3 as vpls_pe3
import configuring.conf_ngmvpn_service_pe1 as ngmvpn_pe1
import configuring.conf_ngmvpn_service_pe2 as ngmvpn_pe2
import configuring.conf_ngmvpn_service_pe3 as ngmvpn_pe3
import configuring.conf_rosen_service_pe1 as rosen_pe1
import configuring.conf_rosen_service_pe2 as rosen_pe2
import configuring.conf_rosen_service_pe3 as rosen_pe3
import configuring.service_groups_apply as group_apply
import checking.check_l2vpn as cl2
import checking.check_l2circuit as cc
import checking.check_vpls as cv
import checking.check_l3vpn as c3

pe1_hostname = '172.16.99.34' #input(" PE1 Hostname: ")
pe2_hostname = '172.16.99.87' #input(" PE2 Hostname: ")
pe3_hostname = '172.16.99.71' #input(" PE3 Hostname: ")
junos_username = input("Junos device username: ")
junos_password = getpass("Junos device password: ")
# local_hostname = input("Local PE's Hostname: ")
# remote_hostname = input("Remote PE's Hostname: ")
# local_pe_interface = input("Local PE's Interface : ")
# remote_pe_interface = input("Remote PE's Interface : ")
local_pe_interface = 'ge-2/3/8'
remote_pe_interface = 'xe-2/0/2'
pe1_interface = 'ge-2/3/8'
pe1_ce_interface = 'ge-2/3/9'
pe2_interface = 'xe-2/0/2'
pe2_ce_interface = 'xe-2/0/3'
pe3_interface = 'ge-5/1/2'
pe3_ce_interface = 'ge-5/1/3'

def clean_all_services():
    print("\n Clean up all services from provisioning tool ... ")
    rm_all_services = '''
    delete apply-groups L2circuit-services
    delete groups L2circuit-services
    delete apply-groups L2vpn-services
    delete groups L2vpn-services
    delete apply-groups L3vpn-services
    delete groups L3vpn-services
    delete apply-groups Vpls-services
    delete groups Vpls-services
    delete apply-groups Ngmvpn-services
    delete groups Ngmvpn-services
    delete apply-groups Rosen-services
    delete groups Rosen-services
    '''
    group_apply.groups_apply_by_cli(pe1_hostname,junos_username,junos_password,rm_all_services)
    group_apply.groups_apply_by_cli(pe2_hostname,junos_username,junos_password,rm_all_services)
    group_apply.groups_apply_by_cli(pe3_hostname,junos_username,junos_password,rm_all_services)
    print("\n Services from provisioning tools are all deleted ! ")

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
    print("\n Layer 2 circuit services (vlan id range 10-19) provisioning completed ! ")
    Layer2_circuit_status = '''\n
    * Configuration provisioning completed on Layer 2 Circuit services !
    * Starting to check the status of all Layer 2 Circuit services ... ...\n'''
    print(Layer2_circuit_status)
    cc.check_l2circuit(local_hostname,junos_username,junos_password)
    cc.check_l2circuit(remote_hostname,junos_username,junos_password)

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
    print("\n Layer 2 VPN services (vlan id range 20-29) provisioning completed ! ")
    Layer2_vpn_status = '''\n
    * Configuration provisioning completed on Layer 2 VPN services !
    * Starting to check the status of all Layer 2 VPN services ... ...\n'''
    print(Layer2_vpn_status)
    cl2.check_l2vpn(local_hostname,junos_username,junos_password)
    cl2.check_l2vpn(remote_hostname,junos_username,junos_password)

def l3vpn_service():
    Layer3_vpn='''
    * Provisioning Layer 3 VPN on PE1, PE2 and PE3 under groups of L3vpn-services ;
    * And apply the Layer 3 VPN service group on the routers as well.
    '''
    print(Layer3_vpn)
    l3vpn_group = 'set apply-groups L3vpn-services'
    l3vpn_pe1.conf_l3vpn_service_pe1(pe1_hostname, junos_username, junos_password, pe1_interface, pe1_ce_interface)
    l3vpn_pe2.conf_l3vpn_service_pe2(pe2_hostname, junos_username, junos_password, pe2_interface, pe2_ce_interface)
    l3vpn_pe3.conf_l3vpn_service_pe3(pe3_hostname, junos_username, junos_password, pe3_interface, pe3_ce_interface)
    group_apply.groups_apply_by_cli(pe1_hostname,junos_username,junos_password,l3vpn_group)
    group_apply.groups_apply_by_cli(pe2_hostname,junos_username,junos_password,l3vpn_group)
    group_apply.groups_apply_by_cli(pe3_hostname,junos_username,junos_password,l3vpn_group)
    print("\n Layer 3 VPN services (vlan id range 30-39) provisioning completed ! ")
    Layer3_vpn_status = '''\n
    * Configuration provisioning completed on Layer 3 VPN services !
    * Starting to check the status of all Layer 3 VPN services ... ...\n'''
    print(Layer3_vpn_status)
    c3.check_l3vpn(pe1_hostname,junos_username,junos_password)
    c3.check_l3vpn(pe2_hostname,junos_username,junos_password)
    c3.check_l3vpn(pe3_hostname,junos_username,junos_password)

def vpls_service():
    vpls='''
    * Provisioning BGP VPLS on PE1, PE2 and PE3 under groups of Vpls-services ;
    * And apply the VPLS service group on the routers as well.
    '''
    print(vpls)
    vpls_group = 'set apply-groups Vpls-services'
    vpls_pe1.conf_vpls_service_pe1(pe1_hostname, junos_username, junos_password, pe1_interface, pe1_ce_interface)
    vpls_pe2.conf_vpls_service_pe2(pe2_hostname, junos_username, junos_password, pe2_interface, pe2_ce_interface)
    vpls_pe3.conf_vpls_service_pe3(pe3_hostname, junos_username, junos_password, pe3_interface, pe3_ce_interface)
    group_apply.groups_apply_by_cli(pe1_hostname,junos_username,junos_password,vpls_group)
    group_apply.groups_apply_by_cli(pe2_hostname,junos_username,junos_password,vpls_group)
    group_apply.groups_apply_by_cli(pe3_hostname,junos_username,junos_password,vpls_group)
    print("\n VPLS services (vlan id range 40-49) provisioning completed ! ")
    vpls_status = '''\n
    * Configuration provisioning completed on VPLS services !
    * Starting to check the status of all VPLS services ... ...\n'''
    print(vpls_status)
    cv.check_vpls(pe1_hostname,junos_username,junos_password)
    cv.check_vpls(pe2_hostname,junos_username,junos_password)
    cv.check_vpls(pe3_hostname,junos_username,junos_password)

def ngmvpn_service():
    ngmvpn='''
    * Provisioning BGP NG-MVPN on PE1, PE2 and PE3 under groups of Ngmvpn-services ;
    * And apply the NG-MVPN service group on the routers as well.
    '''
    print(ngmvpn)
    ngmvpn_group = 'set apply-groups Ngmvpn-services'
    ngmvpn_pe1.conf_ngmvpn_service_pe1(pe1_hostname, junos_username, junos_password, pe1_interface, pe1_ce_interface)
    ngmvpn_pe2.conf_ngmvpn_service_pe2(pe2_hostname, junos_username, junos_password, pe2_interface, pe2_ce_interface)
    ngmvpn_pe3.conf_ngmvpn_service_pe3(pe3_hostname, junos_username, junos_password, pe3_interface, pe3_ce_interface)
    group_apply.groups_apply_by_cli(pe1_hostname,junos_username,junos_password,ngmvpn_group)
    group_apply.groups_apply_by_cli(pe2_hostname,junos_username,junos_password,ngmvpn_group)
    group_apply.groups_apply_by_cli(pe3_hostname,junos_username,junos_password,ngmvpn_group)
    print("\n NG-MVPN services (vlan id range 50-51) provisioning completed ! ")

def rosen_service():
    rosen='''
    * Provisioning Rosen on PE1, PE2 and PE3 under groups of Rosen-services ;
    * And apply the Rosen Multicast service group on the routers as well.
    '''
    print(rosen)
    rosen_group = 'set apply-groups Rosen-services'
    rosen_pe1.conf_rosen_service_pe1(pe1_hostname, junos_username, junos_password, pe1_interface, pe1_ce_interface)
    rosen_pe2.conf_rosen_service_pe2(pe2_hostname, junos_username, junos_password, pe2_interface, pe2_ce_interface)
    rosen_pe3.conf_rosen_service_pe3(pe3_hostname, junos_username, junos_password, pe3_interface, pe3_ce_interface)
    group_apply.groups_apply_by_cli(pe1_hostname,junos_username,junos_password,rosen_group)
    group_apply.groups_apply_by_cli(pe2_hostname,junos_username,junos_password,rosen_group)
    group_apply.groups_apply_by_cli(pe3_hostname,junos_username,junos_password,rosen_group)
    print("\n Rosen multicast services (vlan id range 52-53) provisioning completed ! ")

clean_all_services()
#vpls_service()
#ngmvpn_service()
#rosen_service()
l3vpn_service()
# l2vpn_service()
# l2circuit_service()