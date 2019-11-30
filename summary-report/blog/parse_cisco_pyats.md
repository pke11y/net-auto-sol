# Gather IOS Device Data using pyATS on Ansible
Ansible provides some very useful modules to gather facts from Cisco IOS/IOS-XE devices. The <code>ios_facts</code> core module can collect generic facts from IOS/IOS-XE devices, returning hardware model, software version and interfaces etc. Cisco IOS/IOS-XE devices don't provide full support for extracting structured data for all show commands. Getting this type of operational data requires parsing of CLI output.

## Ansible Parsing Options
Ansible supports various options for parsing CLI output. Network CLI filters are a tool within the Ansible core modules that use Jinja2 features to manipulate data. These filters can parse the CLI output retrieved from a network device and store it in a custom data structure. The filter requires a user-defined regular expression to be developed to parse the CLI data into structured data. Regular expressions can be difficult to maintain and time consuming to write for complex CLI output.

An alternative to custom parsing, is to use pre-built text parsers such as the TextFSM templates on the Network to Code repository, in conjunction with the <code>parse_cli_textfsm</code> Ansible filter. The template repo provides a large collection of textfsm files containing the regular expression parsing operations for common commands on multivendor operating systems. Not all commands are supported, so if the vendor and command required does have an existing template, a new textfsm or Jinja2 filter will need to be created.

For Cisco devices, a Python based framework called pyATS | Genie can be used parse CLI output for many of their network operating systems. It has support for an extensive number of commands and is Cisco supported with some open-source libraries. This post will focus on how to get started with pyATS and Ansible to parse Cisco CLI output.

Parser? | Description | Example
------ | ----------- | --------
Network CLI Filters | Jinja2 filters for customer regex based text parsing on CLI strings | <code>parse_cli</code>
TextFSM | Repository of text parses for common networking vendor operations | ntc-templates
pyATS | Framework developed by Cisco for use as their core test automation solution for IOS/XE/XR/NX-OS products | genie 


## Cisco pyATS & genie
Cisco's test automation suite was released to the DevNet community for external use. pyATS defines a framework hat standardises how to connect to devices, define test topologies and test execution/reporting. 

The genie package contains open-source libraries that provide the main network automation functionality:

* OS agnostic device configuration
* retrieve operational state using common data models
* extensive library of Cisco OS parsing

Components of the automation suite are loosely coupled, facilitating feature integration with other automation platforms e.g. Ansible. 

### Ansible with pyATS | genie
Pre-requisite: pyATS and Genie require Python >= 3.4 

The easiest way to use pyATS | Genie is to include the functionality in an Ansible role. Follow the installation instructions on the CiscoDevNet github page (https://github.com/CiscoDevNet/ansible-pyats) 

Let's use the Ansible role to retrieve data for 'VRF_ACME' from a Cisco IOS-XE PE router. Adding the role to the playbook provides access to the <code>pyats_parser</code> filter that takes the parser name and OS as arguments.

        ---
        - hosts: pe2.rtr.lab
          connection: network_cli
          gather_facts: no
          roles:
            - ansible-pyats
          tasks:
            - name: Run command to get VRF data
              cli_command:
                command: sh ip bgp vpnv4 vrf VRF_ACME
              register: cli_output
            - name: Parsing output
              set_fact:
                parsed_output: "{{ cli_output.stdout | pyats_parser('show ip bgp vpnv4 vrf VRF_ACME', 'iosxe') }}"

The <code>pyats_parser</code> will parse the output into a python dictionary using the pre-defined data model.  

        ok: [pe2.pk.lab] => {
            "parsed_output": {
                "vrf": {
                    "VRF_ACME": {
                        "address_family": {
                            "vpnv4 RD 10.10.10.2:100": {
                                "bgp_table_version": 17,
                                "default_vrf": "VRF_ACME",
                                "route_distinguisher": "10.10.10.2:100",
                                "route_identifier": "10.10.10.2",
                                "routes": {
                                    "10.0.3.0/30": {
                                        "index": {
                                            "1": {
                                                "localpref": 100,
                                                "metric": 0,
                                                "next_hop": "10.10.10.1",
                                                "origin_codes": "?",
                                                "status_codes": "*>i",
                                                "weight": 0
                                            }
                                        }
                                    },
                                    "10.0.3.4/30": {
                                        "index": {
                                            "1": {
                                                "metric": 0,
                                                "next_hop": "0.0.0.0",
                                                "origin_codes": "?",
                                                "status_codes": "*>",
                                                "weight": 32768
                                            }
                                        }
                                    },
          ...                          

To access the VRF routes, traverse the parsed_output variable using the schema for the parser. In the example, variable <code>rd_cli</code> is defined as <code>rd_cli: "{{vrf_type + ' RD ' + router_id + ':' + vrf_rd}}"</code>. 

        - name: Set VRF_ROUTES variable
              set_fact:
                vrf_routes: "{{parsed_output['vrf']['VRF_ACME']['address_family'][rd_cli]['routes']}}"

Returning the VRF route objects.

        ok: [pe2.pk.lab] => {
            "vrf_routes": {
                "10.0.3.0/30": {
                    "index": {
                        "1": {
                            "localpref": 100,
                            "metric": 0,
                            "next_hop": "10.10.10.1",
                            "origin_codes": "?",
                            "status_codes": "*>i",
                            "weight": 0
                        }
                    }
                },
                "10.0.3.4/30": {
                    "index": {
                        "1": {
                            "metric": 0,
                            "next_hop": "0.0.0.0",
                            "origin_codes": "?",
                            "status_codes": "*>",
                            "weight": 32768
                        }
                    }
                },
       ...         

## Conclusion 

## Links
pyATS and genie libs - https://github.com/CiscoTestAutomation
ansible-pyats - https://github.com/CiscoDevNet/ansible-pyats
genie API - https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/
