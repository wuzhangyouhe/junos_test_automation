"""
Pythonifier for Route Table/View
"""

from jnpr.junos import Device
from jnpr.junos.factory.factory_loader import FactoryLoader
import yaml

def check_route(router_name, username, password):

    with open("sensors/route_sensor.yml", 'r') as tvs:
        globals().update(FactoryLoader().load(yaml.load(tvs)))
    with Device(host=router_name, user=username, password=password, gather_facts=False) as dev:
        print(dev.facts['hostname'])
        # route = RouteTable(dev)
        routes = RouteSummaryTable(dev)
        # route.get()
        routes.get()
        for item in routes:
            print(item)

check_route('172.16.99.34', 'liutao','mx960-123')
