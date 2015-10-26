from fabric.api import env, puts, task
from fabric.utils import error
from prettytable import PrettyTable

from hivemind_contrib.nova import client as nova_client

@task
def show():
    """Show information about an instance
    """
    if not env.instance_uuid:
        error("No instance_uuid specified.")
    nc = nova_client()
    server = nc.servers.get(env.instance_uuid)

    table = PrettyTable(["Field", "Value"])
    table.add_row(["Instance ID", server.id])
    table.add_row(["Instance Name", server.name])
    table.add_row(["OS-EXT-SRV-ATTR:host", server._info["OS-EXT-SRV-ATTR:host"]])
    table.add_row(["OS-EXT-SRV-ATTR:instance_name", server._info["OS-EXT-SRV-ATTR:instance_name"]])
    print table

    print "Listing Interfaces"
    interfaces = server.interface_list()
    for interface in interfaces:
        interfacetable = PrettyTable(["Port ID", interface.port_id])
        interfacetable.add_row(["Port State", interface.port_state])
        interfacetable.add_row(["Net ID", interface.net_id])
        interfacetable.add_row(["MAC Address", interface._info["mac_addr"]])
        ip_addresses = ",".join([fip['ip_address'] for fip in
            interface.fixed_ips])
        interfacetable.add_row(["IP Addresses", ip_addresses])

        print interfacetable
