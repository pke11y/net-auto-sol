#
# 
#
from ipaddress import IPv4Address, IPv4Network

def get_service_test_ip(services):
    """ Return a dict  destination IP addresses that should be reachable per service
    """
    service_test_ip = {}
    for vpn_type, vpn_data in services.items():
        if vpn_type == 'l3vpn':
            for service_type, service_vrfs in vpn_data.items():
                for vrf in service_vrfs:
                    vrf_name = vrf['vrf_name']
                    dest_ip_list = []
                    for site in vrf['sites']:
                        for link in site['links']:
                            host_ip = str(IPv4Network(link['wan_ip_pfx'])[2])
                        dest_ip_list.append(host_ip)
                    service_test_ip[vrf_name] = dest_ip_list                          
    return service_test_ip


class FilterModule(object):
    def filters(self):
        return {"get_service_test_ip": get_service_test_ip}