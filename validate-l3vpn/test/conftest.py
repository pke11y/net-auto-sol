import pytest

def pytest_addoption(parser):
    parser.addoption("--all", action="store_true", help="run all combinations")
    parser.addoption("--scenario_fail_fabric", action="store_true", help="Run fabric fail scenario")
    parser.addoption("--scenario_fail_service", action="store_true", help="Run service fail scenario")


# def pytest_generate_tests(metafunc):
#     if "param1" in metafunc.fixturenames:
#         if metafunc.config.getoption("all"):
#             end = 5
#         else:
#             end = 2
#         metafunc.parametrize("param1", range(end))


# def pytest_generate_tests(metafunc):
#     if "double" in metafunc.fixturenames:
#         metafunc.parametrize("double", ["scenario1", "scenario2"], indirect=True)

# @pytest.fixture()
# def double(request):
#     if request.param == 'scenario1':
#         return [dict(name='s1-node1'), dict(name='s1-node2')]
#     elif request.param == 'scenario2':
#         return [dict(name='s2-node1'), dict(name='s2-node2')]
#     else:
#         raise ValueError("invalid internal test config")