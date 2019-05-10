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

from jnpr.junos.utils.config import Config
from jnpr.junos import Device
import configuring.templates.l2circuit_config_vars_remote as define_vars
from lxml import etree
import re

def conf_l2circuit_service_remote(hostname, remotehost,username, password, interface):
    conf_file = "configuring/templates/l2circuit-service-remote.conf"
    current_dict = define_vars.config_vars

    def replace_value_with_definition(key_to_find, definition):
        for key in current_dict.keys():
            if key == key_to_find:
                current_dict[key] = definition

    dev = Device(host=remotehost, user=username, passwd=password).open()
    rid_output = dev.rpc.get_route_summary_information({'format':'text'})
    index = int(re.search(r'Router\sID:',str(etree.tostring(rid_output))).start())+6
    rid= str(etree.tostring(rid_output)[index:(index+14)], 'UTF-8').strip(' \n')
    replace_value_with_definition('interface', interface)
    replace_value_with_definition('remote_loopback', rid)
    config_vars = current_dict
    dev.close()

    dev = Device(host=hostname, user=username, passwd=password).open()
    with Config(dev, mode='exclusive') as cu:
        cu.load(template_path=conf_file, template_vars=config_vars, merge=True)
        print (cu.diff())
        cu.commit()

    dev.close()
