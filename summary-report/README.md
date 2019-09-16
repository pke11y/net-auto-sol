# Reporting

## Basic L3VPN Topology
These playbooks gather BGP MPLS VPN data from an IOS-XE PE node and extract VRF and IP information using the Cisco pyATS framework. The Cisco framework is imported as an Ansible role.

Filter plugins are created to simplify the generation of a diagram in DOT file format, using the extracted data.

The following basic data model was used to describe the L3VPN.

[group_vars](./group_vars/all.yml)
 
 L3VPN topology sample in DOT file format.
 
 ![L3VPN Diagram](./results/pe2.pk.lab.png)
