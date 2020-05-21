#
# 
#
from ipaddress import IPv4Address, IPv4Network

def get_service_test_ip(services):
    """ Parse the service data model to extract the PE IP addresses that should be reachable for all CPE's
        Return a dict destination IP addresses per service/vrf
        Key: vrf_name, Value: [dest_ip1, dest_ip2,..]
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

def find_vrfs_with_ip(parsed_vpnv4_routes, ip_prefix, allowed_vrfs=[]):
    """ Get all of the VRF's that have the IP address in the VRF route table 
        
        Return a list of VRF names that have a routing table entry for the 
        List: [vrf_name1, vrf_name2,..]
    """
    all_vrfs = parsed_vpnv4_routes['vrf']
    active_vrfs = []
    prefix = IPv4Network(ip_prefix)
    for vrf, vrf_data in all_vrfs.items():
        for vpnv4_type, vpnv4_data in vrf_data['address_family'].items():
            vrf_name = vpnv4_data['default_vrf']
            if vrf_name in allowed_vrfs:
                continue
            for ip_pfx, ip_pfx_data in vpnv4_data['routes'].items():
                if IPv4Network(ip_pfx) == prefix:
                    active_vrfs.append(vrf_name)
    return active_vrfs

def get_cpe_allowed_vrfs(cpenodes):
    """ Return a dict of CPE routers with a list of remote VRF names they connect to
        {cpe1.pk.lab: [VRF1, VRF2, ..], ..}
    """
    cpe_allowed_vrfs = {}
    for cpe_name, cpe_data in cpenodes.items():
        allowed_vrf_names = []
        for intf_name, intf_data in cpe_data['interfaces'].items():
            allowed_vrf_names.append(intf_data['remote_vrf'])
        cpe_allowed_vrfs[cpe_name] =  allowed_vrf_names                       
    return cpe_allowed_vrfs

class FilterModule(object):
    def filters(self):
        return {"get_service_test_ip": get_service_test_ip,
                "find_vrfs_with_ip": find_vrfs_with_ip,
                "get_cpe_allowed_vrfs":get_cpe_allowed_vrfs}