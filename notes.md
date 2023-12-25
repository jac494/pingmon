# Scratchpad Notes

look for loss in the logs with:

```sh
grep "packet_loss" logs/* | cut -d" " -f1,8
```

Sample output:

```txt
<hostnames and IP addresses have been replaced with random strings>
pingmon.20231209094511.somehost_1.log:2023-12-09 packet_loss=0.15
pingmon.20231209094511.somehost_1.log:2023-12-09 packet_loss=0.2
pingmon.20231209094511.somehost_1.log:2023-12-09 packet_loss=0.05
pingmon.20231209094511.somehost_1.log:2023-12-09 packet_loss=0.05
pingmon.20231209094520.google.com.log:2023-12-09 packet_loss=0.1
pingmon.20231209094520.google.com.log:2023-12-09 packet_loss=0.1
pingmon.20231209094520.google.com.log:2023-12-09 packet_loss=0.05
pingmon.20231209094520.google.com.log:2023-12-09 packet_loss=0.0
pingmon.20231209094526.random_dns_server_addr.log:2023-12-09 packet_loss=0.05
pingmon.20231209094526.random_dns_server_addr.log:2023-12-09 packet_loss=0.15
pingmon.20231209094526.random_dns_server_addr.log:2023-12-09 packet_loss=0.0
pingmon.20231209094526.random_dns_server_addr.log:2023-12-09 packet_loss=0.2
```

Future improvements:

* instead of logging as the default (and only) storage: **push into a sqlite db**
  * this would also allow querying
* prometheus exporter?
* restructure into a service that allows for a client to call and control the monitors
  * start and stop monitors to a specific host, get some stats on a specific monitor, query for stats on all monitors
* refactor config to load from:
  * default config that ships to the repo, then the install script copies into the consumed prod config. keep local for now
  * allow reloading of config variables on-demand for the service. having to restart to load the config always seems like it causes headaches later on down the road and having the ability to dynamically change config values during runtime always seems so nice
* tests
