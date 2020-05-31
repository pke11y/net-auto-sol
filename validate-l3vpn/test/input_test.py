# Test Classes to validate the input data-models 
import pytest
from ipaddress import IPv4Address

def node_fabric_data():
    import yaml
    _FABRIC_DIR = r'/home/pk/net-auto-sol/validate-l3vpn/data_models/fabric.yml'
    _fabric_nodes = {}
    with open(_FABRIC_DIR) as f:
        fabric = yaml.load(f, Loader=yaml.FullLoader)
    for node_dict in fabric['nodes'].values():
        _fabric_nodes.update(**node_dict)
    return _fabric_nodes

def node_fabric_list():
    return [{k:v} for k, v in node_fabric_data().items()]

def fabric_links():
    import yaml
    _FABRIC_DIR = r'/home/pk/net-auto-sol/validate-l3vpn/data_models/fabric.yml'
    with open(_FABRIC_DIR) as f:
        fabric = yaml.load(f, Loader=yaml.FullLoader)
    return fabric['links']

class TestFabric:

    @pytest.mark.parametrize('link_dict', fabric_links())
    def test_link_a_end_valid(self, link_dict):
        a_end_node = link_dict['a_end']
        node_data = node_fabric_data()
        assert a_end_node in node_data

    @pytest.mark.parametrize('link_dict', fabric_links())
    def test_link_a_end_intf_exists(self, link_dict):
        assert 'a_end_intf' in link_dict

    @pytest.mark.parametrize('link_dict', fabric_links())
    def test_link_b_end_valid(self, link_dict):
        b_end_node = link_dict['b_end']
        node_data = node_fabric_data()
        assert b_end_node in node_data

    @pytest.mark.parametrize('link_dict', fabric_links())
    def test_link_b_end_intf_exists(self, link_dict):
        assert 'b_end_intf' in link_dict
    
    @pytest.mark.parametrize('link_dict', fabric_links())
    def test_link_ip_pfx_exists(self, link_dict):
        assert 'link_ip_pfx' in link_dict

    @pytest.mark.parametrize('link_dict', fabric_links())
    def test_link_cost_exists(self, link_dict):
        assert 'cost' in link_dict            
    
    @pytest.mark.parametrize('node_dict', node_fabric_list())
    def test_routerid_validIPv4(self, node_dict):
        node_data = list(node_dict.values())[0]
        assert IPv4Address(node_data['routerid'])

    @pytest.mark.parametrize('node_dict', node_fabric_list())
    def test_mgmt_validIPv4(self, node_dict):
        node_data = list(node_dict.values())[0]
        assert IPv4Address(node_data['mgmt'])

    @pytest.mark.parametrize('node_dict', node_fabric_list())
    def test_asn_exists(self, node_dict):
        node_data = list(node_dict.values())[0]
        assert 'asn' in node_data

    @pytest.mark.parametrize('node_dict', node_fabric_list())
    def test_asn_integer(self, node_dict):
        node_data = list(node_dict.values())[0]
        assert isinstance(node_data['asn'], int)

class TestNode:

    def node_data_as_list():
        import yaml
        _NODE_DIR = r'/home/pk/net-auto-sol/validate-l3vpn/data_models/nodes.yml'
        with open(_NODE_DIR) as f:
            services = yaml.load(f, Loader=yaml.FullLoader)
        return [{k:v} for k, v in services['nodes'].items()]

    @pytest.mark.parametrize('node_dict', node_data_as_list())
    def test_interfaces_exist(self, node_dict):
        node_data = list(node_dict.values())[0]
        assert len(node_data['interfaces']) > 0

    @pytest.mark.parametrize('node_dict', node_data_as_list())
    def test_vrf_exists(self, node_dict):
        node_data = list(node_dict.values())[0]
        assert len(node_data['vrfs']) > 0
    
    @pytest.mark.parametrize('node_dict', node_data_as_list())
    def test_routerid_validIPv4(self, node_dict):
        node_data = list(node_dict.values())[0]
        assert IPv4Address(node_data['routerid'])

    @pytest.mark.parametrize('node_dict', node_data_as_list())
    def test_mgmt_validIPv4(self, node_dict):
        node_data = list(node_dict.values())[0]
        assert IPv4Address(node_data['mgmt'])

    @pytest.mark.parametrize('node_dict', node_data_as_list())
    def test_asn_exists(self, node_dict):
        node_data = list(node_dict.values())[0]
        assert 'asn' in node_data

    @pytest.mark.parametrize('node_dict', node_data_as_list())
    def test_asn_integer(self, node_dict):
        node_data = list(node_dict.values())[0]
        assert isinstance(node_data['asn'], int)

    @pytest.mark.parametrize('node_dict', node_data_as_list())
    def test_type_valid(self, node_dict):
        types = ['pe', 'p', 'ce']
        node_data = list(node_dict.values())[0]
        assert node_data['type'] in types

    @pytest.mark.parametrize('node_dict', node_data_as_list())
    def test_is_rr_valid(self, node_dict):
        rr = [True, False]
        node_data = list(node_dict.values())[0]
        assert node_data['is_rr'] in rr        

