# Gather Device Data from IOS
Ansible provides some very useful modules to gather facts from Cisco IOS/IOS-XE devices. The <code>ios_facts</code> core module can collect generic facts from IOS/IOS-XE devices, returning hardware model, software version and interfaces etc. Cisco IOS/IOS-XE devices don't provide full support for extracting structured data for all show commands. Getting this type of operational data requires parsing of CLI output.

## Ansible Parsing Options
Ansible supports various options for parsing CLI output. Network CLI filters are a tool within the Ansible core modules that use Jinja2 features to manipulate data. These filters can parse the CLI output retrieved from a network device and store it in a custom data structure. The filter requires a user-defined regular expression to be developed to parse the CLI data into structured data. Regular expressions can be difficult to maintain and time consuming to write for complex CLI output.

An alternative to custom parsing, is to use pre-built text parsers such as the TextFSM templates on the Network to Code repository, in conjunction with the <code>parse_cli_textfsm</code> Ansible filter. The template repo provides a large collection of textfsm files containing the regular expression parsing operations for common commands on multivendor operating systems. Not all commands are supported, so if the vendor and command required does not exist, a new textfsm or Jinja2 filter will need to be created.

Cisco have released an internal test framework called pyATS that can be used parse CLI output for many of their network operating systems. The framework is packaged with a number of libraries (e.g. genie library) that provide configuration models, operational models and also parsing. It has support for an extensive number of commands and is Cisco supported. This post will focus on how to get started with pyATS and Ansible to parse Cisco CLI output.

Parser | Description | Example
------ | ----------- | --------
Network CLI Filters | Jinja2 filters for customer regex based text parsing on CLI strings | <code>parse_cli<\code>
TextFSM | Repository of text parses for common networking vendor operations | ntc_templates
pyATS | Framework developed by Cisco for use as their core test automation solution for IOS/XE/XR/NX-OS products | genie 


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
