# Gather Device Data from IOS
Ansible provides some very useful modules to gather facts from Cisco IOS/IOS-XE devices. The <code>ios_facts</code> core module can collect generic facts from IOS/IOS-XE devices, returning hardware model, software version and interfaces etc. Cisco IOS/IOS-XE devices don't provide full support for extracting structured data for all show commands. To get this type of operational data, which is not included in the base set of deivce facts, requires parsing of CLI output.

## Ansible Parsing Options
A number of options exist to parse CLI output
<ul>
<li>Network CLI Filters - parse_cli</li>
<li>TextFSM - ntc_templates</li>
<li>pyATS</li>
</ul>


## pyATS
	* 
Cisco internal test framework launched 2014
	* 
Released to devnet for external use in 2018
	* 
The framework provides

		* 
common operations

			* 
connectivity
			* 
Command execution
			* 
Configuration
		* 
parsing

			* 
Genie library
			* 
TextFSM
			* 
regex
	* 
Test framework allows you to concentrate on test validation based on your requirements
	* 
Some elements not open source



## Genie
	* 
Concentrates on the feature-centric object implementation built within network elements
	* 
Intangible
	* 
All parsers and libraries are open source on GitHub (attach links)
	* 
Three libraries

		* 
genie.conf

			* 
conf t
		* 
genie.ops

			* 
show
		* 
genie.sdk (triggers/verification)

			* 
clear ip bgp
			* 
show ip bgp
	* 
Provide Structured data for all configuration and operational objects with access to their properties

		* 
Avoiding screen scrapping

			* 
TextFSM, regex
	* 
Device agnostic

		* 
data structure between different objects IOS NXOS is identical so easier to control network devices on a single schema
	* 
Management interface agnostic

		* 
Works with cli, Yang, XML etc.



Check genie 
learn('bgp', 'pe2")

### Pre-requisites 

### Ansible pyATS Install

### Example

### Output

## Conclusion 
