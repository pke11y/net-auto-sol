

def build_vrf_pe(vrfdata):
    """ Build a list of items that can be used to develop a DOT file graph
    """
    routes = vrfdata[0]
    nodes = vrfdata[1]
    vrf_pe = []
    for prefix, route_d in routes.items():
        nexthop = route_d['index'][1]['next_hop']
        vrf_pe.append(['vrf', get_nodename(nodes, nexthop)])
    return vrf_pe

def printdot(edges):
    """ Create string from list elements in .DOT file format"""
    edge_str = ''
    for edge in edges:
        edge_str += '{} -- {};\n'.format(edge[0],edge[1])
    return edge_str

def get_nodename(nodes, nexthop):
    """ Internal function to get the node name from the VRF route nexthop
    """
    name = ''
    for pename, pe in nodes['pe'].items():
        if pe['routerid'] == nexthop:
            name = pename
        else:
            name = nexthop
    return name

class FilterModule(object):
    def filters(self):
        return {"build_vrf_pe": build_vrf_pe,
                "printdot": printdot}