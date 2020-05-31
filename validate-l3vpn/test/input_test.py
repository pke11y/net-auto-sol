# Test Classes to validate the input data-models 
import pytest
from ipaddress import IPv4Address

# @pytest.fixture
# def fabric_yaml():
#     import yaml
#     _FABRIC_DIR = r'/home/pk/net-auto-sol/validate-l3vpn/data_models/fabric.yml'
#     with open(_FABRIC_DIR) as f:
#         fabric = yaml.load(f)
#     return fabric
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

    __FABRIC_DIR = r"../data_models/fabric.yml"
    __SERV_DIR = r"../data_models/services.yml"
    __INTRA_SERV_DIR = r"../data_models/intra-services.yml"  


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