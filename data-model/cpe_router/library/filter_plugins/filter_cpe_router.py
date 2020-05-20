#
# 
#
from ipaddress import IPv4Address, IPv4Network

def get_service_cpe_routers(services):
    """ Return a dict of CPE routers
    """
    cpe_routers = {}
    for vpn_type, vpn_data in services.items():
        if vpn_type == 'l3vpn':
            for service_type, service_vrfs in vpn_data.items():
                for vrf in service_vrfs:
                    for site in vrf['sites']:
                        for cpe_name, cpe_data in site['nodes'].items():
                            interfaces = {}
                            if cpe_name in cpe_routers.keys():
                                cpe_data                = cpe_routers[cpe_name]
                                interfaces              = cpe_routers[cpe_name].get('interfaces')
                            
                            if service_type == 'wan':
                                cpe_data['asn']         = vrf['remote_asn']
                                cpe_data['customer']    = vrf['customer']
                            elif service_type == 'internet':
                                cpe_data['asn']         = site['asn']
                                cpe_data['customer']    = site['customer']

                            for link in site['links']:
                                if link['a_end'] == cpe_name:                                     
                                    intf_name = link['a_end_intf']
                                    host_ip = str(IPv4Network(link['wan_ip_pfx'])[1])
                                    interfaces[intf_name] = dict(ip=host_ip, cost=5, service_type=service_type, remote_node=link['b_end'], remote_intf=link['b_end_intf'])
                                    cpe_data['interfaces'] = interfaces
                                    cpe_routers[cpe_name] = cpe_data                           
    return cpe_routers


class FilterModule(object):
    def filters(self):
        return {"get_service_cpe_routers": get_service_cpe_routers}