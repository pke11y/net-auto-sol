from netaddr import IPNetwork
import copy
import re   
import pandas
"""

            "192.168.1.0/29": {
                "Customer": "Total Produce",
                "Site": "All",
                "Solution Type": " Reserved (but not yet used) for possible future expansion",
                "Subnet": "192.168.1.0/29"
            },
"""


def addiprange(custdict):
    """ Return a list of IP addresses from a prefix
    """
    cdata = copy.deepcopy(custdict)
    for prefix, vals in custdict.items():
        iphosts = [str(ip) for ip in IPNetwork(prefix).iter_hosts()]
        cdata[prefix]['PublicIPs'] = iphosts
        cdata[prefix]['Customer']
        # take all none alphanumeric chars out of customer name and use as an ID for a set_fact to save ping results
        cdata[prefix]['ID'] = re.sub('[\W]', '', cdata[prefix]['Customer'] + cdata[prefix]['Site'])
    return cdata

def active_ip_addr(data):
    """ Return a list of active IP addresses from ping results
    """
    cust_data = data[0]
    cust_results = data[1]
    cdata = copy.deepcopy(cust_data)
    for prefix, custdict in cust_data.items():
        id = custdict['ID']
        iplist = []
        for pingresult in cust_results[id].results:
            if pingresult.rc == 0:
                iplist.append(pingresult.item)
        cdata[prefix]['ActiveIPs'] = iplist
    return pandas.read_json(json.dumps(cdata.values())).to_csv()

def hashfact(val):
    """ Return a hash value with first character as an underscore
    """
    import hashlib
    hash_object = hashlib.md5(val.encode('utf-8'))
    return '_' + hash_object.hexdigest()

class FilterModule(object):
    def filters(self):
        return {"addiprange": addiprange,
                "hashfact": hashfact,
                "active_ip_addr": active_ip_addr}