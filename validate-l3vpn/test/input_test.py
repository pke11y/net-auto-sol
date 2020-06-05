#!/usr/bin/env python3
# 
# ## Test Classes to validate the input data-models 
import pytest
from ipaddress import IPv4Address

def node_fabric_data(fname):
    """ Load the 'fabric.yml' data model  and return the 'nodes' data """
    import yaml
    _fabric_nodes = {}
    with open(fname) as f:
        fabric = yaml.load(f, Loader=yaml.FullLoader)
    for node_dict in fabric['nodes'].values():
        _fabric_nodes.update(**node_dict)
    return _fabric_nodes

def node_fabric_list(fname):
    """ Call the node fabric data function and return a list of dict objects that pytest can iterate through 
        Return: [{node1}, {node2},..]
    """
    return [{k:v} for k, v in node_fabric_data(fname).items()]

def fabric_links(fname):
    """ Load the 'fabric.yml' data model  and return the 'links' data """
    import yaml
    with open(fname) as f:
        fabric = yaml.load(f, Loader=yaml.FullLoader)
    return fabric['links']

def node_data_as_list(fname):
    """ Load the 'nodes.yml' data model """
    import yaml
    with open(fname) as f:
        services = yaml.load(f, Loader=yaml.FullLoader)
    return [{k:v} for k, v in services['nodes'].items()]

def service_l3vpn_wan_data(fname):
    import yaml
    with open(fname) as f:
        services = yaml.load(f, Loader=yaml.FullLoader)
    return services['services']['l3vpn']['wan']

def service_l3vpn_internet_data(fname):
    import yaml
    with open(fname) as f:
        services = yaml.load(f, Loader=yaml.FullLoader)
    return services['services']['l3vpn']['internet']

def pytest_generate_tests(metafunc):
    # called once per each test function and per test class

    func_arg = metafunc.fixturenames[0]             # get function arg 
    if metafunc.cls.__name__ == 'TestFabric':
        fabric_dict = {}
        if metafunc.config.getoption("scenario_fail_fabric_node"):
            _FABRIC_DM = r'/home/pk/net-auto-sol/validate-l3vpn/test/fabric_fail_node.yml'
        elif metafunc.config.getoption("scenario_fail_fabric_link"):
            _FABRIC_DM = r'/home/pk/net-auto-sol/validate-l3vpn/test/fabric_fail_link.yml'
        else:
            _FABRIC_DM = r'/home/pk/net-auto-sol/validate-l3vpn/data_models/fabric.yml'

        TestFabric.node_file = _FABRIC_DM
        if func_arg == 'node_dict':
            fabric_dict = node_fabric_list(_FABRIC_DM)
        elif func_arg == 'link_dict':
            fabric_dict = fabric_links(_FABRIC_DM)
        
        metafunc.parametrize(
            func_arg, [element for element in fabric_dict]
        )
    elif metafunc.cls.__name__ == 'TestNode':
        _NODE_DM = r'/home/pk/net-auto-sol/validate-l3vpn/data_models/nodes.yml'
        if func_arg == 'node_dict':
            node_list = node_data_as_list(_NODE_DM)
        metafunc.parametrize(func_arg, node_list)
    elif metafunc.cls.__name__ == 'TestWanService':
        _SERV_DM = r'/home/pk/net-auto-sol/validate-l3vpn/data_models/services.yml'
        metafunc.parametrize(func_arg, service_l3vpn_wan_data(_SERV_DM))
    elif metafunc.cls.__name__ == 'TestInternetService':
        _SERV_DM = r'/home/pk/net-auto-sol/validate-l3vpn/data_models/services.yml'
        metafunc.parametrize(func_arg, service_l3vpn_internet_data(_SERV_DM))

class TestFabric:

    node_file = ''

    def test_link_a_end_valid(self, link_dict):
        a_end_node = link_dict['a_end']
        node_data = node_fabric_data(TestFabric.node_file)
        assert a_end_node in node_data

    def test_link_a_end_intf_exists(self, link_dict):
        assert 'a_end_intf' in link_dict

    def test_link_b_end_valid(self, link_dict):
        b_end_node = link_dict['b_end']
        node_data = node_fabric_data(TestFabric.node_file)
        assert b_end_node in node_data

    def test_link_b_end_intf_exists(self, link_dict):
        assert 'b_end_intf' in link_dict
    
    def test_link_ip_pfx_exists(self, link_dict):
        assert 'link_ip_pfx' in link_dict

    def test_link_cost_exists(self, link_dict):
        assert 'cost' in link_dict            
    
    def test_routerid_validIPv4(self, node_dict):
        node_data = list(node_dict.values())[0]
        assert IPv4Address(node_data['routerid'])

    def test_mgmt_validIPv4(self, node_dict):
        node_data = list(node_dict.values())[0]
        assert IPv4Address(node_data['mgmt'])

    def test_asn_exists(self, node_dict):
        node_data = list(node_dict.values())[0]
        assert 'asn' in node_data

    def test_asn_integer(self, node_dict):
        node_data = list(node_dict.values())[0]
        assert isinstance(node_data['asn'], int)

