import sys
import json
import urllib3.contrib.pyopenssl

import ansible.runner
import ansible.playbook
import ansible.inventory
from ansible import callbacks
from ansible import utils

from linode import api

urllib3.contrib.pyopenssl.inject_into_urllib3()

path = sys.argv[-1]

API_KEY = ''
MASTER_ADDR = ''

linode = api.Api(API_KEY)

group = ansible.inventory.group.Group(name='spark_group')

for ip in linode.linode_ip_list():
    if ip['IPADDRESS'] == MASTER_ADDR:
        tmp_host = ansible.inventory.host.Host(name=ip['IPADDRESS'], port=22)
        group.add_host(tmp_host)

workers = ansible.inventory.Inventory()
workers.add_group(group)
workers.subset('spark_group')

spark_stats = callbacks.AggregateStats()
spark_pb = ansible.playbook.PlayBook(
        playbook = path,
        stats = spark_stats,
        callbacks = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY),
        runner_callbacks = callbacks.PlaybookRunnerCallbacks(spark_stats, verbose=utils.VERBOSITY),
        inventory = workers
        )

out = spark_pb.run()
print json.dumps(out, sort_keys=True, indent=4, separators=(',', ': '))
