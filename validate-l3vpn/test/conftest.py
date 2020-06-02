
def pytest_addoption(parser):
    parser.addoption("--all", action="store_true", help="run all combinations")
    parser.addoption("--scenario_fail_fabric_node", action="store_true", help="Run fabric fail node scenario")
    parser.addoption("--scenario_fail_fabric_link", action="store_true", help="Run fabric fail link scenario")
    parser.addoption("--scenario_fail_service", action="store_true", help="Run service fail scenario")