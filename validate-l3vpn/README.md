
# Validate and Test MPLS/VPN Services
These playbooks are submissions for exercise 5 as part of the Building Network Automation Solutions course on ipspace.net. They build on the data model developed during exercise 3 and 4.

## Overview
The overall objective of the playbooks is to deploy MPLS infrastructure and internal services onto a service provider IP/MPLS core network to provision and deploy enterprise L3VPN services. 

---
## Logging 
Capability to enable debug logging of facts and results returned from network command operations is supported with the command below. Setting `logging=true` and passing it as an extra variable an runtime allows an operator to switch on/off easily without file manipulation.

`sudo ansible-playbook provision_service.yml -e logging=true`

## Testing 
Unit testing was developed using pytest for the main data models (**node.yml**, **fabric.yml**, **services.yml**).

Failure scenarios were created to test the automation system. These scenarios will load the invalid data models below.

- **fabric_fail_link.yml**: defines the IP/MPLS core infrastructure parameters. 
- **fabric_fail_link.yml**: defines the internal OAM L3VPN service parameters.

Execution of the valid and invalid data models is achieved with the pytest custom commands:

- `pytest -s -q input_test.py`: unit test valid data models 
- `pytest -s -q input_test.py --scenario_fail_fabric_link`: unit test invalid fabric link data model
  - Issue 1: No `link_ip_pfx` in first link
  - Issue 2: Node 'random_node' does not exist in the nodes data
- `pytest -s -q input_test.py --scenario_fail_fabric_node`: unit test invalid fabric node data model
  - Issue 1: `pe2.pk.lab` has an invalid routerid
  - Issue 2: `pe3.pk.lab` has no `asn` 


## Validation
Napalm_validate was used to validate service deployment instead of the assert modules originally used in ex 3/4, as recommended by Ivan. New templates were created for the BGP and interface IP validation files. 

## Automated Testing
GitLab CI was integrated into the solution to support automated execution of unit testing steps. The **.gitlab-ci.yml** in the repository root folder details the stages of execution when a push is made to a GitHub branch. 

- **yamllint**: test all of the data models for valid yaml format and file structure
- **data model test**: unit test (with pytest) the valid data models
- **automation test**: unit test (with pytest) the invalid data models

## Templates
All jinja2 templates are stored in the **templates** folder
- `validate_bgp.j2`: transformation template to create napalm_validation files for BGP neighbours depliyed as part of the L3VPN service
- `validate_interfaces.j2`: transformation template to create napalm_validation files for L3VPN interfaces


## Results
All configuration outputs are stored in the **results** folder.

- **service_validation**: per node napalm_validate files
- **reports**: added napalm compliance validation reports 


## Learnings
- Need to split P and PE routers into separate groups in the inventory fileto avoid conditional checks for service deployment.
- unit tests could be more specific with more time e.g. regex check against hostnames, link ip prefix valid IPv4Network, management and routerid's within specific subnet etc. 
- pytest parametrize and fixture features look like the can solve a lot of unit testing requirements. However, I had to resort to a custom paramterize innvocation using pytest_generate_tests. It provided the control I needed to allow me to run the valid and invalid tests using the same test cases, but different test data. I'm sure there is an easier way to do it, but under the time constraints pytest_generate_tests was sufficient. 
- Running failed tests in Ansible removes the node from subsequent plays. Napalm validation reports is better for that type of failure than assert
- Failed tests for invalid scenarios in GitLab causes the CI execution to stop. Steps following the failure are lost. Need a better way to run tests with expected failure results.
- Gitlab-runner is executed as root and command execution can be different for user installed applications e.g. pytest. Needed to install pytest as root to ensure the runner was successful `sudo pip3 install pytest`. The `gitlab-runner exec shell <CMD>` was a good troubleshooting tool.
- GitLab integration required a lot of Unix/Linux skills which may be lacking!
- GitLab repository mirroring of GitHub repository was used to monitor for any commits. Testing was conducted by manually refreshing the mirrored repository, which initiated the pipeline job execution. A better solution is needed here, such as running the CI when a branch is merged into master.

