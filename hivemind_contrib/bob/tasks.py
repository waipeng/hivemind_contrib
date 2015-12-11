from fabric.api import env, puts, task
from fabric.utils import error
from prettytable import PrettyTable

from hivemind_contrib.nova import client as nova_client

from .server_tests import run as run_server_tests

from pprint import pprint

@task
def check():
    """Check if instance is 'healthy'
    """
    if not env.instance_uuid:
        error("No instance_uuid specified.")
    nc = nova_client()
    server = nc.servers.get(env.instance_uuid)

    print "Running tests for instance %s" % (server.id)
    testresult = run_server_tests(server)

    print "Tests: %s Errors: %s Failures: %s Skipped: %s" % (
            testresult.testsRun,
            len(testresult.errors),
            len(testresult.failures),
            len(testresult.skipped))

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
    table.add_row(["OS-EXT-STS:task_state", server._info["OS-EXT-STS:task_state"]])
    table.add_row(["OS-EXT-STS:vm_state", server._info["OS-EXT-STS:vm_state"]])
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

        # reasonable guess
        tapdev = 'tap'+interface.port_id[:11]
        interfacetable.add_row(["Tap Name", tapdev])

        print interfacetable

    print "Listing Security Groups"
    secgroups = server.list_security_group()

    for secgroup in secgroups:
        secgrouptable = PrettyTable(['Security Group ID', 'Name', 'Proto', 'From Port', 'To Port'])
        for rule in secgroup.rules:
            secgrouptable.add_row([secgroup.id, secgroup.name,
                rule['ip_protocol'], rule['from_port'], rule['to_port']])

        print secgrouptable
