# Test Classes to validate the input data-models 
import pytest
from ipaddress import IPv4Address

# nodes = [, ]
# scenarios = ['scenario1', 'scenario2']
# scenario1 = ("basic", dict(name='node1', routerid=111))
# scenario2 = ("advanced", dict(name='node2', routerid=222))
_NODE_DM_FILE = r'/home/pk/net-auto-sol/validate-l3vpn/data_models/nodes.yml'

def node_data_as_list(nodefile=_NODE_DM_FILE):
    import yaml
    with open(nodefile) as f:
        services = yaml.load(f, Loader=yaml.FullLoader)
    return [{k:v} for k, v in services['nodes'].items()]

def node_fabric_data(fname):
    import yaml
    _fabric_nodes = {}
    with open(fname) as f:
        fabric = yaml.load(f, Loader=yaml.FullLoader)
    for node_dict in fabric['nodes'].values():
        _fabric_nodes.update(**node_dict)
    return _fabric_nodes

def node_fabric_list(fname):
    return [{k:v} for k, v in node_fabric_data(fname).items()]

def pytest_generate_tests(metafunc):
    # called once per each test function
    # funcarglist = metafunc.cls.params[metafunc.function.__name__]
    # print("\nfuncarglist: ",funcarglist)
    # argnames = sorted(funcarglist[0])
    # print("\nargnames: ",argnames)
    if metafunc.cls.__name__ == 'TestTempFabric':
        if metafunc.config.getoption("scenario_fail_fabric"):
            _FABRIC_DM = r'/home/pk/net-auto-sol/validate-l3vpn/test/fabric_scenario1.yml'
        else:
            _FABRIC_DM = r'/home/pk/net-auto-sol/validate-l3vpn/data_models/fabric.yml'
        nodedict = node_fabric_list(_FABRIC_DM)
        metafunc.parametrize(
            'node_dict', [node for node in nodedict]
        )     

    

# class TestTempNode:
#     # params = {
#     #     "test_rid": [dict(name='node1', routerid=111), dict(name='node2', routerid=222)],
#     #     "test_node": [dict(name='node3', routerid=333), dict(name='node4', routerid=444)],
#     # }

#     def test_rid(self, node_dict):
#         node_data = list(node_dict.values())[0]
#         print(node_data['routerid'])
#         assert IPv4Address(node_data['mgmt'])
    
#     def test_node(self, node_dict):
#         node_data = list(node_dict.values())[0]
#         print(node_data['mgmt'])
#         assert IPv4Address(node_data['mgmt'])

class TestTempFabric:
    # params = {
    #     "test_rid": [dict(name='node1', routerid=111), dict(name='node2', routerid=222)],
    #     "test_node": [dict(name='node3', routerid=333), dict(name='node4', routerid=444)],
    # }
    params = ["nodes", "links"]

    def test_rid(self, node_dict):
        node_data = list(node_dict.values())[0]
        assert IPv4Address(node_data['mgmt'])
    
    def test_node(self, node_dict):
        node_data = list(node_dict.values())[0]
        assert IPv4Address(node_data['mgmt'])