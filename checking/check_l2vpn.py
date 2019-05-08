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

from jnpr.junos import Device
from jnpr.junos.factory.factory_loader import FactoryLoader
import yaml

def check_l2vpn(router_name, username, password):

    with open("checking/sensors/l2vpn_sensor.yml", 'r') as tvs:
        globals().update(FactoryLoader().load(yaml.load(tvs)))
    with Device(host=router_name, user=username, password=password, gather_facts=False) as dev:
        print(dev.facts['hostname'])
        l2vpn = L2vpnConnectionTable(dev)
        l2vpn.get()
        for item in l2vpn:
            print(item + '\n')
