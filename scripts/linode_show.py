
import json
import urllib3.contrib.pyopenssl

from linode import api

urllib3.contrib.pyopenssl.inject_into_urllib3()

API_KEY = ''

linode = api.Api(API_KEY)
for node in linode.linode_list():
    print json.dumps(node, sort_keys=True, indent=4, separators=(',', ':'))
    #print linode.linode_job_list(LinodeID=node["LINODEID"])

for ip in linode.linode_ip_list():
    print json.dumps(ip, sort_keys=True, indent=4, separators=(',', ':'))

#print linode.avail_datacenters()
#print json.dumps(linode.avail_datacenters(), sort_keys=True, indent=4, separators=(',', ':'))
print linode.avail_linodeplans()
#print json.dumps(linode.avail_kernels(), sort_keys=True, indent=4, separators=(',', ':'))
#print json.dumps(linode.avail_distributions(), sort_keys=True, indent=4, separators=(',', ':'))
