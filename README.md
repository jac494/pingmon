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
# start pingmon and background it
nohup ./pingmon <monitor_host> &
# now detach it from the current process
disown
```
