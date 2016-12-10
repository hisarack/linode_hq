import sys
import time
import paramiko

import urllib3.contrib.pyopenssl

from linode import api

urllib3.contrib.pyopenssl.inject_into_urllib3()

API_KEY = ""
SPARK_PASSWD = ""
linode = api.Api(API_KEY)


def _linode_create():
    obj = linode.linode_create(DatacenterID=2, PlanID=7, PaymentTerm=1)
    new_server_id = obj["LinodeID"]

    obj = linode.linode_disk_createfromdistribution(
        LinodeID=new_server_id,
        DistributionID=124,
        rootPass=SPARK_PASSWD,
        Label="CFD{}".format(new_server_id),
        Size=102400
    )

    disk_list = linode.linode_disk_list(LinodeID=new_server_id)
    print disk_list
    disk_list_str = ""
    for disk_obj in disk_list:
        if disk_list_str != "":
            disk_list_str = disk_list_str+","
        disk_list_str = "{}{}".format(disk_list_str, disk_obj["DISKID"])

    obj = linode.linode_config_create(LinodeID=new_server_id, KernelID=215, Label="CONFIG{}".format(new_server_id), DiskList=disk_list_str)
    print obj
    new_config_id = obj["ConfigID"]

    obj = linode.linode_boot(LinodeID=new_server_id, ConfigID=new_config_id)
    print obj
    return new_server_id


def is_node_ready(new_server_id):
    obj = linode.linode_list(LinodeID=new_server_id)
    if int(obj[0]["STATUS"]) != 1:
        return False
    return True


def _get_new_server_ip(new_server_id):
    obj = linode.linode_ip_list(LinodeID=new_server_id)
    return str(obj[0]["IPADDRESS"])


def sshkey_sync(new_server_id):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    new_server_ip = _get_new_server_ip(new_server_id)
    print new_server_ip
    ssh.connect(new_server_ip, username="root", password=SPARK_PASSWD)
    ssh.exec_command("mkdir ~/.ssh")
    sftp = ssh.open_sftp()
    sftp.put("/root/.ssh/id_dsa.pub", "/root/.ssh/authorized_keys")
    sftp.close()
    ssh.close()


def linode_create():
    new_server_id = _linode_create()
    while is_node_ready(new_server_id) is False:
        time.sleep(3)
        print ".........."
    time.sleep(3)
    sshkey_sync(new_server_id)
    time.sleep(1)


linode_size = int(sys.argv[1])
for i in xrange(0, linode_size, 1):
    linode_create()
