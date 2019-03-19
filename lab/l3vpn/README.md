# L3VPN Lab Setup 
The objective of this lab is to provide a platform to test L3VPN automation solutions for a service provider network.

The nework lab consists of the following physical and virtual routers:
- IOS-XE 3.15.02 (CSR1000V)
- IOS Version 12.4 (C2620XM)
- IOS Version 15.0 (C3560G) 
- IOS-XRv Version 6.1.2
- JunOS TBC

All virtual routers are running on an EVE-NG VM within a KVM hypervisor. Two Open vSwitch instances provide the virtual switches, with a Cisco 3560 and a HP 1920G switch providing the trunk links from the physical devices to the virtual platform.

Ansible 2.7 is running on a network management host Ubuntu VM. Any other management systems and applications will run on this host.

## Physical

![Physical Diagram](l3vpn/physical.png)

## Logical

![Logical Diagram](l3vpn/logical.png)
