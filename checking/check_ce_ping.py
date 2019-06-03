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
from lxml import etree

def check_ce_ping(router_name, username, password, dest_ip):

    with Device(host=router_name, user=username, password=password, gather_facts=False) as dev:
        test_ping =dev.rpc.ping(host=dest_ip)
        print (etree.tostring(test_ping))

