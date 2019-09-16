

def build_vrf_pe(vrfdata):
    """ Build a list of PE nodes that can be used to develop a DOT file graph for a L3VPN
    """
    routes = vrfdata[0]
    nodes = vrfdata[1]
    routerid = vrfdata[2]
    vrf_pe = []
    pe = []
    for prefix, routedict in routes.items():
        nexthop = routedict['index'][1]['next_hop']
        if nexthop == '0.0.0.0':
            nexthop = routerid
        pename = get_pename(nodes, nexthop)
        if pename in pe:
            continue
        else:
            pe.append(pename)
            vrf_pe.append(['vrf', pename])
    return vrf_pe

def build_pe_cpe(hostdata):
    """ Build a list of PE and CPE items that can be used to develop a DOT file graph for a L3VPN
    """
    pe_cpe = []
    cpe = []
    for hostname, hostdict in hostdata.items():

        try:
            bgp_peers = hostdict['bgp_neigh_output']['list_of_neighbors']
            pass
        except:
            continue
        vrf_name = hostdict['vrfs'][0]['name']
        for neighbor in bgp_peers:
            cpe_rid = hostdict['bgp_neigh_output']['vrf'][vrf_name]['neighbor'][neighbor]['router_id']
            cpename = get_cpename(hostdict['nodes'], cpe_rid)
            if not cpename in cpe:
                cpe.append(cpename)
            pe_cpe.append([hostname, cpename])
    return pe_cpe

def printdot(edges):
    """ Create string from list elements in .DOT file format"""
    edge_str = ''
    nodes = set()
    for edge in edges:
        nodes.add('"'+edge[1]+'"')
        edge_str += '"{}" -- "{}"\n'.format(edge[0],edge[1])
    node_str = '\n'.join(nodes)
    return node_str + '\n' + edge_str

def get_pename(nodes, routerid):
    """ Internal function to get the PE name from the VRF route nexthop
    """
    name = ''
    for pename, pe in nodes['pe'].items():
        if pe['routerid'] == routerid:
            name = pename
    return name

def get_cpename(nodes, routerid):
    """ Internal function to get the CPE name from the VRF route nexthop
    """
    name = ''
    for cpename, cpe in nodes['cpe'].items():
        if cpe['routerid'] == routerid:
            name = cpename
    return name

class FilterModule(object):
    def filters(self):
        return {"build_vrf_pe": build_vrf_pe,
                "printdot": printdot,
                "build_pe_cpe": build_pe_cpe}