class TestNode:

    def test_interfaces_exist(self, node_dict):
        node_data = list(node_dict.values())[0]
        assert len(node_data['interfaces']) > 0

    def test_vrf_exists(self, node_dict):
        node_data = list(node_dict.values())[0]
        assert len(node_data['vrfs']) > 0
    
    def test_routerid_validIPv4(self, node_dict):
        node_data = list(node_dict.values())[0]
        assert IPv4Address(node_data['routerid'])

    def test_mgmt_validIPv4(self, node_dict):
        node_data = list(node_dict.values())[0]
        assert IPv4Address(node_data['mgmt'])

    def test_asn_exists(self, node_dict):
        node_data = list(node_dict.values())[0]
        assert 'asn' in node_data

    def test_asn_integer(self, node_dict):
        node_data = list(node_dict.values())[0]
        assert isinstance(node_data['asn'], int)

    def test_type_valid(self, node_dict):
        types = ['pe', 'p', 'ce']
        node_data = list(node_dict.values())[0]
        assert node_data['type'] in types

    def test_is_rr_valid(self, node_dict):
        rr = [True, False]
        node_data = list(node_dict.values())[0]
        assert node_data['is_rr'] in rr        

class TestWanService:

    def test_vrf_name_exists(self, vrf_dict):
        assert 'vrf_name' in vrf_dict
    
    def test_vrf_description_exists(self, vrf_dict):
        assert 'description' in vrf_dict 

    def test_vrf_state_valid(self, vrf_dict):
        states = ['touch', 'absent', 'started', 'stopped']
        assert vrf_dict['state'] in states 

    def test_vrf_customer_exists(self, vrf_dict):
        assert 'customer' in vrf_dict

    def test_vrf_remote_asn_exists(self, vrf_dict):
        assert 'remote_asn' in vrf_dict

    def test_vrf_remote_asn_valid(self, vrf_dict):
        remote_asn = vrf_dict['remote_asn']
        assert int(remote_asn) != 65001

    def test_vrf_rd_valid(self, vrf_dict):
        rd = vrf_dict['rd']
        assert int(rd)      

    def test_vrf_rt_import_exists(self, vrf_dict):
        import_list = vrf_dict['rt_import']
        assert len(import_list) > 0

    def test_vrf_rt_export_exists(self, vrf_dict):
        export_list = vrf_dict['rt_export']
        assert len(export_list) > 0

    def test_vrf_sites_exist(self, vrf_dict):
        sites = vrf_dict['sites']
        assert len(sites) > 0

    def test_vrf_sites_nodes_exist(self, vrf_dict):
        for site in vrf_dict['sites']:
            nodes = site['nodes']
            assert len(nodes) > 0

    def test_vrf_sites_links_exist(self, vrf_dict):
        for site in vrf_dict['sites']:
            links = site['links']
            assert len(links) > 0        

class TestInternetService:

    def test_vrf_name_exists(self, vrf_dict):
        assert 'vrf_name' in vrf_dict
    
    def test_vrf_description_exists(self, vrf_dict):
        assert 'description' in vrf_dict 

    def test_vrf_state_valid(self, vrf_dict):
        states = ['touch', 'absent', 'started', 'stopped']
        assert vrf_dict['state'] in states 
    
    def test_vrf_rd_valid(self, vrf_dict):
        rd = vrf_dict['rd']
        assert int(rd)      

    def test_vrf_rt_import_exists(self, vrf_dict):
        import_list = vrf_dict['rt_import']
        assert len(import_list) > 0

    def test_vrf_rt_export_exists(self, vrf_dict):
        export_list = vrf_dict['rt_export']
        assert len(export_list) > 0    

    def test_vrf_sites_exist(self, vrf_dict):
        sites = vrf_dict['sites']
        assert len(sites) > 0

    def test_vrf_sites_nodes_exist(self, vrf_dict):
        for site in vrf_dict['sites']:
            nodes = site['nodes']
            assert len(nodes) > 0

    def test_vrf_sites_links_exist(self, vrf_dict):
        for site in vrf_dict['sites']:
            links = site['links']
            assert len(links) > 0  

    def test_vrf_customer_exists(self, vrf_dict):
        for site in vrf_dict['sites']:
            assert 'customer' in site

    def test_vrf_remote_asn_exists(self, vrf_dict):
        for site in vrf_dict['sites']:
            assert 'asn' in site

    def test_vrf_remote_asn_valid(self, vrf_dict):
        for site in vrf_dict['sites']:
            remote_asn = site['asn']
            assert int(remote_asn) != 65001