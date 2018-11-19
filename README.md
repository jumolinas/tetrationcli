# Tetrationcli to interact with Tetration Cluster via the cli

## Installation
Currently there are very limited options working, this application still in ALPHA state. For any improvements or comments fill an issue and we'll work on it.

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

## How to use the application:
To access to the cluster you need to get the API Credentials. 
The file `api_credentials.json` downloaded from the cluster is expected to be placed in folder `~/.config/tetrationcli/` then to define the cluster name you need to create the config file `tetrationcli.conf` in `~/.config/tetrationcli/`

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
