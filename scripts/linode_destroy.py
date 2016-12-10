import time

import urllib3.contrib.pyopenssl

from linode import api

import netifaces as ni

urllib3.contrib.pyopenssl.inject_into_urllib3()

API_KEY = ""
MASTER_ADDR = ""

ni.ifaddresses('eth0')
host_ip = ni.ifaddresses('eth0')[2][0]['addr']
if host_ip != MASTER_ADDR:
    print "host ip is changed, please check the code"

linode = api.Api(API_KEY)
servers = linode.linode_list()
for server in servers:
    linode_id = server["LINODEID"]
    if linode_id != 515307:
        ip_obj = linode.linode_ip_list(LinodeID=linode_id)
        if len(ip_obj) != 1:
            print "ip information is ambiguous"
        if ip_obj[0]["IPADDRESS"] != host_ip:

            print ip_obj
            disks_obj = linode.linode_disk_list(LinodeID=linode_id)

            # shutdown linode server
            print linode.linode_shutdown(LinodeID=linode_id)
            time.sleep(5)

            # remove disk
            for disk_obj in disks_obj:
                print disk_obj
                print linode.linode_disk_delete(LinodeID=linode_id, DiskID=disk_obj["DISKID"])
                while len(linode.linode_disk_list(LinodeID=linode_id)) > 0:
                    time.sleep(5)

            # delete linode server
            print linode.linode_delete(LinodeID=linode_id)
            print "#############################"