class TestWanService:

    def service_l3vpn_wan_data():
        import yaml
        _SERV_DIR = r'/home/pk/net-auto-sol/validate-l3vpn/data_models/services.yml'
        with open(_SERV_DIR) as f:
            services = yaml.load(f, Loader=yaml.FullLoader)
        return services['services']['l3vpn']['wan']

    @pytest.mark.parametrize('vrf_dict', service_l3vpn_wan_data())
    def test_vrf_name_exists(self, vrf_dict):
        assert 'vrf_name' in vrf_dict
    
    @pytest.mark.parametrize('vrf_dict', service_l3vpn_wan_data())
    def test_vrf_description_exists(self, vrf_dict):
        assert 'description' in vrf_dict 

    @pytest.mark.parametrize('vrf_dict', service_l3vpn_wan_data())
    def test_vrf_state_valid(self, vrf_dict):
        states = ['touch', 'absent', 'started', 'stopped']
        assert vrf_dict['state'] in states 

    @pytest.mark.parametrize('vrf_dict', service_l3vpn_wan_data())
    def test_vrf_customer_exists(self, vrf_dict):
        assert 'customer' in vrf_dict

    @pytest.mark.parametrize('vrf_dict', service_l3vpn_wan_data())
    def test_vrf_remote_asn_exists(self, vrf_dict):
        assert 'remote_asn' in vrf_dict

    @pytest.mark.parametrize('vrf_dict', service_l3vpn_wan_data())
    def test_vrf_remote_asn_valid(self, vrf_dict):
        remote_asn = vrf_dict['remote_asn']
        assert int(remote_asn) != 65001

    @pytest.mark.parametrize('vrf_dict', service_l3vpn_wan_data())
    def test_vrf_rd_valid(self, vrf_dict):
        rd = vrf_dict['rd']
        assert int(rd)      

    @pytest.mark.parametrize('vrf_dict', service_l3vpn_wan_data())
    def test_vrf_rt_import_exists(self, vrf_dict):
        import_list = vrf_dict['rt_import']
        assert len(import_list) > 0

    @pytest.mark.parametrize('vrf_dict', service_l3vpn_wan_data())
    def test_vrf_rt_export_exists(self, vrf_dict):
        export_list = vrf_dict['rt_export']
        assert len(export_list) > 0

    @pytest.mark.parametrize('vrf_dict', service_l3vpn_wan_data())
    def test_vrf_sites_exist(self, vrf_dict):
        sites = vrf_dict['sites']
        assert len(sites) > 0

    @pytest.mark.parametrize('vrf_dict', service_l3vpn_wan_data())
    def test_vrf_sites_nodes_exist(self, vrf_dict):
        for site in vrf_dict['sites']:
            nodes = site['nodes']
            assert len(nodes) > 0

    @pytest.mark.parametrize('vrf_dict', service_l3vpn_wan_data())
    def test_vrf_sites_links_exist(self, vrf_dict):
        for site in vrf_dict['sites']:
            links = site['links']
            assert len(links) > 0        

class TestInternetService:

    def service_l3vpn_internet_data():
        import yaml
        _SERV_DIR = r'/home/pk/net-auto-sol/validate-l3vpn/data_models/services.yml'
        with open(_SERV_DIR) as f:
            services = yaml.load(f, Loader=yaml.FullLoader)
        return services['services']['l3vpn']['internet']

    @pytest.mark.parametrize('vrf_dict', service_l3vpn_internet_data())
    def test_vrf_name_exists(self, vrf_dict):
        assert 'vrf_name' in vrf_dict
    
    @pytest.mark.parametrize('vrf_dict', service_l3vpn_internet_data())
    def test_vrf_description_exists(self, vrf_dict):
        assert 'description' in vrf_dict 

    @pytest.mark.parametrize('vrf_dict', service_l3vpn_internet_data())
    def test_vrf_state_valid(self, vrf_dict):
        states = ['touch', 'absent', 'started', 'stopped']
        assert vrf_dict['state'] in states 
    
    @pytest.mark.parametrize('vrf_dict', service_l3vpn_internet_data())
    def test_vrf_rd_valid(self, vrf_dict):
        rd = vrf_dict['rd']
        assert int(rd)      

    @pytest.mark.parametrize('vrf_dict', service_l3vpn_internet_data())
    def test_vrf_rt_import_exists(self, vrf_dict):
        import_list = vrf_dict['rt_import']
        assert len(import_list) > 0

    @pytest.mark.parametrize('vrf_dict', service_l3vpn_internet_data())
    def test_vrf_rt_export_exists(self, vrf_dict):
        export_list = vrf_dict['rt_export']
        assert len(export_list) > 0    

    @pytest.mark.parametrize('vrf_dict', service_l3vpn_internet_data())
    def test_vrf_sites_exist(self, vrf_dict):
        sites = vrf_dict['sites']
        assert len(sites) > 0

    @pytest.mark.parametrize('vrf_dict', service_l3vpn_internet_data())
    def test_vrf_sites_nodes_exist(self, vrf_dict):
        for site in vrf_dict['sites']:
            nodes = site['nodes']
            assert len(nodes) > 0

    @pytest.mark.parametrize('vrf_dict', service_l3vpn_internet_data())
    def test_vrf_sites_links_exist(self, vrf_dict):
        for site in vrf_dict['sites']:
            links = site['links']
            assert len(links) > 0  

    @pytest.mark.parametrize('vrf_dict', service_l3vpn_internet_data())
    def test_vrf_customer_exists(self, vrf_dict):
        for site in vrf_dict['sites']:
            assert 'customer' in site

    @pytest.mark.parametrize('vrf_dict', service_l3vpn_internet_data())
    def test_vrf_remote_asn_exists(self, vrf_dict):
        for site in vrf_dict['sites']:
            assert 'asn' in site

    @pytest.mark.parametrize('vrf_dict', service_l3vpn_internet_data())
    def test_vrf_remote_asn_valid(self, vrf_dict):
        for site in vrf_dict['sites']:
            remote_asn = site['asn']
            assert int(remote_asn) != 65001