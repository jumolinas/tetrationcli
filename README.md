# Tetrationcli to interact with Tetration Cluster via the cli

## Installation

### From PyPI

```
pip install tetrationcli
```

### From sources

Download the sources from [Github](https://github.com/jumolinas/tetrationcli), extract and execute the following commands

```
$ pip install -r requirements.txt

$ pip install setup.py
```

## How to use this application:
To access to the cluster you need to get the API Credentials. Download the api_credentials.json locally 
to get the information required for the setup.

```
$ tetrationcli -h
usage: tetrationcli [-h] [-d] [-q] [-v]
                    {inventory,vrfs,applications,users,roles,scopes,switches,agents,clear,setup}
                    ...

Tetration Analytics CLI tool

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           full application debug mode
  -q, --quiet           suppress all console output
  -v, --version         show program's version number and exit

sub-commands:
  {inventory,vrfs,applications,users,roles,scopes,switches,agents,clear,setup}
    inventory           Interact with Inventory from Tetration Cluster
    vrfs                Interact with VRFs in Tetration Cluster
    applications        Interact with ADM Application from Tetration Cluster
    users               Interact with Users from Tetration Cluster
    roles               Interact with Roles in Tetration Cluster
    scopes              Interact with Scopes configured in Tetration Cluster
    switches            Interact with Hardware Sensors from Tetration Cluster
    agents              Interact with Software Sensors in Tetration Cluster
    clear               Clear the configuration
    setup               Application setup

Usage: tetrationcli command
```
### Easy setup

Step 1: Issue `tetrationcli setup` and folow the instructions and place the correct information presented
```
$ tetrationcli setup
Tetration Analytics cluster (eg: https://great.example.com/): https://great.example.com/
Tetration API Key: ASDASDASADS
Tetration API Secret: ASDASDASDASDFFF
```

Step 2: Test if you can successfully query the cluster from the command line
```
$ tetrationcli agents list
```

### Alternative way to setup the application

The file `api_credentials.json` downloaded from the cluster is expected to be placed in 
folder `~/.config/tetrationcli/` then to define the cluster name you need to create the 
config file `tetrationcli.conf` in `~/.config/tetrationcli/`

```
total 16
0 drwxr-xr-x   4 user  staff  128 Nov 11 16:16 .
0 drwx------  13 user  staff  416 Nov 11 16:10 ..
8 -rw-r--r--@  1 user  staff  111 Nov 11 09:52 api_credentials.json
8 -rw-r--r--   1 user  staff  121 Nov 11 16:16 tetrationcli.conf
```
and the file `tetrationcli.conf` requires the information:
```
[tetrationcli]
api_endpoint = https://mygreatapp.example.com
api_credentials = ~/.config/tetrationcli/api_credentials.json
```

## More information

### Options used

#### Current scope for tetrationcli
1. inventory
2. vrfs
3. applications
4. users
5. roles
6. scopes
7. switches
8. agents

For any new functionalites open an issue to be added.
