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
import configuring.templates.nat_config_vars as define_vars

def conf_nat_service(hostname, username, password, interface, ms_interface):
    conf_file = "configuring/templates/nat-service.conf"
    current_dict = define_vars.config_vars

    def replace_value_with_definition(key_to_find, definition):
        for key in current_dict.keys():
            if key == key_to_find:
                current_dict[key] = definition
    replace_value_with_definition('interface', interface)
    replace_value_with_definition('ms_interface', ms_interface)
    config_vars = current_dict
    dev = Device(host=hostname, user=username, passwd=password).open()

    with Config(dev, mode='private') as cu:
        cu.load(template_path=conf_file, template_vars=config_vars, merge=True)
        print (cu.diff())
        cu.commit()

    dev.close()