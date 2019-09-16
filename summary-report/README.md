# Reporting

## Basic L3VPN Topology
These playbooks gather BGP MPLS VPN data from an IOS-XE PE node and extract VRF and IP information using the Cisco pyATS framework. 

The following basic data model was used to describe the L3VPN

nodes:
  pe:
    "pe1.pk.lab": 
        routerid: "10.10.10.1"
    "pe2.pk.lab": 
        routerid: "10.10.10.2"
    "pe3.pk.lab": 
        routerid: "10.10.10.3"
  cpe:
    "cpe1.pk.lab": 
        routerid: "10.10.10.11"
    "cpe2.pk.lab": 
        routerid: "10.10.10.12"
    "cpe3.pk.lab": 
        routerid: "10.10.10.13"
vrfs:
  - name: "VRF_ACME"
    description: "TEST VRF"
    type: "vpnv4"
    rd: "100"
    rt_import:
      - "65001:100"
    rt_export:
      - "65001:100"
      
 L3VPN topology sample in DOT file format
 ![L3VPN Diagram]
 (./results/pe2.pk.lab.png)
