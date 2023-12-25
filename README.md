# pingmon.py

Simple utility to ping a host forever and log the result.

## Installation

```sh
cd pingmon
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```sh
./pingmon.py <monitor_host>
```

Use `./pingmon.py --help` for additional information.

I wish I could build this in but so far it is just wishful (maybe by building as a daemon and then providing a cli to communicate with and send commands to/read commands from a common db):

```sh
# start pingmon
# (to also not accept a SIGHUP from it's current process)
# and background it
nohup ./pingmon <monitor_host> &
# now detach it from the current process
disown
```

where the better behavior I think

```sh
pingmon start <monitor_host>
```

and output something like...

```sh
<timestamp> ping monitor requested for host ...
<timestamp> ping monitor started for host ...
```

which would indicate that ping monitor had successfully started

internal question to myself:

> in the case of `no active ping monitor` should it try to start one locally by default? or just suggest the directions to do so?

```sh
pingmon stop <monitor_host>
```

would then:

* record request to stop pingmon to host
* validate that monitor stopped or host didn't exist in monitor table/queue/topic/whatever
